"""Simulate Kelderby's E gates: the carriers' summer 2026 lines of flying (the season schedule), each day's operation
along every aircraft's rotation (a late departure from Kelderby comes back as a late arrival), each turn's need, the
holds that are not the turn's, delay codes, stand allocation and tows; and the summer 2027 initial submissions
(the lines again at the filed ground times, codeshare duplicates, through flights, night stops and the CRJ900 lines
the fleet plan hands to E175s). Everything downstream reads `everything()`."""
import datetime as dt

import numpy as np

import world as W

Z80 = 0.8416


def _rng(*k):
    return np.random.default_rng([W.SEED] + list(k))


def r5(m):
    return int(5 * round(m / 5.0))


# ---------------------------------------------------------------- the season schedule (lines of flying)
LO = {("PMV", "NV"): 3000, ("GYA", "NV"): 3800, ("SBC", "NV"): 3500, ("PMV", "TQ"): 5100, ("SBC", "TQ"): 5300,
      ("GYA", "GY"): 200}


def lines():
    """Each aircraft line of flying: segment, line number, based at Kelderby or not, days it flies, and its legs as
    scheduled in minutes after Kelderby midnight (local), with flight numbers, stations and 2026 ground times. One
    turn on most lines is a through flight: the inbound's flight number carries on to the next station."""
    rng = _rng(1)
    out = []
    used = set()
    st_i = 0
    for seg in W.ORDER:
        s = W.SEGMENTS[seg]
        nxt = [LO[(s["op"], s["brand"])]]

        def num():
            while nxt[0] in used:
                nxt[0] += 1
            used.add(nxt[0])
            return nxt[0]
        for ln in range(s["lines"]):
            based = ln < s["based"]
            trips = s["trips"] - (1 if (not based and ln % 2) else 0)
            start = (6 * 60 + 10 + 25 * ln) if based else (7 * 60 + 35 + 20 * ln)
            start = r5(start + int(rng.integers(-2, 3)) * 5)
            legs = []
            t = start
            for k in range(trips):
                code, name, block, tz = W.STATIONS[st_i % len(W.STATIONS)]
                st_i += 3
                turn_out = 30 if s["type"] == "E75" else 25
                if k > 0 and t + 2 * block + turn_out > 22 * 60 + 50:
                    break
                if not based and k == 0:
                    arr = t
                    legs.append(dict(out_num=None, back_num=num(), station=code, block=block, tz=tz, std=None,
                                     sta_out=None, std_out=arr - block, sta=arr, turn_out=turn_out))
                    t = arr + W.ground_2026(seg, arr // 60)
                    continue
                dep = t
                arr_out = dep + block
                dep_back = arr_out + turn_out
                arr = dep_back + block
                legs.append(dict(out_num=num(), back_num=num(), station=code, block=block, tz=tz, std=dep,
                                 sta_out=arr_out, std_out=dep_back, sta=arr, turn_out=turn_out))
                t = arr + W.ground_2026(seg, arr // 60)
            if not based:
                code, name, block, tz = W.STATIONS[st_i % len(W.STATIONS)]
                st_i += 3
                legs.append(dict(out_num=num(), back_num=None, station=code, block=block, tz=tz, std=t,
                                 sta_out=t + block, std_out=None, sta=None, turn_out=None))
            # one through flight per line: the inbound on the line's second turn carries on outbound
            arrs = [i for i, lg in enumerate(legs) if lg["sta"] is not None]
            deps_after = [i for i in arrs if i + 1 < len(legs) and legs[i + 1]["std"] is not None]
            if len(deps_after) >= 2 and ln % 4 != 3:
                j = deps_after[1]
                used.discard(legs[j + 1]["out_num"])
                legs[j + 1]["out_num"] = legs[j]["back_num"]
                legs[j]["through"] = True
            dow = "12345 7" if (seg == "S1" and ln == 7) else "1234567"
            out.append(dict(seg=seg, line=ln, based=based, legs=legs, dow=dow))
    return out


def kdy_events(line):
    ev = []
    for lg in line["legs"]:
        if lg["std"] is not None:
            ev.append(("DEP", lg))
        if lg["sta"] is not None:
            ev.append(("ARR", lg))
    ev.sort(key=lambda e: e[1]["std"] if e[0] == "DEP" else e[1]["sta"])
    return ev


def retimed(line):
    return line["line"] % 3 == 1


def shift(line, d):
    return 5 if (retimed(line) and d >= W.RETIME_FROM) else 0


def flies(line, d):
    return line["dow"][d.isoweekday() - 1] != " "


# ---------------------------------------------------------------- the aircraft
def registrations():
    rng = _rng(2)
    regs = {}
    pref = {"PMV": "C-GP", "SBC": "C-FS", "GYA": "C-GG"}
    taken = set()
    for ln in lines():
        while True:
            r = pref[W.SEGMENTS[ln["seg"]]["op"]] + "".join(rng.choice(list("ABCDEFGHJKLMNPRSTUVWXYZ"), 2))
            if r not in taken:
                break
        taken.add(r)
        regs[(ln["seg"], ln["line"])] = r
    return regs


def day_reg(regs, line, d):
    """The aircraft on a line that day: the aircraft that night-stop at Kelderby take the based lines in turn, one line
    further each day; an aircraft on a line that ends away from Kelderby keeps that line."""
    s = W.SEGMENTS[line["seg"]]
    if not line["based"]:
        return regs[(line["seg"], line["line"])]
    k = (d - W.EXPORT_FROM).days
    return regs[(line["seg"], (line["line"] + k) % s["based"])]


# ---------------------------------------------------------------- one season of operation
def storm_days():
    rng = _rng(3)
    return {d: bool(rng.random() < 0.22) for d in W.days()}


def operate():
    """Run every line on every day of the export. Returns the Kelderby movements (one row per arrival and
    departure) and the turns (an arrival and the same aircraft's next departure the same day)."""
    rng = _rng(4)
    L = lines()
    regs = registrations()
    storms = storm_days()
    rows, turns = [], []
    for d in W.days():
        storm = storms[d]
        for ln in L:
            if not flies(ln, d):
                continue
            seg = ln["seg"]
            s = W.SEGMENTS[seg]
            sd = np.log(s["p80"] / s["med"]) / Z80
            reg = day_reg(regs, ln, d)
            sh = shift(ln, d)
            delay = 0.0
            pend = None
            for kind, lg in kdy_events(ln):
                if kind == "ARR":
                    sta = lg["sta"] + sh
                    hour = sta // 60
                    if lg["std"] is None and lg is ln["legs"][0]:
                        dep_o = -7.0 + (max(0.0, rng.normal(0, 4)) if rng.random() < 0.25 else 0.0)
                    else:
                        arr_o = delay + rng.normal(-3, 6)
                        n_o = np.exp(np.log(lg["turn_out"] - 6) + 0.16 * rng.standard_normal())
                        dep_o = max(0.0, arr_o + n_o - lg["turn_out"])
                    p_o = 0.08 + 0.016 * max(0, hour - 9) + (0.30 if storm and hour >= 13 else 0)
                    hold_o = rng.gamma(1.4, 10 + (15 if storm else 0)) if rng.random() < p_o else 0.0
                    D = max(dep_o + hold_o + rng.normal(-6 if hour < 11 else -4, 5), -15.0)
                    aibt = float(sta + D)
                    pend = dict(flight=lg["back_num"], sta=sta, aibt=aibt, D=D, through=lg.get("through", False))
                    rows.append(dict(kind="ARR", day=d, seg=seg, line=ln["line"], reg=reg, flight=lg["back_num"],
                                     station=lg["station"], sched=sta, actual=aibt, tz=lg["tz"], block=lg["block"],
                                     sched_other=(lg["std_out"] + sh) if lg["std_out"] is not None else None))
                    continue
                std = lg["std"] + sh
                hour = std // 60
                p_hold = s["hold"] + 0.006 * max(0, hour - 9) + (0.30 if storm and hour >= 14 else 0)
                H = float(rng.gamma(1.3, 7 + (10 if storm else 0))) if rng.random() < p_hold else 0.0
                if pend is None:
                    ready_late = float(rng.gamma(1.5, 4)) if rng.random() < 0.06 else 0.0
                    aobt = std + ready_late + H
                    rows.append(dict(kind="DEP", day=d, seg=seg, line=ln["line"], reg=reg, flight=lg["out_num"],
                                     station=lg["station"], sched=std, actual=aobt, tz=lg["tz"], block=lg["block"],
                                     turn_min=ready_late, hold_min=H, first=True, late_in=0.0,
                                     sched_other=lg["sta_out"] + sh))
                    delay = aobt - std
                    continue
                N = float(np.exp(np.log(s["med"]) + sd * rng.standard_normal()))
                B = std - pend["aibt"]
                turn_min = max(0.0, N - B)
                early = 0.0
                if turn_min == 0 and H == 0 and B - N > 6 and rng.random() < 0.03:
                    early = float(rng.integers(1, 4))
                aobt = max(std, pend["aibt"] + N) + H - early
                rows.append(dict(kind="DEP", day=d, seg=seg, line=ln["line"], reg=reg, flight=lg["out_num"],
                                 station=lg["station"], sched=std, actual=aobt, tz=lg["tz"], block=lg["block"],
                                 turn_min=turn_min, hold_min=H, first=False, late_in=pend["D"],
                                 sched_other=lg["sta_out"] + sh))
                turns.append(dict(day=d, seg=seg, line=ln["line"], reg=reg, arr_flight=pend["flight"],
                                  dep_flight=lg["out_num"], sta=pend["sta"], aibt=pend["aibt"], std=std, aobt=aobt,
                                  N=N, B=B, S=std - pend["sta"], turn_min=turn_min, hold_min=H, early=early,
                                  D=pend["D"], storm=storm, through=pend["through"]))
                pend = None
                delay = aobt - std
    return rows, turns


# ---------------------------------------------------------------- stands and tows
def allocate(rows, turns):
    """Give every movement its stand. A visit (arrival to the same aircraft's next departure, or the night) takes
    the lowest-numbered E stand free for ten minutes, else a remote stand; about one turn in sixteen with fifty
    minutes or more scheduled on the ground is towed to a remote stand and leaves from there. Returns the tows."""
    rng = _rng(5)
    tow_turns = set()
    for t in turns:
        if t["S"] >= 50 and rng.random() < 0.06:
            tow_turns.add((t["day"], t["reg"], round(t["aibt"], 3)))
    by_day = {}
    for r in rows:
        by_day.setdefault(r["day"], []).append(r)
    tows = []
    # the aircraft that night-stopped at Kelderby before the export's first day, on the E stands in order
    first = sorted((r for r in by_day[min(by_day)] if r["kind"] == "DEP" and r["first"]), key=lambda r: r["actual"])
    overnight = {r["reg"]: W.STANDS_E[i] for i, r in enumerate(first)}
    for d in sorted(by_day):
        free_at = {s: -1e9 for s in W.STANDS_E + W.STANDS_R}
        on = {}
        for reg, st in overnight.items():
            on[reg] = st
            free_at[st] = 1e9
        overnight = {}
        pending = []
        for r in sorted(by_day[d], key=lambda r: (r["actual"], 0 if r["kind"] == "DEP" else 1)):
            while pending and pending[0][0] <= r["actual"]:
                tt, reg, st_from = pending.pop(0)
                if on.get(reg) != st_from:
                    continue
                st_to = next(s for s in W.STANDS_R if free_at[s] <= tt - 10)
                free_at[st_from] = tt
                free_at[st_to] = 1e9
                on[reg] = st_to
                tows.append(dict(kind="TOW-OFF", day=d, reg=reg, stand=st_from, actual=tt))
                tows.append(dict(kind="TOW-ON", day=d, reg=reg, stand=st_to, actual=tt + 6))
            if r["kind"] == "ARR":
                t = r["actual"]
                cand = [s for s in W.STANDS_E if free_at[s] <= t - 10]
                st = cand[0] if cand else next(s for s in W.STANDS_R if free_at[s] <= t - 10)
                r["stand"] = st
                free_at[st] = 1e9
                on[r["reg"]] = st
                if (d, r["reg"], round(t, 3)) in tow_turns and st.startswith("E"):
                    pending.append((t + 12 + float(rng.integers(0, 6)), r["reg"], st))
                    pending.sort()
            else:
                st = on.pop(r["reg"], None)
                if st is None:
                    st = next(s for s in W.STANDS_R if free_at[s] <= r["actual"] - 10)
                r["stand"] = st
                free_at[st] = r["actual"]
        for reg, st in on.items():
            overnight[reg] = st
    return tows


# ---------------------------------------------------------------- summer 2027 initial submissions
def lines27():
    """The 2027 lines: the 2026 lines at the ground times the carriers filed, with a few turns scheduled shorter than
    the carrier's own filing (the inconsistency Ask A's second figure counts) and some five minutes longer."""
    rng = _rng(6)
    out = []
    short = {"S1": (30, 0.12), "S2": (35, 0.0), "S3": (25, 0.06), "S4": (35, 0.10), "S5": (25, 0.0), "S6": (25, 0.15)}
    for ln in lines():
        seg = ln["seg"]
        g = W.SEGMENTS[seg]["filed"]
        t_shift = 0
        new = []
        prev_arr = None
        for lg in ln["legs"]:
            lg = dict(lg)
            if lg["std"] is not None and prev_arr is not None:
                gs, p = short[seg]
                gt = gs if rng.random() < p else g + (5 if rng.random() < 0.25 else 0)
                t_shift = prev_arr + gt - lg["std"]
            for k in ("std", "sta_out", "std_out", "sta"):
                if lg.get(k) is not None:
                    lg[k] = lg[k] + t_shift
            if lg["sta"] is not None:
                prev_arr = lg["sta"]
            new.append(lg)
        out.append(dict(ln, legs=new))
    return out


def everything():
    rows, turns = operate()
    tows = allocate(rows, turns)
    return dict(lines=lines(), regs=registrations(), rows=rows, turns=turns, tows=tows, lines27=lines27(),
                storms=storm_days())
