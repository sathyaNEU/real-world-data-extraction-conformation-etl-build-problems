"""task131 generator: the billing system's account history, the trial register, the March survey, the weather
files and the three files the solution never reads (zone substation loads, rooftop PV connections, generation
availability)."""
from datetime import date, datetime, timedelta

import numpy as np
import pandas as pd

import params as P
import knobs as K
import weather as WX

HIST_PULLED = date(2026, 3, 12)


def _d(x):
    return x.isoformat() if x else ""


def account_history(hh, ev, newp, occ, exch, seed):
    """one row per account, register and tariff period, as the billing system holds it on 12 March 2026"""
    rng = np.random.default_rng(seed)
    rows = []
    n = P.N_HH
    starts = {}
    for i in range(n):
        y = int(rng.integers(2011, 2025))
        m = int(rng.integers(1, 13)) if y < 2024 else int(rng.integers(1, 11))
        starts[i] = date(y, m, int(rng.integers(1, 28)))

    def add(cust, acct, nmi, reg, code, f, t, why_in, why_out, keyed):
        rows.append({"customer_id": cust, "account_id": acct, "nmi": nmi, "register": reg, "tariff_code": code,
                     "valid_from": _d(f), "valid_to": _d(t), "start_reason": why_in, "end_reason": why_out,
                     "keyed_on": _d(keyed)})

    trial_end = P.END
    for i in range(n):
        a = hh["arm"][i]
        cust, acct, nmi = hh["customer"][i], hh["account"][i], hh["nmi"][i]
        st = starts[i]
        evs = ev[i]
        leave = next((e for e in evs if e[0] == "leave"), None)
        move = next((e for e in evs if e[0] in ("move_keep", "move_home", "return_move")), None)
        close = leave[1] - timedelta(1) if leave else (move[1] - timedelta(1) if move else None)
        close_why = leave[2] if leave else ("MOVE OUT" if move else "")
        # general supply
        if a == "CTRL":
            add(cust, acct, nmi, "E1", P.CODE["HOME"], st, close, "MOVE IN", close_why, st)
        else:
            code = P.CODE[a]
            add(cust, acct, nmi, "E1", P.CODE["HOME"], st, P.START - timedelta(1), "MOVE IN", "TARIFF CHANGE", st)
            cur_from, cur_code, cur_why = P.START, code, "TRIAL START"
            keyed = date(2025, 11, 24)
            for kind, d, why in evs:
                if kind in ("return", "lifesupport"):
                    add(cust, acct, nmi, "E1", cur_code, cur_from, d - timedelta(1), cur_why, "TARIFF CHANGE", keyed)
                    cur_from, cur_code, cur_why = d, P.CODE["HOME"], why
                    keyed = d - timedelta(1) if kind == "return" else d
                elif kind == "withdrawn":
                    add(cust, acct, nmi, "E1", cur_code, cur_from, d - timedelta(1), cur_why, "TARIFF CHANGE", keyed)
                    add(cust, acct, nmi, "E1", P.CODE["HOME"], d, d - timedelta(1), "CUSTOMER REQUEST", "CANCELLED", d - timedelta(1))
                    cur_from, cur_code, cur_why = d, code, "CORRECTION"
                    keyed = d + timedelta(int(rng.integers(2, 6)))
            if close is not None:
                add(cust, acct, nmi, "E1", cur_code, cur_from, close, cur_why, close_why, keyed)
            elif cur_code == code:
                add(cust, acct, nmi, "E1", cur_code, cur_from, trial_end, cur_why, "TRIAL END", keyed)
                add(cust, acct, nmi, "E1", P.CODE["HOME"], trial_end + timedelta(1), None, "TRIAL END", "", date(2026, 2, 23))
            else:
                add(cust, acct, nmi, "E1", cur_code, cur_from, None, cur_why, "", keyed)
        # controlled load and export registers
        if hh["e2"][i]:
            add(cust, acct, nmi, "E2", P.CODE["CL"], st, close, "MOVE IN", close_why, st)
        if hh["pv0"][i]:
            f = max(st, date(2015, 1, 1) + timedelta(int(rng.integers(0, 3300))))
            f = min(f, date(2025, 9, 30))
            add(cust, acct, nmi, "B1", "BB1", f, close, "PV CONNECTION", close_why, f)
        elif i in exch and exch[i]["why"] == "PV":
            add(cust, acct, nmi, "B1", "BB1", exch[i]["date"], close, "PV CONNECTION", close_why, exch[i]["date"])
        # the new occupant at the trial NMI
        if i in occ:
            o = occ[i]
            add(o["customer"], o["account"], nmi, "E1", P.CODE["HOME"], o["date"], None, "MOVE IN", "", o["date"])
            if hh["e2"][i]:
                add(o["customer"], o["account"], nmi, "E2", P.CODE["CL"], o["date"], None, "MOVE IN", "", o["date"])
            if hh["pv0"][i] or (i in exch and exch[i]["why"] == "PV"):
                add(o["customer"], o["account"], nmi, "B1", "BB1", o["date"], None, "MOVE IN", "", o["date"])
        # the household's new premise in Murrandi
        if i in newp:
            r = newp[i]
            d = r["date"]
            if r["kind"] == "move_keep":
                add(cust, r["account"], r["nmi"], "E1", P.CODE[a], d, trial_end, "TRANSFER - TRIAL", "TRIAL END", d + timedelta(int(rng.integers(1, 5))))
                add(cust, r["account"], r["nmi"], "E1", P.CODE["HOME"], trial_end + timedelta(1), None, "TRIAL END", "", date(2026, 2, 23))
            else:
                add(cust, r["account"], r["nmi"], "E1", P.CODE["HOME"], d, None, "MOVE IN", "", d)
            if hh["e2"][i]:
                add(cust, r["account"], r["nmi"], "E2", P.CODE["CL"], d, None, "MOVE IN", "", d)
    df = pd.DataFrame(rows)
    df = df.sort_values(["account_id", "register", "valid_from", "keyed_on"], kind="mergesort").reset_index(drop=True)
    return df


