"""Every rung, the golden and every ask figure, computed from target/ alone.

    python3 task149/generator/analysis.py [target_dir]

The variants the fork table licenses are computed beside the golden so checks.py can assert each one inside
its graded bin."""
import collections
import csv
import datetime as dt
import json
import os
import re
import sys
from zoneinfo import ZoneInfo

from openpyxl import load_workbook

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import io_util as IO  # noqa: E402

LOCAL = ZoneInfo("Europe/Dublin")
UTC = ZoneInfo("UTC")
F = {
    "stays": "mobility_stays_2027w36_w47.csv", "devices": "mobility_devices_2027w36_w47.csv",
    "cells": "cell_zone_lookup_v3.csv", "census": "census2022_pow_rathgarvan_catchment.xlsx",
    "case": "rathgarvan_fbc_demand_refresh_dec2027.pdf", "gates": "ardnagree_line_gate_entries_20180101_20271130.csv",
    "register": "ardnagree_line_station_register.csv", "calendar": "kilcarrow_calendar_2018_2027.csv",
}
PANEL = (dt.date(2027, 9, 6), dt.date(2027, 11, 26))
LONG_MIN = 240
AM = (7 * 60, 9 * 60 + 30)


def rd(path):
    with open(path, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def utc(s):
    return dt.datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=UTC)


def loc(s):
    return utc(s).astimezone(LOCAL).replace(tzinfo=None)


def load(target):
    T = lambda k: os.path.join(target, F[k])  # noqa: E731
    out = {}
    wb = load_workbook(T("census"), read_only=True, data_only=True)
    for sheet, key in (("Final release", "census"), ("Provisional release", "census_prov")):
        ws = wb[sheet]
        rows = list(ws.iter_rows(min_row=6, values_only=True))
        c = collections.Counter()
        names = {}
        for sa, code, name, k in rows:
            if code:
                c[code] += int(k)
                names[code] = name
        out[key], out[key + "_names"] = c, names
    text = IO.pdf_text(T("case"))
    out["case_text"] = text
    shares = {}
    for m in re.finditer(r"(KW\d\d)\s+(.+?)\s+(0\.\d\d|1\.00)", text):
        shares.setdefault(m.group(1), float(m.group(3)))
    out["shares"] = shares
    thr = re.search(r"carries ([\d,]+) or more commuter boardings", text)
    out["threshold"] = int(thr.group(1).replace(",", ""))
    cal = rd(T("calendar"))
    out["nonordinary"] = {dt.date.fromisoformat(r["date"]) for r in cal}
    out["cal"] = cal
    cells = collections.defaultdict(list)
    for r in rd(T("cells")):
        cells[r["cell_id"]].append((r["zone_code"], float(r["area_share"])))
    out["cells"] = cells
    out["devices"] = {r["device_id"]: r for r in rd(T("devices"))}
    st = collections.defaultdict(list)
    for r in rd(T("stays")):
        st[r["device_id"]].append((r["cell_id"], loc(r["stay_start_utc"]), loc(r["stay_end_utc"]),
                                   utc(r["stay_start_utc"]).replace(tzinfo=None), utc(r["stay_end_utc"]).replace(tzinfo=None)))
    for k in st:
        st[k].sort(key=lambda x: x[1])
    out["stays"] = st
    out["gates"] = [(dt.date.fromisoformat(r["date"]), r["station_code"], int(r["entries"])) for r in rd(T("gates"))]
    out["register"] = rd(T("register"))
    return out


def ordinary_days(D):
    d, out = PANEL[0], []
    while d <= PANEL[1]:
        if d.weekday() < 5 and d not in D["nonordinary"]:
            out.append(d)
        d += dt.timedelta(days=1)
    return out


def zone_major(D, cell):
    z = D["cells"].get(cell)
    if not z:
        return None
    return max(z, key=lambda x: (x[1], x[0]))[0]


