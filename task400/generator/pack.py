"""Cut the pack (target/) from the clean truth in world.py. Each file is written the way its producing system
writes it; nothing here describes the data."""
import csv
import datetime as dt
import os

import numpy as np
import pandas as pd

import postprocess as PP
import world as W

UTC_OFF = dt.timedelta(hours=8)
LOC_NAMES = {
    "CRU": ("ROM crusher pad", "Plant"), "SHR": ("South haul road", "South"), "SRP": ("South pit ramp", "South"),
    "SWD": ("South waste dump", "South"), "NHR": ("North haul road", "North"), "NRP": ("North pit ramp", "North"),
    "NWD": ("North waste dump", "North"), "NRJ": ("North ramp junction (workshop access)", "North"),
    "WKR": ("Workshop road", "Plant"), "GOL": ("Go-line and park-up", "Plant"),
}
ROUTES = {"SP-ORE": "S-ORE>ROM", "NP-ORE": "N-ORE>ROM", "SP-WST": "S-WST>SWD", "NP-WST": "N-WST>NWD"}
LOADS = {"SP-ORE": 21.0, "NP-ORE": 17.5, "SP-WST": 25.0, "NP-WST": 14.5}
LIMITS = [("NRP", 40, dt.date(2024, 7, 1)), ("NRP", 32, dt.date(2026, 6, 9)), ("SRP", 40, dt.date(2024, 7, 1)),
          ("SRP", 35, dt.date(2026, 8, 18)), ("NHR", 60, dt.date(2024, 7, 1)), ("SHR", 60, dt.date(2024, 7, 1)),
          ("CRU", 20, dt.date(2024, 7, 1)), ("NWD", 25, dt.date(2024, 7, 1)), ("SWD", 25, dt.date(2024, 7, 1))]
GATE_FROM = dt.date(2026, 7, 1)
NG2_FROM = dt.datetime(2026, 7, 14, 10, 40)
FMS72 = dt.datetime(2026, 8, 1, 9, 0)
STAMP = dt.datetime(2026, 11, 2, 7, 15)


def rng(name):
    return W.rng("pack/" + name)


def limit_on(seg, day):
    cur = None
    for s, lim, eff in LIMITS:
        if s == seg and eff <= day:
            cur = lim
    return cur


def current_limit(seg):
    return limit_on(seg, W.END)


# ----------------------------------------------------------------------------------------------- entities
def light_vehicles():
    r = rng("lv")
    letters = "ABCDEFGHJKLMNPQRSTUVWXYZ"
    depts = [("Mine production", "Ternhallow", 0.30), ("Mine maintenance", "Ternhallow", 0.18), ("Geology and survey", "Ternhallow", 0.10),
             ("Processing plant", "Ternhallow", 0.12), ("HSE", "Ternhallow", 0.05), ("Electrical services", "Brannock Electrical", 0.09),
             ("Drill and blast", "Quarrington Drill & Blast", 0.10), ("Tyre services", "Outback Tyre Co", 0.06)]
    pw = np.array([d[2] for d in depts])
    types = ["Toyota LC79 single cab", "Toyota LC79 dual cab", "Toyota LC76 wagon", "Toyota Hilux SR dual cab"]
    lvs, used = [], set()
    while len(lvs) < 96:
        rego = "1%s%s%s%03d" % tuple([letters[int(r.integers(0, 24))] for _ in range(3)] + [int(r.integers(100, 999))])
        if rego in used:
            continue
        used.add(rego)
        d = depts[int(r.choice(len(depts), p=pw / pw.sum()))]
        lvs.append(dict(rego=rego, dept=d[0], employer=d[1], type=types[int(r.integers(0, 4))],
                        tag="LT%06d" % int(r.integers(100000, 999999))))
    return lvs


def ancillary():
    r = rng("anc")
    out = []
    for prefix, n, kind in (("WC", 4, "Water cart"), ("GR", 3, "Grader"), ("DZ", 4, "Track dozer"), ("SV", 3, "Service truck")):
        nums = sorted(r.choice(np.arange(600, 990), size=n, replace=False).tolist())
        for k in nums:
            out.append(dict(asset="%s%d" % (prefix, k), kind=kind, serial="PX3-%06d" % int(r.integers(100000, 999999))))
    return out


def lv_faults(lvs):
    """Each LV tag's not-working spells (fault reported to repair fitted) over the gate window."""
    r = rng("faults")
    out = {}
    start = dt.datetime(2026, 6, 1)
    for lv in lvs:
        spells = []
        t = start + dt.timedelta(days=float(r.exponential(380)))
        while t < dt.datetime(2026, 11, 1):
            dur = dt.timedelta(days=float(r.uniform(2, 19)))
            spells.append((t, t + dur))
            t = t + dur + dt.timedelta(days=float(r.exponential(380)))
        out[lv["rego"]] = spells
    return out


