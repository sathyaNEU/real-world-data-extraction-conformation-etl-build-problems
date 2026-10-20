"""The pack's data files, cut from the clean truth: the data acquisition system's hourly export for every monitored
unit (standard time), the monitor outage tickets, the gas supplier's daily invoices, the outage event report and the
ambient ozone monitor's daily values (a distractor)."""
import csv
import datetime as dt
import functools

import numpy as np

import records as R
import sources as S
import world as W

FACILITY = {"Cutler Bend": "Cutler Bend Energy Center", "Ashfork": "Ashfork Generating Station",
            "Dunmore Flats": "Dunmore Flats Power Plant", "Sable Ridge": "Sable Ridge Energy Center",
            "Holt Creek": "Holt Creek Station"}
DAHS_COLS = ["FACILITY_NAME", "UNIT_ID", "OP_DATE", "OP_HOUR", "OP_TIME", "GLOAD_MW", "HEAT_INPUT_MMBTU",
             "NOX_RATE_LB_MMBTU", "NOX_MASS_LB", "NOX_STATUS"]
EXPORT_END = dt.date(2026, 10, 18)
TICKET_COLS = ["ticket", "unit", "opened_local", "closed_local", "component", "description"]
INV_COLS = ["invoice_no", "delivery_point", "gas_day", "quantity_dth", "price_usd_per_dth", "amount_usd"]
EVENT_COLS = ["unit", "event_no", "event_type", "start_local", "end_local", "cause_code", "derate_mw", "date_reported"]
OZONE_COLS = ["site_id", "site_name", "date", "max_8hr_ozone_ppm", "aqi"]


@functools.lru_cache(None)
def everything():
    rng = np.random.default_rng(W.SEED)
    fleet = S.fleet(rng)
    asks = R.build(np.random.default_rng(W.SEED + 1000), fleet)
    return dict(fleet=fleet, asks=asks)


def dahs_rows(x):
    out = []
    f = x["fleet"]
    order = sorted(f, key=lambda u: (f[u]["plant"], u))
    for u in order:
        v = f[u]
        fac = FACILITY[v["plant"]]
        for h, t in enumerate(S.HOURS):
            if t.date() > EXPORT_END:
                break
            if not v["on"][h]:
                out.append([fac, u, t.strftime("%Y-%m-%d"), t.hour, "0.00", "", "", "", "", ""])
                continue
            heat = float(v["heat"][h])
            if v["out"][h]:
                out.append([fac, u, t.strftime("%Y-%m-%d"), t.hour, "1.00", "%.2f" % v["load"][h], "%.1f" % heat, "", "",
                            str(v["status"][h])])
            else:
                lb = float(v["lb"][h])
                out.append([fac, u, t.strftime("%Y-%m-%d"), t.hour, "1.00", "%.2f" % v["load"][h], "%.1f" % heat,
                            "%.4f" % (lb / heat if heat else 0), "%.1f" % lb, "OK"])
    return out


