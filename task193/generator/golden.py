"""The golden, computed from the cut pack the way the plan and the field procedure require: both laboratories'
deliverables conformed, the background results classified by the head relation at the waste boundary on each event's
gauging, the plan's limits, the October 2026 comparison, and the two field figures for every well sampled that
October."""
import csv
import datetime as dt
import math
import os
from zoneinfo import ZoneInfo

import routes as RT
import world as W

EV = [e["label"] for e in W.EVENTS]
IND_A = {"Chloride": "chloride", "Sodium, Dissolved": "sodium", "Boron, Dissolved": "boron"}
IND_B = {("Chloride", "N"): "chloride", ("Sodium", "D"): "sodium", ("Boron", "D"): "boron"}


def event_of(day):
    for i, e in enumerate(W.EVENTS):
        if day in e["days"]:
            return i
    raise ValueError(day)


def norm_loc(s):
    s = s.strip().upper()
    if s.startswith("MW-") and s[3:].isdigit():
        return "MW-%d" % int(s[3:])
    if s.startswith("MW-") and s[3:-1].isdigit() and s.endswith("R"):
        return "MW-%dR" % int(s[3:-1])
    return s


def read_indicators(tgt, files):
    """{(location, event, indicator): reportable primary result}, boron in ug/L"""
    out = {}
    with open(os.path.join(tgt, files["edd_a"]), encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r["Sample_Type"] != "N" or r["Reportable"] != "Y" or r["Parameter"] not in IND_A:
                continue
            loc = norm_loc(r["Location"])
            if not loc.startswith("MW"):
                continue
            k = IND_A[r["Parameter"]]
            v = float(r["Result"])
            if k == "boron" and r["Units"] == "mg/L":
                v = round(v * 1000.0, 6)
            ei = event_of(dt.datetime.strptime(r["Sample_Date"], "%m/%d/%Y").date())
            assert (loc, ei, k) not in out, (loc, ei, k)
            out[(loc, ei, k)] = v
    with open(os.path.join(tgt, files["edd_b"]), encoding="utf-8") as f:
        for r in csv.DictReader(f, delimiter="\t"):
            if r["sample_type_code"] != "N" or r["reportable_result"] != "Yes":
                continue
            key = (r["chemical_name"], r["fraction"])
            if key not in IND_B or not r["sys_loc_code"].startswith("MW"):
                continue
            k = IND_B[key]
            v = float(r["result_value"])
            if k == "boron" and r["result_unit"] == "mg/L":
                v *= 1000.0
            ei = event_of(dt.date.fromisoformat(r["sample_date"][:10]))
            loc = norm_loc(r["sys_loc_code"])
            assert (loc, ei, k) not in out, (loc, ei, k)
            out[(loc, ei, k)] = v
    return out


def read_heads(tgt, files):
    """{(point, event): head in the datum of the survey in force on the gauging date} with that datum"""
    from openpyxl import load_workbook
    wb = load_workbook(os.path.join(tgt, files["points"]), read_only=True)
    surveys = {}
    for row in list(wb["Survey"].iter_rows(values_only=True))[1:]:
        p, d, datum, toc = row[0], dt.date.fromisoformat(str(row[1])[:10]), row[2], float(row[3])
        surveys.setdefault(p, []).append((d, datum, toc))
    heads = {}
    with open(os.path.join(tgt, files["gauging"]), encoding="utf-8") as f:
        for r in csv.DictReader(f):
            p = r["location"]
            d = dt.date.fromisoformat(r["date"])
            ei = EV.index(r["event"])
            ss = sorted(x for x in surveys[p] if x[0] <= d)
            sd, datum, toc = ss[-1]
            heads[(p, ei)] = (round(toc - float(r["dtw_ft_btoc"]), 2), datum)
    return heads


def reversed_events(heads):
    """a background well is reversed on an event when its head stands below its boundary piezometer's, both read
    against the survey in force that day (one datum)"""
    rev = {}
    for w in W.BACKGROUND:
        for ei in range(len(EV)):
            hw, dw = heads[(w, ei)]
            hp, dp = heads[(W.BOUNDARY[w], ei)]
            assert dw == dp
            rev[(w, ei)] = hw < hp
    return rev


def read_purge(tgt, files):
    rows = []
    with open(os.path.join(tgt, files["purge"]), encoding="utf-8") as f:
        for r in csv.DictReader(f):
            r["t"] = dt.datetime.strptime(r["entry_utc"], "%Y-%m-%dT%H:%M:%SZ")
            rows.append(r)
    return rows


def read_calib(tgt, files):
    """the field app's calibration entries: for each sonde and day, whether its conductivity reports at 25 C (the units
    of the morning calibration; the end-of-day check is read back by the checks)"""
    mode = {}
    with open(os.path.join(tgt, files["calib"]), encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r["sensor"] == "Conductivity" and r["check_type"] == "calibration":
                mode[(r["cal_date"], r["meter_sn"])] = r["reading_units"] == "uS/cm at 25 C"
    return mode


CENTRAL = ZoneInfo("America/Chicago")


def read_coc(tgt, files, event_days):
    """each well's sample collection time on the laboratory's deliverable (the chain of custody's local minute), as UTC"""
    days = {d.isoformat() for d in event_days}
    coc = {}
    with open(os.path.join(tgt, files["edd_b"]), encoding="utf-8") as f:
        for r in csv.DictReader(f, delimiter="\t"):
            if r["sample_type_code"] != "N" or not r["sys_loc_code"].startswith("MW") or r["sample_date"][:10] not in days:
                continue
            local = dt.datetime.strptime(r["sample_date"], "%Y-%m-%d %H:%M").replace(tzinfo=CENTRAL)
            utc = local.astimezone(dt.timezone.utc).replace(tzinfo=None)
            w = norm_loc(r["sys_loc_code"])
            assert coc.get(w, utc) == utc, (w, coc.get(w), utc)
            coc[w] = utc
    return coc


def field_asks(rows, event_days, cal_mode, coc):
    """for every well sampled that event: specific conductance at 25 C from the set the sample was collected
    immediately after (FS-03 3: the last set the field app logged before the chain of custody's collection time),
    corrected to 25 C where the day's calibration shows the meter reporting conductivity at the sample's temperature,
    and the purge volume from the controller's day counter to that set"""
    spc, purge, detail = {}, {}, {}
    days = {d.strftime("%Y-%m-%d") for d in event_days}
    by_day = {}
    for r in rows:
        if r["visit_date"] in days:
            by_day.setdefault(r["visit_date"], []).append(r)
    for day, rs in by_day.items():
        rs = sorted(rs, key=lambda r: r["t"])
        meter = ""
        for r in rs:            # FS-03 3: the serial is recorded with the day's first set and whenever the meter changes
            r["meter_logged"] = bool(r["meter_sn"])
            if r["meter_sn"]:
                meter = r["meter_sn"]
            elif r["remark"] not in ("decon rinse", "bottles filled, pump off"):
                r["meter_sn"] = meter
        mark = 0.0                      # the controller counter when the pump last stopped (zeroed each morning)
        start, at = {}, {}
        for r in rs:
            if r["remark"] in ("decon rinse", "bottles filled, pump off"):
                mark = float(r["controller_l"])
                continue
            w = r["location"]
            start.setdefault(w, mark)
            if r["t"] <= coc[w]:
                at[w] = r                # the last set logged before the sample was collected
        for w, r in at.items():
            end = float(r["controller_l"])
            purge[w] = (end - start[w]) / W.L_PER_GAL
            cond = float(r["spc_us_cm"])
            T = float(r["temperature_c"])
            compensated = cal_mode[(r["visit_date"], r["meter_sn"])]
            if not compensated:          # FS-03 4: conductivity corrected to 25 C at 1.91 per cent per degree
                cond = cond / (1 + W.TEMP_COEF * (T - 25.0))
            spc[w] = cond
            later = [x for x in rs if x["location"] == w and x["remark"] == "" and x["t"] > r["t"]]
            detail[w] = {"start_l": start[w], "end_l": end, "meter": r["meter_sn"],
                         "recorded": float(r["spc_us_cm"]), "temp": T, "compensated": compensated,
                         "meter_logged": r["meter_logged"], "set_utc": r["t"], "coc_utc": coc[w],
                         "sets_after_sample": len(later)}
    return spc, purge, detail


def compute(tgt, files):
    ind = read_indicators(tgt, files)
    heads = read_heads(tgt, files)
    rev = reversed_events(heads)
    bg = {(w, ei, k): v for (w, ei, k), v in ind.items() if w in W.BACKGROUND and ei in W.BG_EVENTS}
    hdiff = {(w, ei): heads[(w, ei)][0] - heads[(W.BOUNDARY[w], ei)][0] for w in W.BACKGROUND for ei in range(len(EV))}
    lim, cnt = RT.background_limits(bg, rev, EV, W.DRY, hdiff)
    G = lim[RT.GOLDEN]
    october = {(w, k): ind[(w, W.EVAL, k)] for w in W.COMPLIANCE for k in W.INDICATORS}
    resample = RT.designate(G, october)
    sets = {r: RT.designate(lim[r], october) for r in lim}
    hist = {}
    for (w, ei, k), v in ind.items():
        if w in W.COMPLIANCE + ["MW-5"] and ei < W.EVAL:
            hist.setdefault(("MW-5R" if w == "MW-5" else w, k), []).append(v)
    sets["R2f intrawell, each well against its own record"] = RT.intrawell(hist, october)
    rows = read_purge(tgt, files)
    spc, purge, fdetail = field_asks(rows, W.EVENTS[W.EVAL]["days"], read_calib(tgt, files),
                                     read_coc(tgt, files, W.EVENTS[W.EVAL]["days"]))
    excluded = sorted(((w, EV[ei]) for (w, ei), r in rev.items() if r and ei in W.BG_EVENTS),
                      key=lambda x: (W.BACKGROUND.index(x[0]), EV.index(x[1])))
    exceed = {(w, k): october[(w, k)] > G[k] for w in W.COMPLIANCE for k in W.INDICATORS}
    head_diff = {(w, ei): round(heads[(w, ei)][0] - heads[(W.BOUNDARY[w], ei)][0], 2)
                 for w in W.BACKGROUND for ei in range(len(EV))}
    return {"indicators": ind, "heads": heads, "rev": rev, "bg": bg, "limits": lim, "counts": cnt, "golden": G,
            "golden_n": cnt[RT.GOLDEN], "october": october, "resample": resample, "sets": sets, "spc": spc,
            "purge": purge, "field_detail": fdetail, "excluded": excluded, "exceed": exceed, "head_diff": head_diff,
            "history": hist}


def sig3(x):
    d = 3 - int(math.floor(math.log10(abs(x)))) - 1
    return round(x, d)
