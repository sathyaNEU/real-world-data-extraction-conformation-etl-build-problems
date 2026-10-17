"""Write the pack's data files: the authority's stand log, the three operators' flight logs (Pellmont in UTC, Sable
Coast's workbook in station local time with AHM 731 sub-codes, Grayling's sector file with its delays in one field),
the 2026 season schedule and the merged 2027 initial submissions (SSIM), the filings, the registers and the two
files the review does not use."""
import csv
import datetime as dt

import numpy as np

import schedule as SC
import sim as S
import ssim as SS
import world as W

UTC_H = -W.UTC_OFF          # hours to add to Kelderby local for UTC


def _rng(*k):
    return np.random.default_rng([W.SEED, 9] + list(k))


def mround(m):
    return int(np.floor(m + 0.5))


def stamp(day, minutes):
    """A date and minutes after its midnight as 'YYYY-MM-DD HH:MM'."""
    t = dt.datetime(day.year, day.month, day.day) + dt.timedelta(minutes=int(minutes))
    return t.strftime("%Y-%m-%d %H:%M")


def hhmm(minutes):
    m = int(minutes) % 1440
    return "%02d:%02d" % (m // 60, m % 60)


def callsign(seg, flight):
    return W.SEGMENTS[seg]["op"] + str(flight)


def commercial(seg, flight):
    return W.SEGMENTS[seg]["brand"] + str(flight)


def write_csv(path, cols, rows):
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, lineterminator="\r\n")
        w.writerow(cols)
        for r in rows:
            w.writerow(r)
    return len(rows)


# ---------------------------------------------------------------- what happened, once
def everything():
    x = S.everything()
    rng = _rng(1)
    for r in x["rows"]:
        r["t"] = mround(r["actual"])
        # the operator's own clock (ACARS) against the stand log's: a minute apart on a few movements
        r["t_op"] = r["t"] + (int(rng.choice([-1, 1])) if rng.random() < 0.07 else 0)
        r["codes"] = delay_codes(r, rng) if r["kind"] == "DEP" else []
        # the far end of the leg: the outstation's off-block for an arrival, its on-block for a departure
        taxi = float(rng.normal(0, 3))
        r["t_far"] = mround(r["actual"] - r["block"] + taxi) if r["kind"] == "ARR" else \
            mround(r["actual"] + r["block"] + taxi)
    x["legs26"] = SC.season26()
    x["legs27"], x["refs27"] = SC.season27()
    x["lines27"] = SC.lines27()
    return x


def delay_codes(r, rng):
    """The operator's delay codes for a departure: the minutes past its scheduled departure on its own clock, split
    into the minutes the aircraft was not ready (late inbound rotation 93, or the turn's own process) and the minutes
    a ready aircraft was held. Every late minute is coded; a ready aircraft a minute late is a start-up minute."""
    total = r["t_op"] - r["sched"]
    if total <= 0:
        return []
    tm, hold = r["turn_min"], r["hold_min"]
    if tm >= 0.5 and hold >= 0.5:
        nr = max(1, min(total - 1, mround(tm))) if total > 1 else total
    elif tm >= 0.5:
        nr = total
    else:
        nr = 0
    held = total - nr
    out = []
    if nr > 0:
        if r["first"]:
            out.append((str(rng.choice(["41", "63", "34", "35"])), nr))
        elif r["late_in"] > 5 and nr >= 4 and rng.random() < 0.35:
            k = int(rng.integers(1, nr))
            out += [("93", nr - k), (str(rng.choice(W.TURN_CODES)), k)]
        elif r["late_in"] > 5:
            out.append(("93", nr))
        else:
            out.append((str(rng.choice(W.TURN_CODES)), nr))
    if held > 0:
        hour = r["sched"] // 60
        pool = ["81", "89", "87", "16"] + (["71", "84", "83"] if hour >= 13 else [])
        out.append(("89" if hold < 0.5 else str(rng.choice(pool)), held))
    return out


# ---------------------------------------------------------------- the authority's stand log
AODB_COLS = ["event_id", "event_local_time", "event_type", "stand", "registration", "callsign", "recorded_by"]


