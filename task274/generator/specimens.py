"""Specimen and instrument records around the world's results: the survey's specimen tracking events, the laboratory
information system's result rows (with the runs it voided and repeated), the bridging run's rows, and the analyzers'
event log in UTC (calibrations, QC, reagent loads, maintenance, errors)."""
from __future__ import annotations

import datetime as dt

import numpy as np

import common as K
import world as W

VIALS = [("01", "SERUM 1.0 ML - 25OHD"), ("02", "SERUM 1.0 ML - STORED DUPLICATE"), ("03", "SERUM 2.0 ML - CHEMISTRY"),
         ("04", "WHOLE BLOOD EDTA - HBA1C")]
STAFF_MEC = ["JRM", "TLB", "KAW", "DPS", "MEH", "RCN", "SLO", "AVG"]
STAFF_LAB = ["BW2", "KLY", "PNT", "GHR", "MLC", "SDV", "CJO"]


def labels(seed, P):
    """Each examined adult's pre-printed label number; the vial is the suffix."""
    r = W.rng(seed, "track")
    nums = r.choice(np.arange(2500000, 2599999), size=len(P), replace=False)
    for p, q in zip(P, nums):
        p["label"] = "MH%07d" % int(q)
    return P


def tracking(seed, w):
    r = W.rng(seed, "track")
    r = np.random.default_rng(int(r.integers(1 << 30)) + 3)
    P = w["P"]
    bridge = {b["seqn"]: b for b in w["bridge"]}
    rows = []
    boxes = {}
    pos = {"F1": [1, 1, 1], "F2": [1, 1, 1]}
    relabels = []
    for p in sorted(P, key=lambda p: (p["exam"], p["session"], p["seqn"])):
        if not p.get("blood"):
            continue
        h0 = {0: (8, 30), 1: (12, 40), 2: (17, 10)}[p["session"]]
        t = dt.datetime.combine(p["exam"], dt.time(*h0)) + dt.timedelta(minutes=int(r.integers(0, 170)))
        mec = "MEC-1 %s" % K.CNAME[p["ccode"]]
        box = boxes.get(p["shipped"])
        if box is None:
            box = "BX25-%04d" % (len(boxes) + 101)
            boxes[p["shipped"]] = box
        vials = ["01", "02", "03", "04"] if p.get("dup") else ["01", "03", "04"]
        for v in vials:
            bc = "%s-%s" % (p["label"], v)
            st = STAFF_MEC[int(r.integers(len(STAFF_MEC)))]
            rows.append([bc, p["seqn"], v, "COLLECTED", t, mec, "", st])
            if v != "04":
                tp = t + dt.timedelta(minutes=int(r.integers(35, 61)))
                rows.append([bc, p["seqn"], v, "PROCESSED", tp, mec, "", st])
                rows.append([bc, p["seqn"], v, "FROZEN", tp + dt.timedelta(minutes=int(r.integers(8, 21))), mec,
                             "-70C", st])
            else:
                rows.append([bc, p["seqn"], v, "REFRIGERATED", t + dt.timedelta(minutes=int(r.integers(5, 15))), mec,
                             "4C", st])
            ts = dt.datetime.combine(p["shipped"], dt.time(14, 0)) + dt.timedelta(minutes=int(r.integers(0, 110)))
            rows.append([bc, p["seqn"], v, "SHIPPED", ts, mec, box, STAFF_MEC[int(r.integers(len(STAFF_MEC)))]])
            dest = "MRMC LAB" if v in ("01", "02") else "STATE PUBLIC HEALTH LAB"
            tr = dt.datetime.combine(p["received"], dt.time(9, 0)) + dt.timedelta(minutes=int(r.integers(0, 120)))
            lab = STAFF_LAB[int(r.integers(len(STAFF_LAB)))]
            rows.append([bc, p["seqn"], v, "RECEIVED", tr, dest, box, lab])
            if v == "01":
                if p.get("reject"):
                    why = "HEMOLYZED" if p["reject"] == "HEM" else "QUANTITY NOT SUFFICIENT"
                    rows.append([bc, p["seqn"], v, "REJECTED", tr + dt.timedelta(minutes=int(r.integers(20, 90))),
                                 dest, why, lab])
                else:
                    rows.append([bc, p["seqn"], v, "ACCESSIONED", tr + dt.timedelta(minutes=int(r.integers(10, 60))),
                                 dest, p["accession"], lab])
                    rows.append([bc, p["seqn"], v, "ASSAYED", p["run_time"], dest, p["accession"], lab])
            if v == "02":
                fz = "F1" if r.random() < 0.55 else "F2"
                pp = pos[fz]
                loc = "%s-R%d-B%03d-P%02d" % (fz, pp[0], pp[1], pp[2])
                pp[2] += 1
                if pp[2] > 81:
                    pp[2] = 1
                    pp[1] += 1
                    if pp[1] > 24:
                        pp[1] = 1
                        pp[0] += 1
                rows.append([bc, p["seqn"], v, "STORED", tr + dt.timedelta(minutes=int(r.integers(60, 200))), dest,
                             loc, lab])
                b = bridge.get(p["seqn"])
                if b is not None:
                    pl = dt.datetime.combine(K.BRIDGE_PULL, dt.time(13, 0)) + dt.timedelta(minutes=int(r.integers(0, 200)))
                    rows.append([bc, p["seqn"], v, "PULLED", pl, dest, loc, "KLY"])
                    rows.append([bc, p["seqn"], v, "THAWED", b["time"] - dt.timedelta(minutes=int(r.integers(40, 90))),
                                 dest, "", "KLY"])
                    rows.append([bc, p["seqn"], v, "ASSAYED", b["time"], dest, b["accession"], "KLY"])
                    rows.append([bc, p["seqn"], v, "RETURNED", b["time"] + dt.timedelta(minutes=int(r.integers(30, 240))),
                                 dest, loc, "KLY"])
    rows.sort(key=lambda x: (x[4], x[0], x[3]))
    out = []
    for k, x in enumerate(rows, 1):
        out.append(["E%07d" % (3000000 + k)] + x)
    return out


