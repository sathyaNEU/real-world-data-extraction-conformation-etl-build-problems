"""The golden from the cut pack: the 2026 release-event return (each event's start, closure and methane), its band and
the 2027 levy, and Schedule B's fugitive methane by route in each half of the year. Every handling of the pack's mess is a named option, so checks.py
can run the golden with any one of them mishandled."""
import collections
import datetime as dt
import re
from zoneinfo import ZoneInfo

import numpy as np
from scipy.optimize import minimize

import pack_read as PR

TZ = ZoneInfo("America/Edmonton")
UTC = dt.timezone.utc
EPOCH = dt.datetime(2025, 12, 15, tzinfo=UTC)
DENSITY = 0.6785
FACTOR = {"Continuous high-bleed": 0.62, "Continuous low-bleed": 0.04, "Intermittent": 0.25, "pump": 0.45}
BANDS = [("A", 0, 36, 330), ("B", 36, 48, 640), ("C", 48, 60, 950), ("D", 60, 72, 1360), ("E", 72, 1e9, 2000)]
KIND_CODE = {"TH": "HATCH", "CP": "COMBUSTOR", "PV": "RELIEF"}
DEFAULT = dict(rename=True, utc=True, merge_split=True, dedupe_parallel=True, rtu_time=True, start="expected",
               fit_group=None, fg_chain="chain", fg_survey="log", fg_rate="first", fg_prev="log", fg_clip=True,
               fg_repair="work", fg_route="apps", fg_sessions="full")
Y0, Y1 = dt.date(2026, 1, 1), dt.date(2027, 1, 1)
HALVES = (("h1", dt.date(2026, 1, 1), dt.date(2026, 7, 1)), ("h2", dt.date(2026, 7, 1), dt.date(2027, 1, 1)))


def band(t):
    for b, lo, hi, levy in BANDS:
        if lo <= t < hi:
            return b, levy
    raise ValueError(t)


# ---------------------------------------------------------------- time
def h_local(s):
    """'2026-01-05 07:41' local, or the check-in app's '2026-07-02T07:41:22-06:00' -> hours since the epoch"""
    d = s if isinstance(s, dt.datetime) else dt.datetime.fromisoformat(s)
    if d.tzinfo is None:
        d = d.replace(tzinfo=TZ)
    return (d.astimezone(UTC) - EPOCH).total_seconds() / 3600


def h_app(s, o):
    """an app time; mishandled, the check-in app's offset times are taken at their UTC wall-clock reading"""
    if o["utc"] or "T" not in str(s):
        return h_local(s)
    u = dt.datetime.fromisoformat(s).astimezone(UTC).replace(tzinfo=None)
    return h_local(u)


def h_utc(s):
    d = dt.datetime.fromisoformat(s.replace("Z", "+00:00")) if isinstance(s, str) else s
    if d.tzinfo is None:
        d = d.replace(tzinfo=UTC)
    return (d - EPOCH).total_seconds() / 3600


def local_day(h):
    return (EPOCH + dt.timedelta(hours=h)).astimezone(TZ).date()


def local_dt(h):
    return (EPOCH + dt.timedelta(hours=h)).astimezone(TZ).replace(tzinfo=None)


# ---------------------------------------------------------------- the register and the codes
def codes(p, rename=True):
    reg = {r["battery"]: r for r in p["register"]}
    cur = {c: c for c in reg}
    if rename:
        for c, r in reg.items():
            if r["former_battery"]:
                cur[r["former_battery"]] = c
    return reg, cur


def runs(p, cur):
    """the run each battery was on in each half of 2026: the route app's Route to 30 June, the check-in app's run
    from 1 July (the register carries the runs as at its 8 January 2027 export)"""
    h1, h2 = {}, {}
    for r in p["fieldlog"]:
        b = cur.get(r["Site"])
        if b is not None:
            h1.setdefault(b, collections.Counter())[r["Route"]] += 1
    site = {s["site_id"]: s["battery"] for s in p["sites"]}
    for r in p["sitelink"]:
        if dt.date(2026, 7, 1) <= dt.date.fromisoformat(r["check_in"][:10]) <= dt.date(2026, 12, 31):
            h2.setdefault(site[r["site"]], collections.Counter())[r["run"]] += 1
    return ({b: c.most_common(1)[0][0] for b, c in h1.items()}, {b: c.most_common(1)[0][0] for b, c in h2.items()},
            {b: len(c) for b, c in h1.items()}, {b: len(c) for b, c in h2.items()})