def register(hh):
    df = pd.DataFrame({
        "trial_id": hh["trial_id"], "customer_id": hh["customer"], "account_id": hh["account"], "nmi": hh["nmi"],
        "block": hh["block"], "arm": ["CONTROL" if a == "CTRL" else "DESIGN " + a for a in hh["arm"]],
        "rooftop_pv": np.where(hh["pv0"], "Y", "N"), "hot_water_circuit": np.where(hh["e2"], "Y", "N"),
        "summer_2024_25_4to9pm_kw": hh["prior_kw"],
    })
    return df.sort_values(["block", "trial_id"]).reset_index(drop=True)


def survey(hh, ev, seed):
    """the March 2026 survey of design households: web first, then telephone for those who had not answered"""
    rng = np.random.default_rng(seed)
    n = P.N_HH
    rows = []
    p_like = K.SURVEY_STAY
    gone = {i for i, es in ev.items() if any(e[0] == "leave" for e in es)}
    rid = 260000
    for i in range(n):
        a = hh["arm"][i]
        if a not in P.DESIGNS:
            continue
        p_web = 0.40 if i in gone else 0.47
        stay = rng.random() < p_like[a]
        strength = rng.random() < 0.42
        if stay:
            lik = 5 if strength else 4
        else:
            lik = 1 if rng.random() < 0.34 else (2 if rng.random() < 0.6 else 3)
        und = int(np.clip(round(rng.normal(3.9, 0.9)), 1, 5))
        bill = int(np.clip(round(rng.normal(3.1, 1.0)), 1, 5))
        comf = int(np.clip(round(rng.normal(3.4 if a == "A" else (3.0 if a == "B" else 3.7), 1.0)), 1, 5))
        rec = int(np.clip(round(rng.normal(3.0 + (0.8 if stay else -0.6), 0.9)), 1, 5))
        web = rng.random() < p_web
        phone = (not web) and rng.random() < 0.31
        done = []
        if web:
            done.append("WEB")
        if phone:
            done.append("CATI")
            if rng.random() < 0.035:
                done.append("WEB")      # answered the reminder link after the call
        for k, mode in enumerate(done):
            rid += int(rng.integers(1, 7))
            if mode == "WEB":
                day = date(2026, 3, 2) + timedelta(int(rng.integers(0, 12))) if k == 0 else date(2026, 3, 20) + timedelta(int(rng.integers(0, 5)))
            else:
                day = date(2026, 3, 12) + timedelta(int(rng.integers(0, 10)))
            hh_ = int(rng.integers(7, 21)) if mode == "WEB" else int(rng.integers(9, 20))
            t0 = datetime(day.year, day.month, day.day, hh_, int(rng.integers(0, 60)))
            t1 = t0 + timedelta(minutes=int(rng.integers(4, 15)))
            complete = rng.random() > 0.04
            q4 = lik
            if mode == "WEB":
                q4 = 6 - lik                 # the web form lists very likely first
            unanswered = rng.random() <= 0.025       # both modes need Q4 answered before a response can be submitted
            if not complete:
                q4 = q4 if (rng.random() < 0.5 and not unanswered) else None
            rows.append({"response_id": "R%d" % rid, "trial_id": hh["trial_id"][i], "mode": mode,
                         "started_at": t0.strftime("%Y-%m-%d %H:%M"), "submitted_at": t1.strftime("%Y-%m-%d %H:%M") if complete else "",
                         "complete": "Y" if complete else "N",
                         "q1_understood": und, "q2_bill": bill, "q3_comfort": comf,
                         "q4_stay": q4, "q5_recommend": rec if complete else None})
    df = pd.DataFrame(rows)
    df = df.sort_values(["started_at", "response_id"], kind="mergesort").reset_index(drop=True)
    df["q4_stay"] = df["q4_stay"].astype("Int64")
    df["q5_recommend"] = df["q5_recommend"].astype("Int64")
    return df