# ----------------------------------------------------------------------------------------------- the CAS log
def cas_alerts(S, lvs, anc):
    r = rng("alerts")
    fleet = S["fleet"]
    sh = S["shifts"]
    lv_tags = [lv["tag"] for lv in lvs]
    anc_ser = [a["serial"] for a in anc]
    truck_units = {}
    rows, crit = [], []
    used = set()
    for k, a in enumerate(S["alarms"]):
        s = sh[a["sid"]]
        unit = W.unit_on(fleet, s["truck"], s["day"])
        if a["real"]:
            peer = lv_tags[int(r.integers(0, len(lv_tags)))] if r.random() < 0.7 else anc_ser[int(r.integers(0, len(anc_ser)))]
        else:
            u = r.random()
            if u < 0.6:
                peer = lv_tags[int(r.integers(0, len(lv_tags)))]
            elif u < 0.85:
                peer = anc_ser[int(r.integers(0, len(anc_ser)))]
            else:
                other = fleet["trucks"][int(r.integers(0, len(fleet["trucks"])))]
                if other == s["truck"]:
                    other = fleet["trucks"][(fleet["trucks"].index(other) + 1) % len(fleet["trucks"])]
                peer = W.unit_on(fleet, other, s["day"])
        onset_utc = a["onset_local"] - UTC_OFF
        onset_utc = onset_utc.replace(microsecond=0)
        if a["level"] == "WARN":
            dur = float(r.uniform(4, 42))
            rng_m = float(r.uniform(31, 58))
        else:
            dur = float(r.uniform(2, 16))
            rng_m = float(r.uniform(7, 24))
        ack = onset_utc + dt.timedelta(seconds=float(r.uniform(0.8, 4.6))) if r.random() < 0.962 else None
        while True:
            eid = "%010x" % int(r.integers(0, 16 ** 10))
            if eid not in used:
                used.add(eid)
                break
        row = dict(event_id=eid, unit_serial=unit, peer_tag=peer, alert_level=a["level"],
                   onset_utc=onset_utc.strftime("%Y-%m-%dT%H:%M:%SZ"),
                   cleared_utc=(onset_utc + dt.timedelta(seconds=round(dur))).strftime("%Y-%m-%dT%H:%M:%SZ"),
                   range_at_onset_m=round(rng_m, 1),
                   ack_utc=ack.strftime("%Y-%m-%dT%H:%M:%SZ") if ack else None)
        rows.append(row)
        if a["level"] == "CRIT":
            crit.append((k, a, s, onset_utc))
    df = pd.DataFrame(rows).sort_values(["onset_utc", "event_id"]).reset_index(drop=True)
    return df, crit


# ----------------------------------------------------------------------------------------------- FMS windows
OFFSETS = [-2, 0, 2, 4, 6, 8]


def _response_trace(r, v0):
    # an operator who acts on a critical alert brakes within two seconds and keeps braking to a crawl or a stop
    start = float(r.uniform(0.7, 1.7))
    rate = float(r.uniform(4.5, 9.0))
    drop = float(r.uniform(11.0, 28.0))
    out = []
    for t in OFFSETS:
        if t <= start:
            v = v0 + float(r.normal(0, 0.5))
        else:
            v = v0 - min(drop, rate * (t - start)) + float(r.normal(0, 0.5))
        out.append(max(0.0, v))
    return out


def _carry_on_trace(r, v0):
    kind = r.random()
    out = []
    v = v0
    for t in OFFSETS:
        if t > 0:
            if kind < 0.12:      # an unrelated easing for a bend, a dump approach or a give-way line
                v -= float(r.uniform(0.3, 0.9))
            elif kind < 0.20:
                v += float(r.uniform(0.4, 1.4))
            else:
                v += float(r.normal(0, 0.6))
        out.append(max(0.0, v + float(r.normal(0, 0.4))))
    return out


