"""task127: the transaction ledger and the default records, drawn from world.py's truth.

The ledger is the core banking extract of business transaction accounts, January 2021 to December 2026, one row
per posted transaction. History before the 17 June 2023 cut-over was migrated under each account's new number, but
the other party's account number is what the payment carried: payers keyed the old numbers before the cut-over, and
some kept them for months after it, so an on-us counterparty can sit in either numbering and in the payer's own
spelling of it.
"""
import datetime as dt
import random

import world as W

EXT_BANKS = ["01-0505", "01-0817", "02-0108", "02-0560", "03-1702", "03-0257", "06-0501", "12-3101", "12-3191",
             "15-3946", "38-9010", "38-9017"]
EXT_WORDS = ["Pacific", "Southern", "Kowhai Road", "Central", "Summit", "Bayside", "Riverside", "Plains", "Hilltop",
             "Ranges", "Northern", "Coastal", "Valley", "Harbour", "Totara Park", "Meadow", "Gateway", "Highland"]
EXT_TRADE = ["Supermarkets", "Wholesale", "Builders", "Farms", "Motors", "Distribution", "Retail", "Holdings",
             "Contractors", "Hospitality", "Health", "Developments", "Industries", "Group", "Co-operative"]
SUPPLIERS = ["Fuel", "Power", "Freight", "Steel", "Timber", "Insurance", "Telecom", "Rent", "Packaging", "Parts"]


def fmt_variants(acct, r):
    """How a payer types an account number into its banking system."""
    k = r.random()
    if k < 0.62:
        return acct
    if k < 0.84:
        return acct.replace("-", "")
    return acct.replace("-", " ")


