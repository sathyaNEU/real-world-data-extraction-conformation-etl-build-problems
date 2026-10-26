"""The clean truth for task270: the six channels' programme grids and commercial breaks over the four reference
weeks, the audience panel's members and their viewing second by second, the sales houses' traffic (first-in-break,
last-in-break, fixed and rotation bookings placed by demand for the breaks' young audiences), the 2027 rate cards
and the three schedules Meridiano Media drafted at one budget.

Everything is simulated on the panel's local wall clock (seconds from 00:00 local on 2 March 2026); records.py
writes the panel's statements in UTC and the as-run log in local time."""
import numpy as np

import common as K

# genre appeal for adults 18 to 34 and for older adults; the share of viewers who leave the channel at a break
APPEAL_YOUNG = {"reality": 2.4, "drama": 0.75, "football": 1.6, "sporttalk": 0.7, "series": 2.0, "comedy": 1.8,
                "talk": 0.5, "news": 0.45, "magazine": 0.2, "game": 0.6, "film": 1.1, "music": 1.4, "docs": 0.3,
                "sport": 0.9, "kids": 0.1, "sitcom": 1.2}
APPEAL_OLD = {"reality": 0.8, "drama": 2.0, "football": 1.1, "sporttalk": 0.8, "series": 0.4, "comedy": 0.4,
              "talk": 1.1, "news": 2.0, "magazine": 1.5, "game": 1.4, "film": 0.8, "music": 0.3, "docs": 0.8,
              "sport": 0.6, "kids": 0.2, "sitcom": 0.9}
BASE_Q = {"reality": 0.30, "drama": 0.26, "football": 0.10, "sporttalk": 0.30, "series": 0.34, "comedy": 0.30,
          "talk": 0.34, "news": 0.24, "magazine": 0.40, "game": 0.28, "film": 0.32, "music": 0.42, "docs": 0.25,
          "sport": 0.22, "kids": 0.30, "sitcom": 0.30}
# share of a window's breaks whose first place is sold as a first-in-break booking, at the top of demand
P_FP = {("VRT", "prime"): 0.93, ("LIT", "prime"): 0.92, ("VRT", "access"): 0.75, ("LIT", "access"): 0.72,
        ("VRT", "late"): 0.55, ("LIT", "late"): 0.50, ("PLS", "prime"): 0.45, ("ARN", "prime"): 0.85,
        ("ARN", "access"): 0.75, ("FAR1", "prime"): 0.80}
# fixed-spot demand by window (daytime sells few fixed spots)
FIX_W = {"day": 0.45, "access": 0.85, "prime": 1.0, "late": 0.9}
SPOT_LEN = [30, 30, 30, 30, 30, 30, 20, 20, 15, 45, 10, 30]