def fms_windows(S, crit):
    r = rng("fms")
    sh = S["shifts"]
    rows = []
    ref = 7104331
    events = []
    for k, a, s, onset_utc in crit:
        if r.random() < 0.019:
            continue
        local = onset_utc + UTC_OFF + dt.timedelta(seconds=float(r.uniform(0.3, 1.6)))
        v0 = float(r.uniform(14, 48))
        trace = _response_trace(r, v0) if a["responded"] else _carry_on_trace(r, v0)
        events.append((local.replace(microsecond=0), s["truck"], "CAS_CRITICAL", "", "", trace))
    # overspeed events: the FMS opens a window when a truck crosses the segment's limit plus two
    r2 = rng("overspeed")
    segs = {"SP-ORE": [("SRP", 0.045), ("SHR", 0.05), ("CRU", 0.02)], "NP-ORE": [("NRP", 0.05), ("NHR", 0.05), ("CRU", 0.02)],
            "SP-WST": [("SRP", 0.045), ("SHR", 0.05), ("SWD", 0.02)], "NP-WST": [("NRP", 0.06), ("NHR", 0.05), ("NWD", 0.02)]}

    def excess_draw(base=None):
        while True:
            e = 2.0 + float(r2.exponential(3.4)) if base is None else max(2.4, base * float(r2.uniform(0.75, 1.15)))
            if abs(e - 5.0) > 0.35:
                return e
            base = None

    for s in sh:
        for seg, lam in segs[s["circuit"]]:
            for _ in range(r2.poisson(lam)):
                lim = limit_on(seg, s["day"])
                excess = excess_draw()
                peak = lim + excess
                when = (s["start"] + dt.timedelta(seconds=float(r2.uniform(600, s["op_hours"] * 3600)))).replace(microsecond=0)
                long_run = r2.random() < 0.34
                ipk = int(r2.integers(2, 5))
                trace = []
                for j, t in enumerate(OFFSETS):
                    if j == ipk:
                        v = peak
                    else:
                        v = peak - abs(j - ipk) * float(r2.uniform(0.9, 2.2)) - float(r2.uniform(0.05, 0.4))
                    if long_run and t >= 6:
                        v = max(v, lim + 2.3 + float(r2.uniform(0, 1.2)))
                    trace.append(v)
                # a run on a long descent: the operator brakes under the limit and the truck runs away again
                rerun = (not long_run) and ipk <= 3 and r2.random() < (0.32 if seg in ("NRP", "SRP") else 0.08)
                if rerun:
                    trace[-1] = lim - float(r2.uniform(0.6, 2.6))
                    trace[-2] = min(trace[-2], lim + float(r2.uniform(0.2, 1.6)))
                events.append((when, s["truck"], "OVERSPEED", seg, current_limit(seg), trace))
                if long_run and when >= FMS72:
                    # from the 7.2 release a run still over the limit when its window closes is logged again; the new
                    # window opens on the sample that closed the last one
                    tr2 = [trace[-1]] + [max(lim + 2.1, trace[-1] - float(r2.uniform(0, 1.5)) +
                                             (0 if k < 3 else -k * float(r2.uniform(0.6, 1.8)))) for k in range(1, len(OFFSETS))]
                    tr2 = [tr2[0]] + [min(v, peak - 0.6) for v in tr2[1:]]
                    events.append((when + dt.timedelta(seconds=10), s["truck"], "OVERSPEED", seg, current_limit(seg), tr2))
                if rerun:
                    gap = int(r2.choice([10, 12, 14], p=[0.5, 0.3, 0.2]))
                    ex2 = excess_draw(base=excess)
                    ip2 = int(r2.integers(2, 4))
                    tr3 = []
                    for j, t in enumerate(OFFSETS):
                        if j == 0:
                            v = trace[-1] if gap == 10 else lim - float(r2.uniform(0.3, 2.2))
                        elif j == 1:
                            v = lim + 2.0 + float(r2.uniform(0.1, 0.6))
                        elif j == ip2:
                            v = lim + ex2
                        else:
                            v = lim + ex2 - abs(j - ip2) * float(r2.uniform(0.9, 2.0)) - float(r2.uniform(0.05, 0.4))
                        tr3.append(v)
                    tr3[1] = min(tr3[1], lim + ex2 - 0.2)
                    events.append((when + dt.timedelta(seconds=gap), s["truck"], "OVERSPEED", seg, current_limit(seg), tr3))
    events.sort(key=lambda e: (e[0], e[1], e[2]))
    r_os = rng("overspeed-gps")
    for when, truck, trig, seg, lim, trace in events:
        if trig == "OVERSPEED":
            ref += int(r_os.integers(1, 9))
            # the window's edges and its highest sample always carry a fix (the trigger and the run's own record)
            keep = {0, len(OFFSETS) - 1, int(np.argmax(trace))}
            oks = [True if j in keep else r_os.random() > 0.016 for j in range(len(OFFSETS))]
        else:
            ref += int(r.integers(1, 9))
            oks = [r.random() > 0.016 for _ in OFFSETS]
        for t, v, ok in zip(OFFSETS, trace, oks):
            rows.append(dict(event_ref=ref, truck_no=truck, trigger=trig,
                             trigger_time_awst=when.strftime("%Y-%m-%d %H:%M:%S"), segment=seg,
                             limit_kmh=lim if lim != "" else None, t_offset_s=t,
                             speed_kmh=round(v, 1) if ok else None, gps_fix="3D" if ok else "NONE"))
    df = pd.DataFrame(rows)
    df["limit_kmh"] = df["limit_kmh"].astype("Int64")
    return df


