"""The main call from the shipped pack, read the way an analyst reads it: the panel's members with their 28-day
weight, their live viewing on the panel's local clock, the as-run log's places, and each 2027 schedule replayed over
the four reference weeks under the brief's clauses 3.2 to 3.5.

route "golden": a fixed-place spot at its place; a rotation spot at each place where that day's rotation bookings
for the same channel and window aired (the sales houses' bookings joined to the as-run log by booking number), each
with the share of those bookings that aired there. The other routes are the same code with one reading changed:
"asrun" (the rotation places inside the window that day, as the as-run log shows them), "nonpremium" (every place in
the window that a first- or last-place booking did not hold), "uniform" (every place in the window, and every place
of a fixed spot's break) and "breaks" (anyone tuned for 15 seconds or more of the break)."""
import csv
import datetime as dt
import os

import numpy as np
from openpyxl import load_workbook

import common as K

T0 = dt.datetime.combine(K.REF_START, dt.time(0, 0))
SWITCH = dt.datetime(2026, 3, 29, 1, 0)        # UTC
NAME2CODE = {"Farol": "FAR1", "Farol 2": "FAR2", "Vértice": "VRT", "Litoral": "LIT", "Pulsar": "PLS", "Pulsar+": "PLS",
             "Arena": "ARN"}
PRIME = (20 * 3600, 24 * 3600 + 30 * 60)