def accessions(seed, w):
    """The laboratory's accession numbers, in order of receipt, for primary vials and the bridging vials."""
    P = w["P"]
    k = 0
    for p in sorted([p for p in P if p.get("result") is not None], key=lambda p: (p["received"], p["seqn"])):
        k += 1
        p["accession"] = "V25%06d" % (k + 40211)
    for b in w["bridge"]:
        k += 1
        b["accession"] = "V25%06d" % (k + 40211)
    return w


def lis_results(seed, w):
    """One row a result the LIS released for the survey's primary vials, plus the runs it voided: a run whose
    controls failed after it was released was voided and its vials run again the next working day."""
    r = W.rng(seed, "track")
    r = np.random.default_rng(int(r.integers(1 << 30)) + 17)
    out = []
    lotno = [lot[0] for lot in K.REAGENT_LOTS]
    for p in sorted([p for p in w["P"] if p.get("result") is not None], key=lambda p: p["run_time"]):
        code = K.ANALYZERS[p["analyzer"]][0]
        v = p["result"]
        txt = "<%.1f" % K.REPORT_LOW if v < K.REPORT_LOW else (">%.1f" % K.REPORT_HIGH if v > K.REPORT_HIGH else "%.1f" % v)
        out.append(dict(accession=p["accession"], barcode=p["label"] + "01", result=txt, analyzer=code,
                        lot=lotno[p["lot"]], time=p["run_time"], status="F", seqn=p["seqn"], comment=""))
    return out


def lis_bridge(seed, w):
    lotno = [lot[0] for lot in K.REAGENT_LOTS]
    pmap = {p["seqn"]: p for p in w["P"]}
    out = []
    cal = {c["id"]: c for c in w["cals"]}
    for b in sorted(w["bridge"], key=lambda b: b["time"]):
        p = pmap[b["seqn"]]
        v = b["result"]
        txt = "<%.1f" % K.REPORT_LOW if v < K.REPORT_LOW else "%.1f" % v
        out.append(dict(accession=b["accession"], barcode=p["label"] + "02", result=txt, analyzer="IA1",
                        lot=lotno[cal[b["cal"]]["lot"]], time=b["time"], seqn=b["seqn"]))
    return out


