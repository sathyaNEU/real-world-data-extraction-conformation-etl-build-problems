"""The seeded world behind task268: Corcally's homes, members, Rewards cards and bank cards; every 2026 coffee purchase
in the three stores and the online shop; the coffee counter's labels and payments; the multibuy deals, their savings,
the missed ones and the service desk's adjustments; Faircourt's settlement of every card payment. The truth tables
(each card's home, each label's sale) stay here; the pack writes only what each system holds."""
import bisect
import collections
import datetime as dt
import itertools

import numpy as np

import common as K

D0 = dt.date(K.YEAR, 1, 1)
DAYS = [D0 + dt.timedelta(days=i) for i in range(365)]
CLOSED = {dt.date(K.YEAR, 12, 25), dt.date(K.YEAR, 12, 26)}
TRADING = [d for d in DAYS if d not in CLOSED]
BANK_HOLIDAYS = {dt.date(2026, 1, 1), dt.date(2026, 2, 2), dt.date(2026, 3, 17), dt.date(2026, 4, 6),
                 dt.date(2026, 5, 4), dt.date(2026, 6, 1), dt.date(2026, 8, 3), dt.date(2026, 10, 26),
                 dt.date(2026, 12, 25), dt.date(2026, 12, 28), dt.date(2027, 1, 1)}
BI = {b: i for i, b in enumerate(K.B)}

PARAMS = dict(
    H=3000, nonmem=0.8, alpha=0.35, occ=1.8, pres=0.92, house=0.45, cash=0.15,
    shop=0.86, sep=0.08, ksh=0.6, kmin=3, mb=0.35, claim=0.7,
    mix={
        'P':   [0.33, 0.24, 0.10, 0.02, 0.05, 0.17, 0.02, 0.10],
        'PON': [0.02, 0.17, 0.08, 0.02, 0.04, 0.10, 0.40, 0.12],
        'Q':   [0.02, 0.12, 0.17, 0.46, 0.04, 0.07, 0.00, 0.10],
        'QON': [0.01, 0.13, 0.18, 0.47, 0.04, 0.07, 0.00, 0.10],
        'K':   [0.07, 0.15, 0.07, 0.16, 0.34, 0.17, 0.00, 0.04],
        'KON': [0.01, 0.16, 0.08, 0.17, 0.35, 0.19, 0.00, 0.04],
        'S':   [0.065, 0.24, 0.10, 0.04, 0.32, 0.13, 0.00, 0.06],
        'ON':  [0.62, 0.15, 0.06, 0.02, 0.03, 0.08, 0.00, 0.04],
        'N':   [0.10, 0.24, 0.12, 0.08, 0.14, 0.18, 0.04, 0.10],
    },
    rate={'S': 2.6, 'P': 3.6, 'Q': 3.0, 'K': 1.8},
    online={'S': 0.07, 'C': 0.32, 'F': 0.36},
)


def next_banking_day(d, n=1):
    while n:
        d += dt.timedelta(days=1)
        if d.weekday() < 5 and d not in BANK_HOLIDAYS:
            n -= 1
    return d


