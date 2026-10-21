"""task252 records: the historian's readings export, the laboratory's export, the check workbook's rows, the
register, and the two operational series the analysis does not need (daily output, daily rainfall)."""
import datetime as dt

import numpy as np

import params as P

LIMS_RAW = {c: "RW-%s" % c for c in P.CODES}
LIMS_OLD = {(c, s): "TW-%s-%s" % (c, "F" if s == "fil" else "W") for c in P.CODES for s in ("fil", "fin")}
SITE_NO = {"ASH": 4, "BRN": 7, "CAL": 9, "DUN": 12, "ELS": 15, "FEN": 18, "GAR": 21, "HOL": 26}
LIMS_NEW = {(c, s): "TUR%04d%s" % (SITE_NO[c], "B" if s == "fil" else "D") for c in P.CODES for s in ("fil", "fin")}
RECODE = dt.datetime(2027, 11, 1, tzinfo=P.NZ)
LOCATION = {"raw": "raw water tap after the intake screens", "fil": "filtered water tap, combined filtrate channel",
            "fin": "final water tap, outlet main after the contact tank"}
TECH = {"ASH": "Cameron Waugh", "BRN": "Cameron Waugh", "CAL": "Caleb MacDonald", "DUN": "Cameron Waugh",
        "ELS": "Caleb MacDonald", "FEN": "Cameron Waugh", "GAR": "Caleb MacDonald", "HOL": "Caleb MacDonald"}


def _utc(i):
    return P.slot_end(i).strftime("%Y-%m-%dT%H:%M:%SZ")


def readings(W):
    """the historian's export for the quarter, sorted by plant and time; a failed poll leaves the slot's F row and,
    once the historian has filled it from the outstation's store, the slot's G row beneath it; the polls that failed
    while a plant's outstation was being changed were never filled (the new unit's store started empty); a port whose
    signal never reached the PLC has F rows the polls returned as they were"""
    rows = []
    for code in P.CODES:
        x = W[code]
        tg = P.tag(code)
        fault = np.zeros(P.NS, dtype=bool)
        for f in x["faults"] + x["signals"]:
            for i in range(f["a"], f["b"]):
                if f["port"] is None or x["sl"][i] == f["port"]:
                    fault[i] = True
        chk = {}
        for k, s0 in enumerate(x["check_slots"]):
            for j in range(3):
                chk[s0 + j] = x["checks"][k][j]
        for k, s0 in enumerate(x["repair_checks"]):
            for j in range(3):
                chk[s0 + j] = x["repair_reads"][k][j]
        comms = np.zeros(P.NS, dtype=bool)
        for s, e in x["comms"]:
            comms[s:e] = True
        a, b = x["lost"]
        sa, sb = x["swap"]
        for i in range(P.NS):
            if a <= i < b:
                continue
            ts = _utc(i)
            if i in chk:
                rows.append((code, tg, ts, "%s-CHK" % code, "%.3f" % chk[i], "V"))
                continue
            sp = P.point(code, x["sl"][i])
            if fault[i] or sa <= i < sb:
                rows.append((code, tg, ts, sp, "", "F"))
                continue
            if comms[i]:
                rows.append((code, tg, ts, sp, "", "F"))
            rows.append((code, tg, ts, sp, "%.3f" % x["reading"][i], "G"))
    return rows


def lims(W):
    """the laboratory's export of the quarter's ammonia results: collected and received in New Zealand time as the
    sampler and the reception desk keyed them, analysed as the analyser stamped its run (standard time all year),
    released in New Zealand time by the laboratory system"""
    out = []
    rounds = W[P.CODES[0]]["round"]
    for r in rounds:
        for smp in r["samples"] + r.get("extras", []):
            code, s = smp["code"], smp["stream"]
            if s == "raw":
                lp = LIMS_RAW[code]
            else:
                lp = LIMS_NEW[(code, s)] if smp["collected"] >= RECODE else LIMS_OLD[(code, s)]
            res = smp["lab"]
            txt = ("<%.3f" % P.LOD) if (s != "raw" and res < P.LOD) else "%.3f" % max(res, 0.0)
            stamp = (smp["analysed"] - dt.timedelta(hours=1)).replace(tzinfo=None)    # NZST on the analyser
            out.append(dict(sample_no="K27-%06d" % (318000 + smp["no"]), lims_point=lp,
                            location="%s WTP, %s" % (P.NAME[code], LOCATION[s]),
                            collected=smp["collected"].strftime("%d/%m/%Y %H:%M"),
                            received=smp["received"].strftime("%d/%m/%Y %H:%M"),
                            analysed=stamp.strftime("%d/%m/%Y %H:%M"),
                            released=smp["released"].strftime("%d/%m/%Y %H:%M"),
                            determinand="Ammoniacal-N", result=txt, units="mg/L", lod="%.3f" % P.LOD,
                            _code=code, _stream=s, _true_hours=(smp["analysed"] - smp["collected"]).total_seconds() / 3600,
                            _stamp_hours=(stamp.replace(tzinfo=P.NZ) - smp["collected"]).total_seconds() / 3600))
    return out


def checks(W):
    out = []
    for code in P.CODES:
        x = W[code]
        for k, s0 in enumerate(x["check_slots"]):
            start = (P.T0 + dt.timedelta(minutes=P.SLOT_MIN * s0)).astimezone(P.NZ)
            reads = x["checks"][k]
            mean = sum(reads) / 3
            out.append(dict(tag=P.tag(code), plant=P.NAME[code], start=start, reads=reads, mean=mean,
                            result="PASS" if abs(mean - P.CHECK_STD) <= P.CHECK_TOL * P.CHECK_STD + 1e-9 else "FAIL",
                            by=TECH[code]))
    return out


def output(W, rng):
    """daily water supplied by each plant (megalitres), from the outlet flow meters"""
    base = {"ASH": 9.4, "BRN": 6.1, "CAL": 14.8, "DUN": 7.7, "ELS": 4.9, "FEN": 11.2, "GAR": 8.6, "HOL": 12.3}
    rows = []
    for d in range(P.DAYS):
        day = dt.date(2027, 10, 1) + dt.timedelta(days=d)
        warm = 1 + 0.18 * d / P.DAYS + (0.06 if day.weekday() >= 5 else 0)
        for code in P.CODES:
            v = base[code] * warm * (1 + rng.normal(0, 0.05))
            rows.append((day.isoformat(), code, P.NAME[code], "%.2f" % v))
    return rows


def rainfall(W, rng):
    """daily rainfall at the council's five catchment gauges (09:00 to 09:00 local)"""
    gauges = [("RG01", "Upper Harrow at Bell Road"), ("RG02", "Kestrel Stream at Glenbrae"),
              ("RG03", "Bramble at Station Bridge"), ("RG04", "Linnet at Ridge Road"),
              ("RG05", "Sedge at the Quarry")]
    rows = []
    wet = rng.random(P.DAYS) < 0.38
    for d in range(P.DAYS):
        day = dt.date(2027, 10, 1) + dt.timedelta(days=d)
        for g, name in gauges:
            mm = float(rng.gamma(1.2, 7.0)) if (wet[d] and rng.random() < 0.85) else (0.2 if rng.random() < 0.12 else 0.0)
            rows.append((day.isoformat(), g, name, "%.1f" % mm))
    return rows
