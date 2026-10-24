# The three supplemental asks of the v2 build, computed from the v2 inputs, with the easy-route variants
# each device is aimed against. Usage: python3 -I asks.py <v2 inputs dir> [figures.json]
import json, sys
import numpy as np, pandas as pd

D = sys.argv[1]
OUT = sys.argv[2] if len(sys.argv) > 2 else None
UPGRADE = {"BV113": "2027-10-26", "BV115": "2027-10-26", "BV118": "2027-11-02", "BV132": "2027-11-02",
           "BV125": "2027-11-09", "BV128": "2027-11-09", "BV141": "2027-11-16"}

crm = pd.read_csv(f"{D}/crm_members_extract_2028-01-08.csv", dtype=str)
crm["closed_date"] = pd.to_datetime(crm.closed_date)
cm = crm.set_index("member_id")
pos = pd.read_csv(f"{D}/pos_offer_redemptions_2027.csv", sep=";", decimal=",",
                  dtype={"receipt_id": str, "member_id": str, "offer_code": str, "store_code": str})
stores = pd.read_csv(f"{D}/stores.csv", dtype=str).set_index("store_code")
areas = pd.read_csv(f"{D}/postcode_areas.csv", dtype=str).set_index("postcode_area")
dm = pd.read_csv(f"{D}/direct_mail_drops_2027.csv", dtype=str)
snap = pd.read_csv(f"{D}/consent_snapshot_2026-01-01.csv", dtype=str).set_index("member_id")
ev = pd.read_csv(f"{D}/consent_events_2026-2027.csv", dtype={"event_id": int, "member_id": str})
ev["t"] = pd.to_datetime(ev.event_time_utc.str.replace("Z", ""))
sends = pd.read_csv(f"{D}/esp_sends_2027.csv", dtype=str)
mailings = pd.read_csv(f"{D}/esp_mailings_2027.csv", dtype=str)
push = pd.read_csv(f"{D}/app_push_log_2027.csv", dtype=str)
push["t"] = pd.to_datetime(push.sent_at, utc=True)

# ---------------------------------------------------------------- A: the Julbrevet card offers
jul = pos[pos.offer_code.isin(["BV27-13-O1", "BV27-13-O2"])].copy()
assert jul.redeemed_at.str[:10].between("2027-12-01", "2027-12-24").all()
up = jul.store_code.map(UPGRADE)
jul["gross_till"] = up.notna() & (jul.redeemed_at.str[:10] >= up.fillna("9999"))
jul["paid"] = jul.receipt_total_sek - np.where(jul.gross_till, jul.discount_sek, 0.0)
jul["format"] = jul.store_code.map(stores.format)
jul["hh"] = jul.member_id.map(cm.household_id)

def table_a(col, df=jul):
    return {f"{o[-2:]}|{f}": round(df[(df.offer_code == o) & (df.format == f)][col].sum() / 1000, 1)
            for o in ["BV27-13-O1", "BV27-13-O2"] for f in ["Stor", "Mellan", "Nära"]}

A = table_a("paid")
A_easy = table_a("receipt_total_sek")                                  # the column read as the amount paid
jul["minus_all"] = jul.receipt_total_sek - jul.discount_sek
A_over = table_a("minus_all")                                          # the discount taken off at every till
keep = ~((jul.offer_code == "BV27-13-O2") & (jul.receipt_total_sek < 700))
A_drop = table_a("paid", jul[keep])                                    # O2 receipts under 700 dropped as invalid

# ---------------------------------------------------------------- B: 2028 reach of the households mailed in 2027
END = pd.Timestamp("2027-12-31 23:00:00")                              # 1 January 2028 00:00 Swedish time
open_end = cm.closed_date.isna() | (cm.closed_date > pd.Timestamp("2027-12-31"))

def state(ch, cut):
    st = pd.Series(False, index=cm.index)
    s = snap[ch].eq("Y")
    i = s.index.intersection(st.index)
    st.loc[i] = s.loc[i]
    e = ev[(ev.channel == ch) & (ev.t < cut)].sort_values(["t", "event_id"])
    last = e.groupby("member_id").action.last()
    st.loc[last.index] = last.eq("granted")
    return st