def weather_files(tmax, tmin):
    """the Bureau's daily maximum product for Murrandi Aero and the station's half-hourly observations"""
    missing = {date(2025, 12, 7), date(2025, 12, 8)}
    d_rows = []
    for d in WX.WDAYS:
        v = "" if d in missing else ("%.1f" % tmax[d])
        q = "" if d in missing else ("N" if d >= date(2026, 3, 1) else "Y")
        d_rows.append({"Product code": "IDCJAC0010", "Bureau of Meteorology station number": "013027", "Year": d.year,
                       "Month": "%02d" % d.month, "Day": "%02d" % d.day, "Maximum temperature (Degree C)": v,
                       "Days of accumulation of maximum temperature": "1" if v else "", "Quality": q})
    daily = pd.DataFrame(d_rows)
    hh_rows = []
    prev = tmax[WX.W0]
    rng = np.random.default_rng(P.SEED + 909)
    for d in WX.WDAYS:
        if d < date(2025, 11, 1) or d > date(2026, 2, 28):
            prev = tmax[d]
            continue
        tr = WX.trace(tmax[d], tmin[d], prev)
        prev = tmax[d]
        if d in missing:
            continue
        for k in range(48):
            t = datetime(d.year, d.month, d.day) + timedelta(minutes=30 * k)
            temp = min(tr[k] + rng.normal(0, 0.25), tmax[d] - 0.1)   # a spot reading never tops the day's maximum
            rh = float(np.clip(62 - 1.25 * (temp - 20) + rng.normal(0, 4), 5, 95))
            hh_rows.append({"hm": "hm", "Station Number": "013027", "Year Month Day Hours Minutes in YYYY": t.year,
                            "MM": "%02d" % t.month, "DD": "%02d" % t.day, "HH24": "%02d" % t.hour,
                            "MI format in Local time": "%02d" % t.minute,
                            "Air Temperature in degrees C": "%.1f" % temp, "Quality of air temperature": "N",
                            "Relative humidity in percentage %": "%d" % round(rh), "Quality of relative humidity": "N", "#": "#"})
    return daily, pd.DataFrame(hh_rows)


