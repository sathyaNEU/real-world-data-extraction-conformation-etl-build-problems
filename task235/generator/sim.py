"""The world behind task235's pack: players and their devices, every session the game's session service records, every
purchase the purchase service verifies, and the analytics SDK's purchase_completed events as the warehouse receives
them. The clean truth (which events were dropped, which wait on a phone) stays here for the checks."""
import datetime as dt
import math
import zlib

import numpy as np
import pandas as pd

import params as P

HOUR = dt.timedelta(hours=1)
MERGE_REQUESTS_START, MERGE_REQUESTS_END = dt.datetime(2026, 10, 3, 0, 0), dt.datetime(2026, 11, 6, 9, 0)


def support_hours(t, key=""):
    """player support merges accounts on weekdays, 09:00 to 18:00 Irish time; a request that comes in out of hours is
    taken up during the next working day, when the desk reaches it in its queue"""
    pushed = False
    while True:
        local = t + (HOUR if t < P.IST_END else dt.timedelta(0))
        if local.weekday() < 5 and 9 <= local.hour < 18:
            break
        t += dt.timedelta(minutes=37)
        pushed = True
    if pushed:
        t += dt.timedelta(minutes=zlib.crc32(key.encode()) % 420)
    return t


def rollout_share(t):
    s = 0.0
    for d, x in P.ROLLOUT:
        if t >= d:
            s = x
    return s