# ----------------------------------------------------------------------------------------------- dispatch
def dispatch(S):
    r = rng("dispatch")
    rows = []
    for s in S["shifts"]:
        loads = max(1, int(round(LOADS[s["circuit"]] * s["op_hours"] / 10.6 + r.normal(0, 1.6))))
        tonnes = round(sum(float(r.normal(226.0, 7.5)) for _ in range(loads)), 1)
        rows.append(dict(shift_date=s["day"].isoformat(), shift="DAY" if s["shift"] == "D" else "NIGHT",
                         truck_no=s["truck"], operator_id=s["badge"], route=ROUTES[s["circuit"]], loads=loads,
                         tonnes=tonnes, operating_hrs=round(s["op_hours"], 2),
                         delay_hrs=round(max(0.0, 12 - s["op_hours"] - float(r.uniform(0.4, 0.9))), 2)))
    return pd.DataFrame(rows)


# ----------------------------------------------------------------------------------------------- gate reads
def gate_reads(lvs, faults):
    r = rng("gate")
    rows = []
    day = GATE_FROM
    passages = []
    while day <= W.END:
        for lv in lvs:
            n = r.poisson(3.4 if lv["dept"] in ("Mine production", "Geology and survey", "Drill and blast") else 1.6)
            for _ in range(n):
                u = r.random()
                if u < 0.35:     # around the day shift start
                    t = dt.datetime.combine(day, dt.time(5, 25)) + dt.timedelta(minutes=float(r.uniform(0, 55)))
                elif u < 0.55:
                    t = dt.datetime.combine(day, dt.time(17, 25)) + dt.timedelta(minutes=float(r.uniform(0, 55)))
                else:
                    t = dt.datetime.combine(day, dt.time(0, 0)) + dt.timedelta(minutes=float(r.uniform(0, 1440)))
                gate = "N" if r.random() < 0.52 else "S"
                passages.append((t.replace(microsecond=0), lv, gate))
        day += dt.timedelta(days=1)
    passages.sort(key=lambda p: (p[0], p[1]["rego"]))
    # one vehicle per boom cycle at each gate: a vehicle arriving inside the cycle waits for the next one
    spaced, last = [], {"N": None, "S": None}
    for t, lv, gate in passages:
        if last[gate] is not None and t < last[gate] + dt.timedelta(seconds=16):
            t = last[gate] + dt.timedelta(seconds=16 + int(r.integers(0, 5)))
        last[gate] = t
        spaced.append((t, lv, gate))
    passages = sorted(spaced, key=lambda p: (p[0], p[1]["rego"]))

    def tag_seen(lv, t):
        for a, b in faults[lv["rego"]]:
            if a <= t < b:
                return ""
        return lv["tag"]

    def anpr(plate):
        if r.random() < 0.031:
            i = int(r.integers(1, len(plate)))
            sub = {"0": "O", "O": "0", "1": "I", "8": "B", "B": "8", "5": "S", "S": "5", "2": "Z", "Z": "2"}
            c = plate[i]
            return plate[:i] + sub.get(c, "") + plate[i + 1:] if c in sub or r.random() < 0.5 else plate[:i] + plate[i + 1:]
        return plate

    nxt = {}
    seen = {}
    for t, lv, gate in reversed(passages):
        nxt[(t, lv["rego"])] = seen.get(lv["rego"])
        seen[lv["rego"]] = t
    truth = []
    for t, lv, gate in passages:
        tag = tag_seen(lv, t)
        nt = nxt[(t, lv["rego"])]
        truth.append((t, lv["rego"], gate, tag == ""))
        if gate == "S":
            rows.append((t, "SG-IN", anpr(lv["rego"]), tag, "IN"))
        else:
            both = t >= NG2_FROM
            miss1 = both and r.random() < 0.035
            if not miss1:
                rows.append((t, "NG-1", anpr(lv["rego"]), tag, "IN"))
            if both and not (not miss1 and r.random() < 0.03):
                lag = float(r.uniform(4.0, 11.5))
                rows.append(((t + dt.timedelta(seconds=lag)).replace(microsecond=0), "NG-2", anpr(lv["rego"]), tag, "IN"))
        out_t = t + dt.timedelta(hours=float(r.uniform(0.6, 9.5)))
        if nt is not None and out_t > nt - dt.timedelta(minutes=6):
            out_t = t + (nt - t) * float(r.uniform(0.35, 0.8))
        if out_t <= dt.datetime(2026, 10, 31, 23, 59, 59) and out_t - t > dt.timedelta(minutes=3):
            rows.append((out_t.replace(microsecond=0), "SG-OUT" if gate == "S" else "NG-OUT", anpr(lv["rego"]), tag_seen(lv, out_t), "OUT"))
    rows.sort(key=lambda x: (x[0], x[1]))
    df = pd.DataFrame(rows, columns=["read_time_awst", "reader", "plate_read", "cas_tag", "direction"])
    df["read_time_awst"] = df["read_time_awst"].dt.strftime("%Y-%m-%d %H:%M:%S")
    return df, truth


