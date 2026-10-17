"""The pack's tables as each system keeps them: the purchase service's validations (store units, renewals, refunds,
testers), the warehouse's purchase_completed events (duplicate uploads, restored purchases, device clocks), the session
service's session starts, the account service's links, the ECB's reference rates and the context files."""
import datetime as dt
import string

import numpy as np
import pandas as pd

import params as P

B36 = np.array(list(string.digits + string.ascii_lowercase))
ISO = "%Y-%m-%dT%H:%M:%S.%fZ"


def iso(t):
    return pd.Timestamp(t).strftime("%Y-%m-%dT%H:%M:%S.") + "%03dZ" % (pd.Timestamp(t).microsecond // 1000)


def iso_series(s):
    s = pd.to_datetime(pd.Series(s))
    return (s.dt.strftime("%Y-%m-%dT%H:%M:%S.") + (s.dt.microsecond // 1000).astype(str).str.zfill(3) + "Z").values


def irish_date(t):
    t = pd.Timestamp(t)
    return (t + pd.Timedelta(hours=1 if t < pd.Timestamp(P.IST_END) else 0)).date()


class Records:
    def __init__(self, W, seed=P.RECORD_SEED):
        self.W = W
        self.seed = seed
        self.rng = np.random.default_rng(seed)
        self.build_no = {(b[0], b[1]): b[2] for b in P.BUILDS}
        self._ids()

    # ------------------------------------------------------------------ identifiers each system issues
    def _ids(self):
        rng = self.rng
        devs = sorted(set(self.W.sessions.device) | set(self.W.purchases.device))
        self.dev_id = {}
        for d in devs:
            if d.startswith("I"):
                h = "".join(rng.choice(list("0123456789ABCDEF"), 32))
                self.dev_id[d] = "%s-%s-%s-%s-%s" % (h[:8], h[8:12], h[12:16], h[16:20], h[20:])
            else:
                self.dev_id[d] = "".join(rng.choice(list("0123456789abcdef"), 16))
        accts = sorted({i for ids in self.W.accounts.ids for (_, i) in ids})
        self.acc_id = {a: ("gst_" if a.startswith("g") else "plr_") + "".join(rng.choice(B36, 10)) for a in accts}
        self.testers = ["plr_" + "".join(rng.choice(B36, 10)) for _ in range(12)]
        self.tester_dev = {}
        for k in range(9):
            h = "".join(rng.choice(list("0123456789ABCDEF"), 32))
            self.tester_dev[("ios", k)] = "%s-%s-%s-%s-%s" % (h[:8], h[8:12], h[12:16], h[16:20], h[20:])
            self.tester_dev[("android", k)] = "".join(rng.choice(list("0123456789abcdef"), 16))

    def _price(self, product, country):
        """the storefront's price point for the product's euro tier"""
        sf = next(s for s in P.STOREFRONTS if s[0] == country)
        tier = next(p for p in P.PRODUCTS if p[0] == product)[2]
        cur, local = sf[1], tier * sf[3]
        if cur == "EUR":
            return tier, cur
        if cur in ("JPY", "KRW"):
            step = 10 if cur == "JPY" else 100
            return float(max(step, round(local / step) * step)), cur
        if cur in ("INR", "SEK", "MXN"):
            return float(max(1, round(local))), cur
        if cur == "BRL":
            return round(max(4.9, round(local) - 0.10), 2), cur
        return round(max(0.99, float(np.ceil(local)) - 0.01), 2), cur

    # ------------------------------------------------------------------ the purchase service's validations
    def _stream(self, k):
        """each table draws from its own stream, so a change to one leaves the others as they are"""
        self.rng = np.random.default_rng(self.seed * 100 + k)
        return self.rng

    def validations(self):
        rng = self._stream(1)
        W = self.W
        pu = W.purchases.copy()
        self.country = {i: a.country for a in W.accounts.itertuples() for (_, i) in a.ids}
        rows = []
        self.txn = {}
        apple_next = [2000000940000000 + int(rng.integers(0, 50000))]
        for i, r in enumerate(pu.itertuples()):
            country = self.country[r.account]
            price, cur = self._price(r.product, country)
            if r.platform == "ios":
                apple_next[0] += int(rng.integers(3, 900))
                txn = str(apple_next[0])
            else:
                txn = "GPA.%04d-%04d-%04d-%05d" % tuple(int(x) for x in rng.integers(0, [10000, 10000, 10000, 100000]))
            self.txn[i] = txn
            rows.append(self._row(r.platform, "Production", "standard", "purchase", txn, txn if r.kind == "subscription" else "",
                                  r.account, r.device, self.build_no[(r.platform, r.version)], r.product, price, cur, country,
                                  r.purchased_at))
            # the pass renews every 30 days on the store's side, with no device and no build
            if r.kind == "subscription":
                t = r.purchased_at + dt.timedelta(days=30)
                while t < P.RUN:
                    rows.append(self._renewal(r.platform, txn, r.account, r.product, price, cur, country, t))
                    t += dt.timedelta(days=30)
            # a few purchases are refunded later; the refund is its own row
            if rng.random() < 0.012:
                rt = r.purchased_at + dt.timedelta(hours=float(rng.uniform(6, 240)))
                if rt < P.RUN:
                    rows.append(self._row(r.platform, "Production", "standard", "refund", txn,
                                          txn if r.kind == "subscription" else "", r.account, r.device,
                                          self.build_no[(r.platform, r.version)], r.product, price, cur, country, rt))
        # passes bought before the export that renew inside it
        holders = W.accounts.sample(frac=0.035, random_state=int(rng.integers(0, 2 ** 31)))
        for h in holders.itertuples():
            start = P.T0 - dt.timedelta(days=float(rng.uniform(1, 30)))
            price, cur = self._price("kc.harbour_pass.monthly", h.country)
            otx = str(2000000880000000 + int(rng.integers(0, 10 ** 7))) if h.platform == "ios" else \
                "GPA.%04d-%04d-%04d-%05d" % tuple(int(x) for x in rng.integers(0, [10000, 10000, 10000, 100000]))
            t = start + dt.timedelta(days=30)
            while t < P.RUN:
                rows.append(self._renewal(h.platform, otx, h.account, "kc.harbour_pass.monthly", price, cur, h.country, t))
                t += dt.timedelta(days=30)
        # the studio's testers: TestFlight and App Review purchases in Apple's sandbox, licence testers on Google Play
        self.tester_buys = []
        for k in range(int(rng.integers(140, 190))):
            plat = "ios" if rng.random() < 0.5 else "android"
            ver = rng.choice([b[1] for b in P.BUILDS if b[0] == plat][-3:])
            prod = P.PRODUCTS[int(rng.integers(0, len(P.PRODUCTS)))][0]
            t = P.T0 + dt.timedelta(hours=float(rng.uniform(0, (P.RUN - P.T0).total_seconds() / 3600 - 1)))
            price, cur = self._price(prod, "IE")
            txn = str(2000000950000000 + k) if plat == "ios" else \
                "GPA.%04d-%04d-%04d-%05d" % tuple(int(x) for x in rng.integers(0, [10000, 10000, 10000, 100000]))
            env, ptype = ("Sandbox", "standard") if plat == "ios" else ("Production", "test")
            rows.append(self._row(plat, env, ptype, "purchase", txn, "", self.testers[k % 12],
                                  self.tester_dev[(plat, k % 9)], self.build_no[(plat, ver)], prod, price, cur, "IE", t))
            self.tester_buys.append((plat, ver, self.tester_dev[(plat, k % 9)], self.testers[k % 12], txn, t))
        V = pd.DataFrame(rows).sort_values(["validated_at", "store_transaction_id"], kind="mergesort").reset_index(drop=True)
        V.insert(0, "validation_id", ["val_%012x" % int(x) for x in rng.integers(0, 2 ** 47, len(V))])
        return V

    def _row(self, plat, env, ptype, kind, txn, otx, account, device, build, product, price, cur, country, t):
        rng = self.rng
        lag = float(rng.uniform(0.4, 4.0)) if kind == "purchase" else float(rng.uniform(1, 90))
        acct = self.acc_id.get(account, account)
        dev = self.dev_id.get(device, device)
        return dict(store="app_store" if plat == "ios" else "google_play", environment=env, purchase_type=ptype,
                    transaction_kind=kind, store_transaction_id=txn, original_transaction_id=otx, account_id=acct,
                    device_id=dev if kind != "renewal" else "", app_build=build if kind != "renewal" else "",
                    product_id=product,
                    price_minor=int(round(price * (1 if cur in ("JPY", "KRW") else 100))),
                    currency=cur, storefront=country, purchased_at=iso(t),
                    validated_at=iso(pd.Timestamp(t) + pd.Timedelta(seconds=lag)))

    def _renewal(self, plat, otx, account, product, price, cur, country, t):
        rng = self.rng
        txn = str(int(otx) + int(rng.integers(10 ** 6, 10 ** 8))) if plat == "ios" else otx + "..%d" % int(rng.integers(0, 9))
        return self._row(plat, "Production", "standard", "renewal", txn, otx, account, "", "", product, price, cur, country, t)

    # ------------------------------------------------------------------ the warehouse's purchase_completed events
    def events(self):
        rng = self._stream(2)
        W = self.W
        pu = W.purchases
        sdk_full = {(b[0], b[1]): b[4] for b in P.BUILDS}
        rows = []
        for i, r in enumerate(pu.itertuples()):
            if pd.isna(r.received):
                continue
            # the phone's clock: most within seconds, some minutes out, a few days out (players who move the clock on)
            u = rng.random()
            skew = rng.normal(0, 2) if u < 0.90 else (rng.uniform(-1800, 1800) if u < 0.98 else rng.uniform(1, 14) * 86400)
            client = pd.Timestamp(r.purchased_at) + pd.Timedelta(seconds=float(skew) + float(rng.uniform(0.2, 1.5)))
            e = dict(event_id=self._uuid(), event_name="purchase_completed", device_id=self.dev_id[r.device],
                     account_id=self.acc_id[r.account], platform=r.platform, app_version=r.version,
                     sdk_version=sdk_full[(r.platform, r.version)], store_transaction_id=self.txn[i], restored="false",
                     client_ts=int(client.value // 1_000_000), received_at=iso(r.received))
            rows.append(e)
            # an upload whose acknowledgement was lost is sent again with the same event
            if rng.random() < 0.008:
                d = dict(e); d["received_at"] = iso(pd.Timestamp(r.received) + pd.Timedelta(seconds=float(rng.uniform(20, 900))))
                rows.append(d)
            # a pass bought on a phone that later installs the game again is restored, and the game logs it again
            if r.kind == "subscription" and rng.random() < 0.10:
                t = pd.Timestamp(r.received) + pd.Timedelta(days=float(rng.uniform(1, 20)))
                if t < pd.Timestamp(P.RUN):
                    d = dict(e); d["event_id"] = self._uuid(); d["restored"] = "true"; d["received_at"] = iso(t)
                    d["client_ts"] = int(t.value // 1_000_000)
                    rows.append(d)
        # the testers' purchases are logged by the game like any other, from phones that stay in the game
        for plat, ver, dev, acct, txn, t in self.tester_buys:
            recv = pd.Timestamp(t) + pd.Timedelta(seconds=float(rng.uniform(1, 40)))
            rows.append(dict(event_id=self._uuid(), event_name="purchase_completed", device_id=dev, account_id=acct,
                             platform=plat, app_version=ver, sdk_version=sdk_full[(plat, ver)], store_transaction_id=txn,
                             restored="false", client_ts=int((pd.Timestamp(t) + pd.Timedelta(seconds=0.6)).value // 1_000_000),
                             received_at=iso(recv)))
        E = pd.DataFrame(rows).sort_values(["received_at", "event_id"], kind="mergesort").reset_index(drop=True)
        return E

    def _uuid(self):
        h = "%032x" % int(self.rng.integers(0, 2 ** 63)) + "%016x" % int(self.rng.integers(0, 2 ** 63))
        h = h[-32:]
        return "%s-%s-4%s-%s%s-%s" % (h[:8], h[8:12], h[13:16], "89ab"[int(h[16], 16) % 4], h[17:20], h[20:32])

    # ------------------------------------------------------------------ the session service's starts
    def sessions(self):
        rng = self._stream(3)
        S = self.W.sessions.sort_values(["start", "device"], kind="mergesort").reset_index(drop=True)
        ctry = {i: a.country for a in self.W.accounts.itertuples() for (_, i) in a.ids}
        out = pd.DataFrame({
            "session_id": ["%016x" % int(x) for x in rng.integers(0, 2 ** 63, len(S))],
            "device_id": S.device.map(self.dev_id),
            "account_id": S.account.map(self.acc_id),
            "platform": S.platform,
            "app_build": [self.build_no[(p, v)] for p, v in zip(S.platform, S.version)],
            "country": S.account.map(ctry),
            "started_at": iso_series(S.start),
        })
        return out

    def links(self):
        L = self.W.links
        return pd.DataFrame({"from_account_id": L.from_account.map(self.acc_id), "to_account_id": L.to_account.map(self.acc_id),
                             "link_type": L.link_type, "linked_at": [iso(t) for t in L.linked_at]}
                            ).sort_values("linked_at").reset_index(drop=True)

    # ------------------------------------------------------------------ the ECB's euro reference rates
    def rates(self):
        rng = self._stream(4)
        base = {"USD": 1.0820, "GBP": 0.8430, "BRL": 5.9210, "JPY": 163.42, "CAD": 1.4870, "AUD": 1.6510, "MXN": 19.884,
                "PLN": 4.3120, "SEK": 11.4630, "INR": 90.715, "KRW": 1488.20}
        rows = []
        lvl = dict(base)
        d = dt.date(2026, 9, 28)
        while d <= dt.date(2026, 11, 6):
            if d.weekday() < 5:
                for c in sorted(base):
                    lvl[c] *= float(np.exp(rng.normal(0, 0.0035)))
                    dec = 2 if c in ("JPY", "KRW", "INR") else 4
                    rows.append(dict(date=d.isoformat(), currency=c, rate=round(lvl[c], dec)))
            d += dt.timedelta(days=1)
        return pd.DataFrame(rows)

    # ------------------------------------------------------------------ context files
    def crash_free(self):
        rng = self._stream(5)
        S = self.W.sessions
        S = S.assign(day=S.start.dt.floor("D"))
        g = S.groupby(["day", "platform", "version"]).size().reset_index(name="n")
        rows = []
        for r in g.itertuples():
            sessions = int(r.n * rng.uniform(1.15, 1.35))       # the reporter counts every return to the foreground
            share = min(0.9995, rng.normal(0.9972 if r.version != "7.42.0" else 0.9961, 0.0009))
            rows.append(dict(date=r.day.date().isoformat(), platform=r.platform, version=r.version, sessions=sessions,
                             crash_free_share=round(share, 4)))
        return pd.DataFrame(rows).sort_values(["date", "platform", "version"]).reset_index(drop=True)

    def ratings(self):
        """the stores' weekly ratings by version: a small share of the week's players rate the game, so the counts follow
        each version's players and its average is noisier the fewer ratings it has"""
        rng = self._stream(6)
        S = self.W.sessions
        day = S.start.dt.floor("D")
        S = S.assign(week=day - pd.to_timedelta(day.dt.weekday, unit="D"))
        act = S.groupby(["week", "platform", "version"]).device.nunique()
        rows = []
        for wk in pd.date_range("2026-10-05", "2026-11-02", freq="7D"):
            for b in P.BUILDS:
                devices = int(act.get((wk, b[0], b[1]), 0))
                if not devices:
                    continue
                n = int(rng.poisson(devices * (0.011 if b[0] == "ios" else 0.008)))
                if not n:
                    continue
                avg = rng.normal(4.47 if b[1] != "7.42.0" else 4.38, 0.85 / np.sqrt(n))
                rows.append(dict(week_starting=wk.date().isoformat(), store="app_store" if b[0] == "ios" else "google_play",
                                 version=b[1], ratings=n, average_rating=round(float(np.clip(avg, 3.6, 4.9)), 2)))
        return pd.DataFrame(rows)

    def push(self):
        rng = self._stream(7)
        rows = []
        names = ["harbour_festival_day%d" % i for i in range(1, 4)] + ["lives_refill_reminder", "weekend_booster_offer",
                                                                       "pass_renewal_nudge", "new_chapter_tidepools",
                                                                       "lapsed_7d_comeback", "lapsed_14d_comeback"]
        # players who allow notifications, by platform
        base = {"ios": 0.48 * P.N_ACCOUNTS["ios"], "android": 0.81 * P.N_ACCOUNTS["android"]}
        reach = {"all players": (0.93, 1.0), "active players": (0.55, 0.68), "lapsed players": (0.08, 0.17),
                 "pass holders": (0.035, 0.05)}
        t = dt.datetime(2026, 10, 5, 17)
        k = n = 0
        while t < dt.datetime(2026, 11, 9):
            nm = names[n % len(names)]
            aud = ("lapsed players" if "lapsed" in nm else "all players" if "festival" in nm or "chapter" in nm
                   else "pass holders" if "pass" in nm else "active players")
            for plat in ("ios", "android"):
                sends = int(base[plat] * rng.uniform(*reach[aud]))
                rows.append(dict(campaign_id="pc_%05d" % (31200 + k), name=nm, platform=plat, sent_at=iso(t),
                                 audience=aud, sends=sends, opens=int(sends * rng.uniform(0.03, 0.11))))
                k += 1
            n += 1
            t = (t + dt.timedelta(days=int(rng.choice([2, 3, 4])))).replace(hour=int(rng.choice([17, 18, 19])))
        return pd.DataFrame(rows)