class World:
    def __init__(self, seed=K.SEED, **over):
        self.seed = seed
        self.P = dict(PARAMS)
        self.P.update(over)
        self.rng = np.random.default_rng(seed)
        self._members()
        self._deal_days()
        self._store_coffee()
        self._non_members()
        self._online()
        self._links()
        self._refunds()
        self._counter()
        self._receipts()
        self._settlement()
        self._register()

    # ------------------------------------------------------------------ people, cards, bank cards
    def _hexref(self):
        while True:
            v = "%016X" % int(self.rng.integers(0, 2 ** 63))
            if v not in self.token_owner:
                return v

    def _members(self):
        P, rng = self.P, self.rng
        self.homes, self.members, self.token_owner, self.cards = [], [], {}, {}
        self.card_seq = 0
        stores = [s[0] for s in K.STORES]
        sp = np.array([s[3] for s in K.STORES])
        for h in range(P["H"]):
            u = rng.random()
            t = 'S' if u < 0.52 else ('C' if u < 0.88 else 'F')
            online = bool(rng.random() < P["online"][t])
            roles = ['S'] if t == 'S' else (['P', 'Q'] if t == 'C' else ['P', 'Q', 'K'])
            if len(roles) == 1:
                habit = 'own'
            else:
                v = rng.random()
                habit = 'shop' if v < P["shop"] else ('own' if v < P["shop"] + P["sep"] else 'mixed')
            store = stores[int(rng.choice(3, p=sp / sp.sum()))]
            home = dict(id=h, type=t, online=online, roles=roles, habit=habit, ksh=bool(rng.random() < P["ksh"]),
                        store=store, members=[])
            self.homes.append(home)
            for r in roles:
                m = dict(id=len(self.members), home=h, role=r, tokens=[], card=None, cards=[], store=store,
                         age=self._age(r))
                for k in range(2 if rng.random() < 0.25 else 1):
                    tok = self._hexref()
                    self.token_owner[tok] = m["id"]
                    m["tokens"].append(tok)
                if rng.random() < {'S': 1.0, 'P': 1.0, 'Q': 0.93, 'K': 0.85}[r]:
                    m["card"] = self._new_card(m, None)
                self.members.append(m)
                home["members"].append(m["id"])
        self.tok_info = {}
        for tok in self.token_owner:
            self._tok_info(tok)

    def _age(self, r):
        rng = self.rng
        bands = ["18-24", "25-34", "35-44", "45-54", "55-64", "65+"]
        p = {'S': [0.10, 0.22, 0.14, 0.14, 0.16, 0.24], 'P': [0.02, 0.18, 0.26, 0.24, 0.18, 0.12],
             'Q': [0.03, 0.19, 0.25, 0.24, 0.17, 0.12], 'K': [0.62, 0.38, 0, 0, 0, 0]}[r]
        return bands[int(rng.choice(6, p=p))]

    def _tok_info(self, tok, region=None):
        rng = self.rng
        u = rng.random()
        product = 'DEBIT' if u < 0.78 else ('CREDIT' if u < 0.96 else ('PREPAID' if u < 0.99 else 'COMMERCIAL'))
        scheme = 'VISA' if rng.random() < 0.6 else 'MASTERCARD'
        self.tok_info[tok] = (scheme, product, region or 'DOMESTIC')

    def _new_card(self, m, issued):
        rng = self.rng
        while True:
            body = "2981" + "%08d" % int(rng.integers(0, 10 ** 8))
            no = K.ean13(body)
            if no not in self.cards:
                break
        if issued is None:
            issued = dt.date(2019, 4, 1) + dt.timedelta(days=int(rng.integers(0, 2400)))
        self.cards[no] = dict(no=no, member=m["id"], type="MEMBER", issued=issued, status="ACTIVE", status_date=None,
                              replaced_by=None, store=m["store"])
        m["cards"].append(no)
        return no

    # ------------------------------------------------------------------ deals: which days the tills ran them
    def _deal_days(self):
        rng = self.rng
        self.deal_missed = {}
        for d in K.DEALS:
            # the store whose tills did not take the deal's promotion file until someone noticed
            store = ["DRM", "LSG", "KBN"][int(rng.choice(3, p=[0.5, 0.25, 0.25]))]
            n = int(rng.integers(7, 12)) + (3 if store != "DRM" else 0)
            self.deal_missed[d[0]] = (store, set(d[4] + dt.timedelta(days=i) for i in range(n)))

    def deal_for(self, plu, day):
        for d in K.DEALS:
            if plu in d[2] and d[4] <= day <= d[5]:
                return d
        return None

    # ------------------------------------------------------------------ store coffee purchases
    def _pick_time(self, store, day):
        rng = self.rng
        lo, hi = dict((s[0], s[4]) for s in K.STORES)[store]
        prof = np.array([0.5, 0.8, 1.1, 1.3, 1.2, 1.1, 1.0, 1.0, 1.1, 1.3, 1.2, 0.9, 0.6, 0.4][: hi - lo])
        hr = lo + int(rng.choice(len(prof), p=prof / prof.sum()))
        return dt.datetime.combine(day, dt.time(hr, int(rng.integers(0, 60)), int(rng.integers(0, 60))))

    def _payer(self, m):
        """The bank card a member pays a store purchase with, or None for cash."""
        rng = self.rng
        home = self.homes[m["home"]]
        if rng.random() < self.P["cash"]:
            return None
        own = m["tokens"][0] if (len(m["tokens"]) == 1 or rng.random() < 0.8) else m["tokens"][1]
        if m["role"] in ('Q', 'K') and home["habit"] != 'own':
            p_use = {'shop': 0.7, 'mixed': 0.3}[home["habit"]] * (1.0 if m["role"] == 'Q' else (0.5 if home["ksh"] else 0.0))
            if rng.random() < p_use:
                return self.members[home["members"][0]]["tokens"][0]
        return own

    def _basket(self, brands, day, store):
        """Pack lines for the chosen brands; a deal on the pack makes a pair likelier. Returns lines and the multibuy
        state (deal id, pairs, missed)."""
        rng = self.rng
        lines, mbs = [], []
        for b in brands:
            plus = K.SKUS_OF[b]
            w = np.array([3.0 if K.SKU[p][7] < 6 else 1.6 for p in plus])
            plu = plus[int(rng.choice(len(plus), p=w / w.sum()))]
            deal = self.deal_for(plu, day)
            qty = 1
            if deal is not None and rng.random() < self.P["mb"]:
                qty = 2
                if rng.random() < 0.2:
                    qty = 4
            elif rng.random() < 0.06:
                qty = 2
            for _ in range(qty):
                lines.append(dict(plu=plu, brand=b, qty=1, value=K.SKU[plu][7]))
            if deal is not None and qty >= 2:
                mbs.append((deal[0], qty // 2))
        return lines, mbs

    def _store_coffee(self):
        P, rng = self.P, self.rng
        self.tx = []
        self.adj_claims = []
        for home in self.homes:
            for mid in home["members"]:
                m = self.members[mid]
                key = (m["role"] + 'ON') if (home["online"] and m["role"] in ('P', 'Q', 'K')) else m["role"]
                pv = rng.dirichlet(P["alpha"] * np.array(P["mix"][key]) * len(K.B))
                n = int(rng.poisson(rng.gamma(2.0, P["rate"][m["role"]]) * P["occ"]))
                days = sorted(TRADING[int(i)] for i in rng.integers(0, len(TRADING), size=n))
                for day in days:
                    nb = 1 + int(rng.random() < 0.18)
                    brands = sorted(set(K.B[j] for j in rng.choice(len(K.B), size=nb, p=pv)), key=BI.get)
                    store = home["store"] if rng.random() < 0.95 else ["DRM", "LSG", "KBN"][int(rng.integers(0, 3))]
                    when = self._pick_time(store, day)
                    self._add_store_tx(m, store, when, brands)

    def _add_store_tx(self, m, store, when, brands):
        rng = self.rng
        lines, mbs = self._basket(brands, when.date(), store)
        if m is not None and m["card"] is not None and rng.random() < self.P["pres"]:
            card = 'MEMBER'
        else:
            card = None
        tok = self._payer(m) if m is not None else None
        t = dict(kind='sale', store=store, when=when, member=m["id"] if m else None,
                 home=m["home"] if m else None, card=card, tok=tok, lines=lines, saving=[])
        for deal_id, pairs in mbs:
            missed_store, missed_days = self.deal_missed[deal_id]
            missed = store == missed_store and when.date() in missed_days
            deal = K.DEAL[deal_id]
            plus = [ln["plu"] for ln in lines if ln["plu"] in deal[2]]
            save = K.r2(sum(K.SKU[p][7] for p in plus[:2]) - deal[3])
            if missed:
                if rng.random() < self.P["claim"]:
                    self.adj_claims.append(dict(tx=t, deal=deal_id, pairs=pairs, save=save))
            else:
                for _ in range(pairs):
                    t["saving"].append(dict(deal=deal_id, value=-save))
        self.tx.append(t)
        return t

    def _non_members(self):
        P, rng = self.P, self.rng
        self.nonmem_tokens = []
        stores = [s[0] for s in K.STORES]
        for k in range(int(P["H"] * P["nonmem"])):
            tok = self._hexref()
            self.token_owner[tok] = -1 - k
            region = 'DOMESTIC' if rng.random() < 0.93 else ('EEA' if rng.random() < 0.6 else 'INTERNATIONAL')
            self._tok_info(tok, region)
            self.nonmem_tokens.append(tok)
            pv = rng.dirichlet(P["alpha"] * np.array(P["mix"]['N']) * len(K.B))
            store = stores[int(rng.choice(3, p=[0.62, 0.2, 0.18]))]
            n = int(rng.poisson(rng.gamma(2.0, 2.0)))
            for i in range(n):
                day = TRADING[int(rng.integers(0, len(TRADING)))]
                brand = K.B[int(rng.choice(len(K.B), p=pv))]
                when = self._pick_time(store, day)
                lines, mbs = self._basket([brand], day, store)
                card = 'HOUSE' if rng.random() < 0.35 else None
                tk = None if rng.random() < 0.25 else tok
                t = dict(kind='sale', store=store, when=when, member=None, home=None, nonmem=k, card=card, tok=tk,
                         lines=lines, saving=[])
                for deal_id, pairs in mbs:
                    missed_store, missed_days = self.deal_missed[deal_id]
                    deal = K.DEAL[deal_id]
                    plus = [ln["plu"] for ln in lines if ln["plu"] in deal[2]]
                    save = K.r2(sum(K.SKU[p][7] for p in plus[:2]) - deal[3])
                    if store == missed_store and day in missed_days:
                        if rng.random() < self.P["claim"]:
                            self.adj_claims.append(dict(tx=t, deal=deal_id, pairs=pairs, save=save))
                    else:
                        for _ in range(pairs):
                            t["saving"].append(dict(deal=deal_id, value=-save))
                self.tx.append(t)

    # ------------------------------------------------------------------ the online shop
    def _online(self):
        P, rng = self.P, self.rng
        self.accounts, self.orders = {}, []
        seq = 0
        online_plus = {b: [p for p in K.SKUS_OF[b] if K.SKU[p][8] == "Y"] for b in K.B}
        for home in self.homes:
            if not home["online"]:
                continue
            holder = self.members[home["members"][0]]
            acc = "CA%06d" % (104000 + int(rng.integers(0, 890000)))
            while acc in self.accounts:
                acc = "CA%06d" % (104000 + int(rng.integers(0, 890000)))
            self.accounts[acc] = dict(id=acc, home=home["id"], holder=holder["id"],
                                      opened=dt.date(2023, 5, 1) + dt.timedelta(days=int(rng.integers(0, 900))))
            pv = rng.dirichlet(P["alpha"] * np.array(P["mix"]['ON']) * len(K.B))
            n = int(rng.poisson(17))
            starts = sorted(K.ONLINE_FROM + dt.timedelta(days=int(i)) for i in rng.integers(0, 395, size=n))
            first = len(self.orders)
            for placed_day in starts:
                has_coffee = rng.random() < 0.40
                nb = 1 + int(rng.random() < 0.25)
                brands = sorted(set(K.B[j] for j in rng.choice(len(K.B), size=nb, p=pv)), key=BI.get)
                brands = [b for b in brands if online_plus[b]]
                seq += 1
                if has_coffee and brands:
                    self._add_order(acc, home, holder, placed_day, brands, online_plus, seq)
            # an order straddling a year end carries only coffee the account also had delivered inside 2026
            mine = self.orders[first:]
            core = set()
            for o in mine:
                if o["status"] == 'delivered' and o["placed"].year == K.YEAR and o["delivery"].year == K.YEAR:
                    core |= {K.SKU[c["plu"]][1] for c in o["versions"][-1]["coffee"]}
            keep = []
            for o in mine:
                if o["placed"].year != K.YEAR or o["delivery"].year != K.YEAR:
                    for v in o["versions"]:
                        v["coffee"] = [c for c in v["coffee"] if K.SKU[c["plu"]][1] in core]
                    if not o["versions"][-1]["coffee"]:
                        continue
                keep.append(o)
            self.orders[first:] = keep
        self.orders.sort(key=lambda o: (o["placed"], o["no"]))

    def _order_token(self, home, holder):
        rng = self.rng
        if len(home["members"]) > 1 and home["habit"] != 'own' and rng.random() < 0.3:
            return self.members[home["members"][1]]["tokens"][0]
        return holder["tokens"][0]

    def _add_order(self, acc, home, holder, placed_day, brands, online_plus, seq, cancel_ok=True):
        rng = self.rng
        placed = dt.datetime.combine(placed_day, dt.time(int(rng.integers(7, 23)), int(rng.integers(0, 60)),
                                                         int(rng.integers(0, 60))))
        delivery = placed_day + dt.timedelta(days=int(rng.integers(1, 6)))
        if delivery in CLOSED:
            delivery += dt.timedelta(days=2)
        coffee = []
        for b in brands:
            plus = online_plus[b]
            plu = plus[int(rng.integers(0, len(plus)))]
            coffee.append(dict(plu=plu, qty=1 + int(rng.random() < 0.2)))
        other = K.r2(float(rng.lognormal(4.1, 0.45)))
        versions = [dict(coffee=[dict(c) for c in coffee], other=other)]
        for _ in range(int(rng.poisson(0.4))):
            last = versions[-1]
            cv = [dict(c) for c in last["coffee"]]
            if cv and rng.random() < 0.6:
                c = cv[int(rng.integers(0, len(cv)))]
                c["qty"] = max(1, c["qty"] + (1 if rng.random() < 0.6 else -1))
            versions.append(dict(coffee=cv, other=K.r2(last["other"] * float(rng.uniform(0.85, 1.25)))))
        status = 'cancelled' if (cancel_ok and rng.random() < 0.04) else 'delivered'
        o = dict(no="WO%07d" % (2600000 + seq * 7 + int(rng.integers(0, 7))), account=acc, home=home["id"],
                 placed=placed, delivery=delivery, versions=versions, status=status,
                 tok=self._order_token(home, holder))
        self.orders.append(o)
        if status == 'cancelled' and brands:
            # the order is placed again a few days later with the same coffee
            redo = placed_day + dt.timedelta(days=int(rng.integers(1, 4)))
            self._add_order(acc, home, holder, redo, brands, online_plus, seq + 500000, cancel_ok=False)
        return o

    # ------------------------------------------------------------------ link strength
    def _node(self, t):
        if t.get("kind") != 'sale' or t["card"] != 'MEMBER':
            return None
        return self.members[t["member"]]["card"]

    def _links(self):
        """A home's shared bank card is a habit: every card (or account) that pays with a bank card someone else's card
        also pays with does so at least kmin times; a weaker use falls back to the member's own card (an account gets a
        card of its own), so one, two or three shared payments build the same homes."""
        kmin = self.P["kmin"]
        own_of = {m["id"]: m["tokens"][0] for m in self.members}
        owner_card = {tk: m["card"] for m in self.members for tk in m["tokens"]}
        sales = [t for t in self.tx if self._node(t) is not None]
        deliv = [o for o in self.orders if o["status"] == 'delivered' and o["delivery"].year == K.YEAR]
        for it in range(200):
            cnt = collections.Counter()
            for t in sales:
                if t["tok"] is not None:
                    cnt[(t["tok"], self._node(t))] += 1
            for o in deliv:
                cnt[(o["tok"], o["account"])] += 1
            nodes = collections.defaultdict(set)
            for (tk, nd) in cnt:
                nodes[tk].add(nd)
            weak = sorted((tk, nd) for (tk, nd), n in cnt.items() if len(nodes[tk]) > 1 and n < kmin)
            if not weak:
                break
            by_tok = collections.defaultdict(list)
            for t in sales:
                by_tok[t["tok"]].append(t)
            ord_tok = collections.defaultdict(list)
            for o in self.orders:
                ord_tok[o["tok"]].append(o)
            done = set()
            for tk, nd in weak:
                if tk in done:
                    continue
                done.add(tk)
                if nd.startswith("CA"):
                    newtok = self._fresh_token(self.accounts[nd])
                    for o in ord_tok[tk]:
                        if o["account"] == nd:
                            o["tok"] = newtok
                elif owner_card.get(tk) != nd:
                    for t in by_tok[tk]:
                        if self._node(t) == nd:
                            t["tok"] = own_of[t["member"]]
                else:
                    for t in by_tok[tk]:
                        if self._node(t) != nd:
                            t["tok"] = own_of[t["member"]]
                    fresh = {}
                    for o in ord_tok[tk]:
                        if o["account"] not in fresh:
                            fresh[o["account"]] = self._fresh_token(self.accounts[o["account"]])
                        o["tok"] = fresh[o["account"]]
        self.link_iterations = it

    def _fresh_token(self, acc):
        holder = self.members[acc["holder"]]
        for tk in holder["tokens"][1:]:
            if not any(t["tok"] == tk for t in self.tx if t.get("kind") == 'sale'):
                return tk
        tk = self._hexref()
        self.token_owner[tk] = holder["id"]
        self._tok_info(tk)
        holder["tokens"].append(tk)
        return tk

    # ------------------------------------------------------------------ refunds (a pack bought again later)
    def _refunds(self):
        rng = self.rng
        by_card = collections.defaultdict(list)
        for t in self.tx:
            if t["card"] == 'MEMBER' and t["tok"] is not None:
                by_card[self.members[t["member"]]["card"]].append(t)
        self.refunds = []
        for card, txs in sorted(by_card.items()):
            if len(txs) < 3 or rng.random() > 0.05:
                continue
            txs = sorted(txs, key=lambda x: x["when"])
            src = txs[int(rng.integers(0, len(txs) - 1))]
            ln = src["lines"][0]
            # only a brand the card buys again on a later receipt
            later = [x for x in txs if x["when"] > src["when"] and any(l2["brand"] == ln["brand"] for l2 in x["lines"])]
            if not later:
                continue
            when = src["when"] + dt.timedelta(days=int(rng.integers(1, 12)), minutes=int(rng.integers(5, 300)))
            if when.year != K.YEAR or when.date() in CLOSED:
                continue
            when = when.replace(hour=min(max(when.hour, 9), 19))
            rev = []
            for s in src["saving"]:
                if K.DEAL[s["deal"]][2] and ln["plu"] in K.DEAL[s["deal"]][2]:
                    rev.append(dict(deal=s["deal"], value=-s["value"]))
                    break
            r = dict(kind='refund', store=src["store"], when=when, member=src["member"], home=src["home"],
                     card='MEMBER', tok=src["tok"], lines=[dict(plu=ln["plu"], brand=ln["brand"], qty=-1,
                                                                value=-ln["value"])],
                     saving=rev, orig=src)
            self.refunds.append(r)
            self.tx.append(r)

    # ------------------------------------------------------------------ the coffee counter
    def _counter(self):
        rng = self.rng
        self.labels, self.counter_pay = [], []
        seq = {"S1": 10418, "S2": 2276}
        members = [m for m in self.members if m["store"] == "DRM"]
        coffees = [(r[0], c[0], c[1], c[2]) for r in K.ROASTERS for c in r[2]]
        rshare = {"GLN": 0.38, "ARD": 0.35, "INB": 0.27}
        cw = np.array([rshare[c[0]] / 2 for c in coffees])
        acc_p = [a[1] for a in K.ACCESSORIES]
        for day in TRADING:
            sunday = day.weekday() == 6
            lo, hi = (12, 17) if sunday else K.COUNTER_HOURS
            n = int(rng.poisson(24 if sunday else 38))
            starts = sorted(dt.datetime.combine(day, dt.time(lo)) + dt.timedelta(seconds=int(s))
                            for s in rng.integers(0, (hi - lo) * 3600 - 900, size=n))
            for st in starts:
                scale = "S1" if rng.random() < 0.5 else "S2"
                u = rng.random()
                nlab = 1 if u < 0.8 else (2 if u < 0.97 else 3)
                same = nlab >= 2 and rng.random() < 0.35
                chosen = []
                for i in range(nlab):
                    if i > 0 and same:
                        chosen.append(chosen[0])
                    else:
                        chosen.append(coffees[int(rng.choice(len(coffees), p=cw / cw.sum()))])
                t = st
                sold = []
                for c in chosen:
                    nominal = float(rng.choice([0.125, 0.25, 0.5, 1.0, 0.2, 0.3], p=[0.08, 0.6, 0.2, 0.05, 0.04, 0.03]))
                    if rng.random() < 0.11:
                        w1 = round(nominal * float(rng.uniform(0.82, 0.95)), 3)
                        c1 = c if rng.random() < 0.75 else coffees[int(rng.choice(len(coffees), p=cw / cw.sum()))]
                        self._label(scale, seq, t, c1, w1, sold=False)
                        t += dt.timedelta(seconds=int(rng.integers(40, 150)))
                    w = round(nominal * float(rng.uniform(0.99, 1.05)), 3)
                    sold.append(self._label(scale, seq, t, c, w, sold=True))
                    t += dt.timedelta(seconds=int(rng.integers(30, 110)))
                member = members[int(rng.integers(0, len(members)))] if rng.random() < 0.7 else None
                if rng.random() < 0.72:
                    nacc = 0 if rng.random() > 0.12 else (1 if rng.random() < 0.85 else 2)
                    accs = [int(rng.integers(0, len(acc_p))) for _ in range(nacc)]
                    amount = K.r2(sum(lb["price"] for lb in sold) + sum(acc_p[a] for a in accs))
                    when = t + dt.timedelta(seconds=int(rng.integers(20, 180)))
                    tok = (self._payer(member) if member else None) or (
                        member["tokens"][0] if member else self.nonmem_tokens[int(rng.integers(0, len(self.nonmem_tokens)))])
                    pay = dict(when=when, amount=amount, labels=sold, accessories=accs, tok=tok)
                    for lb in sold:
                        lb["paid"] = ("card", pay)
                    self.counter_pay.append(pay)
                else:
                    when = t + dt.timedelta(minutes=int(rng.integers(5, 90)))
                    if when.hour >= 22:
                        when = when.replace(hour=21, minute=50)
                    tx = dict(kind='counter', store="DRM", when=when, member=member["id"] if member else None,
                              home=member["home"] if member else None,
                              card='MEMBER' if (member and member["card"] and rng.random() < self.P["pres"]) else None,
                              tok=None, lines=[], saving=[], counter=sold)
                    for lb in sold:
                        lb["paid"] = ("till", tx)
                    self.tx.append(tx)
        self._counter_unique()
        self.labels.sort(key=lambda lb: (lb["scale"], lb["no"]))

    COUNTER_WIN = (dt.timedelta(minutes=29), dt.timedelta(minutes=7))
    TILL_WIN = (dt.timedelta(minutes=154), dt.timedelta(minutes=5))

    def _counter_unique(self):
        """Every counter card payment is the sum of one set of labels plus accessories, and every counter line on a till
        is one label's price, among the labels a matcher could consider: a label that would make a second reading
        possible is re-weighed by a gram."""
        acc = [0.0] + [a[1] for a in K.ACCESSORIES] + \
            [a[1] + b[1] for i, a in enumerate(K.ACCESSORIES) for b in K.ACCESSORIES[i:]]
        accset = set(int(round(x * 100)) for x in acc)
        till_tx = [t for t in self.tx if t["kind"] == 'counter']

        def bump(lb):
            lb["kg"] = round(lb["kg"] + 0.001, 3)
            lb["price"] = K.r2(lb["kg"] * lb["ppk"])

        for it in range(60):
            labs = sorted(self.labels, key=lambda x: x["when"])
            keys = [x["when"] for x in labs]
            used = set()
            changed = 0
            for p in sorted(self.counter_pay, key=lambda x: x["when"]):
                p["amount"] = K.r2(sum(lb["price"] for lb in p["labels"]) +
                                   sum(K.ACCESSORIES[a][1] for a in p["accessories"]))
                lo = bisect.bisect_left(keys, p["when"] - self.COUNTER_WIN[0])
                hi = bisect.bisect_right(keys, p["when"] + self.COUNTER_WIN[1])
                cands = [x for x in labs[lo:hi] if (x["scale"], x["no"]) not in used]
                amt = int(round(p["amount"] * 100))
                fits = []
                for k in (1, 2, 3):
                    for comb in itertools.combinations(cands, k):
                        if amt - sum(int(round(x["price"] * 100)) for x in comb) in accset:
                            fits.append(frozenset((x["scale"], x["no"]) for x in comb))
                true = frozenset((x["scale"], x["no"]) for x in p["labels"])
                if fits != [true]:
                    alts = [f for f in fits if f != true]
                    byid = {(x["scale"], x["no"]): x for x in cands}
                    if alts:
                        alt = alts[0]
                        pick = sorted(true - alt) or sorted(alt - true)
                        bump(byid[pick[0]])
                    else:
                        bump(max(p["labels"], key=lambda x: x["price"]))
                    changed += 1
                used |= true
            for t in sorted(till_tx, key=lambda x: x["when"]):
                for lb in t["counter"]:
                    lo = bisect.bisect_left(keys, t["when"] - self.TILL_WIN[0])
                    hi = bisect.bisect_right(keys, t["when"] + self.TILL_WIN[1])
                    cands = [x for x in labs[lo:hi] if (x["scale"], x["no"]) not in used and abs(x["price"] - lb["price"]) < 0.005]
                    if [(x["scale"], x["no"]) for x in cands] != [(lb["scale"], lb["no"])]:
                        bump(lb)
                        changed += 1
                    used.add((lb["scale"], lb["no"]))
            if not changed:
                break
        self.counter_iterations = it

    def _label(self, scale, seq, when, coffee, weight, sold):
        seq[scale] += 1
        rid, name, ph1, ph2 = coffee
        ppk = ph1 if when.date() < K.PRICE_CHANGE else ph2
        shown = when
        if scale == "S2" and K.SCALE_RESET <= when < K.SCALE_FIXED:
            shown = dt.datetime(K.YEAR, 1, 1) + (when - K.SCALE_RESET)
        lb = dict(no=seq[scale], scale=scale, when=when, shown=shown, roaster=rid, coffee=name, kg=weight,
                  ppk=ppk, price=K.r2(weight * ppk), sold=sold, paid=None)
        self.labels.append(lb)
        return lb

    # ------------------------------------------------------------------ till receipts and the service desk
    def _receipts(self):
        rng = self.rng
        # service-desk adjustments for multibuys the tills missed: cash, a later receipt, the original cited
        for c in self.adj_claims:
            src = c["tx"]
            when = src["when"] + dt.timedelta(days=int(rng.integers(3, 49)), minutes=int(rng.integers(0, 240)))
            if when.year != K.YEAR or when.date() in CLOSED:
                continue
            when = when.replace(hour=min(max(when.hour, 9), 20))
            c["when"] = when
        claims = [c for c in self.adj_claims if "when" in c]
        # a customer missing two multibuys on one receipt gets one adjustment line for both
        by_src = collections.defaultdict(list)
        for c in claims:
            by_src[id(c["tx"])].append(c)
        self.adjust = []
        for key, cs in by_src.items():
            src = cs[0]["tx"]
            total = K.r2(sum(c["save"] * c["pairs"] for c in cs))
            a = dict(kind='adjust', store=src["store"], when=cs[0]["when"], member=src["member"], home=src["home"],
                     card=src["card"], tok=None, lines=[], saving=[], claims=cs, value=-total, orig=src)
            self.adjust.append(a)
            self.tx.append(a)
        # tills, receipt numbers, baskets and amounts
        tills = {s[0]: [t for t in s[2] if t != K.DESK] for s in K.STORES}
        self.tx.sort(key=lambda t: (t["when"], t["store"], t.get("member") or 0))
        busy = collections.defaultdict(list)
        for t in self.tx:
            if t["kind"] in ('refund', 'adjust'):
                t["till"] = K.DESK
            else:
                opts = tills[t["store"]]
                t["till"] = opts[int(rng.integers(0, len(opts)))]
            key = (t["store"], t["till"], t["when"].date())
            # one receipt at a time on a till: keep sixty seconds between the extract's receipts
            while any(abs((t["when"] - w).total_seconds()) < 60 for w in busy[key]):
                t["when"] += dt.timedelta(seconds=61)
            busy[key].append(t["when"])
        self.tx.sort(key=lambda t: (t["store"], t["till"], t["when"]))
        counter = {}
        for t in self.tx:
            k = (t["store"], t["till"])
            counter.setdefault(k, int(rng.integers(1200, 9000)))
            counter[k] += int(rng.integers(3, 40))
            t["receipt"] = counter[k]
            coffee = sum(ln["value"] for ln in t["lines"]) + sum(s["value"] for s in t["saving"])
            coffee += sum(lb["price"] for lb in t.get("counter", []))
            if t["kind"] == 'adjust':
                coffee = t["value"]
            if t["kind"] in ('refund', 'adjust'):
                other = 0.0
            else:
                other = K.r2(float(rng.lognormal(3.2, 0.8))) if rng.random() < 0.85 else 0.0
            t["total"] = K.r2(coffee + other)
            if t["kind"] == 'adjust':
                t["tok"] = None
            if t["tok"] is None:
                t["card_amount"] = 0.0
            elif t["kind"] == 'sale' and t["total"] > 25 and rng.random() < 0.02:
                cash = float(rng.choice([5, 10, 20]))
                t["card_amount"] = K.r2(t["total"] - cash)
            else:
                t["card_amount"] = t["total"]
        seen = collections.defaultdict(list)
        for t in sorted(self.tx, key=lambda x: (x["store"], x["till"], x["when"])):
            if t["card_amount"] == 0:
                continue
            if t["kind"] == 'refund':
                continue
            key = (t["store"], t["till"], t["when"].date())
            while round(t["card_amount"], 2) in seen[key]:
                t["total"] = K.r2(t["total"] + 0.37)
                t["card_amount"] = K.r2(t["card_amount"] + 0.37)
            seen[key].append(round(t["card_amount"], 2))
        self.tx.sort(key=lambda t: (t["when"], t["store"], t["till"]))

    # ------------------------------------------------------------------ Faircourt's settlement
    def tid_of(self, store, till, when):
        if (store, till) == ("LSG", 2):
            return "41023202" if when < K.SWAP_DATE else "41023212"
        return [tid for s, tl, tid, a, b in K.TERMINALS if s == store and tl == till][0]

    def _fees(self, tok, amount, ecom=False):
        scheme, product, region = self.tok_info[tok]
        rate = {'DEBIT': 0.0010, 'CREDIT': 0.0030, 'PREPAID': 0.0020, 'COMMERCIAL': 0.0150}[product]
        if region != 'DOMESTIC':
            rate = 0.0030 if region == 'EEA' else 0.0115
        if ecom:
            rate += 0.0005
        inter = K.r2(amount * rate)
        scheme_fee = K.r2(amount * 0.0004 + 0.01)
        service = K.r2(0.045 + amount * 0.0005)
        return inter, scheme_fee, service

    def _settlement(self):
        rng = self.rng
        rows = []
        auth = [100000]

        def add(mid, tid, utc, typ, amount, tok, entry, ref=""):
            auth[0] += int(rng.integers(1, 97))
            scheme, product, region = self.tok_info[tok]
            inter, sf, sv = self._fees(tok, amount, ecom=(entry == 'ECOM'))
            local = K.to_local(utc).date()
            settle = next_banking_day(local, 1 if product == 'DEBIT' else 2)
            net = K.r2(amount - inter - sf - sv) if typ == 'SALE' else K.r2(-(amount) - sf - sv)
            rows.append(dict(merchant_id=mid, terminal_id=tid, txn_time_utc=utc, txn_type=typ, amount=amount,
                             currency="EUR", card_ref=tok, scheme=scheme, card_product=product, card_region=region,
                             entry_mode=entry, auth_code="%06d" % (auth[0] % 1000000), merchant_ref=ref,
                             settle_date=settle, interchange=inter, scheme_fee=sf, service_charge=sv,
                             net_settled=net))
            return rows[-1]

        self.coffee_rows = {}
        for t in self.tx:
            if t["tok"] is None or t["card_amount"] == 0:
                continue
            lag = int(rng.integers(4, 46))
            utc = K.to_utc(t["when"] - dt.timedelta(seconds=lag))
            tid = self.tid_of(t["store"], t["till"], t["when"])
            typ = 'REFUND' if t["kind"] == 'refund' else 'SALE'
            entry = 'CTLS' if (abs(t["card_amount"]) <= 100 and rng.random() < 0.82) else 'CHIP'
            r = add(K.MID[t["store"]], tid, utc, typ, K.r2(abs(t["card_amount"])), t["tok"], entry)
            self.coffee_rows[id(t)] = r
        for p in self.counter_pay:
            utc = K.to_utc(p["when"])
            entry = 'CTLS' if (p["amount"] <= 100 and rng.random() < 0.85) else 'CHIP'
            p["row"] = add(K.MID["DRM"], K.COUNTER_TID, utc, 'SALE', p["amount"], p["tok"], entry)
        for o in self.orders:
            if o["status"] != 'delivered' or o["delivery"].year != K.YEAR:
                continue
            fin = o["versions"][-1]
            total = K.r2(sum(K.SKU[c["plu"]][7] * c["qty"] for c in fin["coffee"]) + fin["other"])
            o["total"] = total
            cap = dt.datetime.combine(o["delivery"], dt.time(6, int(rng.integers(0, 60)), int(rng.integers(0, 60))))
            o["row"] = add(K.MID["WEB"], K.WEB_TID, K.to_utc(cap), 'SALE', total, o["tok"], 'ECOM', o["no"])
        self._background(add)
        rows.sort(key=lambda r: (r["txn_time_utc"], r["terminal_id"], r["amount"]))
        self.settle = rows

    def _background(self, add):
        """Every other card payment on the tills and online: the rest of the shop, never coffee."""
        rng = self.rng
        pool = [tk for m in self.members for tk in m["tokens"]] + self.nonmem_tokens
        weight = np.array([3.0 if self.token_owner[tk] >= 0 else 1.0 for tk in pool])
        weight /= weight.sum()
        taken = set()
        for r in list(self.coffee_rows.values()):
            taken.add((r["terminal_id"], K.to_local(r["txn_time_utc"]).date(), r["amount"]))
        for p in self.counter_pay:
            taken.add((p["row"]["terminal_id"], K.to_local(p["row"]["txn_time_utc"]).date(), p["row"]["amount"]))
        per_day = {"DRM": 330, "LSG": 95, "KBN": 80}
        tills = {s[0]: [t for t in s[2] if t != K.DESK] for s in K.STORES}
        for day in TRADING:
            for store, lam in per_day.items():
                n = int(rng.poisson(lam * (1.15 if day.weekday() >= 4 else 0.95)))
                toks = rng.choice(len(pool), size=n, p=weight)
                tl = rng.integers(0, len(tills[store]), size=n)
                amts = np.round(rng.lognormal(3.3, 0.85, size=n), 2)
                for i in range(n):
                    when = self._pick_time(store, day)
                    till = tills[store][int(tl[i])]
                    tid = self.tid_of(store, till, when)
                    amount = K.r2(max(0.5, float(amts[i])))
                    utc = K.to_utc(when)
                    while (tid, day, amount) in taken:
                        amount = K.r2(amount + 0.01)
                    entry = 'CTLS' if (amount <= 100 and rng.random() < 0.8) else 'CHIP'
                    add(K.MID[store], tid, utc, 'SALE', amount, pool[int(toks[i])], entry)
        # online orders without coffee, numbered from the same series as the coffee orders
        used = {o["no"] for o in self.orders}
        for acc in sorted(self.accounts):
            a = self.accounts[acc]
            home = self.homes[a["home"]]
            holder = self.members[a["holder"]]
            for _ in range(int(rng.poisson(9))):
                day = TRADING[int(rng.integers(0, len(TRADING)))]
                cap = dt.datetime.combine(day, dt.time(6, int(rng.integers(0, 60)), int(rng.integers(0, 60))))
                ref = "WO%07d" % (2600000 + int(rng.integers(0, 4000000)))
                while ref in used:
                    ref = "WO%07d" % (2600000 + int(rng.integers(0, 4000000)))
                used.add(ref)
                add(K.MID["WEB"], K.WEB_TID, K.to_utc(cap), 'SALE', K.r2(float(rng.lognormal(4.1, 0.45))),
                    holder["tokens"][0], 'ECOM', ref)

    # ------------------------------------------------------------------ the Rewards register
    def _register(self):
        rng = self.rng
        # a lost card replaced during the year: only where each half of the year keeps every shared bank card's
        # use at kmin or more, so a replaced card links to its successor and its home under every threshold
        kmin = self.P["kmin"]
        users = collections.defaultdict(set)
        for t in self.tx:
            if t["kind"] == 'sale' and t["card"] == 'MEMBER' and t["tok"] is not None:
                users[t["tok"]].add(t["member"])
        for o in self.orders:
            users[o["tok"]].add(("acc", o["account"]))
        pays = collections.defaultdict(list)
        for t in self.tx:
            if t["card"] == 'MEMBER' and t["member"] is not None:
                pays[t["member"]].append(t)
        self.replaced, self.cut = {}, {}
        for mid in sorted(pays):
            m = self.members[mid]
            sales = sorted((t for t in pays[mid] if t["kind"] == 'sale'), key=lambda x: x["when"])
            if len(sales) < 2 * kmin + 6 or rng.random() > 0.05:
                continue
            cut = sales[len(sales) // 2]["when"].date()
            ok = True
            for tk in set(t["tok"] for t in sales if t["tok"] is not None):
                before = sum(1 for t in sales if t["tok"] == tk and t["when"].date() < cut)
                after = sum(1 for t in sales if t["tok"] == tk and t["when"].date() >= cut)
                if len(users[tk]) > 1 and (0 < before < kmin or 0 < after < kmin or before == 0 or after == 0):
                    ok = False
            own = m["tokens"][0]
            if sum(1 for t in sales if t["tok"] == own and t["when"].date() < cut) < kmin or \
                    sum(1 for t in sales if t["tok"] == own and t["when"].date() >= cut) < kmin:
                ok = False
            if not ok:
                continue
            old = m["card"]
            new = self._new_card(m, cut)
            self.cards[old].update(status="REPLACED", status_date=cut, replaced_by=new)
            m["card"] = new
            self.replaced[old] = new
            self.cut[mid] = (cut, old, new)
        for t in self.tx:
            if t["card"] == 'MEMBER':
                c = self.cut.get(t["member"])
                if c:
                    t["card_no"] = c[1] if t["when"].date() < c[0] else c[2]
                else:
                    t["card_no"] = self.members[t["member"]]["card"]
            elif t["card"] == 'HOUSE':
                t["card_no"] = self.house_card(t["store"])
            else:
                t["card_no"] = ""
        # members who bought no coffee in 2026, and cards closed before or during it
        for i in range(int(len(self.members) * 0.9)):
            fake = dict(id=-10 - i, store=["DRM", "LSG", "KBN"][int(rng.choice(3, p=[0.58, 0.23, 0.19]))], cards=[])
            no = self._new_card(fake, None)
            if rng.random() < 0.06:
                self.cards[no]["status"] = "CLOSED"
                self.cards[no]["status_date"] = dt.date(2024, 1, 1) + dt.timedelta(days=int(rng.integers(0, 1000)))
            self.cards[no]["age"] = self._age('S' if rng.random() < 0.5 else 'P')
        for m in self.members:
            for no in m["cards"]:
                self.cards[no]["age"] = m["age"]
        for code, name, *_ in K.STORES:
            no = self.house_card(code)
            self.cards[no] = dict(no=no, member=None, type="STORE", issued=dt.date(2019, 4, 1), status="ACTIVE",
                                  status_date=None, replaced_by=None, store=code, age="")
        self.member_no = {}
        taken = set()
        for no, c in sorted(self.cards.items()):
            if c["type"] == "STORE":
                continue
            key = c["member"]
            if key not in self.member_no:
                while True:
                    v = "M%07d" % int(rng.integers(1100000, 1990000))
                    if v not in taken:
                        break
                taken.add(v)
                self.member_no[key] = v

    @staticmethod
    def house_card(store):
        return {"DRM": "2980000000017", "LSG": "2980000000024", "KBN": "2980000000031"}[store]

    # ------------------------------------------------------------------ truth
    def card_home(self):
        out = {}
        for m in self.members:
            for no in m["cards"]:
                out[no] = m["home"]
        return out