# ----------------------------------------------------------------------------------------------- incidents
SPI_LEAD = ["{P} entered the haul road in front of {ld}{t}", "{P} pulled out ahead of {ld}{t}",
            "{t} and {P} closed head on", "{P} stopped in the blind spot of {t}", "{P} parked inside the turning circle of {t}",
            "{t} reversing with {P} behind", "{P} passed {t} on the wrong side of the windrow",
            "{P} came round the bend into the path of {ld}{t}", "{P} followed {t} too closely",
            "{t} pulled away with {P} alongside", "{P} crossed in front of {ld}{t}", "{t} turned across the path of {P}"]
SPI_GAP = ["approx {d} m", "about {d} m", "est. {d} m", "roughly {d} m", "{d} m apart", "under {d} m", "{d} to {d2} m"]
SPI_END = ["both stopped", "truck stopped short", "operator braked hard", "{Q} pulled over", "no contact",
           "operator stopped and called the {q}", "{Q} reversed clear", "both drivers stopped and called it in",
           "truck held on the brakes until the {q} cleared"]
ANC_KIND = {"WC": "water cart", "GR": "grader", "DZ": "dozer", "SV": "service truck"}
VI_TAIL = ["", "", "", " Radio call made.", " Supervisor notified.", " Reported at end of shift.", " Both drivers spoken to.",
           " LV driver stood down pending interview.", " Traffic controller attended.", " Area inspected, no defects.",
           " Reported by the truck operator.", " Witness statement taken.", " Pre-start reminder issued to the crew."]
COL_LEAD = ["{t} made contact with {P}", "{t} struck {P}", "{t} clipped {P}", "{P} rolled back into {t}",
            "{t} reversed into {P}", "Low speed contact between {t} and {P}", "{P} ran into the side of {t}"]
COL_DMG = ["front quarter panel", "bullbar", "mirror", "rear tray", "driver's door", "tail light", "bumper", "wheel arch"]
COL_INJ = ["no injury", "nil injuries", "driver checked by ERT, no injury", "driver assessed at the medical centre, cleared",
           "no injuries reported"]
COL_TAIL = ["", "", " LV towed to workshop.", " Scene held for investigation.", " Both drivers tested for drug and alcohol, negative.",
            " Area barricaded.", " Photos taken and investigation opened.", " Truck taken out of service for inspection."]


def vi_text(r, collision, t, peer, is_lv, lname, lcode, when):
    pick = lambda xs: xs[int(r.integers(0, len(xs)))]
    P = ("LV " + peer) if is_lv else peer
    d = int(r.integers(2, 9))
    clock = (" at about %s" % when.strftime("%H:%M")) if r.random() < 0.22 else ""
    if collision:
        lead = pick(COL_LEAD).format(t=t, P=P)
        return "%s at %s%s; %s damaged, %s.%s" % (lead, lname, clock, pick(COL_DMG), pick(COL_INJ), pick(COL_TAIL))
    if r.random() < 0.12:
        return pick(["SPI %s / %s at %s, ~%d m." % (t, peer, lcode, d), "Near miss %s and %s, %s." % (t, peer, lname),
                     "SPI, %s and %s, %s%s, approx %d m." % (t, P, lname, clock, d)])
    lead = pick(SPI_LEAD).format(t=t, P=P, ld=pick(["loaded ", "empty ", ""]))
    gap = pick(SPI_GAP).format(d=d, d2=d + int(r.integers(1, 3)))
    q = "LV" if is_lv else ANC_KIND.get(peer[:2], "vehicle")
    end = pick(SPI_END).format(q=q, Q=q if q == "LV" else q[0].upper() + q[1:])
    return "%s at %s%s, %s; %s.%s" % (lead, lname, clock, gap, end, pick(VI_TAIL))