class World:
    def __init__(self, seed=P.WORLD_SEED):
        self.rng = np.random.default_rng(seed)
        self.builds = {(b[0], b[1]): b for b in P.BUILDS}
        self.reinstalls = []

    # ------------------------------------------------------------------ players and devices
    def _gap(self, cls):
        rng = self.rng
        if cls == "casual" and rng.random() < P.CASUAL_LONG:
            return float(rng.uniform(*P.CASUAL_LONG_DAYS) * 24)
        return float(max(0.6, rng.gamma(1.0, P.CLASSES[cls][1])))

    def build(self):
        rng = self.rng
        accounts, devices, sessions, purchases, links = [], [], [], [], []
        stores = P.STOREFRONTS
        sw = np.array([s[2] for s in stores]); sw = sw / sw.sum()
        prod_w = np.array([p[3] for p in P.PRODUCTS]); prod_w = prod_w / prod_w.sum()
        n_dev = 0
        for plat in ("ios", "android"):
            pb = [b for b in P.BUILDS if b[0] == plat]
            for a in range(P.N_ACCOUNTS[plat]):
                cls = rng.choice(list(P.CLASSES), p=[c[0] for c in P.CLASSES.values()])
                intensity = float(rng.gamma(0.6, 1.0))
                store = stores[int(rng.choice(len(stores), p=sw))]
                guest = rng.random() < 0.33
                n = len(accounts) + 1
                acct = "%s%07d" % ("g" if guest else "a", n)
                accounts.append(dict(account=acct, platform=plat, cls=cls, intensity=intensity, country=store[0],
                                     currency=store[1], guest=guest, n=n))
                kinds = [("phone", cls, rng.random() < P.AUTO_UPDATE[cls])]
                if not guest and rng.random() < P.TABLET[plat]:
                    kinds.append(("tablet", "casual", rng.random() < 0.6))
                for kind, dcls, auto in kinds:
                    n_dev += 1
                    old_ipad = kind == "tablet" and plat == "ios" and rng.random() < P.OLD_IPAD
                    released = [b for b in pb if b[3] <= P.T0]
                    if auto:
                        cur = released[-1] if rng.random() < 0.8 else released[-2]
                    else:
                        cur = released[0] if rng.random() < 0.55 else released[1]
                    if old_ipad and (auto or rng.random() < 0.5):
                        cur = [b for b in pb if b[1] == "7.40.0"][0]
                    dev = dict(device="%s%06d" % ("I" if plat == "ios" else "D", n_dev), account=acct, platform=plat,
                               kind=kind, cls=dcls, auto=auto, old_ipad=old_ipad, roll_u=float(rng.random()),
                               upd_h=float(rng.gamma(2.0, 0.5) * 24), intensity=intensity)
                    devices.append(dev)
                    self._play(dev, cur, pb, accounts[-1], sessions, purchases, prod_w)
        self.accounts = pd.DataFrame(accounts)
        self.devices = pd.DataFrame(devices)
        self.sessions = pd.DataFrame(sessions, columns=["device", "account", "platform", "version", "start", "after_reinstall"])
        self.purchases = pd.DataFrame(purchases, columns=["device", "account", "platform", "version", "product", "kind",
                                                          "purchased_at", "dev_kind", "cls", "session_start"])
        self._ids()
        return self

    def _ids(self, seed=P.WORLD_SEED + 7):
        """the ids each player's history moves through, drawn after play so the sessions stay as they are: a guest
        upgraded to a signed-in account (players are asked to sign in after a purchase), and a signed-in account
        merged by player support into the player's other account"""
        rng = np.random.default_rng(seed)
        pw = self.purchases[self.purchases.purchased_at >= P.WIN0]
        first = pw.groupby("account").purchased_at.min()
        # 7.42.0 asks a guest to sign in straight after a purchase
        first42 = pw[pw.version == "7.42.0"].groupby("account").purchased_at.min()
        links, timeline = [], {}
        for a in self.accounts.itertuples():
            ids = [(P.T0 - dt.timedelta(days=400), a.account)]
            prompt = a.account in first42.index and rng.random() < P.UPGRADE_PROMPT
            if a.guest and (prompt or rng.random() < P.UPGRADE):
                t0 = first42[a.account] if prompt else \
                    first.get(a.account, P.T0 + dt.timedelta(hours=float(rng.uniform(0, 34 * 24))))
                t1 = t0 + dt.timedelta(hours=float(rng.gamma(1.0, 2.0 if prompt else 30.0)) + 0.05)
                if t1 < P.RUN:
                    # signing in to an account made before keeps that account's history and leaves the guest's behind,
                    # so the account service records no link
                    if rng.random() < P.OLD_ACCOUNT:
                        ids.append((t1, "o%07d" % a.n))
                    else:
                        ids.append((t1, "a%07d" % a.n))
                        links.append((a.account, "a%07d" % a.n, "guest_upgrade", t1))
            p_merge = P.MERGE_AFTER_UPGRADE if len(ids) > 1 else (P.MERGE if not a.guest else 0.0)
            if rng.random() < p_merge:
                g = float(rng.gamma(1.0, 4 * 24.0))
                if len(ids) > 1:
                    req = ids[-1][0] + dt.timedelta(hours=g + 1)
                else:
                    # an older account's merge request comes in at any point in the weeks the export covers
                    req = MERGE_REQUESTS_START + (MERGE_REQUESTS_END - MERGE_REQUESTS_START) * (1 - math.exp(-g / 96.0))
                t2 = support_hours(req, a.account)
                if t2 < P.RUN:
                    ids.append((t2, "m%07d" % a.n))
                    links.append((ids[-2][1], "m%07d" % a.n, "support_merge", t2))
            timeline[a.account] = ids
        self.accounts["ids"] = self.accounts.account.map(timeline)
        self.accounts["final"] = [t[-1][1] for t in self.accounts.ids]

        def at(acct, t):
            return [i for (since, i) in timeline[acct] if since <= t][-1]
        self.sessions["player"] = self.sessions.account
        self.sessions["account"] = [at(x, t) for x, t in zip(self.sessions.account, self.sessions.start)]
        self.purchases["player"] = self.purchases.account
        self.purchases["account"] = [at(x, t) for x, t in zip(self.purchases.account, self.purchases.purchased_at)]
        self.links = pd.DataFrame(links, columns=["from_account", "to_account", "link_type", "linked_at"])

    def _play(self, dev, cur, pb, acc, sessions, purchases, prod_w):
        rng = self.rng
        t = P.T0 + dt.timedelta(hours=float(rng.uniform(0, 72)))
        device = dev["device"]
        reinstalled = False
        while t < P.RUN:
            if dev["auto"]:
                for b in pb:
                    if b[3] > cur[3] and b[3] <= t - dt.timedelta(hours=dev["upd_h"]):
                        if dev["old_ipad"] and b[1] >= "7.41":
                            continue
                        if b[1] == "7.42.0" and dev["roll_u"] > rollout_share(t):
                            continue
                        cur = b
            if rng.random() < P.REINSTALL:
                # the game deleted and installed again: a new device id from here on, the old queue gone
                self.reinstalls.append((device, t))
                device = device + "R"
                reinstalled = True
            acct = acc["account"]
            sessions.append((device, acct, dev["platform"], cur[1], t, reinstalled))
            p = P.BUY * dev["intensity"] * (P.BUY_TABLET if dev["kind"] == "tablet" else 1.0) * \
                (P.BUY_CASUAL if dev["cls"] == "casual" else 1.0)
            if rng.random() < min(0.7, p):
                pt = t + dt.timedelta(minutes=float(rng.uniform(1, 25)))
                if pt < P.RUN:
                    prod = P.PRODUCTS[int(rng.choice(len(P.PRODUCTS), p=prod_w))]
                    purchases.append((device, acct, dev["platform"], cur[1], prod[0], prod[1], pt, dev["kind"],
                                      dev["cls"], t))
            if rng.random() < P.QUIT:
                break
            t = t + dt.timedelta(hours=self._gap(dev["cls"]))

    # ------------------------------------------------------------------ the SDK's purchase_completed events
    def events(self, seed=P.EVENT_SEED):
        """for each purchase made in the game: dropped (never created), sent at once, sent on a quick return, or kept
        on the phone until its next session; the warehouse receives what was sent before the run"""
        rng = np.random.default_rng(seed)
        pu = self.purchases.reset_index(drop=True)
        S = self.sessions.sort_values(["device", "start"])
        starts = {d: g.start.values for d, g in S.groupby("device")}
        sdk = {(b[0], b[1]): b[4] for b in P.BUILDS}
        out = []
        U = rng.random((len(pu), 4))                     # drop, late, quick return, timing: drawn for every purchase
        for i, r in enumerate(pu.itertuples()):
            u = U[i]
            v = sdk[(r.platform, r.version)]
            drop = u[0] < P.BASE_DROP + P.DROP.get((r.platform, r.version), 0.0)
            base = P.LATE["tablet" if r.dev_kind == "tablet" else r.cls]
            if v.startswith("5."):
                p_late = P.LATE_50_IOS if r.platform == "ios" else min(0.9, base * P.LATE_50_ANDROID)
            else:
                p_late = base
            late = u[1] < p_late
            quick = u[2] < P.QUICK_RETURN
            s = starts.get(r.device, np.array([], dtype="datetime64[ns]"))
            nxt = s[s > np.datetime64(r.purchased_at)]
            next_start = pd.Timestamp(nxt[0]) if len(nxt) else pd.NaT
            if drop:
                route, recv = "dropped", pd.NaT
            elif not late:
                route, recv = "at_once", pd.Timestamp(r.purchased_at) + pd.Timedelta(seconds=1 + 39 * float(u[3]))
            elif quick:
                route, recv = "quick", pd.Timestamp(r.purchased_at) + pd.Timedelta(minutes=2 + 27 * float(u[3]))
            elif len(nxt):
                route, recv = "next_session", next_start + pd.Timedelta(seconds=2 + 48 * float(u[3]))
            else:
                route, recv = "waiting", pd.NaT
            if pd.notna(recv) and recv > pd.Timestamp(P.RUN):
                route, recv = "waiting", pd.NaT
            out.append(dict(route=route, received=recv, sdk=v, next_start=next_start, late=late))
        ev = pd.DataFrame(out)
        self.purchases = pd.concat([pu, ev], axis=1)
        return self


def make():
    W = World()
    W.build()
    W.events()
    return W