def templates(ch, wd):
    """(start minute, length in minutes, title, genre, breaks inside) for one channel on one weekday"""
    wk = wd >= 5
    if ch == "FAR1":
        return [(420, 180, "Farol da Manhã", "magazine", 2), (780, 60, "Notícias da Tarde", "news", 0),
                (840, 240, "Tardes do Farol", "magazine", 2), (1080, 75, "Aposta Certa", "game", 1),
                (1200, 60, "Jornal do Farol", "news", 1), (1260, 60, "Mãe Coragem", "drama", 1),
                (1320, 75, "Sexta em Cena" if wd == 4 else "Grande Conversa", "comedy" if wd == 4 else "talk", 1),
                (1395, 105, "Cinema Farol", "film", 1)]
    if ch == "FAR2":
        return [(600, 300, "Farol 2 Infantil", "kids", 0), (900, 240, "Documentários", "docs", 0),
                (1140, 60, "Euronotícias", "news", 0), (1200, 120, "Arte e Ofícios", "docs", 1),
                (1320, 120, "Série Europeia", "series", 1), (1440, 60, "Concerto", "music", 0)]
    if ch == "VRT":
        return [(420, 210, "Manhã Vértice", "magazine", 4), (780, 60, "Primeiro Jornal Vértice", "news", 1),
                (840, 180, "Tarde Vértice", "magazine", 4), (1020, 120, "Herança", "drama", 3),
                (1140, 60, "Quem Arrisca", "game", 2), (1200, 60, "Jornal Vértice", "news", 2),
                (1260, 75, "Rosa dos Ventos", "drama", 2),
                (1335, 120, "Lote Sete: Gala" if wd == 6 else "Lote Sete", "reality", 4),
                (1455, 75, "Fim de Noite", "talk", 2)]
    if ch == "LIT":
        return [(420, 210, "Bom Dia Litoral", "magazine", 4), (780, 60, "Litoral Notícias", "news", 1),
                (840, 180, "Tardes do Litoral", "magazine", 4), (1020, 120, "Quiz Litoral", "game", 3),
                (1140, 60, "Família Lopes", "sitcom", 2), (1200, 60, "Litoral Hoje", "news", 2),
                (1260, 90, "Vento Norte", "drama", 3), (1350, 90, "Pedra Negra", "drama", 2),
                (1440, 90, "Mesa Redonda", "sporttalk", 2)]
    if ch == "PLS":
        return [(600, 360, "Riso Contínuo", "series", 12), (960, 120, "Top Pulsar", "music", 4),
                (1080, 120, "Pulsar Reality: Repetição", "reality", 4), (1200, 60, "Os Lunáticos", "series", 2),
                (1260, 120, "Ilha Proibida", "reality", 4), (1380, 120, "Palco Aberto", "comedy", 4)]
    if ch == "ARN":
        if wk:
            return [(600, 360, "Arena em Direto", "sport", 6), (1080, 120, "Liga: Jogo da Tarde", "football", 1),
                    (1230, 120, "Liga: Jogo da Noite", "football", 1), (1350, 90, "Resumo da Jornada", "sporttalk", 2)]
        euro = wd in (1, 2)
        return [(600, 300, "Arena em Direto", "sport", 6), (900, 120, "Antevisão", "sporttalk", 3),
                (1080, 120, "Arena Notícias", "sporttalk", 3),
                (1200, 120, "Taça Europeia" if euro else "Arena Magazine", "football" if euro else "sporttalk",
                 1 if euro else 3),
                (1320, 90, "Futebol Total", "sporttalk", 2)]
    raise KeyError(ch)


def window_of(ch, minute):
    for w, (a, b) in K.WINDOWS.items():
        if a <= minute < b:
            return w
    return "late"