OTHER = [
    ("INJ-FAI", "First aid: {w} {cut} to {hand} while {task}, cleaned and dressed."),
    ("INJ-FAI", "First aid: dust in {eye} eye at {l}, eye wash station used{after}."),
    ("INJ-FAI", "{W} jarred {hand} on a {part} at {l}; ice pack, returned to work."),
    ("INJ-MTI", "Strained {back} {lifting} at {l}, physio referral."),
    ("INJ-MTI", "Laceration to {arm} on {edge}, {stitch} at the site medical centre."),
    ("INJ-MTI", "{W} struck on the {arm} by a {part} that swung free at {l}; X-ray clear, {stitch}."),
    ("INJ-LTI", "Rolled {ankle} ankle stepping off the {l} {access}; off work {n} shifts."),
    ("INJ-LTI", "{W} fell from {access} at {l}, fractured {wrist} wrist."),
    ("PD", "Light vehicle {lvdmg} at {l}; {lvpart} damaged."),
    ("PD", "Tyre damage on a haul truck from rock spillage on the {l}{after}."),
    ("PD", "{Plant} {plantdmg} at {l}."),
    ("ENV", "Hydraulic hose failure on a {plant} at {l}, approx {litres} L spilt, spill kit used."),
    ("ENV", "Dust exceedance alarm at the {l} monitor, {dustfix}."),
    ("NM", "Unsecured load on a service truck at {l} noticed {when}."),
    ("NM", "Person walked into the exclusion zone of the {l} without contact, stopped by {stopper}."),
    ("NM", "{W} found an isolation lock missing on {plant} at {l} before work started."),
]
OTHER_TAIL = ["", "", "", " Day shift.", " Night shift.", " Reported by the supervisor.", " Area inspected.",
              " Toolbox talk at the next pre-start.", " Hazard report raised.", " Task risk assessment reviewed.",
              " Supervisor notified.", " Reported next morning.", " Photos on file."]
FILL = dict(
    cut=["cut", "small cut", "graze", "nick"], hand=["left hand", "right hand", "thumb", "index finger", "knuckle"],
    task=["changing a light tower filter", "opening a toolbox lid", "fitting a hose clamp", "cutting cable ties",
          "handling sample bags", "removing a guard"],
    eye=["left", "right"], after=["", " on day shift", " during the inspection", " at shift change", " after the blast"],
    part=["handrail", "door frame", "step", "tool chest", "battery isolator"],
    back=["lower back", "back", "shoulder", "neck"],
    lifting=["lifting a hose", "moving a pump", "carrying a jerry can", "pulling a cable reel", "lifting a toolbox"],
    arm=["forearm", "upper arm", "hand", "wrist"],
    edge=["a sharp edge of a grader blade", "a sheared bolt", "a damaged cable tray", "a cutting edge on a dozer"],
    stitch=["stitches", "steri-strips", "three stitches", "dressing and review"],
    ankle=["left", "right"], access=["ladder access", "stairs", "walkway", "cab steps", "platform"],
    n=["two", "three", "four", "five"], wrist=["left", "right"],
    lvdmg=["reversed into a bollard", "clipped a windrow", "struck a parked trailer", "ran over a dropped bolt"],
    lvpart=["tail light", "bumper", "rear quarter panel", "tyre", "mirror"],
    Plant=["Water cart", "Grader", "Dozer", "Service truck", "Fuel truck"],
    plantdmg=["side mirror struck a light pole", "clipped a bund wall", "struck a parked light tower",
              "damaged a drain cover", "caught a hose on a gate post"],
    plant=["dozer", "grader", "excavator", "water cart", "drill rig"],
    litres=["5", "10", "15", "20", "30", "40"],
    dustfix=["water cart redirected", "watering increased", "road closed for an hour", "speed restriction applied"],
    when=["before leaving the area", "at the gate", "by the supervisor", "on the pre-start check"],
    stopper=["the spotter", "the operator", "a supervisor", "a radio call", "the traffic controller"],
)


