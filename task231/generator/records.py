"""task231 records: the simulated panel written out as the bank's files.

Nothing here changes a simulated outcome. Identifiers, timestamps and call attempts come from the records layer's own
streams, so every return keeps its simulated day (a weekend return can move to the Monday, which never changes whether
it beat a Friday close), every closure keeps its simulated dates, and every call outcome the simulation drew is the
outcome the call log carries."""
import hashlib
import heapq
from collections import Counter, defaultdict
from datetime import date, datetime, timedelta, timezone

import numpy as np

import params as P
import sim
import world as W

FRAMES = sim.round_dates()
FRAME_SET = set(FRAMES)
CALLS_FROM = date(2022, 3, 1)           # the contact centre's current system; its call records start with March 2022
BUREAU_FROM = date(2023, 2, 1)          # paper questionnaires keyed by an outside bureau from this date
TRANSFER_FROM = date(2024, 4, 9)        # telephone returns reach the survey database in an overnight transfer
REPLAY_DAY = date(2026, 9, 22)          # the contractor's records for this day were sent twice
REPLAY_LOAD = (date(2026, 9, 23), 14, 12)
REFRESH_2026 = date(2026, 3, 1)


def rng(name):
    h = hashlib.sha256(("%d/%s" % (P.REC_SEED, name)).encode()).hexdigest()
    return np.random.default_rng(int(h[:15], 16))


def closed_day(d):
    """weekends, and the Christmas and New Year holidays"""
    return d.weekday() >= 5 or (d.month == 12 and d.day in (24, 25, 26)) or (d.month == 1 and d.day == 1)


def next_monday(d):
    """the next day the post room is open"""
    while closed_day(d):
        d += timedelta(days=1)
    return d


def add_working_days(d, n):
    while n > 0:
        d += timedelta(days=1)
        if not closed_day(d):
            n -= 1
    return d


def local_dt(d, seconds):
    """Brevland wall-clock time `seconds` after midnight on date d, as UTC"""
    h, rem = divmod(int(seconds), 3600)
    m, s = divmod(rem, 60)
    return W.local_to_utc(d, h, m, s)


def wave_label(f):
    if f["wave"] == "2014":
        return "2014 panel"
    if f["wave"] == "expansion":
        return "2024 expansion"
    return "%d refreshment" % f["joined"].year