def ticket_rows(x):
    rng = np.random.default_rng(W.SEED + 77)
    out = []
    n = 5100
    desc = {"NOx analyzer": ["Daily calibration error over limit, recalibrated", "Analyzer drift, span adjusted",
                             "NOx converter efficiency low", "Analyzer fault alarm, reset"],
            "Sample system": ["Sample line heater fault", "Probe blowback, filter replaced", "Moisture in sample line"],
            "DAHS": ["Communication loss to DAHS", "DAHS server restart"],
            "O2 analyzer": ["O2 cell replaced", "O2 span gas changed"]}
    f = x["fleet"]
    air = ["Probe dilution air pressure low; plant instrument air header down",
           "Loss of dilution air to probe (plant instrument air trip)",
           "Dilution air supply lost, plant air compressor tripped"]
    for u in sorted(W.CC):
        v = f[u]
        for h0, d in v["air_events"]:
            hs = [h for h in range(h0, min(S.NH, h0 + d)) if v["air"][h]]
            if not hs:
                continue
            n += int(rng.integers(1, 4))
            op = R.local_of(S.HOURS[hs[0]]) + dt.timedelta(minutes=int(rng.integers(2, 41)))
            cl = R.local_of(S.HOURS[hs[-1] + 1]) - dt.timedelta(minutes=int(rng.integers(1, 13)))
            out.append(["MT-%d" % n, u, op.strftime("%m/%d/%Y %H:%M"), cl.strftime("%m/%d/%Y %H:%M"), "Sample system",
                        str(rng.choice(air))])
        h = 0
        normal = v["out"] & ~v["air"]
        while h < S.NH:
            if normal[h]:
                k = h
                while k < S.NH and normal[k]:
                    k += 1
                if rng.random() < .72:
                    comp = str(rng.choice(list(desc), p=[.55, .2, .15, .1]))
                    n += int(rng.integers(1, 4))
                    op = R.local_of(S.HOURS[h]) + dt.timedelta(minutes=int(rng.integers(0, 50)))
                    cl = R.local_of(S.HOURS[k]) + dt.timedelta(minutes=int(rng.integers(-20, 90)))
                    out.append(["MT-%d" % n, u, op.strftime("%m/%d/%Y %H:%M"), cl.strftime("%m/%d/%Y %H:%M"), comp,
                                str(rng.choice(desc[comp]))])
                h = k
            h += 1
        for _ in range(int(rng.integers(3, 9))):
            hh = int(rng.integers(0, S.NH - 30))
            if not v["on"][hh]:
                n += 1
                op = R.local_of(S.HOURS[hh])
                out.append(["MT-%d" % n, u, op.strftime("%m/%d/%Y %H:%M"),
                            (op + dt.timedelta(hours=int(rng.integers(1, 8)))).strftime("%m/%d/%Y %H:%M"),
                            "NOx analyzer", "Quarterly linearity check"])
    out = [r for r in out if dt.datetime.strptime(r[2], "%m/%d/%Y %H:%M").date() <= EXPORT_END]
    out = [r[:3] + ([""] if dt.datetime.strptime(r[3], "%m/%d/%Y %H:%M").date() > EXPORT_END else [r[3]]) + r[4:]
           for r in out]
    out.sort(key=lambda r: dt.datetime.strptime(r[2], "%m/%d/%Y %H:%M"))
    # ticket numbers run in the order the tickets were opened
    num, step = 5100, np.random.default_rng(W.SEED + 78)
    for r in out:
        num += int(step.integers(1, 4))
        r[0] = "MT-%d" % num
    return out


def invoice_rows(x):
    return [[i["invoice"], FACILITY[i["plant"]], i["gas_day"].strftime("%Y-%m-%d"), "%.1f" % i["dth"],
             "%.4f" % i["price"], "%.2f" % i["amount"]] for i in x["asks"]["invoices"]
            if i["gas_day"] <= dt.date(2026, 9, 30)]


def event_rows(x):
    out = []
    for e in x["asks"]["events"]:
        if e["filed"] > dt.date(2026, 10, 16):
            continue
        out.append([e["unit"], e["event"], e["type"], e["start"].strftime("%Y-%m-%d %H:%M"),
                    e["end"].strftime("%Y-%m-%d %H:%M"), e["cause"], e.get("derate", ""), e["filed"].isoformat()])
    return out


def ozone_rows(x):
    rng = np.random.default_rng(W.SEED + 88)
    sites = [("52-031-0004", "Cutler Bend South"), ("52-077-0011", "Ashfork Airport"), ("52-105-0002", "Dunmore")]
    out = []
    for sid, nm in sites:
        v = .045
        for d in range(122, 274):
            day = dt.date(2026, 1, 1) + dt.timedelta(d - 1)
            v = min(.085, max(.028, v + rng.normal(0, .006) + (.0008 if day.month in (6, 7) else -.0004)))
            ppm = round(v, 3)
            aqi = int(round(ppm / .054 * 50)) if ppm <= .054 else int(round(51 + (ppm - .055) / .015 * 49))
            out.append([sid, nm, day.isoformat(), "%.3f" % ppm, aqi])
    return out


def write_csv(path, cols, rows, crlf=False):
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, lineterminator="\r\n" if crlf else "\n")
        w.writerow(cols)
        w.writerows(rows)
    return len(rows)