def incidents(S, alerts_df, lvs, anc):
    r = rng("incidents")
    sh = S["shifts"]
    lv_rego = [lv["rego"] for lv in lvs]
    anc_ids = [a["asset"] for a in anc]
    recs = []
    for i in S["incidents"]:
        s = sh[i["sid"]]
        is_lv = r.random() < 0.72
        peer = lv_rego[int(r.integers(0, len(lv_rego)))] if is_lv else anc_ids[int(r.integers(0, len(anc_ids)))]
        lname = LOC_NAMES[i["loc"]][0]
        text = vi_text(r, i["collision"], s["truck"], peer, is_lv, lname, i["loc"], i["when_local"])
        if i["collision"]:
            cls = "VI-COL"
            pot = "High" if r.random() < 0.6 else "Medium"
        else:
            cls = "VI-SPI"
            pot = "High" if r.random() < 0.35 else "Medium"
        recs.append(dict(when=i["when_local"].replace(second=0, microsecond=0), loc=i["loc"], cls=cls, pot=pot,
                         vehicles="%s / %s" % (s["truck"], peer), employer="Ternhallow", text=text))
    workers = ["mechanic", "fitter", "electrician", "operator", "surveyor", "plant operator", "boilermaker"]
    for day in W.DAYS:
        for _ in range(r.poisson(0.62)):
            cls, tmpl = OTHER[int(r.integers(0, len(OTHER)))]
            loc = list(LOC_NAMES)[int(r.integers(0, len(LOC_NAMES)))]
            emp = ["Ternhallow", "Ternhallow", "Ternhallow", "Brannock Electrical", "Quarrington Drill & Blast", "Outback Tyre Co"][int(r.integers(0, 6))]
            when = dt.datetime.combine(day, dt.time(0)) + dt.timedelta(minutes=float(r.uniform(0, 1440)))
            wk = workers[int(r.integers(0, len(workers)))]
            fill = {k: v[int(r.integers(0, len(v)))] for k, v in FILL.items()}
            txt = tmpl.format(w=wk, W=wk[0].upper() + wk[1:], l=LOC_NAMES[loc][0], **fill) + \
                OTHER_TAIL[int(r.integers(0, len(OTHER_TAIL)))]
            recs.append(dict(when=when.replace(second=0, microsecond=0), loc=loc, cls=cls,
                             pot=["Low", "Low", "Medium"][int(r.integers(0, 3))], vehicles="",
                             employer=emp, text=txt))
    recs.sort(key=lambda x: (x["when"], x["cls"], x["text"]))
    out = []
    seq = {2025: 3, 2026: 1}
    for x in recs:
        y = x["when"].year
        seq[y] += int(r.integers(1, 4))
        out.append(["INC-%d-%04d" % (y, seq[y]), x["when"], x["loc"], LOC_NAMES[x["loc"]][0],
                    x["cls"], x["pot"], x["employer"], x["vehicles"], x["text"]])
    return out


# ----------------------------------------------------------------------------------------------- register
def device_register(S, lvs, anc):
    fleet = S["fleet"]
    dev = []
    for ser, t, a, b in fleet["units"]:
        dev.append([ser, "Vehicle unit V3", t.replace("DT", "DT-"), a, b])
    for x in anc:
        dev.append([x["serial"], "Vehicle unit V3", x["asset"], dt.date(2023, 3, 14), None])
    for lv in lvs:
        dev.append([lv["tag"], "LV tag T2", lv["rego"], dt.date(2023, 5, 2), None])
    dev.sort(key=lambda d: (d[2], d[3]))
    fw = []
    for ser, t, a, b in fleet["units"]:
        first = max(a, dt.date(2024, 9, 30))
        versions = [("4.3.11", dt.date(2024, 9, 30)), ("4.3.14", fleet["v414_date"][t]), ("5.0.2", fleet["v5_date"][t])]
        cur = [v for v, d in versions if d <= first][-1]
        fw.append([ser, cur, dt.datetime.combine(first, dt.time(2, 10))])
        for v, d in versions:
            if d > first and (b is None or d < b):
                fw.append([ser, v, dt.datetime.combine(d, dt.time(10, 30)) - UTC_OFF])
    for x in anc:
        fw.append([x["serial"], "4.3.11", dt.datetime(2024, 9, 30, 2, 10)])
        fw.append([x["serial"], "4.3.14", dt.datetime(2025, 11, 12, 1, 5)])
        fw.append([x["serial"], "5.0.2", dt.datetime(2026, 6, 24, 1, 40)])
    fw.sort(key=lambda f: (f[2], f[0]))
    return dev, fw


# ----------------------------------------------------------------------------------------------- distractors
def dust(r):
    rows = []
    for day in W.DAYS:
        if day.year < 2026:
            continue
        for h in range(24):
            for mon, base in (("DM-NHR", 46.0), ("DM-SHR", 38.0), ("DM-ROM", 52.0)):
                v = base * (1.35 if 10 <= h <= 16 else 0.8) * float(r.lognormal(0, 0.35))
                rows.append([day.isoformat(), "%02d:00" % h, mon, round(v, 1)])
    return rows


def road_maintenance(r):
    rows = []
    tasks = [("Grade haul road", "GR"), ("Water haul road", "WC"), ("Clean up spillage", "DZ"), ("Windrow repair", "DZ"),
             ("Sheeting", "GR"), ("Drainage clean", "GR")]
    for day in W.DAYS:
        if day.year < 2026:
            continue
        for _ in range(r.poisson(9)):
            task, eq = tasks[int(r.integers(0, len(tasks)))]
            seg = ["NHR", "SHR", "NRP", "SRP", "CRU", "NWD", "SWD"][int(r.integers(0, 7))]
            rows.append([day.isoformat(), ["DAY", "NIGHT"][int(r.integers(0, 2))], seg, task, "%s%d" % (eq, int(r.integers(600, 990))),
                         round(float(r.uniform(0.5, 6.0)), 1)])
    return rows


def write_csv(path, header, rows):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(header)
        for row in rows:
            w.writerow(["" if v is None else v for v in row])