def aodb_rows(x):
    ev = []
    for r in x["rows"]:
        if not (W.EXPORT_FROM <= r["day"] <= W.EXPORT_TO):
            continue
        kind = "ON-BLOCK" if r["kind"] == "ARR" else "OFF-BLOCK"
        e = r["stand"].startswith("E")
        ev.append((r["day"], r["t"], kind, r["stand"], r["reg"], callsign(r["seg"], r["flight"]), e))
    for t in x["tows"]:
        ev.append((t["day"], mround(t["actual"]), t["kind"], t["stand"], t["reg"], "", False))
    order = {"ON-BLOCK": 1, "TOW-OFF": 2, "TOW-ON": 3, "OFF-BLOCK": 4}
    ev.sort(key=lambda v: (v[0], v[1], order[v[2]], v[3]))
    out = []
    for i, (day, t, kind, stand, reg, cs, vdgs) in enumerate(ev):
        out.append([700001 + i, stamp(day, t), kind, stand, reg.replace("-", "") if vdgs else reg, cs,
                    "VDGS" if vdgs else "RAMP"])
    return out


# ---------------------------------------------------------------- the operators' logs
def _legs_by_op(x, op):
    out = [r for r in x["rows"] if W.SEGMENTS[r["seg"]]["op"] == op and W.EXPORT_FROM <= r["day"] <= W.EXPORT_TO]
    return sorted(out, key=lambda r: (r["day"], r["sched"] if r["kind"] == "DEP" else r["sched_other"], r["flight"]))


def _ends(r):
    """(dep station, arr station, scheduled dep and arr, actual off-block and on-block) in Kelderby-local minutes."""
    if r["kind"] == "DEP":
        return W.KDY, r["station"], r["sched"], r["sched_other"], r["t_op"], r["t_far"]
    return r["station"], W.KDY, r["sched_other"], r["sched"], r["t_far"], r["t_op"]


PELLMONT_COLS = ["sched_dep_date_utc", "flight", "atc_callsign", "tail", "dep", "arr", "std_utc", "sta_utc", "out_utc",
                 "in_utc", "delay_code_1", "delay_min_1", "delay_code_2", "delay_min_2"]


def pellmont_rows(x):
    out = []
    for r in _legs_by_op(x, "PMV"):
        dep, arr, std, sta, aout, ain = _ends(r)
        day0 = dt.datetime(r["day"].year, r["day"].month, r["day"].day) + dt.timedelta(hours=UTC_H)
        f = lambda m: (day0 + dt.timedelta(minutes=int(m))).strftime("%Y-%m-%d %H:%M")
        codes = r["codes"] + [("", "")] * (2 - len(r["codes"]))
        out.append([(day0 + dt.timedelta(minutes=int(std))).strftime("%Y-%m-%d"), commercial(r["seg"], r["flight"]),
                    callsign(r["seg"], r["flight"]), r["reg"], dep, arr, f(std), f(sta), f(aout), f(ain),
                    codes[0][0], codes[0][1], codes[1][0], codes[1][1]])
    return out


SABLE_COLS = ["Date", "Flight", "Reg", "From", "To", "STD", "STA", "Off Blocks", "On Blocks", "Delay 1", "Min 1",
              "Delay 2", "Min 2"]