def event_log(seed, w):
    """The analyzers' middleware events from 1 December 2024 to 31 December 2025, in UTC."""
    r = W.rng(seed, "log")
    cals = w["cals"]
    lotno = [lot[0] for lot in K.REAGENT_LOTS]
    calno = [c[0] for c in K.CAL_LOTS]
    rows = []
    for an in (0, 1):
        sn = K.ANALYZERS[an][1]
        mine = [c for c in cals if c["analyzer"] == an]
        qc_days = {c["time"].date() for c in mine if c["reason"] == "QC"}
        d = dt.date(2024, 12, 1)
        cur = None
        k = 0
        while d <= dt.date(2025, 12, 31):
            while k < len(mine) and mine[k]["time"].date() <= d:
                k += 1
            # calibrations of the day
            for c in mine:
                if c["time"].date() != d:
                    continue
                if r.random() < 0.05:
                    rows.append([c["time"] - dt.timedelta(minutes=int(r.integers(30, 45))), sn, "CALIBRATION", "25OHD",
                                 lotno[c["lot"]], calno[c["calot"]], "", "FAILED", "CALIBRATION CURVE OUT OF RANGE"])
                rows.append([c["time"], sn, "CALIBRATION", "25OHD", lotno[c["lot"]], calno[c["calot"]], "",
                             "ACCEPTED", ""])
                cur = c
            lot_now = None
            for c in mine:
                if c["time"].date() <= d:
                    lot_now = c
            if lot_now is None:
                d += dt.timedelta(days=1)
                continue
            base = dt.datetime.combine(d, dt.time(5, 30))
            rows.append([base + dt.timedelta(minutes=int(r.integers(0, 15))), sn, "MAINTENANCE", "", "", "", "",
                         "DONE", "DAILY"])
            if d.weekday() == 6:
                rows.append([base + dt.timedelta(minutes=int(r.integers(20, 50))), sn, "MAINTENANCE", "", "", "",
                             "", "DONE", "WEEKLY"])
            if d.day == 1:
                rows.append([base + dt.timedelta(minutes=int(r.integers(55, 80))), sn, "MAINTENANCE", "", "", "",
                             "", "DONE", "MONTHLY"])
            for hh, mm in ((6, 50), (14, 30)):
                tq = dt.datetime.combine(d, dt.time(hh, mm)) + dt.timedelta(minutes=int(r.integers(0, 25)))
                fail = (d in qc_days and hh == 6)
                for lvl in ("1", "2"):
                    out = "FAIL" if (fail and (lvl == "1" or r.random() < 0.5)) else "PASS"
                    rule = "1-3S" if out == "FAIL" else ""
                    rows.append([tq + dt.timedelta(minutes=int(lvl)), sn, "QC", "25OHD", lotno[lot_now["lot"]], "",
                                 lvl, out, rule])
                if not fail and r.random() < 0.012:
                    tq2 = tq + dt.timedelta(minutes=int(r.integers(18, 30)))
                    rows.append([tq + dt.timedelta(minutes=3), sn, "QC", "25OHD", lotno[lot_now["lot"]], "", "2",
                                 "FAIL", "1-2S"])
                    rows.append([tq2, sn, "QC", "25OHD", lotno[lot_now["lot"]], "", "2", "PASS", "RERUN"])
            if r.random() < 0.38:
                rows.append([dt.datetime.combine(d, dt.time(int(r.integers(9, 20)), int(r.integers(0, 60)))), sn,
                             "REAGENT_LOAD", "25OHD", lotno[lot_now["lot"]], "", "", "DONE", "PACK %d" % int(r.integers(1, 4))])
            if r.random() < 0.07:
                rows.append([dt.datetime.combine(d, dt.time(int(r.integers(8, 22)), int(r.integers(0, 60)))), sn,
                             "ERROR", "25OHD", "", "", "", "SAMPLE", str(r.choice(["CLOT DETECTED", "SHORT SAMPLE",
                                                                                  "BUBBLE DETECTED", "LLD ERROR"]))])
            d += dt.timedelta(days=1)
        for i, (nm, d1, d2) in enumerate(K.CAL_LOTS):
            dd = (d1, d2)[an]
            if dd >= dt.date(2024, 12, 1):
                rows.append([dt.datetime.combine(dd, dt.time(5, 55)), sn, "CALIBRATOR_LOT", "25OHD", "", nm, "",
                             "REGISTERED", "NEW CALIBRATOR LOT"])
    rows.sort(key=lambda x: (x[0], x[1], x[2]))
    return [[W.to_utc(x[0])] + x[1:] for x in rows]