class Ledger:
    def __init__(self, w):
        self.w = w
        self.r = random.Random(W.SEED + 1)
        self.rows = []
        self.ext = {}
        self.seq = 0

    def ext_party(self, key):
        if key not in self.ext:
            r = self.r
            name = "%s %s" % (r.choice(EXT_WORDS), r.choice(EXT_TRADE))
            acct = "%s-%07d-%02d" % (r.choice(EXT_BANKS), r.randint(10000, 9999999), r.choice([0, 0, 1, 2, 25]))
            self.ext[key] = (name, acct)
        return self.ext[key]

    def cheque(self, c):
        return c["accounts"][0]

    def counter_ref(self, c, acct, d, stale_until=None):
        """The other party's account as a payment carries it: the old number before the cut-over (and up to a
        payer's own stale date after it), the new number after."""
        old = acct.get("old")
        if old and (d < W.MIGRATION or (stale_until and d < stale_until)):
            return fmt_variants(old, self.r)
        return fmt_variants(acct["new"], self.r)

    def add(self, d, acct, code, amount, other, other_acct, part="", cd="", ref=""):
        self.seq += 1
        self.rows.append([d, acct["new"], code, round(amount, 2), other, other_acct, part, cd, ref])

    def live(self, c, d):
        a = self.cheque(c)
        return a["opened"] <= d and (a["closed"] is None or d <= a["closed"]) and c["since"] <= d

    def build(self):
        w, r = self.w, self.r
        cust = w.customers
        # payment relations between customers: the designed links plus small on-us links among the rest
        links = list(w.links)
        pool = sorted([c for c in cust.values()], key=lambda c: c["cid"])
        heavy = set(l["payee"] for l in links)
        for c in pool:
            if c["cid"] in heavy:
                continue
            for _ in range(r.choice([0, 1, 1, 2])):
                p = r.choice(pool)
                if p["cid"] == c["cid"]:
                    continue
                links.append(dict(payer=p["cid"], payee=c["cid"], share=round(r.uniform(0.02, 0.09), 3),
                                  start=max(W.START, c["since"], p["since"]), end=W.END, small=True))
        self.links = links
        by_payee = {}
        for l in links:
            by_payee.setdefault(l["payee"], []).append(l)
        stale = {}
        for l in links:
            if r.random() < 0.3:
                stale[(l["payer"], l["payee"])] = W.add_months(W.MIGRATION, r.randint(2, 9))
        for (y, m) in W.MONTHS:
            mdays = 28 if m == 2 else 30
            seas = 1.0 + 0.12 * (1 if m in (10, 11, 12, 3) else 0) - 0.08 * (1 if m in (1, 7) else 0)
            for c in pool:
                d0 = W.D(y, m, 1)
                if not self.live(c, d0) and not self.live(c, W.D(y, m, 25)):
                    continue
                R = (c["turnover"] or 1e6) / 12.0 * seas * r.uniform(0.86, 1.14)
                acct = self.cheque(c)
                # receipts from customers of the bank
                used = 0.0
                for l in by_payee.get(c["cid"], []):
                    if not (l["start"] <= d0 <= l["end"]) and not (l["start"] <= W.D(y, m, 28) <= l["end"]):
                        continue
                    p = cust[l["payer"]]
                    if not self.live(p, d0):
                        continue
                    amt = R * l["share"] * r.uniform(0.9, 1.1)
                    used += l["share"]
                    k = 1 if l.get("small") else 2
                    for j in range(k):
                        d = W.D(y, m, min(mdays, 6 + 14 * j + r.randint(0, 5)))
                        if l["end"] < d:
                            continue
                        part = amt / k * r.uniform(0.94, 1.06)
                        pa = self.cheque(p)
                        self.add(d, acct, "DC", part, p["trading"].upper()[:20],
                                 self.counter_ref(p, pa, d, stale.get((p["cid"], c["cid"]))),
                                 "INV%s" % d.strftime("%y%m"), "", c["trading"].upper()[:12])
                        self.add(d, pa, "DC", -part, c["trading"].upper()[:20],
                                 self.counter_ref(c, acct, d, stale.get((p["cid"], c["cid"]))),
                                 c["trading"][:12].upper(), "SUPPLIER", "INV%s" % d.strftime("%y%m"))
                # receipts from outside the bank
                rest = max(0.0, 1.0 - used)
                card = 0.3 if c["sector"] == "G" else 0.0
                n_ext = r.choice([2, 3, 3, 4])
                if c["role"] in ("watch", "anchor", "survivor"):
                    n_ext = 5
                ws = [r.uniform(0.6, 1.4) for _ in range(n_ext)]
                tot = sum(ws)
                for j, wv in enumerate(ws):
                    key = (c["cid"], (j + y * 7 + m) % (n_ext + 4))
                    name, ea = self.ext_party(key)
                    amt = R * (rest - card) * wv / tot
                    if amt <= 0:
                        continue
                    d = W.D(y, m, min(mdays, 3 + r.randint(0, 24)))
                    self.add(d, acct, r.choice(["DC", "DC", "BP"]), amt, name.upper()[:20], fmt_variants(ea, r),
                             r.choice(["INVOICE", "ACCOUNT", "STMT", ""]), "", "")
                if card:
                    for wk in range(4):
                        d = W.D(y, m, min(mdays, 4 + 7 * wk))
                        self.add(d, acct, "EFT", R * card / 4 * r.uniform(0.85, 1.15), "TAPCARD MERCHANT SVCS",
                                 "", "SETTLEMENT", "", "")
                # outgoings to outside parties
                out = R * r.uniform(0.82, 0.97)
                for s in r.sample(SUPPLIERS, 2):
                    name, ea = self.ext_party((c["cid"], "sup", s))
                    d = W.D(y, m, min(mdays, 10 + r.randint(0, 16)))
                    self.add(d, acct, r.choice(["AP", "BP", "DD"]), -out * r.uniform(0.15, 0.3),
                             name.upper()[:20], fmt_variants(ea, r), s.upper(), "", "")
                d = W.D(y, m, min(mdays, 20 + r.randint(0, 6)))
                self.add(d, acct, "AP", -out * r.uniform(0.25, 0.35), "PAYROLL", "", "WAGES", "", "")
                if m % 2 == 0:
                    self.add(W.D(y, m, 28), acct, "BP", -out * r.uniform(0.06, 0.1), "INLAND REVENUE",
                             "03-0049-0001100-27", "GST", c["nzbn"][-9:], "")
                # own-account moves and loan flows
                if len(c["accounts"]) > 1 and r.random() < 0.35:
                    sv = c["accounts"][1]
                    if sv["opened"] <= d0 and (sv["closed"] is None or d0 <= sv["closed"]):
                        amt = R * r.uniform(0.03, 0.08)
                        d = W.D(y, m, min(mdays, 14 + r.randint(0, 8)))
                        sign = 1 if r.random() < 0.45 else -1
                        self.add(d, acct, "FT", sign * amt, "OWN ACCOUNT", self.counter_ref(c, sv, d), "TRANSFER", "", "")
                        self.add(d, sv, "FT", -sign * amt, "OWN ACCOUNT", self.counter_ref(c, acct, d), "TRANSFER", "", "")
                for f in c.get("facilities", []):
                    if f["revolving"]:
                        continue
                    if r.random() < 0.9:
                        d = W.D(y, m, min(mdays, 15))
                        self.add(d, acct, "LN", -f["drawn"] * 0.012 * r.uniform(0.95, 1.05), "RUAHINE LENDING",
                                 "%s-1299-%07d-%03d" % (W.BANK, int(f["fid"][1:]) % 9999999, 1), "LOAN", "REPAYMENT", "")
        self.rows.sort(key=lambda x: (x[0], x[1], -x[3]))
        return self.rows


def build(w):
    return Ledger(w).build()