def rows(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def wall_from_utc(s, dst=True):
    t = dt.datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ")
    if dst and t >= SWITCH:
        t += dt.timedelta(hours=1)
    return int((t - T0).total_seconds())


def wall_from_local(date, hms):
    t = dt.datetime.strptime(date + " " + hms, "%Y-%m-%d %H:%M:%S")
    return int((t - T0).total_seconds())


def channel_map(target):
    """every code in the channel list to the channel it names (a renamed channel keeps one identity)"""
    out = {}
    for r in rows(os.path.join(target, K.FILES["channels"])):
        out[r["codigo"]] = NAME2CODE[r["nome"]]
    return out


class Pack:
    def __init__(self, target, dst=True, rename=True, guests=False, playback=False, civil=False, length=None):
        """the readings an analyst can get wrong, each a switch: dst (the panel's UTC read across the clock change),
        rename (Pulsar+ as Pulsar), guests and playback (left out), civil (a break found by its civil date instead of
        its panel day), length (every place read at this many seconds from its start instead of its own length)"""
        self.target = target
        p = lambda k: os.path.join(target, K.FILES[k])
        cm = channel_map(target) if rename else {}
        canon = lambda c: cm.get(c, c)
        self.members = {}
        if guests:
            for r in rows(p("viewing")):
                if r["convidado"] != "N":
                    self.members[r["id_individuo"]] = ("18-24", 0.0)
        for r in rows(p("panel")):
            self.members[r["id_individuo"]] = (r["escalao_etario"], float(r["peso_28d"]))
        self.young = {m for m, (a, w) in self.members.items() if a in K.YOUNG and w > 0}
        self.wt = {m: w for m, (a, w) in self.members.items()}
        by = {}
        for r in rows(p("viewing")):
            if (r["modo"] != "AO VIVO" and not playback) or (r["convidado"] != "N" and not guests):
                continue
            by.setdefault(canon(r["canal"]), []).append((wall_from_utc(r["inicio_utc"], dst),
                                                         wall_from_utc(r["fim_utc"], dst), r["id_individuo"]))
        self.view = {}
        for c, lst in by.items():
            lst.sort()
            arr = np.array([(a, b) for a, b, _ in lst], dtype=np.int64)
            self.view[c] = (arr, [m for _, _, m in lst])
        self.maxlen = max(int((a[:, 1] - a[:, 0]).max()) for a, _ in self.view.values())
        self.booking = {}
        for r in rows(p("bookings")):
            self.booking[r["id_reserva"]] = dict(ch=canon(r["canal"]), day=r["dia_tv"], kind=r["colocacao"],
                                                 window=r["janela"])
        self.asrun = []
        for r in rows(p("asrun")):
            s0 = wall_from_local(r["data"], r["hora_inicio"])
            self.asrun.append(dict(ch=canon(r["canal"]), day=r["data"] if civil else r["dia_tv"], prog=r["programa"],
                                   brk=int(r["intervalo_no_programa"]), pos=int(r["posicao"]),
                                   n=int(r["spots_no_intervalo"]), s0=s0, s1=s0 + (length or int(r["duracao_s"])),
                                   kind=r["colocacao"], ref=r["id_reserva"],
                                   clock=s0 - int((dt.datetime.strptime(r["dia_tv"], "%Y-%m-%d") - T0).total_seconds())))
        self.sold = {}
        for a in self.asrun:
            bk = self.booking.get(a["ref"])
            if bk and bk["kind"] == "ROTAÇÃO":
                self.sold.setdefault((bk["ch"], bk["day"], bk["window"].lower()), []).append(a)
        self.by_break = {}
        self.by_day = {}
        for a in self.asrun:
            self.by_break.setdefault((a["ch"], a["day"], a["prog"], a["brk"]), []).append(a)
            self.by_day.setdefault((a["ch"], a["day"]), []).append(a)
        self.sched = self._schedules(p("schedules"))
        self._seen = {}

    def _schedules(self, path):
        wb = load_workbook(path, data_only=False)
        out = {}
        for s in K.SCHED:
            ws = wb["Esquema %s" % s]
            lines = []
            for row in ws.iter_rows(min_row=2, values_only=True):
                if row[0] in (None, "Total"):
                    continue
                week, date, _, chname, prog, brk, place = row[:7]
                d = dt.date.fromisoformat(date) if isinstance(date, str) else date
                ref = K.REF_START + dt.timedelta(days=7 * (int(week) - 1) + d.weekday())
                kind = {"1.º lugar no intervalo": "FP", "Último lugar no intervalo": "LP", "Rotação": "ROS"}[place]
                lines.append(dict(week=int(week), ref=ref.isoformat(), ch=NAME2CODE[chname], prog=prog,
                                  brk=int(brk) if brk not in (None, "") else None, kind=kind, price=row[8],
                                  window=prog[len("Rotação "):].lower() if kind == "ROS" else None))
            out[s] = lines
        return out

    def seen(self, ch, s0, s1, need=None):
        key = (ch, s0, s1, need)
        if key in self._seen:
            return self._seen[key]
        arr, mem = self.view[ch]
        lo = np.searchsorted(arr[:, 0], s0 - self.maxlen)
        hi = np.searchsorted(arr[:, 0], s1)
        acc = {}
        for j in range(lo, hi):
            o = min(arr[j, 1], s1) - max(arr[j, 0], s0)
            if o > 0:
                acc[mem[j]] = acc.get(mem[j], 0) + int(o)
        need = (s1 - s0) / 2.0 if need is None else need
        out = {m for m, v in acc.items() if v >= need}
        self._seen[key] = out
        return out

    def places(self, line, route="golden"):
        if line["kind"] == "ROS":
            if route == "golden":
                return self.sold.get((line["ch"], line["ref"], line["window"]), [])
            day = [a for a in self.by_day.get((line["ch"], line["ref"]), []) if PRIME[0] <= a["clock"] < PRIME[1]]
            if route == "asrun":
                return [a for a in day if a["kind"] == "ROTAÇÃO"]
            if route == "nonpremium":
                return [a for a in day if a["kind"] in ("FIXO", "ROTAÇÃO", "AUTOPROMOÇÃO")]
            if route == "breaks":
                br = {}
                for a in day:
                    br.setdefault((a["prog"], a["brk"]), []).append(a)
                return [("break", v) for v in br.values()]
            return day
        b = sorted(self.by_break.get((line["ch"], line["ref"], line["prog"], line["brk"]), []), key=lambda a: a["pos"])
        if not b:
            return []
        if route == "uniform":
            return b
        if route == "breaks":
            return [("break", b)]
        return [b[0]] if line["kind"] == "FP" else [b[-1]]

    def exposures(self, s, route="golden", weeks=None):
        E = {}
        for line in self.sched[s]:
            if weeks and line["week"] not in weeks:
                continue
            pl = self.places(line, route)
            if not pl:
                continue
            cnt = {}
            for x in pl:
                if isinstance(x, tuple):
                    v = x[1]
                    got = self.seen(line["ch"], v[0]["s0"], v[-1]["s1"], 15)
                else:
                    got = self.seen(line["ch"], x["s0"], x["s1"])
                for m in got & self.young:
                    cnt[m] = cnt.get(m, 0) + 1
            for m, c in cnt.items():
                E.setdefault(m, []).append(c / len(pl))
        return E

    def dist(self, E):
        """each young member's distribution of the number of spots seen"""
        out = {}
        for m, ps in E.items():
            d = np.zeros(len(ps) + 1)
            d[0] = 1.0
            for q in ps:
                d[1:] = d[1:] * (1 - q) + d[:-1] * q
                d[0] *= (1 - q)
            out[m] = d
        return out

    def reach(self, E, kmin):
        tot = sum(self.wt[m] for m in self.young)
        D = self.dist(E)
        return sum(self.wt[m] * d[kmin:].sum() for m, d in D.items()) / tot

    def cuts(self, E):
        """the shares of the 18 to 34 universe seeing the film at least once to at least five times"""
        return [self.reach(E, k) for k in (1, 2, 3, 4, 5)]


def main_call(target, route="golden", pack=None, **kw):
    P = pack or Pack(target, **kw)
    r3 = {s: P.reach(P.exposures(s, route), 3) for s in K.SCHED}
    order = sorted(K.SCHED, key=lambda s: -r3[s])
    return dict(pack=P, reach3=r3, call=order[0], runner=order[1], lead=r3[order[0]] - r3[order[1]])


def prime_bookings(P, chans=("VRT", "LIT", "PLS")):
    """the reference weeks' prime-time rotation bookings on the channels schedule B buys: where each aired"""
    win = K.WINDOW_NAME["prime"].lower()
    n = inside = 0
    for (ch, day, w), lst in P.sold.items():
        if ch in chans and w == win:
            for a in lst:
                n += 1
                inside += PRIME[0] <= a["clock"] < PRIME[1] and a["day"] == day
    return dict(bookings=n, in_prime=inside, elsewhere=n - inside, share_elsewhere=(n - inside) / n)


def b_places(P):
    """schedule B's reference places under the golden reading: how many, and how many outside prime time"""
    n = out = 0
    for line in P.sched["B"]:
        for a in P.places(line, "golden"):
            n += 1
            out += not (PRIME[0] <= a["clock"] < PRIME[1] and a["day"] == line["ref"])
    return dict(places=n, outside=out)


def ratings_grps(target, P):
    """rung 0: each schedule's 18-34 rating points from the Comissão's weekly programme audiences, a rotation line at
    the average of its window's programmes that week"""
    import csv as _csv
    cm = channel_map(target)
    rat = {}
    with open(os.path.join(target, K.FILES["ratings"]), newline="", encoding="utf-8") as f:
        for r in _csv.DictReader(f):
            rat[(int(r["semana"][-2:]) - 9, cm.get(r["canal"], r["canal"]), r["programa"])] = float(r["rat_18_34_pct"])
    win = {}
    for a in P.asrun:
        win.setdefault((a["ch"], a["prog"]), set()).add(window_of_clock(a["clock"]))
    out = {}
    for s in K.SCHED:
        g = 0.0
        for line in P.sched[s]:
            wk = line["week"]
            if line["kind"] == "ROS":
                w = [v for (k, ch, prog), v in rat.items() if k == wk and ch == line["ch"] and
                     "prime" in win.get((ch, prog), ())]
                g += sum(w) / len(w)
            else:
                g += rat[(wk, line["ch"], line["prog"])]
        out[s] = g
    return out


def window_of_clock(sec):
    m = sec / 60.0
    for w, (a, b) in K.WINDOWS.items():
        if a <= m < b:
            return w
    return "late"


def rungs(target, P):
    out = {"R0_ratings_grps": ratings_grps(target, P)}
    for route in ("breaks", "uniform", "nonpremium", "asrun", "golden"):
        out[route] = {s: P.reach(P.exposures(s, route), 3) for s in K.SCHED}
    return out