# ---------------------------------------------------------------- visits
def visits(p, o):
    reg, cur = codes(p, o["rename"])
    site = {s["site_id"]: s["battery"] for s in p["sites"]}
    by = {}
    for r in p["fieldlog"]:
        b = cur.get(r["Site"])
        if b is None:
            continue
        by.setdefault(b, []).append([h_local(r["Arrived"]), h_local(r["Departed"]), "FL"])
    for r in p["sitelink"]:
        b = site[r["site"]]
        by.setdefault(b, []).append([h_app(r["check_in"], o), h_app(r["check_out"], o), "SL"])
    out = {}
    for b, vs in by.items():
        vs.sort()
        merged = []
        for v in vs:
            if merged:
                m = merged[-1]
                gap = v[0] - m[1]
                same_app_split = o["merge_split"] and v[2] == "SL" and m[2] == "SL" and gap < 10 / 60
                both_apps = o["dedupe_parallel"] and v[2] != m[2] and v[0] < m[1] + 15 / 60
                if same_app_split or both_apps:
                    m[1] = max(m[1], v[1])
                    m[2] = m[2] if v[2] == m[2] else "FL+SL"
                    continue
            merged.append(list(v))
        out[b] = merged
    return out


def kind_of(text):
    t = text.lower()
    if "hatch" in t:
        return "TH"
    if any(k in t for k in ("pilot", "combustor", "ecd", "vcu", "flame")):
        return "CP"
    if any(k in t for k in ("pvrv", "relief", "prv", "vent valve")):
        return "PV"
    raise ValueError(text)


def events(p, o, vis):
    reg, cur = codes(p, o["rename"])
    out = []
    for r in p["events"]:
        b = cur.get(r["Battery"])
        if b is None:
            continue
        found, closed = h_app(r["Found"], o), h_app(r["Closed"], o)
        vs = vis.get(b, [])
        k = None
        for i, v in enumerate(vs):
            if v[0] - 5 / 60 <= found <= v[1] + 5 / 60:
                k = i
        if k is None:
            k = max(i for i, v in enumerate(vs) if v[0] <= found + 10 / 60)
        dep = vs[k - 1][1] if k > 0 else None
        out.append(dict(no=r["Event No"], bat=b, tank=r["Tank"], kind=kind_of(r["Event"]), found=found, closed=closed,
                        arr=vs[k][0], dep=dep, text=r["Event"]))
    return out


# ---------------------------------------------------------------- the alarm journal
RTU = re.compile(r"RTU (\d{4}-\d\d-\d\d \d\d:\d\d:\d\d)")


def journal(p, o):
    """tank pressure entries by point: (time, state), on the RTU's clock or the host's"""
    pts = {}
    for r in p["alarms"]:
        if r["State"] not in ("ALARM", "NORMAL"):
            continue
        m = RTU.search(r["Message"])
        t = h_utc(m.group(1)) if (o["rtu_time"] and m) else h_utc(r["Time"])
        pts.setdefault(r["Point"].split("/")[1], []).append((t, r["State"]))
    for k in pts:
        pts[k].sort()
    return pts


def alarm_start(pts, scada_code, found):
    """a relief valve that did not reseat lifted at the last burst of alarms before its find: an open valve holds the
    tank at atmospheric, so nothing follows it; chatter within a few minutes is the same lift"""
    seq = [x for x in pts.get(scada_code, []) if x[0] < found]
    alarms = [t for t, s in seq if s == "ALARM"]
    if not alarms:
        return None
    t = alarms[-1]
    for a in reversed(alarms[:-1]):
        if t - a < 5 / 60:
            t = a
        else:
            break
    return t


# ---------------------------------------------------------------- vapour rates
def rates(p, o):
    reg, cur = codes(p, o["rename"])
    an = {}
    for r in p["vapour"]:
        b = cur.get(r["Battery"])
        d = r["Sampled"].date() if isinstance(r["Sampled"], dt.datetime) else r["Sampled"]
        an.setdefault(b, []).append((d, float(r["Flash GOR (m3/m3)"]), float(r["C1"])))
    for b in an:
        an[b].sort()
    out = {}
    for r in p["production"]:
        b = cur.get(r["Battery"])
        if b is None:
            continue
        d = dt.date.fromisoformat(r["ProdDate"])
        if b not in an:
            continue
        cand = [a for a in an[b] if a[0] <= d]
        a = cand[-1] if cand else an[b][0]
        out[(b, d)] = float(r["OilVol_m3"]) * a[1] * a[2] / 100 * DENSITY / 24
    return out