# ----------------------------------------------------------------------------------------------- the cut
TRUCK_UNITS = set()


def vendor_monthly(alerts, disp):
    a = alerts.copy()
    loc = pd.to_datetime(a["onset_utc"], format="%Y-%m-%dT%H:%M:%SZ") + pd.Timedelta(hours=8)
    a["ym"] = loc.dt.year * 100 + loc.dt.month
    d = disp.copy()
    d["ym"] = d["shift_date"].str[:4].astype(int) * 100 + d["shift_date"].str[5:7].astype(int)
    hours = d.groupby("ym")["operating_hrs"].sum()
    out = []
    for ym in sorted(hours.index):
        x = a[(a["ym"] == ym) & a["unit_serial"].isin(TRUCK_UNITS)]
        warn = int((x["alert_level"] == "WARN").sum())
        crit = int((x["alert_level"] == "CRIT").sum())
        ack = float(x["ack_utc"].notna().mean() * 100)
        out.append(dict(ym=int(ym), label="%s %d" % (["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct",
                                                      "Nov", "Dec"][ym % 100 - 1], ym // 100),
                        units=int(x["unit_serial"].nunique()), hours=float(hours[ym]), warn=warn, crit=crit,
                        per100=(warn + crit) / float(hours[ym]) * 100, ack=ack))
    return out


def cut(out, S=None):
    import docs as D
    if S is None:
        S = W.simulate()
    os.makedirs(out, exist_ok=True)
    lvs = light_vehicles()
    anc = ancillary()
    faults = lv_faults(lvs)
    TRUCK_UNITS.clear()
    TRUCK_UNITS.update(u[0] for u in S["fleet"]["units"])
    alerts, crit = cas_alerts(S, lvs, anc)
    alerts.to_parquet(os.path.join(out, "cas_alert_events_2025-01_2026-10.parquet"), index=False, row_group_size=50000)
    fms = fms_windows(S, crit)
    fms.to_parquet(os.path.join(out, "fms_event_windows_2025-2026.parquet"), index=False, row_group_size=100000)
    disp = dispatch(S)
    disp.to_csv(os.path.join(out, "dispatch_shift_summary_2025-2026.csv"), index=False, lineterminator="\n")
    gate, gate_truth = gate_reads(lvs, faults)
    gate.to_csv(os.path.join(out, "pit_gate_reads_2026-07_2026-10.csv"), index=False, lineterminator="\n")
    inc = incidents(S, alerts, lvs, anc)
    D.incident_register_xlsx(out, inc)
    dev, fw = device_register(S, lvs, anc)
    D.device_register_xlsx(out, dev, fw)
    gates = {"NG": ("North pit access gate", "North pit"),
             "SG": ("South pit access gate", "South pit")}
    write_csv(os.path.join(out, "site_location_codes.csv"), ["code", "location", "area"],
              [[k, v[0], v[1]] for k, v in sorted(list(LOC_NAMES.items()) + list(gates.items()))])
    write_csv(os.path.join(out, "light_vehicle_register.csv"), ["rego", "department", "employer", "vehicle"],
              [[lv["rego"], lv["dept"], lv["employer"], lv["type"]] for lv in sorted(lvs, key=lambda x: x["rego"])])
    write_csv(os.path.join(out, "haul_road_speed_limits.csv"), ["segment", "limit_kmh", "effective_from"],
              [[s, lim, eff.isoformat()] for s, lim, eff in LIMITS])
    r = rng("distractors")
    write_csv(os.path.join(out, "haul_road_dust_pm10_2026.csv"), ["date", "hour", "monitor", "pm10_ugm3"], dust(r))
    write_csv(os.path.join(out, "road_maintenance_log_2026.csv"), ["date", "shift", "segment", "task", "plant", "hours"],
              road_maintenance(r))
    D.terms_docx(out)
    nrj = [x for x in inc if x[2] == "NRJ" and x[4] == "VI-COL" and dt.datetime(2026, 7, 1) <= x[1] < dt.datetime(2026, 9, 1)]
    D.notice_pdf(out, max(x[1] for x in nrj))
    monthly = vendor_monthly(alerts, disp)
    D.vendor_report_pdf(out, monthly, "All haul truck units are on the current release. Hardware replacements: %d haul "
                        "truck units over the period." % sum(1 for u in S["fleet"]["units"] if u[3] is not None))
    ts = STAMP.timestamp()
    for fn in os.listdir(out):
        os.utime(os.path.join(out, fn), (ts, ts))
    return dict(S=S, lvs=lvs, anc=anc, gate_truth=gate_truth, monthly=monthly, alerts=alerts, fms=fms, disp=disp,
                inc=inc, dev=dev, fw=fw, gate=gate)
