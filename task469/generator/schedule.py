"""The lines of flying as SSIM flight legs: the authority's coordinated summer 2026 season schedule (operating flights,
periods split at the 3 August retimings) and the merged summer 2027 initial submissions as each brand sent them (its own
operating flights at the ground times it filed, the new lines Tellura adds, and the legs it sells on a partner's flights
under its own numbers, each tied to the operating flight by a DEI 050 segment data record; Grayling's file in UTC).
Also the ground truth of the schedule ask, read off the operating lines."""
import datetime as dt

import numpy as np

import sim as S
import world as W

S26 = (dt.date(2026, 3, 29), dt.date(2026, 10, 24))
S27 = W.SEASON27
UTC_CARRIERS = {"TQ", "GY"}

# summer 2027: lines added; the ground time each relationship schedules at its through stops (passengers continuing
# on the same flight number stay on board), shorter than its filed minimum
GROWTH = {"S4": 1, "S5": 1}
THROUGH27 = {"S1": 30, "S2": 30, "S3": 25, "S4": 30, "S5": 25, "S6": 25}
# which lines a partner brand sells under its own numbers (operating line -> marketing brand)
DUPLICATED = {"S1": ("TQ", {0, 2, 4, 6}), "S4": ("NV", {0, 1, 2}), "S3": ("TQ", {0, 3, 5}), "S5": ("NV", {0, 1, 2}),
              "S6": ("NV", {0, 1}), "S2": ("GY", {0, 1, 2})}
# where each brand numbers the legs it sells on a partner's flights: inside its own block for the same operator
DUP_LO = {("TQ", "PMV"): 5200, ("NV", "PMV"): 3200, ("TQ", "SBC"): 5350, ("NV", "SBC"): 3700, ("NV", "GYA"): 3870,
          ("GY", "GYA"): 300}
# the same minute to the same station from two relationships' aircraft (two aircraft, two turns)
TWINS = [(("S1", 1), ("S4", 0)), (("S3", 1), ("S5", 0))]


def _rng(*k):
    return np.random.default_rng([W.SEED, 27] + list(k))


# ---------------------------------------------------------------- SSIM legs of a line
def legs_of(line, eqp, periods, airline=None, renumber=None):
    """SSIM legs for one line: for each period (from, to, minutes added), a leg record per flight leg, in Kelderby local
    minutes (kdy_dep, kdy_arr: the Kelderby clock of each end) with station-local times for the record."""
    s = W.SEGMENTS[line["seg"]]
    al = airline or s["brand"]
    num = renumber or (lambda n: n)
    L = line["legs"]
    out = []
    for frm, to, sh in periods:
        first_dep = next((lg for lg in L if lg["std"] is not None), None)
        first_arr = L[0] if L[0]["std"] is None else None
        for i, lg in enumerate(L):
            nxt = L[i + 1] if i + 1 < len(L) else None
            if lg["std"] is not None:
                through_in = i > 0 and L[i - 1].get("through") and L[i - 1]["back_num"] == lg["out_num"]
                if lg["back_num"] is not None:
                    onward = (al, num(lg["back_num"]), 0)
                else:
                    onward = (al, num(first_arr["back_num"]), 1) if first_arr else None
                out.append(dict(airline=al, flight=num(lg["out_num"]), leg=2 if through_in else 1, frm=frm, to=to,
                                dow=line["dow"], dep=W.KDY, arr=lg["station"], dep_tz=0, arr_tz=lg["tz"],
                                kdy_dep=lg["std"] + sh, kdy_arr=lg["sta_out"] + sh, eqp=eqp, onward=onward,
                                seg=line["seg"], line=line["line"], op_flight=lg["out_num"], kind="DEP"))
            if lg["sta"] is not None:
                if lg.get("through"):
                    onward = None
                elif nxt is not None and nxt["std"] is not None:
                    onward = (al, num(nxt["out_num"]), 0)
                else:
                    onward = (al, num(first_dep["out_num"]), 1) if first_dep else None
                out.append(dict(airline=al, flight=num(lg["back_num"]), leg=1, frm=frm, to=to, dow=line["dow"],
                                dep=lg["station"], arr=W.KDY, dep_tz=lg["tz"], arr_tz=0,
                                kdy_dep=lg["std_out"] + sh, kdy_arr=lg["sta"] + sh, eqp=eqp, onward=onward,
                                seg=line["seg"], line=line["line"], op_flight=lg["back_num"], kind="ARR"))
    return out


