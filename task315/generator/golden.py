"""task315 golden: every graded figure computed from the files under target/, and the two deliverables.

Main call. Each of today's legs between fast-charging communities is priced, month by month and in each
direction, from the same cars' consecutive sessions at the two ends: the battery the car used between them
(the first session's SoC at its end less the second's at its start, times the car's usable battery) over its
rated consumption times the leg's length. A band's reference car needs that factor times its rated consumption
times the length of every leg it drives; a new site splits its leg by length. Each projected trip is shared over
the bands by the register and half each way; a package scores the trips it makes completable that today's
network leaves uncompletable.

Remote asks. Hours unavailable are charge-point hours in a faulted or out-of-service state, a replacement unit
taking its predecessor's place from its first status, with approved-in-advance maintenance counted as available;
support is the rate on the kWh of Schedule A charge points' sessions ending in the quarter (Pacific), withheld
below 95 per cent availability. CFC's corrected re-send replaces the earlier records for its months and sites;
Northway's Schedule A charge points are found by their EVSE id, which survived the renumbering.
"""
import csv
import datetime as dt
import io
import json
import os
from collections import defaultdict

import world as W
import routes as R
import records as RC
import remote as RM

APP_TO_SHEET = {s: W.FLEET[k][0] for k, v in RC.VEHICLE_STRINGS.items() for s in v}
REG_TO_SHEET = {v[1]: v[0] for v in list(W.FLEET.values()) + list(W.SMALL_MODELS.values())}
WINDOW_H = 8.0


def parse_ts(s):
    t = dt.datetime.fromisoformat(s.replace("Z", "+00:00"))
    return (t - t.utcoffset()).replace(tzinfo=None)


def local_month(u):
    return RM.to_local(u)[0].month