def methane(rt, b, a, c):
    tot = 0.0
    t = a
    while t < c - 1e-9:
        loc = local_dt(t)
        mid = dt.datetime.combine(loc.date() + dt.timedelta(days=1), dt.time())
        t2 = min(c, h_local(mid))
        tot += rt.get((b, loc.date()), 0.0) * (t2 - t)
        t = t2
    return tot


# ---------------------------------------------------------------- the fit
def fit(y, w):
    """P(found by w) = 1 - (1 - p) exp(-b w): a share p the departing visit starts, a rate b an hour between visits"""
    def nll(x):
        p = 1 / (1 + np.exp(-x[0]))
        b = np.exp(x[1])
        F = 1 - (1 - p) * np.exp(-b * w)
        return -(y * np.log(np.clip(F, 1e-300, 1)) + (1 - y) * np.log(np.clip(1 - F, 1e-300, 1))).sum()
    best = None
    for x0 in ([-5.0, np.log(3e-4)], [-8.0, np.log(6e-4)], [-3.5, np.log(1e-4)]):
        r = minimize(nll, x0, method="Nelder-Mead", options=dict(xatol=1e-11, fatol=1e-11, maxiter=20000))
        if best is None or r.fun < best.fun:
            best = r
    r0 = minimize(lambda x: nll([-60.0, x[0]]), [np.log(3e-4)], method="Nelder-Mead",
                  options=dict(xatol=1e-11, fatol=1e-11))
    return dict(p=float(1 / (1 + np.exp(-best.x[0]))), b=float(np.exp(best.x[1])), lr=float(2 * (r0.fun - best.fun)),
                n=int(y.sum()), windows=int(len(y)))


def expected_hours(p, b, w):
    """expected hours from the start to the find, given the window w"""
    x = b * w
    F = p + (1 - p) * (-np.expm1(-x))
    g = np.where(x > 1e-4, (1 - np.exp(-x) * (1 + x)) / np.maximum(x, 1e-300), x / 2 - x * x / 3)
    return w - (1 - p) * w * g / F


def windows(p, o, vis, evs):
    reg, cur = codes(p, o["rename"])
    h1 = runs(p, cur)[0]
    at = {(e["bat"], round(e["arr"], 6)): e for e in evs}
    out = []
    for b, vs in vis.items():
        for a, c in zip(vs[:-1], vs[1:]):
            if local_day(c[0]).year != 2026:
                continue
            e = at.get((b, round(c[0], 6)))
            out.append(dict(bat=b, w=c[0] - a[1], kind=e["kind"] if e else None, tel=reg[b]["tank_pressure_telemetry"] == "Y",
                            comb=reg[b]["vapour_combustor"] == "Y", route=h1.get(b, reg[b]["route"]),
                            cls=reg[b]["visit_schedule"]))
    return out


def fits(win, group=None):
    w = np.array([x["w"] for x in win])
    elig = {"TH": np.ones(len(win), bool), "CP": np.array([x["comb"] for x in win]),
            "PV": ~np.array([x["tel"] for x in win])}
    out = {}
    for k in ("TH", "CP", "PV"):
        y = np.array([1.0 if x["kind"] == k else 0.0 for x in win])
        if group is None:
            out[k] = fit(y[elig[k]], w[elig[k]])
        else:
            keys = np.array([x[group] for x in win])
            out[k] = {g: fit(y[elig[k] & (keys == g)], w[elig[k] & (keys == g)]) for g in sorted(set(keys))}
    return out


# ---------------------------------------------------------------- Schedule B
def as_date(v):
    if v in (None, ""):
        return None
    return v.date() if isinstance(v, dt.datetime) else dt.date.fromisoformat(str(v)[:10])


def ref_day(ref):
    """the day a work order's reference carries: a field ticket's job day, a notification's day raised"""
    m = re.match(r"(FT|EHS|N) (\d{6})-\d{2}$", ref or "")
    return dt.datetime.strptime(m.group(2), "%y%m%d").date() if m else None


def leak_wos(p, mode="work"):
    """the tags each leak repair work order names, with the day of its repair: the field ticket's day for contract work
    (the maintenance system completes a contract order when its tickets are approved), the day completed otherwise"""
    out = {}
    for r in p["workorders"]:
        if r["Description"].startswith("Leak repair"):
            done = dt.date.fromisoformat(r["Completed"])
            ref = ref_day(r["Reference"])
            day = {"work": ref if r["Reference"].startswith("FT ") else done, "completed": done,
                   "refdate": ref or done}[mode]
            for t in re.findall(r"\((T-\d{5})\)", r["Description"]):
                out.setdefault(t, []).append(day)
    return out