def zone_loads(tmax, seed):
    rng = np.random.default_rng(seed)
    zones = [("MRN North", 0.34), ("MRN South", 0.29), ("MRN East", 0.22), ("MRN Industrial", 0.15)]
    rows = []
    prev = tmax[P.DATA_FROM - timedelta(1)]
    for d in P.DAYS:
        tr = WX.trace(tmax[d], tmax[d] - 12.5, prev)
        prev = tmax[d]
        wk = d.weekday() >= 5 or d in P.HOLIDAYS
        for k in range(48):
            h = (k + 0.5) / 2
            ac = max(0.0, np.roll(tr, 3)[k] - 24) * 3.9
            pv_dip = 22 * max(0.0, np.sin(np.pi * (h - 5.8) / 13.4)) if 5.8 < h < 19.2 else 0
            base = 98 + 26 * np.exp(-0.5 * ((h - 19.3) / 2.4) ** 2) + (0 if wk else 9 * np.exp(-0.5 * ((h - 11) / 4) ** 2))
            tot = base + ac - pv_dip
            t_end = datetime(d.year, d.month, d.day) + timedelta(minutes=30 * (k + 1))
            for z, share in zones:
                f = share * (1.25 if (z == "MRN Industrial" and not wk) else 1.0)
                rows.append({"zone_substation": z, "interval_ending": t_end.strftime("%Y-%m-%d %H:%M"),
                             "mw": "%.2f" % (tot * f * (1 + rng.normal(0, 0.012)))})
    return pd.DataFrame(rows)


def pv_connections(hh, exch, seed):
    rng = np.random.default_rng(seed)
    rows = []
    suburbs = ["Murrandi Central", "Murrandi North", "Murrandi East", "Murrandi South", "Airport Estate", "Railway Flats",
               "Hospital Hill", "Lakeside"]
    trial = {hh["nmi"][i]: i for i in range(P.N_HH)}
    taken = set(trial)
    k = 0
    for nmi, i in trial.items():
        if hh["pv0"][i] or (i in exch and exch[i]["why"] == "PV"):
            k += 1
            conn = (exch[i]["date"] if (i in exch and exch[i]["why"] == "PV")
                    else date(2015, 1, 1) + timedelta(int(rng.integers(0, 3800))))
            appr = conn - timedelta(int(rng.integers(12, 70)))
            kw = float(hh["pvkw"][i]) if hh["pv0"][i] else 5.0
            rows.append(_pvrow(rng, nmi, suburbs, kw, appr, conn))
    while len(rows) < 3180:
        nmi = "8090" + "".join(str(v) for v in rng.integers(0, 10, 6))
        if nmi in taken:
            continue
        taken.add(nmi)
        conn = date(2014, 6, 1) + timedelta(int(rng.integers(0, 4400)))
        appr = conn - timedelta(int(rng.integers(12, 90)))
        kw = float(rng.choice([2.0, 3.0, 4.0, 5.0, 6.6, 8.0, 10.0], p=[.05, .12, .2, .27, .26, .07, .03]))
        rows.append(_pvrow(rng, nmi, suburbs, kw, appr, conn if conn <= date(2026, 6, 20) else None))
    df = pd.DataFrame(rows).sort_values(["approved", "application_id"]).reset_index(drop=True)
    return df


def _pvrow(rng, nmi, suburbs, kw, appr, conn):
    inv = {2.0: 2.0, 3.0: 3.0, 4.0: 3.0, 5.0: 5.0, 6.6: 5.0, 8.0: 6.0, 10.0: 8.2}.get(kw, 5.0)
    return {"application_id": "PV%06d" % int(rng.integers(100000, 999999)), "nmi": nmi,
            "suburb": suburbs[int(rng.integers(0, len(suburbs)))], "panel_kw": "%.1f" % kw, "inverter_kw": "%.1f" % inv,
            "export_limit_kw": "%.1f" % min(inv, 5.0), "approved": appr.isoformat(), "connected": conn.isoformat() if conn else ""}