email_c, sms_c, push_c = state("email", END), state("sms", END), state("push", END)
hard = set(sends.loc[sends.status == "hard_bounce", "member_id"])
nl = mailings[mailings.type == "newsletter"]
held_at_release = pd.Series(False, index=cm.index)
for t in pd.to_datetime(nl.scheduled_utc.str.replace("Z", "")):
    held_at_release |= state("email", t)
never_sent = set(held_at_release[held_at_release].index) - set(sends.member_id)   # on the list from before 2027
p = push.sort_values(["member_id", "t"])
last3 = p.groupby("member_id").tail(3).groupby("member_id").status.agg(lambda s: len(s) == 3 and (s == "failed").all())
removed = set(last3[last3].index)                                      # January clean-up of tokens failed three in a row
app = cm.app_registered_date.notna()

def reach(email_drop, push_drop):
    e = email_c & open_end & ~cm.index.isin(list(email_drop))
    s = sms_c & open_end
    q = push_c & open_end & app & ~cm.index.isin(list(push_drop))
    return e, s, q

mail = dm[dm.drop_code == "BV27-13-D1"][["household_id", "postcode_area"]]
mail["county"] = mail.postcode_area.map(areas.county)
paid_hh = jul.groupby("hh").paid.sum()
easy_hh = jul.groupby("hh").receipt_total_sek.sum()

def table_bc(email_drop, push_drop, paid=paid_hh):
    e, s, q = reach(email_drop, push_drop)
    H = lambda x: set(cm.household_id[x[x].index])
    E, Sm, Q = H(e), H(s), H(q)
    out = {}
    for c in ["Gävleborg", "Västernorrland"]:
        hs = set(mail.household_id[mail.county == c])
        grp = {"email": hs & E, "sms_push_only": (hs & (Sm | Q)) - E, "none": hs - E - Sm - Q}
        for g, x in grp.items():
            out[f"B|{c}|{g}"] = len(x)
            out[f"C|{c}|{g}"] = round(sum(paid.get(h, 0.0) for h in x) / 1000, 1)
    return out

BC = table_bc(hard | never_sent, removed)
e_, s_, q_ = reach(hard | never_sent, removed)
H_ = lambda x: set(cm.household_id[x[x].index])
none_all = set(mail.household_id) - H_(e_) - H_(s_) - H_(q_)
BC["M|none|households"] = len(none_all)
BC["M|none|paid"] = round(sum(paid_hh.get(h, 0.0) for h in none_all) / 1000, 1)
variants = {
    "A_easy (total read as paid)": (A_easy, None),
    "A_over (discount off everywhere)": (A_over, None),
    "A_drop (O2 under 700 dropped)": (A_drop, None),
    "BC no list from before 2027": (table_bc(hard, removed), None),
    "BC no suppression at all": (table_bc(set(), removed), None),
    "BC no token clean-up": (table_bc(hard | never_sent, set()), None),
    "BC gross totals": (table_bc(hard | never_sent, removed, easy_hh), None),
    "BC the cracker of A only": (table_bc(hard, removed), None),
    "BC the cracker of B only": (table_bc(hard | never_sent, removed, easy_hh), None),
}
gold = {("A|" + k): v for k, v in A.items()}
gold.update(BC)
print("never sent although consented", len(never_sent), "hard bounces", len(hard), "tokens removed", len(removed))
print("gross-till receipts", int(jul.gross_till.sum()), "of", len(jul))
for k, v in gold.items():
    print(f"{k:32s} {v}")
for name, (fig, _) in variants.items():
    fig = {("A|" + k) if not k.startswith(("B|", "C|")) else k: v for k, v in fig.items()}
    hit = [k for k in fig if k in gold and abs(fig[k] - gold[k]) < 1e-9]
    print(f"{name:36s} keeps {len(hit)} of {len(fig)}: {hit}")
if OUT:
    json.dump({k: float(v) if k.startswith(("A|", "C|", "M|none|paid")) else int(v) for k, v in gold.items()},
              open(OUT, "w"), ensure_ascii=False, indent=1)
if "--show" in sys.argv:
    for name, (fig, _) in variants.items():
        print(name, fig)