def sable_rows(x):
    """Station local times, the date the leg left; on-block after midnight carries the next day's clock."""
    out = []
    tz = {c: z for c, n, b, z in W.STATIONS}
    tz[W.KDY] = 0
    for r in _legs_by_op(x, "SBC"):
        dep, arr, std, sta, aout, ain = _ends(r)
        dz, az = 60 * tz[dep], 60 * tz[arr]
        dday = r["day"] + dt.timedelta(days=int((std - dz) // 1440))
        codes = [(c + W.SUBCODE.get(c, "A"), m) for c, m in r["codes"]] + [("", "")] * (2 - len(r["codes"]))
        out.append([dday, commercial(r["seg"], r["flight"]), r["reg"], dep, arr, hhmm(std - dz), hhmm(sta - az),
                    hhmm(aout - dz), hhmm(ain - az), codes[0][0], codes[0][1], codes[1][0], codes[1][1]])
    return out


GRAYLING_COLS = ["sector_date", "flt", "reg", "orig", "dest", "sched_dep", "sched_arr", "act_dep", "act_arr", "delays"]


def grayling_rows(x):
    out = []
    tz = {c: z for c, n, b, z in W.STATIONS}
    tz[W.KDY] = 0
    for r in _legs_by_op(x, "GYA"):
        dep, arr, std, sta, aout, ain = _ends(r)
        dz, az = 60 * tz[dep], 60 * tz[arr]
        dday = r["day"] + dt.timedelta(days=int((std - dz) // 1440))
        out.append([dday.isoformat(), commercial(r["seg"], r["flight"]), r["reg"].replace("-", ""), dep, arr,
                    hhmm(std - dz), hhmm(sta - az), hhmm(aout - dz), hhmm(ain - az),
                    " ".join("%s-%d" % (c, m) for c, m in r["codes"])])
    return out


# ---------------------------------------------------------------- schedules
def write_ssim26(path, x):
    car = [(k, x["legs26"][k], {}, dt.date(2026, 3, 2), False, ets(x["legs26"][k])) for k in ("NV", "TQ", "GY")]
    return SS.write(path, car, "S26", SC.S26[0], SC.S26[1])


SUBMITTED = {"NV": dt.date(2026, 10, 1), "TQ": dt.date(2026, 10, 6), "GY": dt.date(2026, 10, 8)}


def write_ssim27(path, x):
    car = [(k, x["legs27"][k], x["refs27"][k], SUBMITTED[k], k in SC.UTC_CARRIERS, ets(x["legs27"][k]))
           for k in ("NV", "TQ", "GY")]
    return SS.write(path, car, "S27", SC.S27[0], SC.S27[1])


def ets(legs):
    """Every leg's electronic ticketing record (DEI 505), as the carriers file it."""
    return {(lg["airline"], lg["flight"], lg["leg"]): [(505, "ET")] for lg in legs}


# ---------------------------------------------------------------- registers and filings
FILING_COLS = ["filing_ref", "brand", "operating_carrier", "aircraft_type", "minimum_ground_time_min", "filed_on",
               "filed_by"]
FILED_BY = {"NV": "Norvale Air network planning", "TQ": "Tellura Airways schedules", "GY": "Grayling Air scheduling"}


def filing_rows():
    out = []
    for i, k in enumerate(W.ORDER):
        s = W.SEGMENTS[k]
        out.append(["KDY-S27-E%02d" % (i + 1), W.REGIONAL[s["brand"]], W.OPERATORS[s["op"]][0], W.TYPES[s["type"]],
                    s["filed"], SUBMITTED[s["brand"]].isoformat(), FILED_BY[s["brand"]]])
    return out


AIRCRAFT_COLS = ["registration", "operator", "aircraft_type", "seats", "serial_number", "in_service_from",
                 "kdy_lines_from", "kdy_lines_to", "home_base"]


def aircraft_rows(x):
    rng = _rng(3)
    out = []
    seen = set()
    for (seg, ln), reg in sorted(x["regs"].items(), key=lambda kv: kv[1]):
        s = W.SEGMENTS[seg]
        seen.add(reg)
        line = next(lv for lv in x["lines"] if lv["seg"] == seg and lv["line"] == ln)
        base = "KDY" if line["based"] else line["legs"][-1]["station"]
        out.append([reg, W.OPERATORS[s["op"]][0], W.TYPES[s["type"]], W.SEATS[s["type"]],
                    str(int(rng.integers(17000, 17999)) if s["type"] == "E75" else
                        int(rng.integers(4300, 4700)) if s["type"] == "DH4" else int(rng.integers(1100, 1500))),
                    dt.date(int(rng.integers(2009, 2022)), int(rng.integers(1, 13)), 1).isoformat(),
                    "2026-03-29", "", base])
    # aircraft on the register that flew no Kelderby lines this summer (other bases, maintenance spares)
    pref = {"PMV": ("C-GP", "E75"), "SBC": ("C-FS", "DH4"), "GYA": ("C-GG", "AT7")}
    for op, n in (("PMV", 3), ("SBC", 2), ("GYA", 1)):
        for j in range(n):
            while True:
                reg = pref[op][0] + "".join(rng.choice(list("ABCDEFGHJKLMNPRSTUVWXYZ"), 2))
                if reg not in seen:
                    break
            seen.add(reg)
            t = pref[op][1]
            out.append([reg, W.OPERATORS[op][0], W.TYPES[t], W.SEATS[t], str(int(rng.integers(17000, 17999))),
                        dt.date(int(rng.integers(2009, 2022)), int(rng.integers(1, 13)), 1).isoformat(), "", "",
                        "spare" if j == 0 else ["Vellacott", "Brannoch", "Orlen Falls"][j % 3]])
    out.sort(key=lambda r: r[0])
    return out


FLEET_COLS = ["operator", "aircraft_type", "month", "aircraft_in_fleet", "aircraft_in_heavy_check",
              "aircraft_available_for_kdy_lines"]


def fleet_rows(x):
    lines27 = x["lines27"]
    out = []
    for op, t in (("PMV", "E75"), ("SBC", "DH4"), ("GYA", "AT7")):
        n = sum(1 for ln in lines27 if W.SEGMENTS[ln["seg"]]["op"] == op)
        for m in range(3, 11):
            check = 1 if (op, m) in {("PMV", 3), ("PMV", 10), ("SBC", 4), ("SBC", 10), ("GYA", 3)} else 0
            out.append([W.OPERATORS[op][0], W.TYPES[t], "2027-%02d" % m, n + 1, check, n + 1 - check])
    return out


DELAY_COLS = ["code", "description", "kda_group"]


def delay_rows():
    out = [[c, d, "aircraft not ready"] for c, d in W.NOT_READY.items()]
    out += [[c, d, "held for another reason"] for c, d in W.HELD_OTHER.items()]
    extra = [("13", "Check-in error, passenger and baggage", "aircraft not ready"),
             ("38", "ULD, lack of or serviceability", "aircraft not ready"),
             ("51", "Damage during flight operations", "aircraft not ready"),
             ("82", "ATFM due to ATC staff or equipment en route", "held for another reason"),
             ("86", "Immigration, customs, health", "held for another reason"),
             ("91", "Load connection, awaiting load from another flight", "held for another reason"),
             ("94", "Cabin crew rotation, awaiting cabin crew from another flight", "aircraft not ready"),
             ("95", "Crew rotation, awaiting crew from another flight", "aircraft not ready")]
    out += [list(e) for e in extra]
    out.sort(key=lambda r: r[0])
    return out


STATION_COLS = ["iata", "name", "utc_offset_summer", "scheduled_block_min_from_kdy"]


def station_rows():
    out = [[W.KDY, "Kelderby", "-04:00", ""]]
    for c, n, b, z in W.STATIONS:
        out.append([c, n, "-%02d:00" % (4 + z), b])
    return sorted(out, key=lambda r: r[0])


# ---------------------------------------------------------------- the two files the review does not use
STAFF_COLS = ["date", "handler", "shift", "ramp_agents_rostered", "ramp_agents_present", "belt_loaders_serviceable",
              "tugs_serviceable"]


def staffing_rows():
    rng = _rng(7)
    out = []
    for d in W.days():
        for h, base in (("Norvale Ground Services", 26), ("Aerocrest Handling", 9), ("Grayling Air", 5)):
            for sh, k in (("early", 1.0), ("late", 0.85)):
                ros = int(round(base * k))
                pres = ros - int(rng.binomial(ros, 0.06))
                out.append([d.isoformat(), h, sh, ros, pres, int(round(base / 6)) - int(rng.random() < 0.1),
                            int(round(base / 5)) - int(rng.random() < 0.08)])
    return out


def punctuality(x):
    """Monthly departures and arrivals by brand at Kelderby, on time within 15 minutes of schedule."""
    out = {}
    for r in x["rows"]:
        if not (W.EXPORT_FROM <= r["day"] <= W.EXPORT_TO):
            continue
        k = (r["day"].month, W.SEGMENTS[r["seg"]]["brand"], r["kind"])
        n, ok = out.get(k, (0, 0))
        out[k] = (n + 1, ok + int(r["t_op"] - r["sched"] <= 15))
    return out
