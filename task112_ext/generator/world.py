"""The chain's 2026-2027 world: stores, members and households, consent by channel, the 2027 campaigns and every
send, response, visit and redemption they produced. Seeded and deterministic; every channel obeys the contact policy
(consent at send time, caps, quiet hours) by construction."""
import datetime as dt
import hashlib
import heapq
from zoneinfo import ZoneInfo

import numpy as np

import params as P

STO = ZoneInfo("Europe/Stockholm")
CH = ("email", "sms", "push", "post")
CLIENTS = ["Gmail", "Outlook", "Samsung Email", "Webmail", "Other"]
OPERATORS = ["Telia", "Tele2", "Telenor", "Tre", "Övriga"]
LINKS = ["offer", "recipes", "store_finder", "app_download", "other"]
SEASON = [0.93, 0.90, 0.98, 1.00, 1.02, 1.07, 0.88, 0.97, 1.00, 1.01, 0.99, 1.13]
DISTRICTS = {"Gävle": ["Centrum", "Sätra", "Hemlingby", "Valbo"],
             "Sundsvall": ["Centrum", "Birsta", "Nacksta", "Skönsberg"],
             "Örnsköldsvik": ["Centrum", "Domö"], "Sandviken": ["Centrum", "Björksätra"],
             "Hudiksvall": ["Centrum", "Håstahamn"]}
D0 = np.datetime64("1970-01-01")


def T(y, mo, d, h=0, mi=0, s=0):
    """Swedish wall time to UTC epoch seconds"""
    return int(dt.datetime(y, mo, d, h, mi, s, tzinfo=STO).timestamp())


def TD(d, h=0, mi=0, s=0):
    return T(d.year, d.month, d.day, h, mi, s)


def day(x):
    """numpy day to datetime.date"""
    return dt.date(1970, 1, 1) + dt.timedelta(days=int((x - D0).astype(int)))


# the offsets of Swedish time in 2026 to 2028, for vectorised local hours
DST = [(T(2026, 3, 29, 3), T(2026, 10, 25, 2)), (T(2027, 3, 28, 3), T(2027, 10, 31, 2)),
       (T(2028, 3, 26, 3), T(2028, 10, 29, 2))]


def offset(t):
    t = np.asarray(t, dtype=np.int64)
    o = np.full(t.shape, 3600, dtype=np.int64)
    for a, b in DST:
        o[(t >= a) & (t < b)] = 7200
    return o


def local_hour(t):
    return ((np.asarray(t, dtype=np.int64) + offset(t)) % 86400) // 3600


def luhn(digits):
    s, dbl = 0, True
    for ch in reversed(digits):
        k = int(ch)
        if dbl:
            k *= 2
            if k > 9:
                k -= 9
        s += k
        dbl = not dbl
    return str((10 - s % 10) % 10)


def hexid(*parts, n=16):
    return hashlib.sha1("|".join(str(p) for p in parts).encode()).hexdigest()[:n].upper()


class Consent:
    """one channel's consent state, advanced through time; the log keeps the changes of state"""

    def __init__(self, init, events):
        self.s = init.copy()
        self.ev = events
        self.i = 0
        self.pend = []
        self.k = 0
        self.log = []

    def add(self, ts, i, granted, src, logged=None):
        heapq.heappush(self.pend, (ts, self.k, i, granted, src, ts if logged is None else logged))
        self.k += 1

    def upto(self, t):
        ev, pend = self.ev, self.pend
        while True:
            a = ev[self.i] if self.i < len(ev) and ev[self.i][0] <= t else None
            b = pend[0] if pend and pend[0][0] <= t else None
            if a is None and b is None:
                return self.s
            if b is None or (a is not None and a[0] <= b[0]):
                ts, i, g, src = a
                logged = ts
                self.i += 1
            else:
                ts, _, i, g, src, logged = heapq.heappop(pend)
            if self.s[i] != g:
                self.s[i] = g
                self.log.append((logged, i, g, src))


