# Builds the input folder from the uploaded v1 inputs. Only pos_offer_redemptions_2027.csv changes:
#   1. December receipt totals are brought into line with member_store_month_2027.csv, whose December spend
#      carries the area and mailing factors the v1 build applied after the receipts were written;
#   2. the tills upgraded in October and November 2027 write the total before the discount;
#   3. the self-service tills write the campaign's first offer code for either Julbrevet card offer, so part of
#      every store's BV27-13-O2 redemptions carry BV27-13-O1.
# The messaging runbook's offers paragraph (7.3) also states the loyalty engine's once-per-member rule, which every
# redemption in the export keeps. Every other file is copied byte for byte.
# Usage: python3 -I patch.py <v1 inputs dir> <out inputs dir>
import os, shutil, sys, zipfile
import numpy as np, pandas as pd

SRC, DST = sys.argv[1], sys.argv[2]
POS = "pos_offer_redemptions_2027.csv"
# till software upgrade: from this day on the store's tills send the loyalty engine the total before the discount
UPGRADE = {"BV110": "2027-10-26", "BV113": "2027-10-26", "BV114": "2027-10-26", "BV115": "2027-10-26",
           "BV118": "2027-11-02", "BV119": "2027-11-02", "BV101": "2027-11-09", "BV104": "2027-11-09",
           "BV106": "2027-11-09", "BV128": "2027-11-16", "BV129": "2027-11-16", "BV132": "2027-11-16",
           "BV138": "2027-11-16", "BV141": "2027-11-16"}

RUNBOOK = "messaging_operations_runbook_2027.docx"
os.makedirs(DST, exist_ok=True)
for f in sorted(os.listdir(SRC)):
    if f not in (POS, RUNBOOK):
        shutil.copyfile(os.path.join(SRC, f), os.path.join(DST, f))

OLD73 = "to the last minute of its last day, and the till honours it accordingly."
NEW73 = "to the last minute of its last day, and the till honours it accordingly, once for each member."
zin = zipfile.ZipFile(os.path.join(SRC, RUNBOOK))
with zipfile.ZipFile(os.path.join(DST, RUNBOOK), "w") as zout:
    for info in zin.infolist():
        data = zin.read(info.filename)
        if info.filename == "word/document.xml":
            assert data.count(OLD73.encode("utf-8")) == 1
            data = data.replace(OLD73.encode("utf-8"), NEW73.encode("utf-8"))
        zout.writestr(info, data)
zin.close()

raw = open(os.path.join(SRC, POS), encoding="ascii").read().split("\n")
head, lines = raw[0], [l for l in raw[1:] if l]
rows = [l.split(";") for l in lines]
pos = pd.DataFrame(rows, columns=head.split(";"))
pos["tot"] = pos.receipt_total_sek.str.replace(",", ".").astype(float)
pos["disc"] = pos.discount_sek.str.replace(",", ".").astype(float)
pos["month"] = pos.redeemed_at.str[:7]

msm = pd.read_csv(os.path.join(SRC, "member_store_month_2027.csv"),
                  dtype={"member_id": str, "month": str, "store_code": str})
crm = pd.read_csv(os.path.join(SRC, "crm_members_extract_2028-01-08.csv"), dtype=str)
dm = pd.read_csv(os.path.join(SRC, "direct_mail_drops_2027.csv"), dtype=str)
mailed = set(dm.loc[dm.drop_code == "BV27-13-D1", "household_id"])
m2h = crm.set_index("member_id").household_id
h2a = crm.groupby("household_id").postcode_area.first()

key = ["member_id", "month", "store_code"]
pos["n"] = pos.groupby(key).receipt_id.transform("size")
pos = pos.merge(msm[key + ["visits", "spend_sek"]], on=key, how="left")
assert pos.visits.notna().all()
pos["hh"] = pos.member_id.map(m2h)
pos["area"] = pos.hh.map(h2a)
pos["mailed"] = pos.hh.isin(mailed)