class Records:
    def __init__(self, pan):
        self.pan = pan
        self.firms = pan.firms
        self.build_firms()
        self.build_calls()
        self.build_returns()

    # ----------------------------------------------------------------------------------------------- firms
    def consent_window(self, joined, wave):
        if wave == "2014":
            return date(2014, 1, 6), date(2014, 2, 21)
        if wave == "expansion":
            return date(2023, 11, 6), date(2024, 2, 23)
        return date(joined.year, 1, 5), date(joined.year, 2, 20)

    def build_firms(self):
        rc = rng("consent")
        rn = rng("nace")
        rx = rng("extra")
        ri = rng("ids")
        firms = self.firms
        # left date and reason, as the panel register records them
        for f in firms:
            if f.get("removed") is not None:
                f["left"], f["left_reason"] = f["registered"], "closure registered"
            elif f["retired"] is not None:
                f["left"], f["left_reason"] = sim.end_of(f["retired"]), "retired: no return in six rounds"
            elif f["withdrawn"] is not None:
                f["left"], f["left_reason"] = f["withdrawn"], "withdrew"
            else:
                f["left"], f["left_reason"] = None, ""
        # consent dates on working days inside each wave's recruitment window
        for f in firms:
            lo, hi = self.consent_window(f["joined"], f["wave"])
            span = (hi - lo).days
            while True:
                d = lo + timedelta(days=int(rc.integers(0, span + 1)))
                if d.weekday() < 5:
                    break
            f["consent"] = d
        # recruits who consented and withdrew before their first round: recruited, never invited
        self.extra = []
        waves = sorted({(f["joined"], f["wave"]) for f in firms if f["wave"] != "2014"})
        for joined, wave in waves:
            n_wave = sum(1 for f in firms if f["joined"] == joined and f["wave"] == wave)
            k = int(round(n_wave * (0.026 if joined == REFRESH_2026 else 0.012))) + int(rx.integers(0, 3))
            lo, hi = self.consent_window(joined, wave)
            for _ in range(k):
                reg = P.REGIONS[int(rx.choice(len(P.REGIONS), p=[r[2] / sum(x[2] for x in P.REGIONS) for r in P.REGIONS]))][0]
                ind = P.INDUSTRIES[int(rx.choice(len(P.INDUSTRIES), p=[x[2] for x in P.INDUSTRIES]))][0]
                size = P.SIZES[int(rx.choice(len(P.SIZES), p=[x[2] for x in P.SIZES]))][0]
                while True:
                    d = lo + timedelta(days=int(rx.integers(0, (hi - lo).days + 1)))
                    if d.weekday() < 5:
                        break
                gone = d + timedelta(days=int(rx.integers(4, 26)))
                if gone >= joined:
                    gone = joined - timedelta(days=int(rx.integers(2, 9)))
                if gone <= d:
                    gone = d + timedelta(days=1)
                self.extra.append(dict(fid=None, xid=len(self.extra), region=reg, industry=ind, size=size, joined=joined,
                                       wave=wave, consent=d, left=gone, left_reason="withdrew", ceased=None, registered=None,
                                       route=None))
        everyone = firms + self.extra
        # industry as the register held it at recruitment: NACE Rev. 2.1 sections from 2025
        for f in everyone:
            if f["consent"] >= W.REV21_FROM:
                g = f["industry"]
                f["nace"] = ("K" if rn.random() < 0.64 else "J") if g == "J" else W.REV2_TO_REV21[g]
            else:
                f["nace"] = f["industry"]
        # company numbers: unique six-digit cores; companies registered since March 2021 have cores from 700000
        old_pool = [c for c in range(100000, 700000) if W.check_digit(c) is not None]
        new_pool = [c for c in range(700000, 1000000) if W.check_digit(c) is not None]
        old_pool = list(ri.permutation(old_pool))
        new_pool = list(ri.permutation(new_pool))
        rank = lambda x: x["fid"] if x["fid"] is not None else 10 ** 9 + x["xid"]
        for f in sorted(everyone, key=lambda x: (x["consent"], x["region"], rank(x))):
            young = f["consent"] >= W.NUMBER_CHANGE and ri.random() < 0.27
            f["core"] = int(new_pool.pop() if young else old_pool.pop())
            f["company_number"] = W.company_number(f["core"])
        # a firm the recruitment contractor signed up twice: the second record kept the contractor's six-digit capture of
        # the company number and was cancelled as a withdrawal before the firm's first round
        rd = rng("duplicates")
        self.dups = []
        for joined, wave in waves:
            if wave != "refresh":
                continue
            pool = [f for f in firms if f["joined"] == joined and f["wave"] == "refresh" and f["core"] < 700000]
            pool.sort(key=lambda f: f["fid"])
            k = int(round(len(pool) * (0.015 if joined == REFRESH_2026 else 0.008))) + int(rd.integers(0, 2))
            for i in sorted(rd.choice(len(pool), size=min(k, len(pool)), replace=False).tolist()):
                f0 = pool[i]
                lo, hi = self.consent_window(joined, wave)
                step = int(rd.integers(2, 10)) * (1 if rd.random() < 0.6 else -1)
                d = min(max(f0["consent"] + timedelta(days=step), lo), joined - timedelta(days=8))
                while d.weekday() >= 5:
                    d -= timedelta(days=1)
                gone = min(d + timedelta(days=int(rd.integers(3, 13))), joined - timedelta(days=2))
                dup = dict(fid=None, xid=10 ** 6 + len(self.dups), region=f0["region"], industry=f0["industry"],
                           nace=f0["nace"], size=f0["size"], joined=joined, wave=wave, consent=d, left=gone,
                           left_reason="withdrew", ceased=None, registered=None, route=None, core=f0["core"],
                           company_number=W.old_number(f0["core"]), duplicate_of=f0)
                self.dups.append(dup)
        everyone = everyone + self.dups
        # panel identifiers: the 2014 panel from 100001, later refreshments continue that block; the 2024 expansion
        # was issued from 300001, and identifiers freed there were issued again to the 2026 refreshment
        order = sorted(everyone, key=lambda x: (x["consent"], rank(x)))
        main_next, exp_next = 100001, 300001
        freed = None
        for f in order:
            if f["wave"] == "expansion":
                f["panel_id"] = exp_next
                exp_next += 1
            elif f["joined"] == REFRESH_2026:
                if freed is None:
                    # identifiers in the expansion block free for six months or more go out again first
                    freed = sorted((x for x in everyone if x["wave"] == "expansion" and x["left"] is not None
                                    and x["left"] < date(2025, 7, 1)), key=lambda x: (x["left"], x["panel_id"]))
                    freed = [x["panel_id"] for x in freed]
                    freed.reverse()
                if freed:
                    f["panel_id"] = freed.pop()
                else:
                    f["panel_id"] = main_next
                    main_next += 1
            else:
                f["panel_id"] = main_next
                main_next += 1
        self.everyone = everyone
        self.pid = {f["fid"]: f["panel_id"] for f in firms}
        self.by_core = {f["core"]: f for f in everyone}

    # ----------------------------------------------------------------------------------------------- calls
    def build_calls(self):
        """The contact centre's call records from March 2022: the bank's own centre (BCB) and, on the busiest days, the
        overflow contractor (OVF). Every called firm's final attempt carries the simulated outcome."""
        r = rng("calls")
        self.calls = []                     # one dict per record
        self.phone_end = {}                 # (fid, frame) -> interview end (UTC) for a telephone return
        self.attempt_of = defaultdict(list)
        by_frame = defaultdict(list)
        for o in self.pan.outcomes:
            by_frame[o["frame"]].append(o)
        inbound = defaultdict(list)
        code_final_ok = lambda c: c in ("COMP", "PROM", "REFU")
        for frame in FRAMES:
            if frame < CALLS_FROM:
                continue
            close = sim.close_of(frame)
            days = sim.call_days(frame, close)
            over_days = set(days[2:5])
            called = [o for o in by_frame[frame] if o["call"] is not None]
            todo = defaultdict(list)        # (day offset, team) -> attempts
            for o in called:
                f = self.firms[o["fid"]]
                fin = o["call_day"]
                before = [d for d in days if d < fin]
                if o["call"] == "unobtainable":
                    k = 0
                elif o["call"] == "no_answer":
                    k = min(len(before), 1 + int(r.random() < 0.45))
                else:
                    u = r.random()
                    k = min(len(before), 0 if u < 0.5 else (1 if u < 0.85 else 2))
                early = sorted(r.choice(before, size=k, replace=False).tolist()) if k else []
                alive = o["alive"]
                seq = []
                for d in early:
                    u = r.random()
                    if alive:
                        code = "NOAN" if u < 0.45 else ("VMSG" if u < 0.75 else ("BUSY" if u < 0.85 else "STAF"))
                    else:
                        code = "NOAN" if u < 0.85 else ("VMSG" if u < 0.95 else "BUSY")
                    seq.append((d, code))
                final = {"returned": "COMP", "promised": "PROM", "refused": "REFU", "ceased": "CEAS",
                         "unobtainable": "UNOB"}.get(o["call"])
                if final is None:
                    final = ("NOAN" if r.random() < 0.55 else "VMSG") if alive else ("NOAN" if r.random() < 0.85 else "VMSG")
                seq.append((fin, final))
                callback = None
                if code_final_ok(final) and fin != (close - frame).days:
                    if r.random() < (0.30 if final == "COMP" else 0.15):
                        callback = final
                        seq[-1] = (fin, "VMSG" if r.random() < 0.65 else "STAF")
                for d, code in seq:
                    team = "OVF" if (d in over_days and r.random() < 0.40) else "BCB"
                    att = dict(o=o, f=f, code=code, final=(d == fin and callback is None), after=None)
                    todo[(d, team)].append(att)
                    if d == fin and callback is not None:
                        inbound[(d, frame)].append(dict(o=o, f=f, code=callback, final=True, after=att))
                    # the dialler tries a busy or unanswered number again later the same day
                    if d != fin and code in ("NOAN", "BUSY") and r.random() < 0.22:
                        u = r.random()
                        if alive:
                            c2 = "NOAN" if u < 0.5 else ("VMSG" if u < 0.75 else ("STAF" if u < 0.9 else "BUSY"))
                        else:
                            c2 = "NOAN" if u < 0.8 else ("VMSG" if u < 0.95 else "BUSY")
                        todo[(d, team)].append(dict(o=o, f=f, code=c2, final=False, after=att))
            for (d, team), atts in sorted(todo.items()):
                day = frame + timedelta(days=d)
                self.schedule(r, frame, day, team, atts, close)
            for (d, fr), atts in sorted(inbound.items()):
                self.take_inbound(r, frame, frame + timedelta(days=d), atts)
            inbound.clear()
        # load order: the bank's centre loads as it calls; the contractor's records arrive the next working morning
        for c in self.calls:
            if c["team"] == "BCB":
                c["loaded"] = c["start"] + timedelta(seconds=c["dur"] + 2)
            else:
                nd = add_working_days(W.utc_to_local(c["start"]).date(), 1)
                c["loaded"] = local_dt(nd, 6 * 3600 + 5 * 60) + timedelta(seconds=c["seq"] * 0.01)
        replay = [dict(c) for c in self.calls if c["team"] == "OVF" and W.utc_to_local(c["start"]).date() == REPLAY_DAY]
        base = local_dt(REPLAY_LOAD[0], REPLAY_LOAD[1] * 3600 + REPLAY_LOAD[2] * 60)
        for i, c in enumerate(sorted(replay, key=lambda x: (x["start"], x["seq"]))):
            c["loaded"] = base + timedelta(seconds=i * 0.01)
            c["replay"] = True
        self.calls.extend(replay)
        self.calls.sort(key=lambda c: (c["loaded"], c["seq"], c.get("replay", False)))
        for i, c in enumerate(self.calls):
            c["call_id"] = 40211507 + i
        self.replay_n = len(replay)

    AGENTS = {"BCB": ["CC1%02d" % i for i in range(1, 29)], "OVF": ["OV-%02d" % i for i in (3, 4, 5, 7, 8, 9, 11, 12, 14, 15, 16, 19)]}
    BCB_BEFORE_2024 = 16                # the bank's centre took on twelve more agents when the panel doubled
    SUPERVISORS = ["OV-S1", "OV-S2"]
    DUR = {"NOAN": (24, 41), "VMSG": (32, 66), "BUSY": (4, 11), "UNOB": (7, 16), "STAF": (45, 140), "PROM": (85, 250),
           "REFU": (60, 200), "CEAS": (40, 130), "COMP": (560, 1260), "XFER": (35, 110)}

    def _passes(self, first, later):
        """first attempts in their drawn order, then the same-day retries in the order their first attempts ended"""
        for a in first:
            yield a
        for a in sorted(later, key=lambda a: (a["after"]["end_s"], self.pid[a["f"]["fid"]])):
            yield a

    def schedule(self, r, frame, day, team, atts, close):
        """lay a day's attempts onto the team's agents without overlaps, inside calling hours"""
        agents = list(self.AGENTS[team])
        if team == "BCB" and frame < P.EXPANSION_ROUND:
            agents = agents[:self.BCB_BEFORE_2024]
        n_on = len(agents) - int(r.integers(0, 4))
        agents = sorted(r.choice(agents, size=n_on, replace=False).tolist())
        open_s = 8 * 3600 + 30 * 60 if team == "BCB" else 9 * 3600
        last_start = 16 * 3600 + 25 * 60
        heap = [(open_s + int(r.integers(0, 600)), a) for a in agents]
        heapq.heapify(heap)
        first = [a for a in atts if a["after"] is None]
        later = [a for a in atts if a["after"] is not None]
        order = [first[int(i)] for i in r.permutation(len(first))]
        sup_free = {s: open_s for s in self.SUPERVISORS}
        close_end = 17 * 3600 if day == close else 24 * 3600
        for a in self._passes(order, later):
            if a["after"] is not None:
                ready = a["after"]["end_s"] + int(r.integers(5400, 10800))
                t0, agent = heapq.heappop(heap)
                t = max(t0, ready)
                if t > last_start:
                    heapq.heappush(heap, (t0, agent))
                    continue
            else:
                t, agent = heapq.heappop(heap)
            assert t <= last_start, ("calling hours exceeded", team, day)
            code = a["code"]
            lo, hi = self.DUR[code]
            dur = int(r.integers(lo, hi + 1))
            rec = dict(team=team, f=a["f"], o=a["o"], frame=frame, agent=agent, start=local_dt(day, t), dur=dur, code=code,
                       seq=len(self.calls))
            xfer = team == "OVF" and code in ("PROM", "REFU", "COMP") and r.random() < 0.06
            if xfer:
                lo2, hi2 = self.DUR["XFER"]
                d1 = int(r.integers(lo2, hi2 + 1))
                rec["code"], rec["dur"] = "XFER", d1
                self.calls.append(rec)
                sup = min(self.SUPERVISORS, key=lambda s_: (sup_free[s_], s_))
                t2 = max(t + d1 + int(r.integers(3, 25)), sup_free[sup])
                rec2 = dict(rec, agent=sup, start=local_dt(day, t2), dur=dur, code=code, seq=len(self.calls))
                self.calls.append(rec2)
                sup_free[sup] = t2 + dur + int(r.integers(20, 60))
                end, free_at = t2 + dur, t + d1
            else:
                self.calls.append(rec)
                end = free_at = t + dur
            assert end < close_end, ("call runs past the close", team, day)
            a["end_s"] = end
            if code == "COMP" and a["final"]:
                self.phone_end[(a["f"]["fid"], frame)] = local_dt(day, end)
            heapq.heappush(heap, (free_at + int(r.integers(15, 76)) + int(r.integers(0, 61)), agent))

    INBOUND_DESK = ["CC141", "CC142", "CC143", "CC144"]

    def take_inbound(self, r, frame, day, atts):
        """calls from firms ringing back, answered at the bank's inbound desk (08:30 to 17:30) after the outbound
        attempt that left the message"""
        free = {a: 8 * 3600 + 30 * 60 for a in self.INBOUND_DESK}
        for a in sorted(atts, key=lambda a: (a["after"]["end_s"], self.pid[a["f"]["fid"]])):
            ready = a["after"]["end_s"] + int(r.integers(600, 5400))
            lo, hi = self.DUR[a["code"]]
            dur = int(r.integers(lo, hi + 1))
            agent = min(self.INBOUND_DESK, key=lambda x: (max(free[x], ready), x))
            t = max(free[agent], ready)
            if t + dur > 17 * 3600 + 25 * 60:
                t = max(free[agent], a["after"]["end_s"] + 300)
            assert t + dur <= 17 * 3600 + 29 * 60, ("inbound desk overrun", day)
            rec = dict(team="BCB", f=a["f"], o=a["o"], frame=frame, agent=agent, start=local_dt(day, t), dur=dur,
                       code=a["code"], seq=len(self.calls), inbound=True)
            self.calls.append(rec)
            free[agent] = t + dur + int(r.integers(20, 90))
            if a["code"] == "COMP":
                self.phone_end[(a["f"]["fid"], frame)] = local_dt(day, t + dur)

    # ----------------------------------------------------------------------------------------------- returns
    def build_returns(self):
        """Return timestamps (UTC) for every simulated return, in the round's outcomes and in September's receipts."""
        r = rng("returns")
        rp = rng("phone")
        self.ret = {}
        for o in self.pan.outcomes:
            if o["ret_day"] is None:
                continue
            frame, close = o["frame"], o["close"]
            d = frame + timedelta(days=o["ret_day"])
            mode = o["mode"]
            if mode == "phone":
                end = self.phone_end.get((o["fid"], frame))
                if end is None:
                    end = local_dt(d, int(rp.integers(9 * 3600 + 40 * 60, 16 * 3600 + 50 * 60)))
                reach = end
            elif mode == "post":
                d = next_monday(d)
                if r.random() < 0.62:
                    s = int(r.integers(8 * 3600 + 50 * 60, 11 * 3600 + 20 * 60))
                else:
                    s = int(r.integers(13 * 3600 + 20 * 60, 15 * 3600 + 40 * 60))
                reach = local_dt(d, s)
            else:
                if closed_day(d) and r.random() < (0.75 if d.weekday() >= 5 else 0.85):
                    d = next_monday(d)
                u = r.random()
                if d == close:
                    s = int(r.integers(7 * 3600 + 30 * 60, 16 * 3600 + 55 * 60))
                elif u < 0.88:
                    s = int(r.integers(7 * 3600 + 30 * 60, 17 * 3600 + 30 * 60))
                else:
                    s = int(r.integers(17 * 3600 + 30 * 60, 22 * 3600 + 50 * 60))
                reach = local_dt(d, s)
            loaded = reach
            if mode == "phone" and frame >= date(2024, 3, 1) and reach.date() >= TRANSFER_FROM:
                nd = W.utc_to_local(reach).date() + timedelta(days=1)
                loaded = local_dt(nd, 2 * 3600 + 30 * 60 + int(rp.integers(4, 900)))
            keyed = loaded
            if mode == "post" and W.utc_to_local(reach).date() >= BUREAU_FROM:
                kd = add_working_days(W.utc_to_local(reach).date(), int(r.integers(1, 7)))
                keyed = local_dt(kd, int(r.integers(9 * 3600, 16 * 3600 + 30 * 60)))
            self.ret[id(o)] = dict(mode=mode, reach=reach, received=loaded, recorded=keyed)
        # firms that returned on paper as well as on the web before the close of the September round
        rd = rng("dups")
        cur = [o for o in self.pan.outcomes if o["frame"] == P.CURRENT and o["ret_day"] is not None and o["mode"] == "web"]
        cur.sort(key=lambda o: self.pid[o["fid"]])
        close = W.close_utc(P.MAIN_CLOSE)
        self.sep_dups = []
        for o in cur:
            x = self.ret[id(o)]
            if x["reach"] + timedelta(days=7) < close and rd.random() < 0.0055:
                d = add_working_days(W.utc_to_local(x["reach"]).date(), int(rd.integers(2, 5)))
                t = local_dt(d, int(rd.integers(8 * 3600 + 50 * 60, 11 * 3600 + 20 * 60)))
                if t < close:
                    self.sep_dups.append((o, t))

    # ----------------------------------------------------------------------------------------------- tables
    def region_code(self, region, frame):
        return region if frame >= date(2023, 6, 1) else W.OLD_CODE[region]

    def panel_register(self):
        rows = []
        for f in sorted(self.everyone, key=lambda x: (x["panel_id"], x["consent"])):
            left = f["left"]
            if left is not None and left >= P.CURRENT:
                left, reason = None, ""
            else:
                reason = f["left_reason"]
            rows.append([f["panel_id"], f["company_number"], f["region"], f["nace"], W.SIZE_NAME[f["size"]],
                         f["consent"].isoformat(), wave_label(f), left.isoformat() if left else "", reason])
        return ["panel_id", "company_number", "region", "nace_section", "size_band", "recruited", "recruitment_wave",
                "left_panel", "left_reason"], rows

    def outcomes(self):
        rows = []
        for o in self.pan.outcomes:
            if o["frame"] >= P.CURRENT:
                continue
            f = self.firms[o["fid"]]
            x = self.ret.get(id(o))
            row = [W.round_quarter(o["frame"]), self.pid[o["fid"]], self.region_code(f["region"], o["frame"])]
            if x:
                row += [x["mode"], W.iso(x["received"]), W.iso(x["recorded"])]
            else:
                row += ["", "", ""]
            rows.append((o["frame"], self.pid[o["fid"]], row))
        rows.sort(key=lambda t: (t[0], t[1]))
        return ["round", "panel_id", "region", "mode", "received_at", "recorded_at"], [t[2] for t in rows]

    def invitations(self):
        rows = []
        r = rng("channel")
        for o in self.pan.outcomes:
            if o["frame"] != P.CURRENT:
                continue
            f = self.firms[o["fid"]]
            ch = "post" if r.random() < 0.09 else "email"
            rows.append([self.pid[o["fid"]], f["company_number"], f["region"], W.NAME[f["region"]], f["nace"],
                         W.SIZE_NAME[f["size"]], P.CURRENT.isoformat(), ch])
        rows.sort(key=lambda x: x[0])
        return ["panel_id", "company_number", "region", "region_name", "nace_section", "size_band", "invited_on",
                "invitation_channel"], rows

    def returns_sep(self):
        recs = []
        for o in self.pan.outcomes:
            if o["frame"] != P.CURRENT or o["ret_day"] is None:
                continue
            x = self.ret[id(o)]
            recs.append((x["reach"], self.pid[o["fid"]], x["mode"]))
        for o, t in self.sep_dups:
            recs.append((t, self.pid[o["fid"]], "post"))
        recs.sort(key=lambda t: (t[0], t[1]))
        rows = [["26Q3-%05d" % (i + 1), pid, mode, W.iso(t)] for i, (t, pid, mode) in enumerate(recs)]
        return ["receipt_no", "panel_id", "mode", "received_at"], rows

    def closures(self):
        rows = []
        for f in self.firms:
            if f["registered"] > P.EXTRACT:
                continue
            ceased = f["ceased"]
            if ceased in FRAME_SET:
                ceased -= timedelta(days=1)
            route = {"voluntary": "voluntary dissolution", "administrative": "administrative strike-off",
                     "insolvency": "liquidation"}[f["route"]]
            rows.append((f["registered"], f["core"], [f["company_number"], ceased.isoformat(), f["registered"].isoformat(), route]))
        rows.sort(key=lambda t: (t[0], t[1]))
        return ["company_number", "ceased_trading", "registered", "procedure"], [t[2] for t in rows]

    OVERFLOW_CODE = {"COMP": "10", "PROM": "21", "REFU": "23", "STAF": "31", "NOAN": "41", "VMSG": "42", "BUSY": "43",
                     "UNOB": "51", "CEAS": "61", "XFER": "71"}

    def calls_table(self):
        rows = []
        for c in self.calls:
            f = c["f"]
            if c["team"] == "BCB":
                pid, num, reg, code = self.pid[f["fid"]], "", "", c["code"]
            else:
                listed_before = f["consent"] < W.NUMBER_CHANGE
                pid, num = "", (W.old_number(f["core"]) if listed_before else f["company_number"])
                reg, code = W.OLD_CODE[f["region"]], self.OVERFLOW_CODE[c["code"]]
            rows.append([c["call_id"], W.round_code(c["frame"]), c["team"], "in" if c.get("inbound") else "out", pid, num, reg,
                         c["agent"], W.iso(c["start"]), c["dur"], code])
        return ["call_id", "round", "team", "direction", "panel_id", "company_number", "region", "agent", "started_at",
                "duration_s", "outcome"], rows