class World:
    def __init__(self, seed=K.SEED, npan=2400, p=None):
        self.p = dict(h=1.4, vis=0.75, dur=42, young_z=1.35, L=30, R=30, ret=0.62, f0=0.05, f1=1.0, fe=2.0,
                      dn=0.12, **(p or {}))
        self.seed = seed
        self.rng = np.random.default_rng(seed)
        self._grid()
        self._panel(npan)
        self._viewing()
        self._index()
        self._traffic()
        self._rates()
        self._schedules()

    # ---------------------------------------------------------------- the grids and the breaks
    def _grid(self):
        rng = self.rng
        self.progs, self.breaks, self.spots = [], [], []
        for d in range(K.NDAYS):
            wd = K.REF_DAYS[d].weekday()
            for ch in K.CH:
                for (st, dur, title, genre, nb) in templates(ch, wd):
                    t0, t1 = d * 86400 + st * 60, d * 86400 + (st + dur) * 60
                    if d == K.DST_DAY - 1 and st + dur > 1500:       # the night the clocks go forward
                        t1 = min(t1, d * 86400 + 1500 * 60)
                        if t1 <= t0 + 600:
                            continue
                    pid = len(self.progs)
                    self.progs.append(dict(pid=pid, day=d, ch=ch, title=title, genre=genre,
                                           window=window_of(ch, st), t0=t0, t1=t1, start=st))
                    for k in range(nb):
                        if genre == "football":
                            bs = t0 + 47 * 60 + int(rng.integers(0, 120))
                            nsp = int(rng.integers(10, 14))
                        else:
                            bs = t0 + int((k + 1) / (nb + 1) * (t1 - t0) + rng.normal(0, 60))
                            w = window_of(ch, st)
                            if ch in ("VRT", "LIT"):
                                nsp = int(rng.integers(9, 14)) if w == "prime" else int(rng.integers(6, 10))
                            elif ch == "PLS":
                                nsp = int(rng.integers(5, 8))
                            else:
                                nsp = int(rng.integers(4, 7))
                        t, sp = bs, []
                        for pos in range(1, nsp + 1):
                            ln = int(rng.choice(SPOT_LEN))
                            sp.append(dict(bid=len(self.breaks), pos=pos, n=nsp, t0=t, t1=t + ln, kind=None))
                            t += ln
                        if t > t1:
                            continue
                        b = dict(bid=len(self.breaks), pid=pid, day=d, ch=ch, no=k + 1, t0=bs, t1=t, n=nsp,
                                 window=window_of(ch, (bs - d * 86400) / 60), genre=genre, title=title, spots=sp)
                        self.breaks.append(b)
                        self.spots += sp

    # ---------------------------------------------------------------- the panel
    def _panel(self, npan):
        rng = self.rng
        sizes = rng.choice([1, 2, 3, 4], 1100, p=[0.25, 0.33, 0.22, 0.20])
        hh = np.repeat(np.arange(len(sizes)), sizes)[:npan]
        n = len(hh)
        self.hh = hh
        self.age = rng.choice(K.AGE_BANDS, n, p=[0.10, 0.15, 0.18, 0.18, 0.17, 0.22])
        self.sex = rng.choice(["F", "M"], n)
        hreg = rng.choice(K.REGIONS, len(sizes), p=[0.35, 0.22, 0.28, 0.07, 0.08])
        self.region = hreg[hh]
        self.young = np.isin(self.age, K.YOUNG)
        AF = {"18-24": 0.42, "25-34": 0.62, "35-44": 1.0, "45-54": 1.25, "55-64": 1.5, "65+": 1.8}
        self.heavy = np.exp(rng.normal(0, 0.6, n)) * np.array([AF[a] for a in self.age]) * self.p["h"]
        self.zap = np.clip(np.exp(rng.normal(0, 0.35, n)) * np.where(self.young, self.p["young_z"], 1.0), 0.3, 3.0)
        pref = np.exp(rng.normal(0, 0.6, (n, len(K.CH))))
        pref[:, K.CH.index("PLS")] *= np.where(self.young, 0.9, 0.3)
        pref[:, K.CH.index("VRT")] *= np.where(self.young, 1.5, 1.0)
        pref[:, K.CH.index("FAR2")] *= np.where(self.young, 0.3, 0.8)
        pref[:, K.CH.index("ARN")] *= np.where(rng.random(n) < 0.45, 1.6, 0.25)
        self.pref = pref
        # days out of tab: about one member in fourteen misses one or more days of the four weeks
        self.out_days = {}
        for i in range(n):
            if rng.random() < 0.07:
                a = int(rng.integers(0, K.NDAYS))
                self.out_days[i] = set(range(a, min(K.NDAYS, a + int(rng.integers(1, 6)))))
        self.intab = np.array([i not in self.out_days for i in range(n)])
        self._weights()

    def _weights(self):
        """the 28-day weight: members in tab every day, raked to the universe by age band and sex, then region"""
        rng = np.random.default_rng(97)
        uni_age = dict(zip(K.AGE_BANDS, [0.103, 0.139, 0.165, 0.172, 0.165, 0.256]))
        uni_reg = dict(zip(K.REGIONS, [0.345, 0.218, 0.287, 0.069, 0.081]))
        self.universe = {}
        tot = K.UNIVERSE_ADULT
        for a in K.AGE_BANDS:
            for s, fs in (("F", 0.525 if a in ("55-64", "65+") else 0.505), ("M", 0.475 if a in ("55-64", "65+")
                                                                                else 0.495)):
                for g in K.REGIONS:
                    self.universe[(a, s, g)] = int(round(tot * uni_age[a] * fs * uni_reg[g] *
                                                         float(np.exp(rng.normal(0, 0.03))), -3))
        young_tot = sum(v for (a, s, g), v in self.universe.items() if a in K.YOUNG)
        scale = K.UNIVERSE_YOUNG / young_tot
        for k in list(self.universe):
            if k[0] in K.YOUNG:
                self.universe[k] = int(round(self.universe[k] * scale, -3))
        w = self.intab.astype(float)
        for _ in range(25):
            for key, arr in (("as", [(a, s) for a, s in zip(self.age, self.sex)]), ("g", list(self.region))):
                tgt, cur = {}, {}
                for (a, s, g), v in self.universe.items():
                    kk = (a, s) if key == "as" else g
                    tgt[kk] = tgt.get(kk, 0) + v
                for i, kk in enumerate(arr):
                    cur[kk] = cur.get(kk, 0) + w[i]
                w = np.array([w[i] * tgt[kk] / cur[kk] if cur[kk] > 0 else 0 for i, kk in enumerate(arr)])
        self.wt = np.round(w, 1)

    # ---------------------------------------------------------------- viewing
    def _viewing(self):
        rng, p = self.rng, self.p
        byday = {}
        for pr in self.progs:
            byday.setdefault(pr["day"], []).append(pr)
        bprog = {}
        for b in self.breaks:
            bprog.setdefault(b["pid"], []).append(b)
        # visits per daypart; adults under 35 watch little in the working day
        dayparts = [(420, 720, 0.5, 0.45), (720, 900, 0.8, 0.55), (900, 1020, 0.65, 0.6), (1020, 1140, 0.8, 0.9),
                    (1140, 1260, 1.2, 1.0), (1260, 1410, 1.5, 1.0), (1410, 1530, 0.6, 1.1)]
        live, play = [], []
        n = len(self.age)
        for i in range(n):
            A = APPEAL_YOUNG if self.young[i] else APPEAL_OLD
            for d in range(K.NDAYS):
                if d in self.out_days.get(i, ()):
                    continue
                plist = byday[d]
                busy = -1
                for (m0, m1, rate, yf) in dayparts:
                    nvis = rng.poisson(rate * (yf if self.young[i] else 1.0) * self.heavy[i] * p["vis"])
                    starts = sorted(d * 86400 + int(rng.uniform(m0, m1) * 60) for _ in range(nvis))
                    for ts in starts:
                        if ts < busy:
                            continue
                        cands = [pr for pr in plist if pr["t0"] <= ts < pr["t1"]]
                        if not cands:
                            continue
                        w = np.array([self.pref[i, K.CH.index(pr["ch"])] * A[pr["genre"]] for pr in cands])
                        pr = cands[rng.choice(len(cands), p=w / w.sum())]
                        dur = np.exp(rng.normal(np.log(p["dur"] * 60 * (0.6 + 0.4 * min(self.heavy[i], 2.5))), 0.6))
                        te = int(ts + max(dur, 180))
                        if rng.random() < 0.5:
                            te = int(min(te, pr["t1"]))
                        te = min(te, d * 86400 + (1500 if d == K.DST_DAY - 1 else 1560) * 60)
                        busy = te
                        if rng.random() < (0.07 if self.young[i] else 0.03):
                            play.append((i, K.CH.index(pr["ch"]), ts, te))      # a recording, watched now
                            continue
                        ch, cur, ended = pr["ch"], ts, False
                        bl = [b for pr2 in plist if pr2["ch"] == ch and pr2["t1"] > ts and pr2["t0"] < te
                              for b in bprog.get(pr2["pid"], [])]
                        bl.sort(key=lambda b: b["t0"])
                        for b in bl:
                            if b["t0"] < cur or b["t0"] >= te:
                                continue
                            q = min(0.97, BASE_Q[b["genre"]] * self.zap[i] * (1.15 if b["no"] >= 3 else 1.0))
                            if rng.random() < q:
                                leave = int(b["t0"] + min(rng.exponential(p["L"]), 120))
                                if leave >= b["t1"]:
                                    continue
                                live.append((i, K.CH.index(ch), cur, leave))
                                if rng.random() < p["ret"]:
                                    back = int(b["t1"] - min(rng.exponential(p["R"]), max(b["t1"] - leave - 5, 0)))
                                    if rng.random() < 0.4:
                                        och = K.CH[int(rng.integers(0, len(K.CH)))]
                                        if och != ch and back - leave > 20:
                                            live.append((i, K.CH.index(och), leave + 3, back - 2))
                                    cur = back
                                else:
                                    ended = True
                                    break
                        if not ended and te > cur:
                            live.append((i, K.CH.index(ch), cur, te))
        # one set, one channel at a time: a statement that would begin before the member's previous one ended
        # begins when it ends (a channel-hop during a break that ran past the end of the visit)
        clipped, last = [], {}
        for (i, c, a0, a1) in sorted(live, key=lambda x: (x[0], x[2], x[3])):
            a0 = max(a0, last.get(i, a0))
            if a1 > a0:
                clipped.append((i, c, a0, a1))
                last[i] = a1
        self.live = np.array(clipped, dtype=np.int64)
        self.recordings = [s for s in play if s[3] > s[2]]
        self.play = self._playback(self.recordings)
        # guests in panel homes: a visitor watching beside a member
        guests = []
        for s in self.live:
            if rng.random() < 0.012:
                guests.append((int(self.hh[s[0]]), int(s[1]), int(s[2]), int(s[3])))
        self.guests = guests

    def _playback(self, recordings):
        """time-shifted viewing: each recording watched later at normal speed, most breaks fast-forwarded, now and
        then a few seconds played again; one statement per stretch of broadcast seen at normal speed, as
        (member, channel, viewing start, viewing end, broadcast second at the start)"""
        rng = np.random.default_rng(self.seed + 2000)
        brk = {}
        for b in self.breaks:
            brk.setdefault(K.CH.index(b["ch"]), []).append((b["t0"], b["t1"]))
        for c in brk:
            brk[c].sort()
        gap = (26 * 86400 + 1500 * 60, 27 * 86400 + 120 * 60)       # the hour the clocks skip on 29 March
        last = 27 * 86400 + 1560 * 60
        out = []
        for (i, c, b0, b1) in recordings:
            d = (b0 - 7200) // 86400
            day_end = d * 86400 + (1500 if d == K.DST_DAY - 1 else 1560) * 60
            span = b1 - b0
            if rng.random() < (0.55 if self.young[i] else 0.45) and b1 + 300 + span < day_end:
                v = b0 + int(rng.uniform(300, max(301, min(10800, day_end - b0 - span))))
            else:
                v = b0 + int(rng.integers(1, 8)) * 86400 + int(rng.uniform(-5400, 5400))
            if v + span > last:
                continue
            if v < gap[1] and v + span > gap[0]:
                v += gap[1] - gap[0]
            cur, segs = b0, []
            for (t0, t1) in brk.get(c, []):
                if t1 <= cur or t0 >= b1:
                    continue
                if rng.random() < 0.62:                                   # fast-forwarded
                    if t0 > cur:
                        segs.append((cur, t0))
                    cur = min(t1, b1)
            if b1 > cur:
                segs.append((cur, b1))
            prev_end = None
            for (s0, s1) in segs:
                if prev_end is not None:
                    v += int((s0 - prev_end) / 8)                         # the break at eight times speed
                v = max(v, s0 + 20)                                       # nobody overtakes the broadcast
                if s1 - s0 > 240 and rng.random() < 0.06:                 # a scene played again
                    cut = int(rng.uniform(s0 + 60, s1 - 60))
                    back = int(rng.uniform(10, 45))
                    out.append((i, c, v, v + cut - s0, s0))
                    v += cut - s0
                    v = max(v, cut - back + 20)
                    out.append((i, c, v, v + s1 - cut + back, cut - back))
                    v += s1 - cut + back
                else:
                    out.append((i, c, v, v + s1 - s0, s0))
                    v += s1 - s0
                prev_end = s1
        return np.array(out, dtype=np.int64)

    def _index(self):
        S = self.live
        self.idx = {}
        for c in range(len(K.CH)):
            Sc = S[S[:, 1] == c]
            self.idx[c] = Sc[np.argsort(Sc[:, 2], kind="stable")]
        self.maxlen = int((S[:, 3] - S[:, 2]).max())

    def seconds(self, ch, s0, s1):
        """each panel member's live seconds on channel ch inside [s0, s1)"""
        Sc = self.idx[K.CH.index(ch)]
        lo = np.searchsorted(Sc[:, 2], s0 - self.maxlen)
        hi = np.searchsorted(Sc[:, 2], s1)
        seg = Sc[lo:hi]
        ov = np.clip(np.minimum(seg[:, 3], s1) - np.maximum(seg[:, 2], s0), 0, None)
        out = {}
        for pid, o in zip(seg[:, 0].tolist(), ov.tolist()):
            if o > 0:
                out[pid] = out.get(pid, 0) + o
        return out

    def seen(self, ch, s0, s1):
        """members tuned live for at least half of [s0, s1)"""
        need = (s1 - s0) / 2.0
        return {k for k, v in self.seconds(ch, s0, s1).items() if v >= need}

    def young_aud(self, ch, s0, s1):
        return sum(self.wt[i] for i in self.seen(ch, s0, s1) if self.young[i])

    # ---------------------------------------------------------------- the sales houses' traffic
    # rotation bookings per open place by channel and window: prime on the two generalist channels is oversold, so
    # the channel moves the excess to the same night's late window, then to the next day's daytime breaks
    ROS_DEMAND = {("VRT", "prime"): 1.45, ("LIT", "prime"): 1.45, ("PLS", "prime"): 1.45,
                  ("VRT", "access"): 0.95, ("LIT", "access"): 0.95, ("PLS", "access"): 0.9,
                  ("VRT", "late"): 0.45, ("LIT", "late"): 0.45, ("VRT", "day"): 0.50, ("LIT", "day"): 0.50,
                  ("PLS", "day"): 0.5}

    MOVE_TO = ("day",)

    def _traffic(self):
        rng, p = np.random.default_rng(self.seed + 1000), self.p
        for b in self.breaks:
            for s in b["spots"]:
                s["kind"] = None
                s.pop("booked", None)
                s.pop("moved", None)
        for b in self.breaks:
            b["demand"] = self.young_aud(b["ch"], b["t0"], b["t0"] + 30) * float(np.exp(rng.normal(0, p["dn"])))
        win = {}
        for b in self.breaks:
            win.setdefault((b["day"], b["ch"], b["window"]), []).append(b)
        for lst in win.values():
            o = sorted(lst, key=lambda x: x["demand"])
            for j, b in enumerate(o):
                b["rank"] = (j + 1) / len(o)
        for b in self.breaks:
            r, sp = b["rank"], b["spots"]
            pfp = P_FP.get((b["ch"], b["window"]), 0.25) * (0.5 + 0.5 * r)
            sp[0]["kind"] = "FP" if rng.random() < pfp else None
            sp[-1]["kind"] = "LP" if rng.random() < 0.8 * pfp else None
            share = min(1.0, max(0.1, FIX_W[b["window"]] * (p["f0"] + p["f1"] * r ** p["fe"]) + rng.normal(0, 0.05)))
            for s in sp:
                if s["kind"] is None and rng.random() < share:
                    s["kind"] = "FIX"
        self.win = win
        leftover, excess = {}, {}
        for key in sorted(win, key=lambda k: (k[0], K.CH.index(k[1]), ["day", "access", "prime", "late"].index(k[2]))):
            day, ch, w = key
            ob = [(b, s) for b in sorted(win[key], key=lambda x: x["t0"]) for s in b["spots"] if s["kind"] is None]
            opens = [s for _, s in ob]
            n_ros = int(round(len(opens) * self.ROS_DEMAND.get((ch, w), 0.8) * float(np.exp(rng.normal(0, 0.06)))))
            n_ros = max(n_ros, sum(1 for b, x in ob if x["pos"] in (1, b["n"])))      # a break's ends are always sold
            # the window's own rotation goes to the better open places; what stays open is the weakest
            pri = np.array([b["demand"] for b, _ in ob]) * np.exp(rng.normal(0, 0.5, len(ob))) + \
                np.array([1e9 if s["pos"] in (1, b["n"]) else 0.0 for b, s in ob])
            order = [int(j) for j in np.argsort(-pri, kind="stable")]
            for j in order[:n_ros]:
                opens[j].update(kind="ROS", booked=(day, ch, w))
            leftover[key] = [opens[j] for j in order[n_ros:]]
            excess[key] = max(0, n_ros - len(opens))
        # the channel's traffic team places what does not fit in a sold-out window in the open places left that
        # day or night, or in the next day's daytime breaks
        self.moved = 0
        for key in sorted(excess, key=lambda k: (k[0], K.CH.index(k[1]))):
            day, ch, w = key
            n = excess[key]
            if not n:
                continue
            dests = [(day, ch, x) for x in ("day", "late") if x != w]
            if day + 1 < K.NDAYS:
                dests.append((day + 1, ch, "day"))
            dests = [x for x in dests if x[2] in self.MOVE_TO]
            pool = [(dk, j) for dk in dests for j in range(len(leftover.get(dk, [])))]
            n = min(n, len(pool))           # the sales house stops selling a night it cannot place
            pick = sorted((pool[int(j)] for j in rng.choice(len(pool), n, replace=False)), key=lambda x: (x[0], -x[1]))
            for dk, j in pick:
                s = leftover[dk].pop(j)
                s.update(kind="ROS", booked=(day, ch, w), moved=True)
                self.moved += 1
        for lst in leftover.values():
            for s in lst:
                s["kind"] = "PROMO"
        self.booked = {}
        for b in self.breaks:
            for s in b["spots"]:
                s["ch"] = b["ch"]
                if s["kind"] == "ROS":
                    self.booked.setdefault(s["booked"], []).append(s)

    # ---------------------------------------------------------------- the 2027 rate cards
    def _rates(self):
        aud = {}
        for b in self.breaks:
            aud.setdefault((b["ch"], b["title"]), []).append(self.young_aud(b["ch"], b["t0"], b["t0"] + 30) / 1000)
        self.rate = {}
        for (ch, title), v in aud.items():
            prem = K.ARENA_PREMIUM if ch == "ARN" else 1.0
            self.rate[(ch, title)] = max(150, int(K.r(K.CPM_YOUNG * float(np.mean(v)) * prem / 50) * 50))
        self.prog_window = {(pr["ch"], pr["title"]): pr["window"] for pr in self.progs}
        acc = {}
        for (ch, title), v in self.rate.items():
            acc.setdefault((ch, self.prog_window[(ch, title)]), []).append((v, len(aud[(ch, title)])))
        self.ros_rate = {k: int(K.r((1 - K.ROS_DISCOUNT) * np.average([x[0] for x in v], weights=[x[1] for x in v])
                                    / 50) * 50) for k, v in acc.items()}

    # ---------------------------------------------------------------- the three schedules
    MENU = {
        "A": [(0, "VRT", "Lote Sete", 2, "FP"), (1, "PLS", "Ilha Proibida", 2, "FP"), (2, "VRT", "Lote Sete", 3, "FP"),
              (3, "LIT", "Vento Norte", 2, "FP"), (4, "VRT", "Lote Sete", 2, "FP"), (6, "VRT", "Lote Sete: Gala", 2, "FP"),
              (1, "VRT", "Lote Sete", 3, "FP"), (3, "PLS", "Ilha Proibida", 3, "FP"), (0, "LIT", "Vento Norte", 3, "FP"),
              (2, "PLS", "Ilha Proibida", 2, "FP"), (3, "VRT", "Lote Sete", 2, "FP"), (6, "VRT", "Lote Sete: Gala", 3, "FP")],
        "B": [(wd, ch, None, "prime", "ROS") for wd in range(7) for ch in ("VRT", "LIT", "PLS")],
        "C": [(1, "ARN", "Taça Europeia", 1, "LP"), (0, "PLS", "Palco Aberto", 2, "LP"),
              (5, "ARN", "Liga: Jogo da Noite", 1, "LP"), (1, "LIT", "Mesa Redonda", 1, "LP"),
              (2, "PLS", "Palco Aberto", 3, "LP"), (6, "ARN", "Liga: Jogo da Noite", 1, "LP"),
              (3, "VRT", "Fim de Noite", 1, "LP"), (2, "ARN", "Taça Europeia", 1, "LP"),
              (4, "PLS", "Palco Aberto", 2, "LP"), (0, "LIT", "Mesa Redonda", 1, "LP"),
              (2, "LIT", "Mesa Redonda", 1, "LP"), (1, "VRT", "Fim de Noite", 1, "LP"),
              (5, "ARN", "Liga: Jogo da Tarde", 1, "LP"), (3, "PLS", "Palco Aberto", 3, "LP"),
              (4, "VRT", "Fim de Noite", 1, "LP"), (3, "LIT", "Mesa Redonda", 1, "LP")],
    }

    def _schedules(self):
        """each schedule's spot lines, taken week by week through its menu until the budget is spent"""
        self.sched = {}
        for s in K.SCHED:
            lines, spent = [], 0
            for i, it in enumerate(self.MENU[s]):
                for wk in range(4):
                    wd, ch, title, b_no, kind = it
                    if kind == "ROS":
                        price = self.ros_rate[(ch, b_no)]
                    else:
                        price = int(K.r(self.rate[(ch, title)] * K.PREMIUM[kind]))
                    if spent + price > K.BUDGET:
                        continue
                    spent += price
                    lines.append(dict(week=wk + 1, wd=wd, ch=ch, title=title, brk=b_no, kind=kind, price=price))
            lines.sort(key=lambda x: (x["week"], x["wd"], x["ch"], x["title"] or "", x["brk"] if x["kind"] != "ROS"
                                      else 0))
            self.sched[s] = lines

    # ---------------------------------------------------------------- the replay
    def break_of(self, day, ch, title, no):
        for b in self.breaks:
            if b["day"] == day and b["ch"] == ch and b["title"] == title and b["no"] == no:
                return b
        return None

    def places(self, line, route="golden"):
        """the places a 2027 spot line takes in its reference week, read in equal shares"""
        day = (line["week"] - 1) * 7 + line["wd"]
        if line["kind"] == "ROS":
            bl = self.win[(day, line["ch"], line["brk"])]
            allsp = [s for b in bl for s in b["spots"]]
            if route == "golden":
                return self.booked[(day, line["ch"], line["brk"])]
            if route == "asrun":
                return [s for s in allsp if s["kind"] == "ROS"]
            if route == "nonpremium":
                return [s for s in allsp if s["kind"] in ("FIX", "ROS", "PROMO")]
            if route == "breaks":
                return [("break", b) for b in bl]
            return allsp
        b = self.break_of(day, line["ch"], line["title"], line["brk"])
        if route in ("uniform", "breaks"):
            return b["spots"] if route == "uniform" else [("break", b)]
        return [b["spots"][0]] if line["kind"] == "FP" else [b["spots"][-1]]

    def exposures(self, sched, route="golden", ids=None):
        """each member's chance of seeing each spot line, as a list per member"""
        ch_of = {}
        E = {}
        for line in self.sched[sched]:
            pl = self.places(line, route)
            cnt = {}
            for x in pl:
                if isinstance(x, tuple):
                    b = x[1]
                    got = {k for k, v in self.seconds(b["ch"], b["t0"], b["t1"]).items() if v >= 15}
                else:
                    got = self.seen(x["ch"], x["t0"], x["t1"])
                for v in got:
                    cnt[v] = cnt.get(v, 0) + 1
            for v, c in cnt.items():
                if ids is None or v in ids:
                    E.setdefault(v, []).append(c / len(pl))
        return E

    def reach(self, E, kmin, ids):
        tot = sum(self.wt[i] for i in ids)
        acc = 0.0
        for i, ps in E.items():
            if i not in ids:
                continue
            dist = np.zeros(len(ps) + 1)
            dist[0] = 1.0
            for q in ps:
                dist[1:] = dist[1:] * (1 - q) + dist[:-1] * q
                dist[0] *= (1 - q)
            acc += self.wt[i] * dist[kmin:].sum()
        return acc / tot

    def young_ids(self):
        return set(np.where(self.young & (self.wt > 0))[0].tolist())