def surveys(p, o, cur):
    """each battery's surveys: the sessions that screened its points, not the re-checks of a few repaired ones"""
    rows = {}
    for r in p["ldar_surveys"]:
        rows.setdefault(cur.get(r["Battery"], r["Battery"]), []).append(r)
    sv = {}
    for b, rs in rows.items():
        top = max(int(r["PointsScreened"]) for r in rs)
        keep = {"full": lambda r: int(r["PointsScreened"]) >= top / 2, "all": lambda r: True,
                "tagged": lambda r: int(r["LeaksTagged"]) > 0}[o["fg_sessions"]]
        sv[b] = sorted(dt.date.fromisoformat(r["Surveyed"]) for r in rs if keep(r))
    return sv


def fugitives(p, o, reg, cur):
    """each leak from the start of the day of its battery's last survey before it was first found until the start of
    the day it was repaired, at the rate measured when it was first found, by half of 2026. A tag's survey is its
    battery's last survey on or before the day the tag reached the tracker; a tag hung on a point whose earlier tag had
    not been repaired by that survey is the same leak found again; a leak is repaired on the day of the last leak
    repair that names its tag (a re-check that found it still leaking names the tag again)"""
    sv = surveys(p, o, cur)
    wos = leak_wos(p, o["fg_repair"]) if o["fg_repair"] != "tracker" else {}
    tags = []
    for r in p["ldar_tags"]:
        b = cur.get(r["Battery"], r["Battery"]) if o["rename"] else r["Battery"]
        d = as_date(r["Received"])
        if o["fg_survey"] == "log":
            d = [x for x in sv.get(b, []) if x <= d][-1]
        rep = max(wos[r["Tag"]]) if wos.get(r["Tag"]) else as_date(r["Closed"])
        tags.append(dict(bat=b, point=r["Component"], surveyed=d, rate=float(r["CH4 rate (g/h)"]), wo=r["Work order"],
                         repaired=rep))
    tags.sort(key=lambda x: (x["bat"], x["point"], x["surveyed"]))
    leaks = []
    if o["fg_chain"] == "workorder":
        by = {}
        for x in tags:
            if x["wo"]:
                by.setdefault(x["wo"], []).append(x)
            else:
                leaks.append(dict(bat=x["bat"], first=x["surveyed"], rate=x["rate"], last_rate=x["rate"],
                                  repaired=x["repaired"]))
        for xs in by.values():
            xs.sort(key=lambda x: x["surveyed"])
            leaks.append(dict(bat=xs[0]["bat"], first=xs[0]["surveyed"], rate=xs[0]["rate"], last_rate=xs[-1]["rate"],
                              repaired=xs[-1]["repaired"]))
    else:
        cur_leak, key = None, None
        for x in tags:
            k = (x["bat"], x["point"])
            same = cur_leak is not None and key == k and (
                o["fg_chain"] == "component" or
                (o["fg_chain"] in ("chain", "dropold") and
                 (cur_leak["repaired"] is None or cur_leak["repaired"] >= x["surveyed"])))
            if same and o["fg_chain"] == "dropold":
                cur_leak.update(first=x["surveyed"], rate=x["rate"], last_rate=x["rate"], repaired=x["repaired"])
            elif same:
                cur_leak["repaired"], cur_leak["last_rate"] = x["repaired"], x["rate"]
            else:
                cur_leak = dict(bat=x["bat"], first=x["surveyed"], rate=x["rate"], last_rate=x["rate"],
                                repaired=x["repaired"])
                leaks.append(cur_leak)
            key = k
    seen = {}
    for x in tags:
        seen.setdefault(x["bat"], []).append(x["surveyed"])
    kg = {}
    for lk in leaks:
        b = lk["bat"]
        days = sorted(set(sv.get(b, []) if o["fg_prev"] == "log" else seen.get(b, [])))
        prev = [d for d in days if d < lk["first"]]
        a = prev[-1] if prev else (Y0 if o["fg_clip"] else lk["first"])
        e = lk["repaired"] if lk["repaired"] is not None else Y1
        rate = lk["rate"] if o["fg_rate"] == "first" else lk["last_rate"]
        for h, lo, hi in HALVES:
            if not o["fg_clip"] and h == "h1":
                lo = dt.date(1900, 1, 1)
            n = max(0, (min(e, hi) - max(a, lo)).days)
            kg[(b, h)] = kg.get((b, h), 0.0) + rate * 24 * n / 1000
    return kg, leaks