def to_record(leg, utc=False):
    """Clock fields of a leg for its record: local times at each end with the day variation of the arrival, or UTC
    with the period and days of operation moved to the UTC date of departure."""
    if not utc:
        dep = leg["kdy_dep"] - 60 * leg["dep_tz"]
        arr = leg["kdy_arr"] - 60 * leg["arr_tz"]
        d0 = dep // 1440
        return dict(leg, std=dep % 1440, sta=arr % 1440, dep_var=W.UTC_OFF - leg["dep_tz"],
                    arr_var=W.UTC_OFF - leg["arr_tz"], arr_dayvar=arr // 1440 - d0, day_shift=d0)
    dep = leg["kdy_dep"] - 60 * W.UTC_OFF
    arr = leg["kdy_arr"] - 60 * W.UTC_OFF
    d0 = dep // 1440
    return dict(leg, std=dep % 1440, sta=arr % 1440, dep_var=0, arr_var=0, arr_dayvar=arr // 1440 - d0, day_shift=d0)


def shift_days(dow, k):
    """Days of operation moved k days later (a leg leaving after midnight UTC flies the next UTC day)."""
    days = [i for i, c in enumerate(dow) if c != " "]
    out = [" "] * 7
    for i in days:
        j = (i + k) % 7
        out[j] = str(j + 1)
    return "".join(out)


def finish(legs, utc=False):
    """Records ready for the writer: clock fields, the UTC day shift on period and days, the rotation layover of each
    onward link counted on the file's own clock."""
    recs = [to_record(lg, utc) for lg in legs]
    by_key = {}
    for r in recs:
        by_key.setdefault((r["airline"], r["flight"], r["frm"]), []).append(r)
    for r in recs:
        if r["day_shift"]:
            r["frm"] = r["frm"] + dt.timedelta(days=r["day_shift"])
            r["to"] = r["to"] + dt.timedelta(days=r["day_shift"])
            r["dow"] = shift_days(r["dow"], r["day_shift"])
    for r in recs:
        if not r["onward"]:
            continue
        oa, of, lay = r["onward"]
        nxt = [x for x in recs if x["airline"] == oa and x["flight"] == of and x["dep"] == r["arr"]
               and x["line"] == r["line"] and x["seg"] == r["seg"]]
        if not nxt:
            continue
        x = nxt[0]
        arr_day = r["day_shift"] + r["arr_dayvar"]
        r["onward"] = (oa, of, lay + x["day_shift"] - arr_day)
    return recs


# ---------------------------------------------------------------- summer 2026
def season26():
    legs = {"NV": [], "TQ": [], "GY": []}
    for ln in S.lines():
        s = W.SEGMENTS[ln["seg"]]
        if S.retimed(ln):
            periods = [(S26[0], W.RETIME_FROM - dt.timedelta(days=1), 0), (W.RETIME_FROM, S26[1], 5)]
        else:
            periods = [(S26[0], S26[1], 0)]
        legs[s["brand"]] += legs_of(ln, s["type"], periods)
    out = {}
    for k in legs:
        out[k] = sorted(finish(legs[k]), key=lambda x: (x["flight"], x["leg"], x["frm"]))
    return out


# ---------------------------------------------------------------- summer 2027
def _copy(ln):
    return dict(ln, legs=[dict(lg) for lg in ln["legs"]])


def _new_line(template, line_no, start_shift, st_shift, used):
    """A line added for 2027: the template line's pattern later in the day to other stations, with new numbers."""
    s = W.SEGMENTS[template["seg"]]
    ln = _copy(template)
    ln["line"] = line_no
    lo = S.LO[(s["op"], s["brand"])]
    n = [lo]

    def num():
        while n[0] in used:
            n[0] += 1
        used.add(n[0])
        return n[0]
    codes = [c for c, nm, b, z in W.STATIONS]
    for lg in ln["legs"]:
        code, name, block, tz = W.STATIONS[(codes.index(lg["station"]) + st_shift) % len(codes)]
        d_block = block - lg["block"]
        lg.update(station=code, tz=tz, block=block)
        for k in ("std", "sta_out", "std_out", "sta"):
            if lg.get(k) is not None:
                lg[k] += start_shift
        if lg["std"] is None:
            lg["std_out"] = lg["sta"] - block
            continue
        lg["sta_out"] += d_block
        if lg["std_out"] is not None:
            lg["std_out"] += d_block
            lg["sta"] += 2 * d_block
        lg["out_num"] = None if lg["out_num"] is None else -1
        lg["back_num"] = None if lg["back_num"] is None else -1
    for i, lg in enumerate(ln["legs"]):
        if lg["out_num"] == -1:
            if i > 0 and ln["legs"][i - 1].get("through"):
                lg["out_num"] = ln["legs"][i - 1]["back_num"]
            else:
                lg["out_num"] = num()
        if lg["back_num"] == -1:
            lg["back_num"] = num()
    return ln


def _retime(ln, rng):
    """Re-time a line on its 2027 ground times: each turn at the filed minimum (five minutes more on about one turn in
    four), the through stop at the carrier's shorter through time; legs away from Kelderby keep their blocks and
    outstation turns."""
    seg = ln["seg"]
    g = W.SEGMENTS[seg]["filed"]
    shift = 0
    prev, prev_through = None, False
    for lg in ln["legs"]:
        if lg["std"] is not None and prev is not None:
            u = rng.random()
            gt = THROUGH27[seg] if prev_through else g + (5 if u < 0.25 else 0)
            shift = prev + gt - lg["std"]
        for k in ("std", "sta_out", "std_out", "sta"):
            if lg.get(k) is not None:
                lg[k] += shift
        if lg["sta"] is not None:
            prev, prev_through = lg["sta"], bool(lg.get("through"))
    return ln


def _align(a, b):
    """Move line b so that its first trip leaves at the same minute as line a's for the same station and returns at the
    same minute; the rest of b follows on b's own ground times."""
    fa = next(lg for lg in a["legs"] if lg["std"] is not None)
    ib = next(i for i, lg in enumerate(b["legs"]) if lg["std"] is not None)
    fb = b["legs"][ib]
    gts = []
    for i in range(ib + 1, len(b["legs"])):
        if b["legs"][i]["std"] is not None and b["legs"][i - 1]["sta"] is not None:
            gts.append(b["legs"][i]["std"] - b["legs"][i - 1]["sta"])
    fb.update(station=fa["station"], block=fa["block"], tz=fa["tz"], std=fa["std"], sta_out=fa["sta_out"],
              std_out=fa["std_out"], sta=fa["sta"])
    prev = fb["sta"]
    k = 0
    for i in range(ib + 1, len(b["legs"])):
        lg = b["legs"][i]
        if lg["std"] is None:
            continue
        d = prev + gts[k] - lg["std"]
        k += 1
        for key in ("std", "sta_out", "std_out", "sta"):
            if lg.get(key) is not None:
                lg[key] += d
        prev = lg["sta"] if lg["sta"] is not None else prev
    return b


def lines27():
    """The 2027 operating lines: the 2026 lines and their numbers, Tellura's two added lines, every line re-timed on
    its relationship's filing, and the two same-minute pairs."""
    base = [_copy(ln) for ln in S.lines()]
    used = {lg[k] for ln in base for lg in ln["legs"] for k in ("out_num", "back_num") if lg.get(k) is not None}
    for seg, k in GROWTH.items():
        mine = [ln for ln in base if ln["seg"] == seg]
        for j in range(k):
            t = mine[(1 + j) % len(mine)]
            base.append(_new_line(t, len(mine) + j, 40, 5, used))
    base.sort(key=lambda ln: (W.ORDER.index(ln["seg"]), ln["line"]))
    out = []
    for ln in base:
        out.append(_retime(ln, _rng(W.ORDER.index(ln["seg"]), ln["line"])))
    idx = {(ln["seg"], ln["line"]): ln for ln in out}
    for a, b in TWINS:
        _align(idx[a], idx[b])
    return out


def season27():
    """Each brand's records: its operating legs, then the legs it sells on partners' flights (renumbered inside its own
    block for that operator, with a DEI 050 reference to the operating flight)."""
    L = lines27()
    legs = {"NV": [], "TQ": [], "GY": []}
    refs = {"NV": {}, "TQ": {}, "GY": {}}
    used = {lg[k] for ln in L for lg in ln["legs"] for k in ("out_num", "back_num") if lg.get(k) is not None}
    for ln in L:
        s = W.SEGMENTS[ln["seg"]]
        legs[s["brand"]] += legs_of(ln, s["type"], [(S27[0], S27[1], 0)])
    nxt = dict(DUP_LO)
    for ln in L:
        mk, which = DUPLICATED[ln["seg"]]
        if ln["line"] not in which:
            continue
        s = W.SEGMENTS[ln["seg"]]
        mapping = {}
        for lg in ln["legs"]:
            for k in ("out_num", "back_num"):
                n0 = lg.get(k)
                if n0 is None or n0 in mapping:
                    continue
                n = nxt[(mk, s["op"])]
                while n in used:
                    n += 1
                used.add(n)
                nxt[(mk, s["op"])] = n + 1
                mapping[n0] = n
        dup = legs_of(ln, s["type"], [(S27[0], S27[1], 0)], airline=mk, renumber=lambda n0: mapping[n0])
        for x in dup:
            x["dup_of"] = (s["brand"], x["op_flight"])
            refs[mk][(mk, x["flight"], x["leg"])] = (s["brand"], x["op_flight"])
        legs[mk] += dup
    out = {}
    for k in legs:
        out[k] = sorted(finish(legs[k], utc=k in UTC_CARRIERS), key=lambda x: (x["flight"], x["leg"], x["frm"]))
    return out, refs


# ---------------------------------------------------------------- the schedule ask's truth
def week_days():
    a, b = W.WEEK27
    return [a + dt.timedelta(days=i) for i in range((b - a).days + 1)]


def turns27(L=None):
    """Every scheduled turn at Kelderby in the peak week on the operating lines: relationship, day, the arrival's and
    the departure's Kelderby clock, scheduled ground time."""
    L = L or lines27()
    out = []
    for ln in L:
        legs = ln["legs"]
        for d in week_days():
            if ln["dow"][d.isoweekday() - 1] == " ":
                continue
            for i, lg in enumerate(legs):
                if lg["sta"] is None or i + 1 >= len(legs) or legs[i + 1]["std"] is None:
                    continue
                out.append(dict(seg=ln["seg"], line=ln["line"], day=d, sta=lg["sta"], std=legs[i + 1]["std"],
                                gt=legs[i + 1]["std"] - lg["sta"], through=bool(lg.get("through"))))
    return out


def ask_a_truth(L=None):
    """Each relationship's turns in the week of 12 July 2027 and how many are scheduled shorter than its filing."""
    out = {k: [0, 0] for k in W.ORDER}
    for t in turns27(L):
        out[t["seg"]][0] += 1
        out[t["seg"]][1] += int(t["gt"] < W.SEGMENTS[t["seg"]]["filed"])
    return out