def workers(D, long_min=LONG_MIN, min_long=3, rule="modal", tz="local", straddle="major"):
    """Each device with a usual workplace: (device, zone weights, commute-day set, observed ordinary days)."""
    days_all = ordinary_days(D)
    out = []
    for did, stays in D["stays"].items():
        dev = D["devices"][did]
        home = dev["home_cell"]
        longs = []
        for cell, s, e, su, eu in stays:
            if cell == home:
                continue
            if (e - s).total_seconds() < long_min * 60:
                continue
            longs.append((cell, s if tz == "local" else su))
        if len(longs) < min_long:
            continue
        zc = collections.Counter()
        for cell, s in longs:
            z = zone_major(D, cell)
            if z:
                zc[z] += 1
        if not zc:
            continue
        z, k = sorted(zc.items(), key=lambda x: (-x[1], x[0]))[0]
        if rule == "majority" and k < 0.5 * len(longs):
            continue
        first = loc(dev["first_seen_utc"]).date() if tz == "local" else utc(dev["first_seen_utc"]).date()
        last = loc(dev["last_seen_utc"]).date() if tz == "local" else utc(dev["last_seen_utc"]).date()
        obs = [d for d in days_all if first <= d <= last]
        cd = set()
        cellsets = collections.Counter()
        for cell, s in longs:
            if zone_major(D, cell) == z:
                if s.date() in set(days_all):
                    cd.add(s.date())
                cellsets[cell] += 1
        wz = {z: 1.0}
        if straddle == "split":
            main = cellsets.most_common(1)[0][0]
            if len(D["cells"].get(main, [])) > 1:
                wz = {zz: sh for zz, sh in D["cells"][main]}
        out.append((did, wz, cd, obs))
    return out


def frequencies(D, W, mode="ratio", days_filter=None):
    num, den, rates, n = collections.Counter(), collections.Counter(), collections.defaultdict(list), collections.Counter()
    for did, wz, cd, obs in W:
        if days_filter is not None:
            obs = [d for d in obs if days_filter(d)]
            cd = {d for d in cd if days_filter(d)}
        if not obs:
            continue
        for z, w in wz.items():
            num[z] += w * len(cd)
            den[z] += w * len(obs)
            rates[z].append((w, len(cd) / len(obs)))
            n[z] += w
    if mode == "ratio":
        return {z: num[z] / den[z] for z in den if den[z]}, n
    return {z: sum(w * r for w, r in rates[z]) / sum(w for w, r in rates[z]) for z in rates}, n


def boardings(D, f):
    rows, tot = {}, 0.0
    for z, s in sorted(D["shares"].items()):
        c = D["census"].get(z, 0)
        b = c * s * f.get(z, 0.0)
        rows[z] = b
        tot += b
    return rows, tot


def departures(D, W):
    """Per destination: share of commuting days on which the commuter left home between 07:00 and 09:30."""
    hit, tot = collections.Counter(), collections.Counter()
    days_all = set(ordinary_days(D))
    for did, wz, cd, obs in W:
        z = max(wz.items(), key=lambda x: x[1])[0]
        stays = D["stays"][did]
        home = D["devices"][did]["home_cell"]
        for i, (cell, s, e, su, eu) in enumerate(stays):
            if cell == home or (e - s).total_seconds() < LONG_MIN * 60 or zone_major(D, cell) != z:
                continue
            if s.date() not in days_all:
                continue
            prev = [x for x in stays[:i] if x[0] == home and x[2] <= s]
            if not prev:
                continue
            dep = prev[-1][2]
            m = dep.hour * 60 + dep.minute
            tot[z] += 1
            if AM[0] <= m <= AM[1]:
                hit[z] += 1
    return {z: hit[z] / tot[z] for z in tot}, tot


def departures_utc(D, W):
    hit, tot = collections.Counter(), collections.Counter()
    days_all = set(ordinary_days(D))
    for did, wz, cd, obs in W:
        z = max(wz.items(), key=lambda x: x[1])[0]
        stays = D["stays"][did]
        home = D["devices"][did]["home_cell"]
        for i, (cell, s, e, su, eu) in enumerate(stays):
            if cell == home or (e - s).total_seconds() < LONG_MIN * 60 or zone_major(D, cell) != z:
                continue
            if s.date() not in days_all:
                continue
            prev = [x for x in stays[:i] if x[0] == home and x[2] <= s]
            if not prev:
                continue
            dep = prev[-1][4]
            m = dep.hour * 60 + dep.minute
            tot[z] += 1
            if AM[0] <= m <= AM[1]:
                hit[z] += 1
    return {z: hit[z] / tot[z] for z in tot}


def station_ratios(D, codes_map=None, naive=False):
    """Average ordinary-weekday entries, September to November 2027 over September to November 2019."""
    hol = D["nonordinary"]
    succ = {"KUH": ["UHK", "KUH"], "CBY": ["CBH", "CBY"], "ARD": ["ARD"], "LSG": ["LSG"], "KCN": ["KCN"],
            "KDK": ["KDK"]}
    if naive:
        succ = {k: [k] for k in succ}
    out = {}
    for st, codes in succ.items():
        def mean(y):
            v = [n for d, c, n in D["gates"] if c in codes and d.year == y and 9 <= d.month <= 11 and d.weekday() < 5
                 and d not in hol]
            return (sum(v) / len(v)) if v else None, len(v)
        a, na = mean(2027)
        b, nb = mean(2019)
        out[st] = (a / b if (a and b) else None, a, b, na, nb)
    return out