def schedule_b(p, o, reg, cur):
    """Schedule B by route: each half's fugitive methane from the batteries each route ran in that half, in tonnes"""
    fg, _ = fugitives(p, o, reg, cur)
    h1, h2, _, _ = runs(p, cur)
    pick = {"apps": (h1, h2), "routeapp": (h1, h1), "checkin": (h2, h2),
            "register": ({c: r["route"] for c, r in reg.items()},) * 2,
            "registerH2": (h1, {c: r["route"] for c, r in reg.items()})}[o["fg_route"]]
    raw = {r["Site"]: r["Route"] for r in p["fieldlog"]}       # a code the register no longer carries
    sched = {rt: {h: 0.0 for h, lo, hi in HALVES} for rt in sorted(set(r["route"] for r in p["register"]))}
    for (c, h), v in fg.items():
        sched[(pick[0] if h == "h1" else pick[1]).get(c) or raw.get(c) or reg[c]["route"]][h] += v / 1000
    sched["field"] = {h: sum(v for (c, hh), v in fg.items() if hh == h) / 1000 for h, lo, hi in HALVES}
    return sched


# ---------------------------------------------------------------- the whole return
def compute(p=None, **opts):
    o = dict(DEFAULT, **opts)
    p = p or PR.read()
    reg, cur = codes(p, o["rename"])
    vis = visits(p, o)
    evs = events(p, o, vis)
    win = windows(p, o, vis, evs)
    rt = rates(p, o)
    pts = journal(p, o)
    fk = fits(win, o["fit_group"])
    scada = {c: (r["former_battery"] or c) for c, r in reg.items()}
    h1 = runs(p, cur)[0]
    rows = []
    for e in evs:
        b = e["bat"]
        tel = reg[b]["tank_pressure_telemetry"] == "Y"
        basis = "EXPECTED"
        st = None
        if e["kind"] == "PV" and tel:
            st = alarm_start(pts, scada[b], e["found"])
            basis = "ALARM"
        if st is None:
            w = e["arr"] - e["dep"]
            if o["start"] == "expected":
                f = fk[e["kind"]] if o["fit_group"] is None else fk[e["kind"]][
                    dict(route=h1.get(b, reg[b]["route"]), cls=reg[b]["visit_schedule"], bat=b)[o["fit_group"]]]
                st = e["arr"] - float(expected_hours(f["p"], f["b"], np.array([w]))[0])
            elif o["start"] == "midpoint":
                st = e["dep"] + w / 2
            elif o["start"] == "departure":
                st = e["dep"]
            elif o["start"] == "hatch_departure":
                st = e["dep"] if e["kind"] == "TH" else e["dep"] + w / 2
            elif o["start"] == "hatch_quarter":
                st = e["dep"] + (w / 4 if e["kind"] == "TH" else w / 2)
            elif o["start"] == "hatch_third":
                st = e["dep"] + (w / 3 if e["kind"] == "TH" else w / 2)
            basis = "EXPECTED"
        kg = methane(rt, b, st, e["closed"])
        dated = methane(rt, b, max(st, e["arr"]) if basis == "EXPECTED" else st, e["closed"])
        rows.append(dict(e, start=st, basis=basis, hours=e["closed"] - st, kg=kg, dated=dated,
                         route=h1.get(b, reg[b]["route"]), licence=reg[b]["facility_licence"]))
    total = sum(r["kg"] for r in rows) / 1000
    bnd, rate = band(total)
    held = sum(1 for r in p["register"] if r["status"] == "Active")
    levy = rate * held
    sched = schedule_b(p, o, reg, cur)
    return dict(rows=rows, total=total, band=bnd, rate=rate, held=held, levy=levy, fits=fk, windows=win, sched=sched,
                opts=o)


if __name__ == "__main__":
    g = compute()
    print("total %.2f t band %s levy %d" % (g["total"], g["band"], g["levy"]))
    print({k: (round(v["p"], 5), round(v["b"] * 1e4, 3), round(v["lr"], 1), v["n"]) for k, v in g["fits"].items()})
    for k, v in g["sched"].items():
        print(k, {a: round(b, 2) for a, b in v.items()})