dec = pos.month == "2027-12"
# a month whose every receipt redeemed an offer: the receipts add up to the month's spend exactly
full = pos.visits == pos.n
pos["sum_tot"] = pos.groupby(key).tot.transform("sum")
assert np.allclose(pos.sum_tot[~dec & full], pos.spend_sek[~dec & full])
fulld = dec & full
ratio = (pos.spend_sek / pos.sum_tot)[fulld]
cell = pd.DataFrame({"area": pos.area[fulld], "mailed": pos.mailed[fulld], "r": ratio})
med = cell.groupby(["area", "mailed"]).r.median()
both = [a for a in med.index.get_level_values(0).unique() if (a, True) in med.index and (a, False) in med.index]
M = float(np.median([med[(a, True)] / med[(a, False)] for a in both]))
A = {}
for a in pos.area.unique():
    if (a, False) in med.index:
        A[a] = med[(a, False)]
    elif (a, True) in med.index:
        A[a] = med[(a, True)] / M
    else:
        A[a] = 1.0
f = pd.Series(pos.area.map(A) * np.where(pos.mailed, M, 1.0), index=pos.index)
hf = ratio.groupby(pos.hh[fulld]).median()
known = pos.hh.isin(hf.index)
f[known] = pos.hh[known].map(hf)

new = pos.tot.copy()
part = dec & ~full
new[part] = (pos.tot[part] * f[part]).round(2)
sc = (pos.tot * pos.spend_sek / pos.sum_tot).round(2)
new[fulld] = sc[fulld]
# put the cent left by rounding on the month's largest receipt so the receipts add up to the spend
res = (pos.spend_sek - new.groupby([pos.member_id, pos.month, pos.store_code]).transform("sum")).round(2)
big = fulld & (pos.tot == pos.groupby(key).tot.transform("max"))
big &= ~pos.duplicated(key + ["tot"]) | ~big
new[big] = (new[big] + res[big]).round(2)
chk = new.groupby([pos.member_id, pos.month, pos.store_code]).transform("sum")
assert np.allclose(chk[fulld], pos.spend_sek[fulld], atol=0.001)
s = new[dec].groupby([pos.member_id[dec], pos.store_code[dec]]).sum()
sp = pos[dec].groupby(["member_id", "store_code"]).spend_sek.first()
assert (s <= sp + 0.001).all()
single = fulld

up = pos.store_code.map(UPGRADE)
gross = up.notna() & (pos.redeemed_at.str[:10] >= up.fillna("9999"))
new[gross] = (new[gross] + pos.disc[gross]).round(2)

# self-service tills: their share of each store's O2 redemptions, drawn once per store
SEED, SHARE = 150, {"Stor": 0.55, "Mellan": 0.45, "Nära": 0.40}
fmt = pd.read_csv(os.path.join(SRC, "stores.csv"), dtype=str).set_index("store_code").format
rng = np.random.default_rng(SEED)
share = {s: SHARE[fmt[s]] + rng.uniform(-0.06, 0.06) for s in sorted(fmt.index)}
u = rng.random(len(pos))
selfco = ((pos.offer_code == "BV27-13-O2") & (u < pos.store_code.map(share).values)).values

out = [head]
for r, v in zip(rows, new):
    r = list(r)
    r[5] = ("%.2f" % v).replace(".", ",")
    out.append(";".join(r))
for i in np.flatnonzero(selfco):
    r = out[i + 1].split(";")
    assert r[2] == "BV27-13-O2"
    r[2] = "BV27-13-O1"
    out[i + 1] = ";".join(r)
open(os.path.join(DST, POS), "w", encoding="ascii", newline="\n").write("\n".join(out) + "\n")
print("factor cells %d, mailing factor %.5f, December rows rescaled %d (single-visit %d), gross rows %d, O2 under O1 %d"
      % (len(med), M, int(dec.sum()), int(single.sum()), int(gross.sum()), int(selfco.sum())))
