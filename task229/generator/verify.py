"""Independent verifier: recomputes every graded figure, the ladder's sets and the chart from target/ alone
(csv module, its own likelihood search, no generator state, no pandas) and checks figures.json and the
golden page against them.

    python3 task229/generator/verify.py [target] [golden_dir]
"""
import csv
import datetime as dt
import json
import math
import os
import re
import sys
from collections import defaultdict
from zoneinfo import ZoneInfo

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
LON = ZoneInfo("Europe/London")
DAY0 = dt.date(2026, 6, 1)
LAST = (dt.date(2026, 12, 6) - DAY0).days
CENTRE = {}


def rows(target, name):
    with open(os.path.join(target, name), newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def tday(utc):
    t = dt.datetime.strptime(utc, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=dt.timezone.utc).astimezone(LON)
    return ((t - dt.timedelta(hours=6)).date() - DAY0).days


def fit(obs):
    """Golden-section search for the per-day error chance maximising the likelihood of (days, matched)."""
    def ll(lp):
        p = math.exp(lp)
        s = 0.0
        for d, hit in obs:
            pr = min(max((1 - p) ** d, 1e-12), 1 - 1e-12)
            s += math.log(pr) if hit else math.log(1 - pr)
        return s
    a, b = -16.0, -1.0
    g = (math.sqrt(5) - 1) / 2
    c, d = b - g * (b - a), a + g * (b - a)
    fc, fd = ll(c), ll(d)
    for _ in range(90):
        if fc > fd:
            b, d, fd = d, c, fc
            c = b - g * (b - a)
            fc = ll(c)
        else:
            a, c, fc = c, d, fd
            d = a + g * (b - a)
            fd = ll(d)
    return math.exp((a + b) / 2)


def gate_faces(target):
    out = {}
    for r in rows(target, "wms_location_master_THN_eff.csv"):
        if (r["location_type"] == "PICK" and r["client"] == "THN" and r["line_no"] and r["status"] == "ACTIVE"
                and r["eff_from"] <= "2026-12-07" and (r["eff_to"] == "" or r["eff_to"] >= "2026-12-07")):
            out[(r["site"], r["location"])] = r
    return out


def record_accuracy(target):
    faces = gate_faces(target)
    hist = defaultdict(list)
    for r in rows(target, "THN_pickface_count_history_20260601_20261207.csv"):
        k = (r["site"], r["location"])
        if k in faces:
            hist[k].append((r["counted_utc"], tday(r["counted_utc"]), r["reason_code"], r["result"] == "MATCH"))
    obs = defaultdict(list)
    last = {}
    rates = defaultdict(lambda: [0, 0])
    for k, h in hist.items():
        h.sort()
        cls = faces[k]["slot_class"]
        for i, (_, d, code, hit) in enumerate(h):
            rates[(k[0], "all")][0] += hit; rates[(k[0], "all")][1] += 1
            if code == "CYC":
                rates[(k[0], "cyc")][0] += hit; rates[(k[0], "cyc")][1] += 1
                rates[(k[0], "cyc", cls)][0] += hit; rates[(k[0], "cyc", cls)][1] += 1
                if i > 0:
                    obs[(k[0], cls)].append((d - h[i - 1][1], hit))
        last[k] = h[-1][1]
    p = {key: fit(v) for key, v in obs.items()}
    acc = defaultdict(list)
    mix = defaultdict(lambda: defaultdict(int))
    for k, r in faces.items():
        acc[k[0]].append((1 - p[(k[0], r["slot_class"])]) ** (LAST - last[k]))
        mix[k[0]][r["slot_class"]] += 1
    out = {}
    for site, v in acc.items():
        n = sum(mix[site].values())
        w = sum(mix[site][c] / n * rates[(site, "cyc", c)][0] / rates[(site, "cyc", c)][1] for c in "ABC")
        out[site] = dict(estimate=100 * sum(v) / len(v), rung0=100 * rates[(site, "all")][0] / rates[(site, "all")][1],
                         rung1=100 * rates[(site, "cyc")][0] / rates[(site, "cyc")][1], rung2=100 * w)
    return out, len(faces)


def stock_value(target):
    faces = gate_faces(target)
    seen, qty = set(), defaultdict(float)
    unit = {}
    for r in rows(target, "WMS_stock_by_location_THN_20261207_0600.csv"):
        k = (r["site"], r["location"], r["line_no"])
        if (r["site"], r["location"]) in faces and faces[(r["site"], r["location"])]["line_no"] == r["line_no"] and k not in seen:
            seen.add(k)
            qty[k] = float(r["qty"])
            unit[k] = r["stock_unit"]
    breg = defaultdict(float)
    for r in rows(target, "WMS_batch_register_THN_20261207_0600.csv"):
        breg[(r["site"], r["location"], r["line_no"])] += float(r["batch_qty"])
    for k, v in breg.items():
        if k in qty:
            assert abs(qty[k] - v) < 1e-9, ("batch register does not tie", k)
    from openpyxl import load_workbook
    ws = load_workbook(os.path.join(target, "Thornacre_line_master_20261204.xlsx"), read_only=True).active
    size = {}
    when = dt.datetime(2026, 12, 7)
    for i, r in enumerate(ws.iter_rows(values_only=True)):
        if i == 0:
            continue
        line, _, _, _, _, cs, vf, vt, _ = r
        if vf <= when and (vt is None or vt >= when):
            size[str(line)] = float(cs)
    cost = {r["line_no"]: float(r["cost_per_case"]) for r in rows(target, "THN_cost_price_list_20261128.csv")}
    for r in rows(target, "THN_cost_changes_P10_2026.csv"):
        if r["effective_from"] <= "2026-12-07":
            cost[r["line_no"]] = float(r["new_cost_per_case"])
    out = defaultdict(float)
    for k, q in qty.items():
        c = q / size[k[2]] if unit[k] == "EA" else q
        out[k[0]] += c * cost[k[2]]
    return out


def forecast_cases(target):
    upc = {r["category"]: r["units_per_case"] for r in rows(target, "THN_category_table.csv")}
    regime = {r["category"]: r["supply_chain"] for r in rows(target, "THN_category_table.csv")}
    closed = {(r["store_no"], r["trading_date"]) for r in rows(target, "THN_store_trading_calendar_2026_27.csv")
              if r["status"] == "CLOSED"}
    sm = defaultdict(list)
    for r in rows(target, "THN_store_servicing_map.csv"):
        sm[(r["store_no"], r["supply_chain"])].append((r["valid_from"], r["valid_to"] or "9999-12-31", r["depot"]))
    out, run = defaultdict(float), defaultdict(float)
    for r in rows(target, "THN_store_replen_forecast_run_20261123.csv"):
        d = r["trading_date"]
        if not ("2026-12-07" <= d <= "2027-01-03"):
            continue
        q = float(r["fcst_qty"])
        if r["uom"] == "EA":
            q /= float(upc[r["category"]])
        run[r["depot"]] += q
        if (r["store_no"], d) in closed:
            continue
        dep = [x[2] for x in sm[(r["store_no"], regime[r["category"]])] if x[0] <= d <= x[1]]
        assert len(dep) == 1, (r, dep)
        out[dep[0]] += q
    return out, run


def main(target=None, golden=None):
    target = target or os.path.join(TASK, "target")
    golden = golden or os.path.join(TASK, "golden")
    reg = rows(target, "corderoy_thornacre_centre_register.csv")
    name = {r["site"]: r["centre"] for r in reg}
    depot = {r["thornacre_depot"]: r["centre"] for r in reg}
    acc, nfaces = record_accuracy(target)
    figs = json.load(open(os.path.join(HERE, "figures.json")))
    page = open(os.path.join(golden, "freeze_gate_2026.html"), encoding="utf-8").read()
    n_checks = 0
    qual = sorted(name[s] for s, v in acc.items() if v["estimate"] >= 97.0)
    assert qual == sorted(figs["call"]["qualify"]), (qual, figs["call"])
    assert sorted(name[s] for s, v in acc.items() if v["rung0"] >= 97.0) == []
    assert sorted(name[s] for s, v in acc.items() if v["rung1"] >= 97.0) == ["Magor"]
    assert sorted(name[s] for s, v in acc.items() if v["rung2"] >= 97.0) == ["Hinckley", "Magor"]
    assert figs["in_scope_faces"] == "{:,}".format(nfaces)
    n_checks += 5
    for s, v in acc.items():
        n = name[s]
        assert int(round(v["estimate"])) == figs["share_whole_pc"][n], (n, v)
        assert abs(v["estimate"] - figs["share_unrounded"][n]) < 0.006, (n, v["estimate"], figs["share_unrounded"][n])
        n_checks += 2
    val = stock_value(target)
    for s, v in val.items():
        n = name[s]
        txt = "£{:,.0f}".format(round(v, -3))
        assert txt == figs["stock_value_gbp"][n], (n, txt, figs["stock_value_gbp"][n])
        assert txt in page
        n_checks += 2
    fc, run = forecast_cases(target)
    for d, v in fc.items():
        n = depot[d]
        txt = "{:,.0f}".format(round(v, -2))
        assert txt == figs["forecast_cases"][n], (n, txt)
        assert txt in page
        n_checks += 2
    order = [depot[d] for d in sorted(fc, key=lambda d: -fc[d])]
    assert order == figs["chart_order"], (order, figs["chart_order"])
    bars = re.findall(r'<title>([A-Za-z]+): ([\d,]+) cases</title>', page)
    assert [b[0] for b in bars] == order and [b[1] for b in bars] == [figs["forecast_cases"][n] for n in order]
    assert ">%s draws the most over the freeze<" % order[0] in page
    assert depot[max(run, key=run.get)] != order[0]
    for n in figs["share_whole_pc"]:
        assert "<td>%s</td><td>%d%%</td>" % (n, figs["share_whole_pc"][n]) in page
    n_checks += 4 + len(figs["share_whole_pc"])
    print("verify.py: %d checks green; qualify %s" % (n_checks, ", ".join(qual)))
    return n_checks


if __name__ == "__main__":
    main(*(sys.argv[1:3]))