def network_ratio(D):
    hol = D["nonordinary"]
    def tot(y):
        days = sorted({d for d, c, n in D["gates"] if d.year == y and 9 <= d.month <= 11 and d.weekday() < 5
                       and d not in hol})
        s = sum(n for d, c, n in D["gates"] if d.year == y and 9 <= d.month <= 11 and d.weekday() < 5 and d not in hol
                and c != "LSG")
        return s / len(days)
    return tot(2027) / tot(2019)


def run(target):
    D = load(target)
    W = workers(D)
    f, n = frequencies(D, W)
    rows, golden = boardings(D, f)
    census_daily = sum(D["census"].get(z, 0) * s for z, s in D["shares"].items())
    pooled_num = sum(len(cd) for _d, _w, cd, obs in W if list(_w)[0] in D["shares"])
    pooled_den = sum(len(obs) for _d, _w, cd, obs in W if list(_w)[0] in D["shares"])
    f_pooled = pooled_num / pooled_den
    net = network_ratio(D)
    sr = station_ratios(D)
    lsg = sr["LSG"][0]
    dep, dep_n = departures(D, W)
    dep_u = departures_utc(D, W)
    # Variants the fork table licenses
    var = {}
    for name, kw in (("long210", dict(long_min=210)), ("long270", dict(long_min=270)), ("long300", dict(long_min=300)),
                     ("majority", dict(rule="majority")), ("minlong5", dict(min_long=5)),
                     ("split", dict(straddle="split")), ("utcdays", dict(tz="utc"))):
        Wv = workers(D, **kw)
        fv, _ = frequencies(D, Wv)
        var[name] = boardings(D, fv)
    var["devmean"] = boardings(D, frequencies(D, W, mode="mean")[0])
    allwk = [d for d in ordinary_days(D)]
    mid = [d for d in [dt.date(2027, 10, 25) + dt.timedelta(days=i) for i in range(5)]]
    # including the mid-term week and the bank holiday as if ordinary
    def incl_mid(D2=D):
        Wm = []
        for did, wz, cd, obs in W:
            dev = D["devices"][did]
            first, last = loc(dev["first_seen_utc"]).date(), loc(dev["last_seen_utc"]).date()
            home = dev["home_cell"]
            z = list(wz)[0]
            extra_obs = [d for d in mid if first <= d <= last]
            extra_cd = {s.date() for cell, s, e, su, eu in D["stays"][did]
                        if cell != home and (e - s).total_seconds() >= LONG_MIN * 60 and zone_major(D, cell) == z
                        and s.date() in mid}
            Wm.append((did, wz, cd | extra_cd, obs + extra_obs))
        return Wm
    var["with_midterm"] = boardings(D, frequencies(D, incl_mid())[0])
    full55 = len(allwk)
    Wall = [(did, wz, cd, allwk) for did, wz, cd, obs in W]
    var["all_days_den"] = boardings(D, frequencies(D, Wall)[0])
    out = {
        "census": dict(D["census"]), "shares": D["shares"], "threshold": D["threshold"],
        "freq": f, "n_devices": dict(n), "boardings": rows, "golden": golden,
        "census_daily": census_daily, "f_pooled": f_pooled, "pooled_route": census_daily * f_pooled,
        "network_ratio": net, "network_route": census_daily * net, "lisnagry_ratio": lsg,
        "lisnagry_route": census_daily * lsg, "station_ratios": {k: v[0] for k, v in sr.items()},
        "station_means": {k: (v[1], v[2], v[3], v[4]) for k, v in sr.items()},
        "station_ratios_naive": {k: v[0] for k, v in station_ratios(D, naive=True).items()},
        "departures": dep, "departure_days": dict(dep_n), "departures_utc": dep_u,
        "variants": {k: {"total": v[1], "rows": v[0]} for k, v in var.items()},
        "scope": "reduced" if golden < D["threshold"] else "full",
        "ordinary_days": full55,
        "census_prov": dict(D["census_prov"]),
    }
    return out


if __name__ == "__main__":
    tgt = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "target")
    r = run(tgt)
    print(json.dumps({k: (round(v, 4) if isinstance(v, float) else v) for k, v in r.items()
                      if k in ("golden", "census_daily", "pooled_route", "network_route", "lisnagry_route",
                               "f_pooled", "network_ratio", "scope", "ordinary_days")}, indent=1))
    for z in sorted(r["boardings"]):
        print(z, round(r["freq"].get(z, 0), 4), r["n_devices"].get(z), round(r["boardings"][z], 2),
              round(r["departures"].get(z, 0), 4), round(r["departures_utc"].get(z, 0), 4))
    print({k: round(v["total"], 1) for k, v in r["variants"].items()})
    print({k: round(v, 4) for k, v in r["station_ratios"].items()})