class World:
    def __init__(self):
        self.end = T(2028, 1, 1)
        self.stores = self._stores()
        self._members()
        self._consent_base()
        self._timeline()
        self.meta_daily, self.meta_life = self._meta()

    # ------------------------------------------------------------------ stores
    def _stores(self):
        r = np.random.default_rng(P.SEED + 1)
        rows, k = [], 101
        for town, n in P.STORES.items():
            names = DISTRICTS.get(town, ["Centrum"])[:n]
            for j, dist in enumerate(names):
                if n == 1:
                    fmt = "Stor" if P.MUNIS[town][3] > 30000 else "Mellan"
                else:
                    fmt = "Stor" if j == 0 else ("Mellan" if j < 3 else "Nära")
                sqm = {"Stor": int(r.integers(2600, 4300)), "Mellan": int(r.integers(1250, 2300)),
                       "Nära": int(r.integers(420, 950))}[fmt]
                pcs = P.MUNIS[town][2]
                rows.append(dict(store_code="BV%03d" % k, store_name="Brännvik %s %s" % (town, dist), municipality=town,
                                 county=P.MUNIS[town][1], postcode_area=pcs[j % len(pcs)], format=fmt, sales_area_sqm=sqm,
                                 opened_year=int(r.integers(1979, 2022))))
                k += int(r.integers(1, 4))
        return rows

    # ------------------------------------------------------------------ members and households
    def _members(self):
        r = np.random.default_rng(P.SEED + 10)
        n = P.MEMBERS
        self.n = n
        munis = list(P.MUNIS)
        w = np.array([P.MUNIS[m][3] * (0.30 if m not in P.STORES else (1.15 if P.STORES[m] >= 2 else 1.0))
                      for m in munis], float)
        w /= w.sum()
        sizes = r.choice([1, 2, 3], size=n, p=[0.77, 0.20, 0.03])
        hh = np.repeat(np.arange(n), sizes)[:n]
        n_hh = int(hh.max()) + 1
        hh_muni = r.choice(len(munis), size=n_hh, p=w)
        hh_pc = np.array([P.MUNIS[munis[m]][2][int(r.integers(0, len(P.MUNIS[munis[m]][2])))] for m in hh_muni])
        self.hh = hh
        self.n_hh = n_hh
        self.muni = np.array(munis)[hh_muni[hh]]
        self.county = np.array([P.MUNIS[m][1] for m in self.muni])
        self._cl = np.array([P.MUNIS[m][0] for m in self.muni])
        self.pc = hh_pc[hh]

        # joining: the launch wave, then steady growth
        launch = np.datetime64(P.LAUNCH)
        late0 = np.datetime64("2013-10-01")
        span2 = int((np.datetime64("2027-12-31") - late0).astype(int)) + 1
        early = r.uniform(size=n) < 0.12
        join = np.where(early, launch + r.integers(0, 214, size=n),
                        late0 + (r.beta(1.7, 1.0, size=n) * span2).astype(int))
        self.join = join.astype("datetime64[D]")
        jy = self.join.astype("datetime64[Y]").astype(int) + 1970
        by = np.clip(np.round(r.normal(1971, 16, size=n)), 1932, 2010).astype(int)
        self.birth = np.minimum(by, jy - 16 - r.integers(0, 4, size=n))
        app_era = self.join >= np.datetime64(P.APP_LAUNCH)
        sig = np.where(app_era, r.choice(["store_kiosk", "web_signup", "app_signup"], size=n, p=[0.5, 0.25, 0.25]),
                       r.choice(["store_kiosk", "web_signup"], size=n, p=[0.72, 0.28]))
        self.signup = sig
        hour_w = np.array([2, 4, 6, 7, 8, 8, 8, 8, 9, 9, 10, 10, 9, 8, 6, 4, 2, 1], float)
        hours = np.where(sig == "store_kiosk", r.integers(8, 21, size=n),
                         r.choice(np.arange(6, 24), size=n, p=hour_w / hour_w.sum()))
        mins, secs = r.integers(0, 60, size=n), r.integers(0, 60, size=n)
        self.join_ts = np.array([TD(day(self.join[i]), int(hours[i]), int(mins[i]), int(secs[i])) for i in range(n)],
                                dtype=np.int64)

        # closures in 2026 and 2027 (the extract holds every account open on or after 1 January 2026)
        lo = np.maximum(self.join + 30, np.datetime64("2026-01-02"))
        hi = np.datetime64("2027-12-20")
        can = (r.uniform(size=n) < 0.065) & (lo < hi)
        span = np.maximum((hi - lo).astype(int), 1)
        cday = lo + (r.uniform(size=n) * span).astype(int)
        self.closed = can
        self.close_day = np.where(can, cday, np.datetime64("2099-01-01")).astype("datetime64[D]")
        ch_ = r.integers(9, 18, size=n)
        self.close_ts = np.array([TD(day(self.close_day[i]), int(ch_[i]), int(r.integers(0, 60))) if can[i] else 2 ** 40
                                  for i in range(n)], dtype=np.int64)

        # contact data, devices, habits
        old = self.birth < 1950
        self.has_email = r.uniform(size=n) < np.where(old, 0.72, 0.88)
        self.email_valid = r.uniform(size=n) < 0.985
        self.has_mobile = r.uniform(size=n) < np.where(old, 0.82, 0.95)
        self.mobile_ok = r.uniform(size=n) > 0.006
        self.apple = r.uniform(size=n) < np.where(self.birth >= 1960, 0.52, 0.38)
        self.mpp = self.apple & (r.uniform(size=n) < 0.90)
        cl = r.choice(len(CLIENTS), size=n, p=[0.42, 0.24, 0.13, 0.11, 0.10])
        self.client = np.where(self.apple, "Apple Mail", np.array(CLIENTS)[cl])
        self.ios = np.where(self.apple, r.uniform(size=n) < 0.9, r.uniform(size=n) < 0.15)
        self.operator = np.array(OPERATORS)[r.choice(5, size=n, p=[0.37, 0.27, 0.21, 0.11, 0.04])]
        self.engage = r.beta(2.0, 3.2, size=n)
        self.rate = np.clip(r.gamma(2.4, 1.75, size=n), 0.2, 16.0)
        self.basket = np.exp(r.normal(5.75, 0.42, size=n))
        self.home_share = r.beta(9.0, 1.6, size=n)
        self.dormant = (r.uniform(size=n) < 0.09) & (self.join < np.datetime64("2027-01-01"))
        self.sortkey = r.permutation(n)

        # the app
        p_app = np.where(self.birth >= 1976, 0.64, np.where(self.birth >= 1956, 0.42, 0.18))
        app = (sig == "app_signup") | (r.uniform(size=n) < p_app)
        start = np.maximum(self.join, np.datetime64(P.APP_LAUNCH))
        since = np.where(sig == "app_signup", self.join, start + r.exponential(520, size=n).astype(int))
        app &= since <= np.datetime64("2027-12-31")
        self.app = app
        self.app_since = np.where(app, since, np.datetime64("2099-01-01")).astype("datetime64[D]")
        ah = r.integers(7, 23, size=n)
        self.app_ts = np.array([TD(day(self.app_since[i]), int(ah[i]), int(r.integers(0, 60))) if app[i] else 2 ** 40
                                for i in range(n)], dtype=np.int64)
        same = app & (sig == "app_signup")
        self.app_ts[same] = self.join_ts[same] + 40
        un_lo = np.maximum(self.app_since + 1, np.datetime64("2027-01-01"))
        un = app & (r.uniform(size=n) < 0.10) & (un_lo < np.datetime64("2027-12-31"))
        uday = un_lo + (r.uniform(size=n) * np.maximum((np.datetime64("2027-12-31") - un_lo).astype(int), 1)).astype(int)
        self.uninstall_ts = np.array([TD(day(uday[i]), 12) if un[i] else 2 ** 40 for i in range(n)], dtype=np.int64)

        # ids
        ids = r.choice(9000000, size=n, replace=False) + 1000000
        self.mid = np.array(["BP%d%s" % (x, luhn(str(x))) for x in ids])
        cards = r.choice(900000000, size=n, replace=False) + 100000000
        self.card = np.array(["637042%d%s" % (x, luhn("637042%d" % x)) for x in cards])
        hids = r.choice(9000000, size=n_hh, replace=False) + 1000000
        self.hid = np.array(["HH%d" % x for x in hids])

        # stores: home store for the household, the second store in the county
        st = self.stores
        codes = np.array([s["store_code"] for s in st])
        size_w = np.array([s["sales_area_sqm"] for s in st], float)
        stown = np.array([s["municipality"] for s in st])
        scounty = np.array([s["county"] for s in st])
        hh_home = np.empty(n_hh, dtype=object)
        for h in range(n_hh):
            m = munis[hh_muni[h]]
            town = P.NEIGHBOUR.get(m, m)
            c = np.where(stown == town)[0]
            hh_home[h] = codes[c[r.choice(len(c), p=size_w[c] / size_w[c].sum())]]
        home = hh_home[hh].astype(str)
        own = r.uniform(size=n) < 0.12          # a household member who shops elsewhere
        sec = np.empty(n, dtype=object)
        for i in range(n):
            c = np.where((scounty == self.county[i]) & (codes != home[i]))[0]
            if own[i]:
                home[i] = codes[c[r.choice(len(c), p=size_w[c] / size_w[c].sum())]]
                c = np.where((scounty == self.county[i]) & (codes != home[i]))[0]
            sec[i] = codes[c[r.choice(len(c), p=size_w[c] / size_w[c].sum())]]
        self.home = home
        self.second = sec.astype(str)

        self._year2026()

    def _year2026(self):
        """2026 shopping, simulated like 2027 at member level: the 2027 tier and the state going into January"""
        r = np.random.default_rng(P.SEED + 11)
        n = self.n
        act = (self.join < np.datetime64("2026-01-01")) & (r.uniform(size=n) < 0.80)
        stop_m = np.where(self.dormant, r.integers(0, 13, size=n), 99)
        y26 = np.zeros(n)
        for m in range(1, 13):
            first = np.datetime64("2026-%02d-01" % m)
            nxt = np.datetime64("2027-01-01") if m == 12 else np.datetime64("2026-%02d-01" % (m + 1))
            nd = int((nxt - first).astype(int))
            frac = np.clip((np.minimum(self.close_day, nxt) - np.maximum(self.join, first)).astype(int), 0, nd) / nd
            newly = (self.join >= first) & (self.join < nxt)
            u = r.uniform(size=n)
            act = np.where(act, u >= 0.035, u < 0.09) | newly
            act &= (frac > 0) & (stop_m >= m)
            v = np.where(act, r.poisson(self.rate * SEASON[m - 1] * frac), 0)
            y26 += v * self.basket * np.exp(r.normal(-0.02, 0.22, size=n))
        self.active = act
        self.y26 = y26
        tier = np.where(y26 >= P.GULD, "Guld", np.where(y26 >= P.SILVER, "Silver", "Bas"))
        self.tier27 = np.where(self.closed & (self.close_day < np.datetime64("2027-01-01")), "", tier)

    # ------------------------------------------------------------------ consent at go-live, signup and by hand
    def _consent_base(self):
        r = np.random.default_rng(P.SEED + 20)
        n, e = self.n, self.engage
        want = {"email": self.has_email & (r.uniform(size=n) < 0.48 + 0.32 * e),
                "sms": self.has_mobile & (r.uniform(size=n) < 0.22 + 0.26 * e),
                "push": self.app & (r.uniform(size=n) < 0.66),
                "post": r.uniform(size=n) > 0.05}
        live = TD(P.CONSENT_LIVE)
        self.live = live
        before = self.join_ts < live
        init = {c: want[c] & before for c in ("email", "sms", "post")}
        init["push"] = want["push"] & (self.app_ts < live)
        self.init = init
        ev = {c: [] for c in CH}
        for i in np.where(~before)[0]:
            for c in ("email", "sms", "post"):
                if want[c][i]:
                    ev[c].append((int(self.join_ts[i]) + 3 + CH.index(c), int(i), True, str(self.signup[i])))
        for i in np.where(want["push"] & (self.app_ts >= live))[0]:
            ev["push"].append((int(self.app_ts[i]) + 2, int(i), True, "app_settings"))
        y27 = T(2027, 1, 1)
        # changes by hand: channel, withdraw (True) or grant, yearly rate per year, sources and weights, who can
        specs = [("email", True, (0.070, 0.0), (["esp_unsubscribe", "customer_service", "my_pages"], [0.80, 0.08, 0.12])),
                 ("email", True, (0.0, 0.012), (["customer_service", "my_pages"], [0.40, 0.60])),
                 ("email", False, (0.020, 0.020), (["my_pages", "store_kiosk"], [0.70, 0.30])),
                 ("sms", True, (0.035, 0.0), (["sms_stop"], [1.0])),
                 ("sms", True, (0.012, 0.012), (["customer_service", "my_pages"], [0.50, 0.50])),
                 ("sms", False, (0.012, 0.012), (["my_pages"], [1.0])),
                 ("push", True, (0.070, 0.070), (["app_settings"], [1.0])),
                 ("push", False, (0.050, 0.050), (["app_settings"], [1.0])),
                 ("post", True, (0.012, 0.012), (["customer_service", "my_pages"], [0.60, 0.40])),
                 ("post", False, (0.004, 0.004), (["my_pages"], [1.0]))]
        lo = np.maximum(self.join_ts + 86400, live)
        lo_push = np.maximum(lo, self.app_ts + 86400)
        hi = np.minimum(self.close_ts - 3600, self.end - 1)
        for c, wd, rates, (srcs, sw) in specs:
            ok = np.ones(n, bool)
            if c == "email" and not wd:
                ok = self.has_email
            if c == "sms" and not wd:
                ok = self.has_mobile
            a = lo_push if c == "push" else lo
            if c == "push":
                ok = ok & self.app
            for yi, (ya, yb) in enumerate([(live, y27), (y27, self.end)]):
                if rates[yi] == 0:
                    continue
                s0 = np.maximum(a, ya)
                s1 = np.minimum(hi, yb)
                dur = np.where(ok & (s1 > s0), s1 - s0, 0)
                k = r.poisson(rates[yi] * dur / (365.25 * 86400))
                for i in np.where(k > 0)[0]:
                    for _ in range(int(k[i])):
                        ts = int(s0[i] + r.integers(0, int(dur[i])))
                        src = srcs[int(r.choice(len(srcs), p=sw))]
                        when = self._when(r, ts, src)
                        if s0[i] <= when < s1[i]:
                            ts = when
                        ev[c].append((ts, int(i), not wd, src))
        for i in np.where(self.closed)[0]:
            for c in CH:
                ev[c].append((int(self.close_ts[i]), int(i), False, "account_closed"))
        self.cons = {c: Consent(init[c], sorted(ev[c])) for c in CH}

    _HOURS = np.array([1, 1, 2, 4, 6, 7, 7, 8, 8, 8, 8, 7, 7, 8, 9, 10, 10, 9, 7, 4], float)   # 04:00 to 23:00

    def _when(self, r, ts, src):
        """a change made by hand happens when people do such things: customer service on weekdays in office hours,
        STOPP replies in the daytime after a campaign SMS, unsubscribes the morning after a newsletter Thursday"""
        d = dt.datetime.fromtimestamp(ts, STO).date()
        if src == "customer_service":
            while d.weekday() >= 5:
                d += dt.timedelta(days=1)
            return TD(d, int(r.integers(8, 17)), int(r.integers(0, 60)), int(r.integers(0, 60)))
        if src == "esp_unsubscribe":
            k = max(0, (d - dt.date(2026, 1, 8)).days // 14)
            sent = TD(dt.date(2026, 1, 8) + dt.timedelta(days=14 * k), 6, 30)
            return sent + int(np.exp(r.normal(np.log(9000), 1.1))) + int(r.integers(30, 300))
        if src == "sms_stop":
            while d.weekday() == 6:
                d += dt.timedelta(days=1)
            return TD(d, int(r.integers(9, 19)), int(r.integers(0, 60)), int(r.integers(0, 60)))
        if src == "store_kiosk":
            return TD(d, int(r.integers(8, 21)), int(r.integers(0, 60)), int(r.integers(0, 60)))
        h = int(r.choice(np.arange(4, 24), p=self._HOURS / self._HOURS.sum()))
        return TD(d, h, int(r.integers(0, 60)), int(r.integers(0, 60)))

    # ------------------------------------------------------------------ the year, drop by drop and month by month
    def _drops(self):
        d = []
        for k, x in enumerate(P.NEWSLETTER):
            d.append(dict(kind="email", id="BV27-01-N%02d" % (k + 1), camp="BV27-01", ts=TD(x, 6, 30), aud="all",
                          subject="Plusbrevet: " + P.THEMES[k], interest=1.0, issue=k, type="newsletter"))
        for mid, camp, tt, aud, subj, interest in P.EMAILS:
            d.append(dict(kind="email", id=mid, camp=camp, ts=T(*tt), aud=aud, subject=subj, interest=interest,
                          type="campaign"))
        for sid, camp, tt, aud, chars in P.SMS:
            d.append(dict(kind="sms", id=sid, camp=camp, ts=T(*tt), aud=aud, chars=chars))
        for pid, camp, tt, aud, title in P.PUSH:
            d.append(dict(kind="push", id=pid, camp=camp, ts=T(*tt), aud=aud, title=title))
        for did, camp, posted, sel, aud, cost in P.MAIL:
            d.append(dict(kind="mail", id=did, camp=camp, ts=TD(sel, 6), posted=posted, aud=aud))
        # the welcome series: on joining, and at 07:15 on days 7 and 21
        j27 = np.where(self.join >= np.datetime64("2027-01-01"))[0]
        for i in j27:
            d.append(dict(kind="welcome", step=0, ts=int(self.join_ts[i]) + 120 + int(self.sortkey[i] % 600), who=int(i)))
        x = dt.date(2027, 1, 1)
        while x <= dt.date(2027, 12, 31):
            for s, (wid, off, _) in enumerate(P.WELCOME):
                if s == 0:
                    continue
                jd = np.datetime64(x - dt.timedelta(days=off))
                who = np.where(self.join == jd)[0]
                if len(who) and jd >= np.datetime64("2027-01-01"):
                    d.append(dict(kind="welcome", step=s, ts=TD(x, 7, 15), who=who))
            x += dt.timedelta(days=1)
        # personal offers loaded to cards
        for code, camp, text, kind, val, base in P.OFFERS:
            if camp == "BV27-02":
                continue
            c = [z for z in P.CAMPAIGNS if z[0] == camp][0]
            a, b = dt.date.fromisoformat(c[4]), dt.date.fromisoformat(c[5])
            aud = {"BV27-10": "lapsed", "BV27-12": "guld"}.get(camp, "all")
            d.append(dict(kind="offer", code=code, camp=camp, ts=TD(a, 0, 5), first=a, last=b, aud=aud, base=base,
                          okind=kind, val=val))
        for k, x in enumerate(P.NEWSLETTER):
            kind, val = P.NEWS_OFFER[k]
            d.append(dict(kind="offer", code="BV27-01-O%02d" % (k + 1), camp="BV27-01-N%02d" % (k + 1),
                          ts=TD(x, 6, 0), first=x, last=x + dt.timedelta(days=13), aud="all", base=0.021, okind=kind,
                          val=val))
        order = {"offer": 0, "mail": 1, "email": 2, "sms": 3, "push": 4, "welcome": 5}
        d.sort(key=lambda z: (z["ts"], order[z["kind"]], str(z.get("id", z.get("code", "")))))
        return d

    def _open_at(self, t):
        return (self.join_ts <= t) & (self.close_ts > t)

    def _audience(self, aud, t):
        m = self._open_at(t)
        if aud == "all":
            return m
        if aud.startswith("county:"):
            return m & (self._cl == aud.split(":")[1])
        if aud == "lapsed":
            return m & self.lapsed
        if aud == "guld":
            return m & (self.tier27 == "Guld")
        raise ValueError(aud)

    def _timeline(self):
        self.r_e = np.random.default_rng(P.SEED + 30)
        self.r_s = np.random.default_rng(P.SEED + 31)
        self.r_p = np.random.default_rng(P.SEED + 32)
        self.r_m = np.random.default_rng(P.SEED + 33)
        self.r_v = np.random.default_rng(P.SEED + 34)
        self.r_o = np.random.default_rng(P.SEED + 35)
        n = self.n
        self.sends, self.events, self.sms, self.push, self.mail = [], [], [], [], []
        self.mailings = []
        self.welcome_sent = [0, 0, 0]
        self.reach = {}
        # addresses that bounced before 2027 are already on the ESP's suppression list
        old = self.join < np.datetime64("2027-01-01")
        self.email_seen = old.copy()
        self.suppressed = old & ~self.email_valid
        self.offers = []
        self.lapsed = np.zeros(n, bool)
        self.visits = np.zeros((12, n), dtype=np.int64)
        self.spend_rows, self.redemptions = [], []
        self.months_done = 0
        self.send_id = 61804229
        self.event_id = 1
        for d in self._drops():
            m = dt.datetime.fromtimestamp(d["ts"], STO).month if d["ts"] < self.end else 13
            while self.months_done + 1 < m and self.months_done < 12:
                self._month(self.months_done + 1)
            if d["kind"] == "offer":
                self._load_offer(d)
            elif d["kind"] == "email":
                self._email(d)
            elif d["kind"] == "welcome":
                self._welcome(d)
            elif d["kind"] == "sms":
                self._sms(d)
            elif d["kind"] == "push":
                self._push(d)
            elif d["kind"] == "mail":
                self._mail(d)
        while self.months_done < 12:
            self._month(self.months_done + 1)
        for c in CH:
            self.cons[c].upto(2 ** 41)

    def _mark(self, key, idx, level):
        a = self.reach.setdefault(key, np.zeros(self.n, np.int8))
        np.maximum.at(a, idx, np.int8(level))

    # ------------------------------------------------------------------ email
    def _email(self, d):
        t = d["ts"]
        cons = self.cons["email"].upto(t)
        cand = np.where(self._audience(d["aud"], t) & cons & ~self.suppressed)[0]
        cand = cand[np.argsort(self.sortkey[cand], kind="stable")]
        sent = t + (np.arange(len(cand)) / 14.0).astype(np.int64) + self.r_e.integers(0, 3, size=len(cand))
        self._deliver_email(d["id"], d["camp"], cand, sent, d["interest"], key=d["id"] if d["camp"] == "BV27-01" else d["camp"])
        self.mailings.append(dict(mailing_id=d["id"], campaign_code=d["camp"], type=d["type"], subject=d["subject"],
                                  scheduled=t, sends=len(cand)))

    def _welcome(self, d):
        wid, off, subj = P.WELCOME[d["step"]]
        t = d["ts"]
        cons = self.cons["email"].upto(t)
        who = np.atleast_1d(np.asarray(d["who"]))
        who = who[cons[who] & ~self.suppressed[who] & self._open_at(t)[who]]
        if not len(who):
            return
        who = who[np.argsort(self.sortkey[who], kind="stable")]
        sent = np.full(len(who), t, dtype=np.int64) + (np.arange(len(who)) / 14.0).astype(np.int64) + \
            (self.r_e.integers(0, 40, size=len(who)) if d["step"] else 0)
        self._deliver_email(wid, "BV27-02", who, sent, 1.45, key="BV27-02")
        self.welcome_sent[d["step"]] += len(who)

    def _deliver_email(self, mailing, camp, who, sent, interest, key):
        r = self.r_e
        k = len(who)
        if not k:
            return
        first = ~self.email_seen[who]
        dead = r.uniform(size=k) < 0.00035          # a mailbox closed since the last send
        hard = (first & ~self.email_valid[who]) | (~first & dead)
        soft = ~hard & (r.uniform(size=k) < 0.0045)
        status = np.where(hard, "hard_bounce", np.where(soft, "soft_bounce", "delivered"))
        self.email_seen[who] = True
        self.suppressed[who[hard]] = True
        ids = self.send_id + np.arange(k)
        self.send_id += k + int(r.integers(3, 40))
        self.sends.append((ids, np.full(k, mailing, dtype=object), who, sent, status))
        dl = ~hard & ~soft
        e = self.engage[who]
        # Apple's proxy loads the images of most messages delivered to Apple Mail with privacy protection
        proxy = dl & self.mpp[who] & (r.uniform(size=k) < 0.86)
        proxy_t = sent + np.exp(r.normal(np.log(360), 1.1, size=k)).astype(np.int64) + 5
        read = dl & (r.uniform(size=k) < np.clip((0.08 + 0.52 * e) * interest, 0, 0.95))
        read_t = sent + np.exp(r.normal(np.log(7900), 1.25, size=k)).astype(np.int64) + 20
        h = local_hour(read_t)
        night = h < 6
        read_t = np.where(night, read_t + (6 - h) * 3600 + r.integers(0, 5400, size=k), read_t)
        pixel = read & ~self.mpp[who]
        again = pixel & (r.uniform(size=k) < 0.24)
        again_t = read_t + np.exp(r.normal(np.log(18000), 1.0, size=k)).astype(np.int64) + 60
        click = read & (r.uniform(size=k) < (0.04 + 0.22 * e ** 1.5) * min(interest, 1.2))
        click_t = read_t + r.integers(15, 400, size=k)
        link = np.array(LINKS)[r.choice(5, size=k, p=[0.55, 0.20, 0.10, 0.10, 0.05])]
        unsub = read & (r.uniform(size=k) < (0.0022 + 0.0060 * (1 - e)) * (1.6 if camp == "BV27-10" else 1.0))
        unsub_t = click_t + r.integers(20, 180, size=k)
        compl = dl & ~read & (r.uniform(size=k) < 0.00025)
        compl_t = sent + np.exp(r.normal(np.log(36000), 0.8, size=k)).astype(np.int64)
        lag = r.integers(60, 900, size=k)
        ev = []
        for mask, tt, typ, extra in [(proxy, proxy_t, "open", "Apple Mail Privacy Protection"),
                                     (pixel, read_t, "open", None), (again, again_t, "open", None),
                                     (click, click_t, "click", "link"), (unsub, unsub_t, "unsubscribe", None),
                                     (compl, compl_t, "spam_complaint", None)]:
            sel = np.where(mask)[0]
            if not len(sel):
                continue
            if extra == "Apple Mail Privacy Protection":
                cl = np.full(len(sel), extra, dtype=object)
            elif typ == "open":
                cl = self.client[who[sel]].astype(object)
            else:
                cl = np.full(len(sel), None, dtype=object)
            lk = link[sel].astype(object) if typ == "click" else np.full(len(sel), None, dtype=object)
            ev.append((ids[sel], np.full(len(sel), mailing, dtype=object), who[sel], tt[sel],
                       np.full(len(sel), typ, dtype=object), cl, lk))
        self.events.extend(ev)
        con = self.cons["email"]
        for j in np.where(unsub)[0]:
            con.add(int(unsub_t[j]), int(who[j]), False, "esp_unsubscribe", int(unsub_t[j] + lag[j]))
        for j in np.where(compl & ~unsub)[0]:
            con.add(int(compl_t[j]), int(who[j]), False, "esp_complaint", int(compl_t[j] + lag[j]))
        self._mark(key, who[dl], 1)
        self._mark(key, who[read], 2)

    # ------------------------------------------------------------------ SMS
    def _sms(self, d):
        r = self.r_s
        t = d["ts"]
        cons = self.cons["sms"].upto(t)
        who = np.where(self._audience(d["aud"], t) & cons & self.has_mobile)[0]
        who = who[np.argsort(self.sortkey[who], kind="stable")]
        k = len(who)
        sub = t + (np.arange(k) / 45.0).astype(np.int64) + r.integers(0, 2, size=k)
        u = r.uniform(size=k)
        bad = ~self.mobile_ok[who]
        st = np.where(bad, np.where(u < 0.5, "REJECTD", "UNDELIV"),
                      np.where(u < 0.976, "DELIVRD", np.where(u < 0.988, "UNDELIV", "EXPIRED")))
        done = np.where(st == "EXPIRED", sub + 172800 + r.integers(1, 95, size=k), sub + r.integers(2, 26, size=k))
        dl = st == "DELIVRD"
        e = self.engage[who]
        stop = dl & (r.uniform(size=k) < (0.005 + 0.012 * (1 - e)) * (1.5 if d["camp"] == "BV27-10" else 1.0))
        reply_t = done + np.exp(r.normal(np.log(360), 1.0, size=k)).astype(np.int64) + 10
        seg = 1 if d["chars"] <= 160 else 2
        price = np.where(st == "REJECTD", 0.0, seg * P.SMS_PRICE)
        self.sms.append((d["id"], who, sub, st, done, seg, price, stop, reply_t))
        con = self.cons["sms"]
        lag = r.integers(20, 240, size=k)
        for j in np.where(stop)[0]:
            con.add(int(reply_t[j]), int(who[j]), False, "sms_stop", int(reply_t[j] + lag[j]))
        self._mark(d["camp"], who[dl], 1)
        self._mark(d["camp"], who[dl & (r.uniform(size=k) < 0.85)], 2)

    # ------------------------------------------------------------------ app push
    def _push(self, d):
        r = self.r_p
        t = d["ts"]
        cons = self.cons["push"].upto(t)
        who = np.where(self._audience(d["aud"], t) & cons & self.app & (self.app_ts <= t))[0]
        who = who[np.argsort(self.sortkey[who], kind="stable")]
        k = len(who)
        sent = t + (np.arange(k) / 120.0).astype(np.int64) + r.integers(0, 4, size=k)
        gone = self.uninstall_ts[who] <= t
        exp_ = ~gone & (r.uniform(size=k) < 0.015)
        st = np.where(gone, "failed", np.where(exp_, "failed", "delivered"))
        reason = np.where(gone, "unregistered", np.where(exp_, "expired_token", ""))
        dl = st == "delivered"
        op = dl & (r.uniform(size=k) < 0.025 + 0.16 * self.engage[who])
        op_t = sent + np.exp(r.normal(np.log(1500), 1.2, size=k)).astype(np.int64) + 5
        self.push.append((d["id"], d["camp"], d["title"], who, sent, st, reason, op, op_t))
        self._mark(d["camp"], who[dl], 1)
        self._mark(d["camp"], who[op], 2)

    # ------------------------------------------------------------------ addressed mail
    def _mail(self, d):
        r = self.r_m
        t = d["ts"]
        cons = self.cons["post"].upto(t)
        open_ = self._open_at(t)
        # the household's main card holder: the earliest-joined open member
        order = np.lexsort((self.join_ts, self.hh))
        first = {}
        for i in order:
            if open_[i] and self.hh[i] not in first:
                first[self.hh[i]] = i
        prim = np.array(sorted(first.values(), key=lambda i: self.hh[i]))
        prim = prim[cons[prim]]
        if d["aud"] == "households_spend":
            hs = np.zeros(self.n_hh)
            np.add.at(hs, self.hh, self.paid[:10].sum(axis=0))
            prim = prim[hs[self.hh[prim]] >= 6000]
        k = len(prim)
        gold = np.zeros(self.n_hh, bool)
        gold[self.hh[self.tier27 == "Guld"]] = True
        ver = np.where(gold[self.hh[prim]] & (d["camp"] == "BV27-13"), "Guld", "Standard")
        ret = r.uniform(size=k) < 0.011
        ret_d = r.integers(6, 22, size=k)
        self.mail.append((d["id"], d["camp"], prim, ver, d["posted"], ret, ret_d))
        hh_got = np.zeros(self.n_hh, bool)
        hh_got[self.hh[prim[~ret]]] = True
        reached = np.where(hh_got[self.hh] & open_)[0]
        self._mark(d["camp"], reached, 1)
        self._mark(d["camp"], reached[r.uniform(size=len(reached)) < 0.55], 2)

    # ------------------------------------------------------------------ offers, loaded at campaign start
    def _load_offer(self, d):
        r = self.r_o
        t = d["ts"]
        who = np.where(self._audience(d["aud"], t))[0]
        a, b = np.datetime64(d["first"]), np.datetime64(d["last"])
        lo = np.maximum(a, self.join[who])
        hi = np.minimum(b, self.close_day[who] - 1)
        ok = hi >= lo
        who, lo, hi = who[ok], lo[ok], hi[ok]
        span = (hi - lo).astype(int) + 1
        dd = lo + (r.uniform(size=len(who)) * span).astype(int)
        self.offers.append(dict(code=d["code"], camp=d["camp"], who=who, u=r.uniform(size=len(who)), day=dd,
                                tod=r.choice(np.arange(8, 21), size=len(who), p=self._tod),
                                minute=r.integers(0, 60, size=len(who)),
                                home=r.uniform(size=len(who)) < 0.9, base=d["base"], okind=d["okind"], val=d["val"],
                                amount=r.uniform(45, 240, size=len(who)), extra=r.uniform(5, 260, size=len(who))))

    _tod = np.array([3, 4, 5, 6, 7, 8, 9, 11, 13, 12, 9, 6, 3], float) / 96.0

    def _welcome_offers(self):
        r = self.r_o
        who = np.where(self.join >= np.datetime64("2027-01-01"))[0]
        lo = self.join[who]
        hi = np.minimum(lo + 29, np.minimum(self.close_day[who] - 1, np.datetime64("2027-12-31")))
        ok = hi >= lo
        who, lo, hi = who[ok], lo[ok], hi[ok]
        span = (hi - lo).astype(int) + 1
        dd = lo + (r.beta(1.0, 2.2, size=len(who)) * span).astype(int)
        code, camp, text, kind, val, base = P.OFFERS[0]
        self.offers.append(dict(code=code, camp=camp, who=who, u=r.uniform(size=len(who)), day=dd,
                                tod=r.choice(np.arange(8, 21), size=len(who), p=self._tod),
                                minute=r.integers(0, 60, size=len(who)), home=r.uniform(size=len(who)) < 0.9,
                                base=base, okind=kind, val=val, amount=r.uniform(45, 240, size=len(who)),
                                extra=r.uniform(5, 260, size=len(who))))

    # ------------------------------------------------------------------ a month of shopping
    def _month(self, m):
        r = self.r_v
        n = self.n
        if m == 1:
            self._welcome_offers()
            self.paid = np.zeros((12, n))
        first = np.datetime64("2027-%02d-01" % m)
        nxt = np.datetime64("2028-01-01") if m == 12 else np.datetime64("2027-%02d-01" % (m + 1))
        ndays = int((nxt - first).astype(int))
        start = np.maximum(self.join, first)
        stop = np.minimum(self.close_day, nxt)
        open_days = np.clip((stop - start).astype(int), 0, ndays)
        frac = open_days / ndays
        joined_before = self.join < first
        newly = (self.join >= first) & (self.join < nxt)
        p_on = np.full(n, 0.09)
        if m in (9, 10) and "BV27-10" in self.reach:
            wb = self.reach["BV27-10"] > 0
            p_on = np.where(wb & self.lapsed, 0.09 + (0.22 if m == 9 else 0.10), p_on)
        u = r.uniform(size=n)
        act = np.where(self.active, u >= 0.035, u < p_on)
        act = np.where(newly, True, act) & ~self.dormant & (frac > 0)
        act &= joined_before | newly
        self.active = np.where(frac > 0, act, self.active)
        lam = self.rate * SEASON[m - 1] * frac
        v = np.where(act, r.poisson(lam), 0)
        hv = r.binomial(v, self.home_share)
        sv = v - hv
        # redemptions dated this month, for members shopping this month
        red = []
        for o in self.offers:
            sel = (o["day"] >= first) & (o["day"] < nxt)
            if not sel.any():
                continue
            w = o["who"][sel]
            lvl = self.reach.get(o["camp"], np.zeros(n, np.int8))[w]
            boost = np.where(lvl == 2, 2.0, np.where(lvl == 1, 1.3, 1.0))
            p = np.clip(o["base"] * (0.35 + 1.3 * self.engage[w]) * (self.rate[w] / 3.5) ** 0.25 * boost, 0, 0.9)
            hit = (o["u"][sel] < p) & act[w]
            for j in np.where(hit)[0]:
                jj = np.where(sel)[0][j]
                red.append((o, int(jj)))
        rows = []
        for o, jj in red:
            i = int(o["who"][jj])
            store = self.home[i] if o["home"][jj] else self.second[i]
            dday = o["day"][jj]
            mn = P.OFFER_MIN.get(o["code"], 0)
            gross = max(self.basket[i] * float(np.exp(0.3 * (o["u"][jj] - 0.5))), mn + float(o["extra"][jj]))
            if o["okind"] == "fixed":
                disc = float(o["val"])
            elif o["code"] == "BV27-12-O1":
                disc = round(gross * o["val"] / 100.0, 2)
            else:
                disc = round(float(o["amount"][jj]) * o["val"] / 100.0, 2)
            gross = round(max(gross, disc + 20.0), 2)
            ts = TD(day(dday), int(o["tod"][jj]), int(o["minute"][jj]), int(o["u"][jj] * 59))
            rows.append((ts, i, o["code"], store, round(gross - disc, 2), disc))
        # each redemption is a receipt of its own; the month's visits at the store cover them
        rk = {}
        for ts, i, code, store, paid, disc in rows:
            x = rk.setdefault((i, store), [0, 0.0, 0.0])
            x[0] += 1
            x[1] += paid
            x[2] += disc
        for (i, store), x in rk.items():
            if store == self.home[i]:
                hv[i] = max(hv[i], x[0])
            else:
                sv[i] = max(sv[i], x[0])
        v = hv + sv
        self.visits[m - 1] = v
        for i in np.where(v > 0)[0]:
            for store, vv in ((self.home[i], hv[i]), (self.second[i], sv[i])):
                if vv <= 0:
                    continue
                x = rk.get((i, store))
                k_red = x[0] if x else 0
                ordinary = vv - k_red
                amt = 0.0
                if ordinary > 0:
                    amt = ordinary * self.basket[i] * float(np.exp(r.normal(-0.02, 0.30 / np.sqrt(ordinary))))
                paid = round(amt + (x[1] if x else 0.0), 2)
                self.paid[m - 1, i] += paid
                self.spend_rows.append((i, m, store, int(vv), paid, round(x[2], 2) if x else 0.0, k_red))
        self.redemptions.extend(rows)
        if m == 8:
            had = (self.visits[:5] > 0).any(axis=0)
            none = (self.visits[5:8] == 0).all(axis=0)
            self.lapsed = had & none
        self.months_done = m

    # ------------------------------------------------------------------ Meta
    def _meta(self):
        r = np.random.default_rng(P.SEED + 60)
        pop = {}
        for m, v in P.MUNIS.items():
            pop[v[1]] = pop.get(v[1], 0) + v[3]
        counties = ["Gävleborg", "Västernorrland"]
        aud = {c: pop[c] * 0.52 * 0.84 for c in counties}
        share = {c: pop[c] / sum(pop.values()) for c in counties}
        cpm_m = [58, 55, 57, 60, 63, 66, 54, 57, 61, 66, 74, 82]
        daily, life = [], []
        names = {c[0]: c[1] for c in P.CAMPAIGNS}
        for camp, a, b, budget, obj in P.META:
            days = [a + dt.timedelta(days=k) for k in range((b - a).days + 1)]
            if camp == "BV27-14":
                days = [x for x in days if not (dt.date(2027, 7, 3) <= x <= dt.date(2027, 8, 8))
                        and not (dt.date(2027, 12, 1) <= x <= dt.date(2027, 12, 3))]
            wf = np.array([1.08 if x.weekday() in (3, 4) else (0.9 if x.weekday() == 6 else 1.0) for x in days])
            for c in counties:
                A = aud[c] * (0.92 if camp == "BV27-14" else 1.0)
                sp = budget * share[c] * wf / wf.sum() * np.exp(r.normal(0, 0.07, size=len(days)))
                sp = np.round(sp * (budget * share[c] / sp.sum()) * float(np.exp(r.normal(-0.01, 0.012))), 2)
                cpm = np.array([cpm_m[x.month - 1] for x in days]) * np.exp(r.normal(0, 0.06, size=len(days)))
                imp = np.round(sp / cpm * 1000).astype(int)
                fq = 1.12 + 0.28 * r.uniform(size=len(days)) + (0.15 if camp == "BV27-14" else 0)
                rch = np.minimum(np.round(imp / fq).astype(int), imp)
                ctr = {"Traffic": 0.0105, "Awareness": 0.0042, "Leads": 0.0068}[obj]
                clk = r.binomial(imp, ctr * float(np.exp(r.normal(0, 0.1))))
                cname = "%s %s | %s" % (camp, names[camp], {"Traffic": "Trafik", "Awareness": "Räckvidd",
                                                             "Leads": "Leads"}[obj])
                aset = "%s 18-64" % c
                for x, s_, i_, r_, k_ in zip(days, sp, imp, rch, clk):
                    daily.append((x, cname, aset, int(r_), int(i_), float(s_), int(k_)))
                I = int(imp.sum())
                R = int(round(A * 0.78 * (1 - np.exp(-I / (A * 2.3)))))
                R = int(min(max(R, int(rch.max() * 1.04)), int(rch.sum() * 0.97)))
                life.append((a, b, cname, aset, R, I, round(float(sp.sum()), 2), int(clk.sum())))
        daily.sort(key=lambda z: (z[0], z[1], z[2]))
        return daily, life
