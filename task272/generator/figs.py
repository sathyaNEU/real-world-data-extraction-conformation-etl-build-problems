"""Everything owed, computed from the cut pack alone: the conformed record, each product's out-of-tolerance rate
rebuilt set by set (the golden) and under every rung of the ladder, the call, and the asks' figures."""
import bisect
import csv
import datetime as dt
import math
import os
from zoneinfo import ZoneInfo

import numpy as np
import openpyxl
import pyarrow.parquet as pq

TZ = ZoneInfo("America/Toronto")
UTC = dt.timezone.utc
LIMIT = 10.0
FILES = {
    "doses": "compounder_dose_log_2026.parquet",
    "events": "compounder_events_2026.csv",
    "checks": "gravimetric_check_register_2026.xlsx",
    "quarantine": "quarantine_register_2026.xlsx",
    "master": "compounded_product_master.xlsx",
    "equipment": "compounding_equipment_register.csv",
}


def _phi(z):
    return 0.5 * math.erfc(-z / math.sqrt(2.0))


def load(target):
    """The conformed record: products, stations, doses on their sets with the litres each set had pumped, checks
    tied to their doses, sorts."""
    wb = openpyxl.load_workbook(os.path.join(target, FILES["master"]), read_only=True)
    rows = list(wb["Products"].iter_rows(values_only=True))
    prods = {}
    for r in rows[1:]:
        prods[r[0]] = dict(code=r[0], name=r[1], vol=float(r[3]), tol=float(r[4]), sg=float(r[5]), tare=float(r[6]),
                           station=r[7], verified=(r[8] == "yes"))
    by_name = {p["name"]: c for c, p in prods.items()}
    station_of = {}
    with open(os.path.join(target, FILES["equipment"]), encoding="utf-8") as f:
        for r in csv.DictReader(f):
            station_of[r["serial"]] = r["station"]
    t = pq.read_table(os.path.join(target, FILES["doses"])).to_pydict()
    doses = []
    for i in range(len(t["status"])):
        ts = dt.datetime.strptime(t["fill_end_time"][i], "%Y-%m-%d %H:%M:%S").replace(tzinfo=UTC)
        doses.append(dict(serial=t["compounder_sn"][i], t=ts, product=t["product_no"][i], batch=t["batch_no"][i],
                          dose=int(t["dose_no"][i]), ml=float(t["programmed_ml"][i]), status=t["status"][i]))
    sets_by_serial = {}
    seen = set()
    with open(os.path.join(target, FILES["events"]), encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r["event"] != "SET_UP":
                continue
            key = (r["compounder_sn"], r["set_lot"])
            if key in seen:
                continue           # a re-seat keeps its lot: the same set
            seen.add(key)
            ts = dt.datetime.strptime(r["event_time"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=UTC)
            sets_by_serial.setdefault(r["compounder_sn"], []).append((ts, r["set_lot"]))
    for s in sets_by_serial:
        sets_by_serial[s].sort()
    # each completed dose on the set its device had installed when it was filled
    sets = {}
    pumped = {}
    for d in sorted((d for d in doses if d["status"] == "COMPLETE"), key=lambda d: (d["serial"], d["t"])):
        lst = sets_by_serial[d["serial"]]
        i = bisect.bisect_right([x[0] for x in lst], d["t"]) - 1
        key = (d["serial"], lst[i][1])
        d["set"] = key
        d["L"] = pumped.get(key, 0.0)
        pumped[key] = d["L"] + d["ml"] / 1000.0
        if key not in sets:
            sets[key] = dict(key=key, product=d["product"], setup=lst[i][0], first=d["t"])
    by_dose = {(d["batch"], d["dose"]): d for d in doses if d["status"] == "COMPLETE"}
    checks = []
    wb = openpyxl.load_workbook(os.path.join(target, FILES["checks"]), read_only=True)
    for q, ws in enumerate(wb.worksheets):
        rows = list(ws.iter_rows(values_only=True))
        gross = rows[0][5].startswith("Gross")
        for r in rows[1:]:
            code = by_name[r[3]]
            p = prods[code]
            wt = float(r[5])
            net = wt - p["tare"] if gross else wt
            vol = net / p["sg"]
            dose = by_dose[(r[2], int(r[4]))]
            checks.append(dict(product=code, quarter=q + 1, vol=vol, dev=100.0 * (vol / p["vol"] - 1.0),
                               result=r[6], dose=dose, local=dt.datetime.fromisoformat("%s %s" % (r[0], r[1]))))
    sorts = {}
    wb = openpyxl.load_workbook(os.path.join(target, FILES["quarantine"]), read_only=True)
    rows = list(wb.worksheets[0].iter_rows(values_only=True))
    batch_product = {d["batch"]: d["product"] for d in doses}
    for r in rows[1:]:
        sorts[r[0]] = dict(no=r[0], batch=r[2], product=batch_product[r[2]], quarantined=int(r[3]), rejected=int(r[5]),
                           opened=r[1])   # a recount under the same number replaces the earlier entry
    return dict(products=prods, station_of=station_of, doses=doses, sets=sets, checks=checks, sorts=list(sorts.values()),
                sets_by_serial=sets_by_serial)


# --------------------------------------------------------------------------------------------- the golden

def fit(rec, code, mode="fixed"):
    """dev = a_set + b * litres pumped before the dose + e, the slope common to the product's sets."""
    cs = [c for c in rec["checks"] if c["product"] == code]
    per = {}
    for c in cs:
        per.setdefault(c["dose"]["set"], []).append((c["dose"]["L"], c["dev"]))
    num = den = 0.0
    for pts in per.values():
        if len(pts) < 2:
            continue
        L = np.array([x[0] for x in pts])
        v = np.array([x[1] for x in pts])
        num += float(((L - L.mean()) * (v - v.mean())).sum())
        den += float(((L - L.mean()) ** 2).sum())
    b = num / den if den > 0 else 0.0
    a, res = {}, []
    for k, pts in per.items():
        L = np.array([x[0] for x in pts])
        v = np.array([x[1] for x in pts])
        if mode == "own_slope" and len(pts) >= 3 and float(((L - L.mean()) ** 2).sum()) > 0:
            bb = float(((L - L.mean()) * (v - v.mean())).sum() / ((L - L.mean()) ** 2).sum())
            a[k] = (float(v.mean() - bb * L.mean()), bb)
        else:
            a[k] = (float(v.mean() - b * L.mean()), b)
        res.extend(list(v - a[k][0] - a[k][1] * L))
    dof = max(1, len(res) - len(per) - 1)
    sig = math.sqrt(sum(x * x for x in res) / dof)
    ints = np.array([x[0] for x in a.values()])
    mu = float(ints.mean())
    tau2 = max(0.0, float(ints.var(ddof=1)) - sig * sig / max(1.0, np.mean([len(p) for p in per.values()])))
    return dict(b=b, sig=sig, a=a, mu=mu, tau2=tau2, n=len(cs), per=per)


def rebuilt_rate(rec, code, mode="fixed"):
    p = rec["products"][code]
    f = fit(rec, code, "own_slope" if mode == "own_slope" else "fixed")
    tol = p["tol"]
    tot = 0.0
    n = 0
    for d in rec["doses"]:
        if d["product"] != code or d["status"] != "COMPLETE":
            continue
        n += 1
        if mode == "random":
            m = f["mu"] + f["b"] * d["L"]
            s = math.sqrt(f["sig"] ** 2 + f["tau2"])
        elif mode == "shrunk":
            k = len(f["per"].get(d["set"], []))
            a0, bb = f["a"].get(d["set"], (f["mu"], f["b"]))
            w = f["tau2"] / (f["tau2"] + f["sig"] ** 2 / max(k, 1)) if k else 0.0
            m = f["mu"] + w * (a0 - f["mu"]) + f["b"] * d["L"]
            s = math.sqrt(f["sig"] ** 2 + (1 - w) * f["tau2"])
        else:
            a0, bb = f["a"].get(d["set"], (f["mu"], f["b"]))
            m = a0 + bb * d["L"]
            s = f["sig"]
        tot += _phi((-tol - m) / s) + _phi((m - tol) / s)
    return 1e5 * tot / n, n


# --------------------------------------------------------------------------------------------- the rungs

def ppk_rate(rec, code):
    p = rec["products"][code]
    v = np.array([c["dev"] for c in rec["checks"] if c["product"] == code])
    mu, sd = float(v.mean()), float(v.std(ddof=1))
    return 1e5 * (_phi((-p["tol"] - mu) / sd) + _phi((mu - p["tol"]) / sd))


def within_rate(rec, code):
    """Cpk's spread: the pooled standard deviation of the checks within each batch, about the overall mean."""
    p = rec["products"][code]
    v = [c for c in rec["checks"] if c["product"] == code]
    mu = float(np.mean([c["dev"] for c in v]))
    by = {}
    for c in v:
        by.setdefault(c["dose"]["batch"], []).append(c["dev"])
    ss = dof = 0.0
    for xs in by.values():
        if len(xs) > 1:
            ss += float(((np.array(xs) - np.mean(xs)) ** 2).sum())
            dof += len(xs) - 1
    sd = math.sqrt(ss / dof)
    return 1e5 * (_phi((-p["tol"] - mu) / sd) + _phi((mu - p["tol"]) / sd))


def checked_share(rec, code):
    v = [c for c in rec["checks"] if c["product"] == code]
    return 1e5 * sum(1 for c in v if c["result"] == "FAIL") / len(v)


def sorted_rate(rec, code):
    n = sum(1 for d in rec["doses"] if d["product"] == code and d["status"] == "COMPLETE")
    return 1e5 * sum(s["rejected"] for s in rec["sorts"] if s["product"] == code) / n


# --------------------------------------------------------------------------------------------- the asks

def quarter(t_local):
    return (t_local.month - 1) // 3 + 1


def ask_a(rec, utc_as_local=False, by_serial=False):
    out = {}
    for d in rec["doses"]:
        if d["status"] != "COMPLETE":
            continue
        t = d["t"].replace(tzinfo=None) if utc_as_local else d["t"].astimezone(TZ).replace(tzinfo=None)
        if t.year != 2026:
            continue
        st = d["serial"] if by_serial else rec["station_of"][d["serial"]]
        k = (st, t.month)
        out[k] = out.get(k, 0) + 1
    return out


def ask_b(rec, rows_not_lots=False, target=None):
    out = {}
    for key, s in rec["sets"].items():
        out[s["product"]] = out.get(s["product"], 0) + 1
    if rows_not_lots:
        # every SET_UP row counted, a re-seat as a second set
        extra = {}
        with open(os.path.join(target, FILES["events"]), encoding="utf-8") as f:
            rows = [r for r in csv.DictReader(f) if r["event"] == "SET_UP"]
        cnt = {}
        for r in rows:
            cnt[(r["compounder_sn"], r["set_lot"])] = cnt.get((r["compounder_sn"], r["set_lot"]), 0) + 1
        for key, s in rec["sets"].items():
            extra[s["product"]] = extra.get(s["product"], 0) + cnt[key] - 1
        out = {k: v + extra.get(k, 0) for k, v in out.items()}
    return out


def compute(target):
    rec = load(target)
    cands = [c for c, p in rec["products"].items() if not p["verified"]]
    gold, fam, rungs, fits = {}, {}, {}, {}
    for c in cands:
        g, n = rebuilt_rate(rec, c, "random")
        gold[c] = dict(rate=g, doses=n)
        fam[c] = {m: rebuilt_rate(rec, c, m)[0] for m in ("fixed", "shrunk", "own_slope")}
        f = fit(rec, c)
        fits[c] = dict(start=round(f["mu"], 2), loss_per_litre=round(f["b"], 3), scatter=round(f["sig"], 3),
                       start_sd=round(math.sqrt(f["tau2"]), 3), checks=f["n"])
        rungs[c] = dict(ppk=ppk_rate(rec, c), within=within_rate(rec, c), checked=checked_share(rec, c),
                        sorted=sorted_rate(rec, c))
    call = sorted(c for c in cands if gold[c]["rate"] > LIMIT)
    ladder = {k: sorted(c for c in cands if rungs[c][k] > LIMIT) for k in ("ppk", "within", "checked", "sorted")}
    ladder.update({m: sorted(c for c in cands if fam[c][m] > LIMIT) for m in ("fixed", "shrunk", "own_slope")})
    a = ask_a(rec)
    b = ask_b(rec)
    fig = dict(
        call=dict(products=call, count=len(call)),
        products={c: rec["products"][c]["name"] for c in cands},
        policy=dict(limit_value=LIMIT),
        golden={c: dict(rate=round(gold[c]["rate"], 1), doses=gold[c]["doses"]) for c in cands},
        family={c: {m: round(v, 1) for m, v in fam[c].items()} for c in cands},
        fits=fits,
        sorts={c: dict(sorts=sum(1 for s in rec["sorts"] if s["product"] == c),
                       rejected=sum(s["rejected"] for s in rec["sorts"] if s["product"] == c)) for c in cands},
        rungs={c: {k: round(v, 1) for k, v in rungs[c].items()} for c in cands},
        ladder=ladder,
        ask_a={"%s %02d" % k: v for k, v in sorted(a.items())},
        ask_b={k: v for k, v in sorted(b.items()) if k in cands},
    )
    return fig, rec


if __name__ == "__main__":
    import json
    import sys
    fig, _ = compute(sys.argv[1])
    print(json.dumps({k: fig[k] for k in ("call", "golden", "family", "rungs", "ladder")}, indent=1))