def read_csv(target, name):
    with open(os.path.join(target, name), encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def read_xlsx(target, name, header_row=1):
    from openpyxl import load_workbook
    ws = load_workbook(os.path.join(target, name), read_only=True, data_only=True).worksheets[0]
    rows = list(ws.iter_rows(values_only=True))
    hdr = rows[header_row - 1]
    return [dict(zip(hdr, r)) for r in rows[header_row:] if r and r[0] is not None and any(c is not None for c in r[1:])]


# ---------------------------------------------------------------------------------------------- inputs
def inputs(target):
    import build as B
    reg = read_xlsx(target, B.F_REG)
    sheet = {r["Make and model"]: (float(r["Usable battery (kWh)"]), float(r["Rated combined (kWh/100 km)"]))
             for r in read_xlsx(target, B.F_REF)}
    zev = [r for r in read_xlsx(target, B.F_ZEV, header_row=3) if r.get("Fuel Type") == "BEV"]
    counts = defaultdict(int)
    for r in zev:
        counts[REG_TO_SHEET[r["Make"] + " " + r["Model"]]] += int(r["Registered"])
    bands = {}
    for b, (lab, lo, hi) in W.BAND_LIMITS.items():
        ms = [m for m in counts if lo <= sheet[m][0] < hi]
        n = sum(counts[m] for m in ms)
        bands[b] = dict(n=n, usable=sum(sheet[m][0] * counts[m] for m in ms) / n,
                        rated=sum(sheet[m][1] * counts[m] for m in ms) / n, models=sorted(ms))
    tot = sum(v["n"] for v in bands.values())
    for v in bands.values():
        v["share"] = v["n"] / tot
    name_to_node = {v[0]: k for k, v in W.NODES.items()}
    corridor = {r["Operator Site Code"]: name_to_node[r["Community"]] for r in reg if r["Programme"] == "Corridor"}
    from openpyxl import load_workbook
    ws = load_workbook(os.path.join(target, B.F_PRJ), read_only=True, data_only=True).worksheets[0]
    od = []
    for r in list(ws.iter_rows(values_only=True))[4:]:
        if r and r[0] in name_to_node and r[1] in name_to_node:
            od.append((name_to_node[r[0]], name_to_node[r[1]], [int(x) for x in r[2:14]], r[14]))
    stretches = {r["stretch_id"]: float(r["length_km"]) for r in read_csv(target, B.F_STR)}
    return dict(reg=reg, sheet=sheet, bands=bands, corridor=corridor, od=od, stretches=stretches)


def cfc_rows(target, resend_replaces=True):
    """The CFC export with each session once: a later batch replaces the earlier records for its site-months."""
    import build as B
    rows = read_csv(target, B.F_CFC)
    for r in rows:
        r["_t0"], r["_t1"] = parse_ts(r["Start"]), parse_ts(r["End"])
        r["_ex"] = parse_ts(r["Exported (UTC)"])
        r["_sm"] = (r["Site Code"], RM.to_local(r["_t1"])[0].strftime("%Y-%m"))
    if resend_replaces:
        latest = {}
        for r in rows:
            latest[r["_sm"]] = max(latest.get(r["_sm"], r["_ex"]), r["_ex"])
        rows = [r for r in rows if r["_ex"] == latest[r["_sm"]]]
    best = {}
    for r in rows:
        k = r["Session ID"]
        if k not in best or r["_ex"] > best[k]["_ex"]:
            best[k] = r
    return sorted(best.values(), key=lambda r: (r["_t0"], r["Session ID"]))


# ---------------------------------------------------------------------------------------------- main call
LEG_ENDS = {}
for _k, _m in R.LEGS_TODAY.items():
    LEG_ENDS[(W.STRETCHES[_m[0]][0], W.STRETCHES[_m[-1]][1])] = (_k, "F")
    LEG_ENDS[(W.STRETCHES[_m[-1]][1], W.STRETCHES[_m[0]][0])] = (_k, "R")


def leg_km(key, stretches):
    return sum(stretches[s] for s in R.LEGS_TODAY[key])


def session_pairs(rows, inp, window_h=WINDOW_H, month_by="end", infer_battery=False):
    """(leg, month, direction) -> list of measured factors from consecutive sessions of one Auth ID."""
    by = defaultdict(list)
    for r in rows:
        if r["Site Code"] in inp["corridor"]:
            by[r["Auth ID"]].append(r)
    out = defaultdict(list)
    for tok, lst in by.items():
        lst.sort(key=lambda r: r["_t0"])
        for a, b in zip(lst, lst[1:]):
            na, nb = inp["corridor"][a["Site Code"]], inp["corridor"][b["Site Code"]]
            if (na, nb) not in LEG_ENDS or not a["SoC End (%)"] or not b["SoC Start (%)"]:
                continue
            if (b["_t0"] - a["_t1"]).total_seconds() > window_h * 3600:
                continue
            if a["Vehicle"]:
                usable, rated = inp["sheet"][APP_TO_SHEET[a["Vehicle"]]]
            elif infer_battery and a["SoC Start (%)"] and int(a["SoC End (%)"]) - int(a["SoC Start (%)"]) >= 20:
                usable = float(a["Energy (kWh)"]) * 0.92 / ((int(a["SoC End (%)"]) - int(a["SoC Start (%)"])) / 100)
                rated = None
            else:
                continue
            key, d = LEG_ENDS[(na, nb)]
            used = (int(a["SoC End (%)"]) - int(b["SoC Start (%)"])) / 100 * usable
            m = local_month(a["_t1"] if month_by == "end" else b["_t0"])
            if rated is None:
                out[(key, m, d)].append(("kwh", used / leg_km(key, inp["stretches"])))
            else:
                out[(key, m, d)].append(("f", used / (rated / 100 * leg_km(key, inp["stretches"]))))
    return out


def factor_table(pairs, stat="mean"):
    import statistics
    t, n = {}, {}
    for key in R.LEGS_TODAY:
        for m in W.MONTHS:
            for d in ("F", "R"):
                v = [x for kind, x in pairs.get((key, m, d), []) if kind == "f"]
                n[(key, m, d)] = len(v)
                if not v:
                    t[(key, m, d)] = None
                elif stat == "mean":
                    t[(key, m, d)] = sum(v) / len(v)
                elif stat == "median":
                    t[(key, m, d)] = statistics.median(v)
                elif stat == "trim":
                    v = sorted(v)
                    c = max(1, len(v) // 10)
                    v = v[c:-c] if len(v) > 2 * c else v
                    t[(key, m, d)] = sum(v) / len(v)
    return t, n


def fill_inert(table, value=None):
    """Legs without a pair in a month are short; the largest measured factor is used there (asserted inert)."""
    mx = max(v for v in table.values() if v is not None) if value is None else value
    return {k: (mx if v is None else v) for k, v in table.items()}


def feasible_band(bd, a, b, m, chargers, efn, inp):
    usable = inp["bands"][bd]["usable"]
    for first, lg in R.legs(a, b, chargers):
        if sum(efn(bd, sid, m, d) for sid, d in lg) > usable * (W.CHARGE_TO - W.RESERVE):
            return False
    return True


def make_efn(table, inp, alloc="km"):
    st = inp["stretches"]

    def fn(bd, sid, m, d):
        rated = inp["bands"][bd]["rated"]
        key = R.STRETCH_LEG[sid]
        f = table[(key, m, d)]
        if alloc == "km":
            return f * rated / 100 * st[sid]
        members = R.LEGS_TODAY[key]
        cl = {s: W.climb_kwh(W.MASS_PER_RATED * rated, *W.oriented(s, d)) for s in members}
        total = f * rated / 100 * sum(st[s] for s in members)
        return (total - sum(cl.values())) * st[sid] / sum(st[s] for s in members) + cl[sid]
    return fn


def package_gains(efn, inp):
    base = set(inp["corridor"].values())
    gains = {p: [0.0] * 12 for p in W.PACKAGES}
    unc = [0.0] * 12
    for a, b, months, annual in inp["od"]:
        for m in W.MONTHS:
            trips = months[m - 1]

            def comp(ch):
                return sum(inp["bands"][bd]["share"] * 0.5 * (feasible_band(bd, a, b, m, ch, efn, inp) +
                                                                feasible_band(bd, b, a, m, ch, efn, inp))
                           for bd in W.BAND_KEYS)
            c0 = comp(base)
            unc[m - 1] += trips * (1 - c0)
            for p, pk in W.PACKAGES.items():
                gains[p][m - 1] += trips * (comp(base | set(pk["nodes"])) - c0)
    return gains, unc


def main_call(target, rows=None, inp=None):
    inp = inp or inputs(target)
    rows = rows if rows is not None else cfc_rows(target)
    pairs = session_pairs(rows, inp)
    table, npairs = factor_table(pairs)
    efn = make_efn(fill_inert(table), inp)
    gains, unc = package_gains(efn, inp)
    return dict(inp=inp, rows=rows, pairs=pairs, table=table, npairs=npairs, gains=gains, unc=unc, efn=efn)


# ---------------------------------------------------------------------------------------------- remote asks
def remote(target, rows=None, code_join=False, resend_replaces=True, extra_unit=False):
    import build as B
    reg = [r for r in read_xlsx(target, B.F_REG) if r["Programme"] == "Remote Operating Support 2024"]
    rows = rows if rows is not None else cfc_rows(target, resend_replaces)
    nwe = [json.loads(l) for l in open(os.path.join(target, B.F_NWE), encoding="utf-8")]
    cst = read_csv(target, B.F_CST)
    nst = read_csv(target, B.F_NST)
    mnt = read_csv(target, B.F_MNT)
    maint = defaultdict(list)
    for r in mnt:
        w0 = dt.datetime.strptime(r["Window Start (Pacific)"], "%Y-%m-%d %H:%M")
        w1 = dt.datetime.strptime(r["Window End (Pacific)"], "%Y-%m-%d %H:%M")
        if dt.date.fromisoformat(r["Approved On"]) < w0.date():
            maint[r["Site ID"]].append((RM.to_utc(w0), RM.to_utc(w1)))
    # CFC serials: the register's, and any serial the sessions file shows at the site
    serial_site = {}
    for r in rows:
        serial_site.setdefault(r["Charge Point"], r["Site Code"])
    out = {}
    for s in reg:
        svrd, code = s["Site ID"], s["Operator Site Code"]
        ids = [x.strip() for x in s["Charge Point IDs"].split(",")]
        n_cp = int(s["Charge Points"])
        timelines = []          # per Schedule A position: list of (status, t0, t1) segments in service
        if s["Operator"].startswith("Columbia"):
            events = defaultdict(list)
            for r in cst:
                events[r["Charge Point"]].append((parse_ts(r["Event Time"]), r["Status"]))
            news = sorted({c for c, sc in serial_site.items() if sc == code and c not in ids and c in events},
                          key=lambda c: events[c][0][0])
            pos = {i: [i] for i in ids}
            for c in news:
                first = events[c][0][0]
                old = [i for i in ids if pos[i][-1] in events and events[pos[i][-1]][-1][0] < first and
                       not any(r["Charge Point"] == pos[i][-1] and r["_t0"] > first for r in rows)]
                pos[old[0]].append(c)
            for i in ids:
                chain = pos[i]
                segs = []
                for j, c in enumerate(chain):
                    t_end = events[chain[j + 1]][0][0] if j + 1 < len(chain) else RM.STATUS_WIN[1]
                    t_beg = events[c][0][0] if j > 0 else RM.STATUS_WIN[0]
                    segs.append((c, t_beg, t_end))
                timelines.append([(events[c], t0, t1) for c, t0, t1 in segs])
            kwh_rows = [(r["_t1"], float(r["Energy (kWh)"])) for r in rows if r["Site Code"] == code]
        else:
            if code_join:
                boxes = sorted({(t["charge_box_id"], t["connector_id"]) for t in nwe if t["charge_box_id"] == code})
                sel = [t for t in nwe if t["charge_box_id"] == code]
            else:
                boxes = sorted({(t["charge_box_id"], t["connector_id"]) for t in nwe if t["evse_id"] in ids})
                sel = [t for t in nwe if t["evse_id"] in ids]
            events = defaultdict(list)
            for r in nst:
                events[(r["charge_box_id"], int(r["connector_id"]))].append((parse_ts(r["timestamp_utc"]), r["status"]))
            for bx in boxes:
                timelines.append([(events[bx], RM.STATUS_WIN[0], RM.STATUS_WIN[1])])
            if code_join:
                n_cp = max(n_cp, len(boxes))
            kwh_rows = [(parse_ts(t["stop_timestamp"]), (t["meter_stop"] - t["meter_start"]) / 1000) for t in sel]
        for qi, (q0, q1) in enumerate(RM.QUARTERS):
            down = 0.0
            for tl in timelines:
                for ev, s0, s1 in tl:
                    ev = sorted(ev)
                    for k, (t, st) in enumerate(ev):
                        if st not in ("Faulted", "Unavailable"):
                            continue
                        t_next = ev[k + 1][0] if k + 1 < len(ev) else s1
                        a, b = max(t, q0, s0), min(t_next, q1, s1)
                        if b <= a:
                            continue
                        span = (b - a).total_seconds()
                        for m0, m1 in maint.get(svrd, []):
                            span -= max(0.0, (min(b, m1) - max(a, m0)).total_seconds())
                        down += span
            hours = down / 3600
            cap = n_cp * (q1 - q0).total_seconds() / 3600
            avail = 1 - hours / cap
            kwh = sum(e for t, e in kwh_rows if q0 <= t < q1)
            out[(svrd, qi)] = dict(hours=hours, avail=avail, kwh=kwh, support=RM.RATE * kwh if avail >= RM.GATE else 0.0)
    return out


# ---------------------------------------------------------------------------------------------- figures
def edge(v, unit):
    return unit / 2 - abs(v - round(v / unit) * unit)


def figures(target):
    mc = main_call(target)
    g = mc["gains"]
    tot = {p: sum(v) for p, v in g.items()}
    order = sorted(tot, key=lambda p: (-tot[p], p))
    rem = remote(target, rows=mc["rows"])
    figs = {
        "call": order[0],
        "call_name": W.PACKAGES[order[0]]["name"],
        "runner_up": order[1],
        "packages": {p: {"name": W.PACKAGES[p]["name"], "by_month": [round(x, 3) for x in g[p]],
                         "total": round(tot[p], 3), "total_10": int(round(tot[p] / 10) * 10)} for p in W.PACKAGES},
        "gap": round(tot[order[0]] - tot[order[1]], 3),
        "gap_10": int(round((tot[order[0]] - tot[order[1]]) / 10) * 10),
        "uncompletable_by_month": [round(x, 3) for x in mc["unc"]],
        "uncompletable": round(sum(mc["unc"]), 3),
        "uncompletable_10": int(round(sum(mc["unc"]) / 10) * 10),
        "pool_trips": int(sum(sum(m) for a, b, m, y in mc["inp"]["od"])),
        "bands": {b: {k: (round(v, 4) if isinstance(v, float) else v) for k, v in mc["inp"]["bands"][b].items()}
                  for b in W.BAND_KEYS},
        "factors": {"%s|%d|%s" % k: (None if v is None else round(v, 4)) for k, v in sorted(mc["table"].items())},
        "pairs": {"%s|%d|%s" % k: v for k, v in sorted(mc["npairs"].items())},
        "remote": {},
    }
    for (svrd, qi), v in sorted(rem.items()):
        figs["remote"]["%s|Q%d" % (svrd, qi + 1)] = dict(hours=round(v["hours"], 4), hours_1=int(round(v["hours"])),
                                                         avail=round(v["avail"], 6), kwh=round(v["kwh"], 3),
                                                         support=round(v["support"], 2),
                                                         support_1=int(round(v["support"])))
    return figs


# ---------------------------------------------------------------------------------------------- deliverables
def _chart(figs, path):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    plt.rcParams["svg.hashsalt"] = "task315"
    fig, ax = plt.subplots(figsize=(7.2, 3.3), dpi=150)
    x = list(range(12))
    colours = {"A": "#8c8c8c", "B": "#1f5a96", "C": "#c9a227"}
    w = 0.27
    for i, p in enumerate(("A", "B", "C")):
        ax.bar([k + (i - 1) * w for k in x], figs["packages"][p]["by_month"], width=w, color=colours[p],
               label="%s  %s" % (p, figs["packages"][p]["name"]))
    ax.set_xticks(x)
    ax.set_xticklabels([m[:3] for m in W.MONTH_NAMES], fontsize=8)
    ax.set_ylabel("2027 trips made completable", fontsize=8)
    ax.tick_params(axis="y", labelsize=8)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.legend(fontsize=7.5, frameon=False, loc="upper center")
    ax.set_title("Trips each package makes completable that today's network does not, by month of 2027", fontsize=9)
    fig.tight_layout()
    fig.savefig(path, metadata={"Software": None})
    plt.close(fig)


def write_golden(folder, figs):
    import golden_docs as GD
    GD.write_workbook(folder, figs)
    GD.write_note(folder, figs, _chart)
