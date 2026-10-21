"""Every owed figure from the pack alone (target/), the way the golden computes it, with the ladder's routes.

The call: each 2027 form's exposure gain per resit sitting (regulation 7.2), the average over its resit sittings of
(a) the excess of the sitting's correct answers on the items an earlier sitting or held review had shown the
candidate (the same item reached at an earlier sitting, scored or trial, or an item written from the same item
model) over the candidate's own ability, read on the items nothing had shown them against the window's first-time
candidates' item statistics; plus (b) the correct answers on the items the sitting reached only because the items
the candidate recognised took less time than their own pace on the other items says they would have (each
recognised item's time at the first-time candidates' mean log time for it, shifted by the candidate's pace, carried
to where the four hours would have ended).   S.solve(target) -> dict"""
import datetime as dt
import os
import re
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build as BLD

FILES = BLD.FILES
WINDOWS = ["2026-02", "2026-05", "2026-08", "2026-11", "2027-02", "2027-05", "2027-08", "2027-11"]
F27 = ["CC27-%s" % x for x in "ABCDEFGHIJ"]
AREAS = ["ICD-10-CM diagnosis coding", "ICD-10-PCS procedure coding", "CPT surgery coding",
         "CPT evaluation and management", "HCPCS and modifiers", "Coding guidelines and conventions",
         "Documentation and query practice", "Compliance and reimbursement"]
LIMIT_S = 4 * 3600
THRESH = 1.0
CODE_CENTRE = {"MAA": "Chennai", "BLR": "Bengaluru", "HYD": "Hyderabad", "PNQ": "Pune", "COK": "Kochi", "NOI": "Noida"}


def lg(p):
    p = np.clip(p, 0.02, 0.98)
    return np.log(p / (1 - p))


# ------------------------------------------------------------------ loading
def load(target):
    j = lambda k: os.path.join(target, FILES[k])
    a = pd.read_csv(j("export3"), dtype={"candidate_no": str, "booking_ref": str}, keep_default_na=False)
    b = pd.read_csv(j("export4"), dtype={"cand_no": str, "booking_ref": str}, keep_default_na=False)
    a["secs"] = [np.array([float(v) if v != "" else np.nan for v in s.split("|")]) for s in a["item_seconds"]]
    b["secs"] = [np.array([float(v) / 1000 if v != "" else np.nan for v in s.split("|")]) for s in b["latency_ms"]]
    b = b.rename(columns={"cand_no": "candidate_no", "exam_window": "window", "form_code": "form",
                          "response_string": "responses", "raw_score": "score"})
    b["sitting_date"] = pd.to_datetime(b["sat_on"], format="%d-%m-%Y").dt.strftime("%Y-%m-%d")
    b["centre"] = b["test_centre"].map(CODE_CENTRE)
    cols = ["candidate_no", "booking_ref", "window", "sitting_date", "centre", "form", "responses", "secs", "score"]
    s = pd.concat([a[cols], b[cols]], ignore_index=True)
    s["w"] = s["window"].map({w: i for i, w in enumerate(WINDOWS)})
    cw = pd.read_csv(j("crosswalk"))
    old2new = dict(zip(cw["previous_item_id"], cw["item_id"]))
    lay = pd.read_csv(j("layouts"))
    lay["item"] = [old2new.get(i, i) for i in lay["item_id"]]
    L = {}
    for (win, f), g in lay.sort_values(["window", "form", "position"]).groupby(["window", "form"]):
        L[(win, f)] = (g["item"].to_numpy(), (g["slot"] == "scored").to_numpy())
    bank = pd.read_excel(j("bank"), dtype=str)
    key = dict(zip(bank["item_id"], bank["key"]))
    model = dict(zip(bank["item_id"], bank["item_model"]))
    area = dict(zip(bank["item_id"], bank["content_area"]))
    reg = pd.read_csv(j("register"), dtype=str)
    link = dict(zip(reg["candidate_no"], reg["previous_candidate_no"]))

    def person(n):
        while n in link:
            n = link[n]
        return n
    s["person"] = [person(n) for n in s["candidate_no"]]
    rv = pd.read_csv(j("reviews"), dtype=str)
    rv = rv[rv["status"] == "held"]
    rv["person"] = [person(n) for n in rv["candidate_no"]]
    held = set(zip(rv["person"], rv["sitting_window"]))
    return dict(s=s, L=L, key=key, model=model, area=area, held=held, old2new=old2new, bank=bank)


def sittings(D):
    """per sitting: delivered items, scored mask, correct, reached, seconds"""
    s, L, key = D["s"], D["L"], D["key"]
    out = []
    for r in s.itertuples(index=False):
        items, scored = L[(r.window, r.form)]
        resp = np.array(list(r.responses))
        reach = resp != "-"
        k = np.array([key[i] for i in items])
        x = ((resp == k) & reach).astype(int)
        out.append(dict(person=r.person, w=int(r.w), window=r.window, form=r.form, items=items, scored=scored,
                        x=x, reach=reach, secs=r.secs, raw=int(r.score), booking=r.booking_ref,
                        date=r.sitting_date, centre=r.centre, cand=r.candidate_no))
    by_p = {}
    for i, t in enumerate(out):
        by_p.setdefault(t["person"], []).append(i)
    for p, idx in by_p.items():
        idx.sort(key=lambda i: (out[i]["w"], out[i]["date"]))
        for n, i in enumerate(idx):
            out[i]["prev"] = idx[:n]
    return out


def norms(T):
    """the window's first-time candidates' share correct and mean log seconds per (window, item), among those who
    answered it"""
    num, den, ls = {}, {}, {}
    var = []
    for t in T:
        if t["prev"] or t["w"] < 4:
            continue
        for it, xv, rc, sc in zip(t["items"], t["x"], t["reach"], t["secs"]):
            if rc:
                k = (t["w"], it)
                num[k] = num.get(k, 0) + xv
                den[k] = den.get(k, 0) + 1
                ls.setdefault(k, []).append(np.log(sc))
    mu = {k: float(np.mean(v)) for k, v in ls.items()}
    p = {k: num[k] / den[k] for k in den}
    return p, mu


def exposure(T, t, D):
    """the delivered items an earlier sitting or held review had shown the candidate: same item reached (scored or
    trial), or an item from the same item model; review: scored items answered wrongly at a sitting reviewed"""
    model = D["model"]
    seen, rev, seen_models = set(), set(), set()
    for i in t["prev"]:
        h = T[i]
        for it, rc, xv, sc in zip(h["items"], h["reach"], h["x"], h["scored"]):
            if rc:
                seen.add(it)
                seen_models.add(model[it])
        if (h["person"], h["window"]) in D["held"]:
            for it, rc, xv, sc in zip(h["items"], h["reach"], h["x"], h["scored"]):
                if rc and sc and not xv:
                    rev.add(it)
    same = np.array([it in seen for it in t["items"]])
    sib = np.array([model[it] in seen_models for it in t["items"]]) & ~same
    return same, sib, rev


def rasch_shift(xv, ep):
    sh = 0.0
    for _ in range(25):
        pp = 1 / (1 + np.exp(-(lg(ep) + sh)))
        step = (xv.sum() - pp.sum()) / max((pp * (1 - pp)).sum(), 1e-6)
        sh += step
        if abs(step) < 1e-9:
            break
    return sh


def sitting_gain(t, same, sib, Pn, Mu, variant="golden"):
    """(direct, reach) for one resit sitting under a variant of the golden family"""
    sc = t["scored"]
    w = t["w"]
    ep = np.array([Pn.get((w, it), np.nan) for it in t["items"]])
    mj = np.array([Mu.get((w, it), np.nan) for it in t["items"]])
    expo = same | sib
    ok = ~np.isnan(ep)
    x, rc, secs = t["x"], t["reach"], t["secs"]
    u = sc & ok & rc & ~expo
    if "blanks" in variant:                       # blanks scored wrong in the baseline (R2)
        u = sc & ok & ~expo
    sh = rasch_shift(x[u], ep[u])
    pe = 1 / (1 + np.exp(-(lg(ep) + sh)))
    if variant.endswith("add"):
        pe = np.clip(ep + (x[u].mean() - ep[u].mean()), 0, 1)
    tu = rc & ~expo & ~np.isnan(mj)
    lr = np.log(secs[tu]) - mj[tu]
    pace = float(np.mean(lr))
    corr = np.exp(float(np.var(lr)) / 2) if "median" not in variant else 1.0
    t0 = np.where(rc & expo & ~np.isnan(mj), np.exp(mj + pace) * corr, np.where(rc, secs, 0.0))
    cum_cf = np.cumsum(np.where(rc, t0, 0.0))
    r_cf = rc & (cum_cf <= LIMIT_S)
    if "hit" in variant and rc[-1]:
        r_cf = rc
    cnt = np.ones_like(sc) if "trial" in variant else sc   # trial positions counted with the scored (R2)
    reach = float((x * (rc & ~r_cf) * cnt).sum())
    e_cf = cnt & ok & r_cf & expo
    direct = float((x[e_cf] - pe[e_cf]).sum())
    return direct, reach


def call(target, D=None, T=None):
    D = D or load(target)
    T = T or sittings(D)
    Pn, Mu = norms(T)
    res = {f: [] for f in F27}
    routes = {f: {} for f in F27}
    ladder_keys = ["direct", "direct_blanks_wrong", "same_item", "raw_within", "golden", "golden_add", "golden_median",
                   "golden_hit", "golden_median_hit"]
    for f in F27:
        routes[f] = {k: [] for k in ladder_keys + ["between"]}
    for t in T:
        if t["w"] < 4 or not t["prev"] or t["form"] not in res:
            continue
        same, sib, rev = exposure(T, t, D)
        f = t["form"]
        d, r = sitting_gain(t, same, sib, Pn, Mu, "golden")
        routes[f]["golden"].append(d + r)
        res[f].append((d, r))
        for v in ("golden_add", "golden_median", "golden_hit", "golden_median_hit"):
            dv, rv_ = sitting_gain(t, same, sib, Pn, Mu, v)
            routes[f][v].append(dv + rv_)
        sc, x, rc = t["scored"], t["x"], t["reach"]
        w = t["w"]
        ep = np.array([Pn.get((w, it), np.nan) for it in t["items"]])
        ok = ~np.isnan(ep)
        expo = same | sib
        u = sc & ok & rc & ~expo
        sh = rasch_shift(x[u], ep[u])
        pe = 1 / (1 + np.exp(-(lg(ep) + sh)))
        e = sc & ok & rc & expo
        routes[f]["direct"].append(float((x[e] - pe[e]).sum()))
        u2 = sc & ok & ~expo
        sh2 = rasch_shift(x[u2], ep[u2])
        pe2 = 1 / (1 + np.exp(-(lg(ep) + sh2)))
        e2 = sc & ok & expo
        routes[f]["direct_blanks_wrong"].append(float((x[e2] - pe2[e2]).sum()))
        e3 = sc & ok & rc & same
        u3 = sc & ok & rc & ~same
        sh3 = rasch_shift(x[u3], ep[u3])
        pe3 = 1 / (1 + np.exp(-(lg(ep) + sh3)))
        routes[f]["same_item"].append(float((x[e3] - pe3[e3]).sum()))
        routes[f]["raw_within"].append(float((x[e].mean() - x[u].mean()) * e.sum()) if e.any() and u.any() else 0.0)
        routes[f]["between"].append(t["raw"] - T[t["prev"][-1]]["raw"])
    gain = {f: float(np.mean([d + r for d, r in res[f]])) for f in F27}
    comp = {f: dict(direct=float(np.mean([d for d, r in res[f]])), reach=float(np.mean([r for d, r in res[f]])),
                    n=len(res[f])) for f in F27}
    table = {f: {k: float(np.mean(v)) for k, v in routes[f].items()} for f in F27}
    flagged = [f for f in F27 if gain[f] > THRESH]
    return dict(gain=gain, comp=comp, flagged=flagged, routes=table, D=D, T=T)


def flagged(table, route):
    return [f for f in F27 if table[f][route] > THRESH]


# ------------------------------------------------------------------ ask A: sittings interrupted
FAILURE_WORDS = ("stopped responding", "froze", "hung", "not responding", "crashed", "frozen", "stopped working",
                 "went blank", "stuck")
IST = pd.Timedelta(hours=5, minutes=30)


def events(target):
    ev = pd.read_csv(os.path.join(target, FILES["events"]), dtype=str, keep_default_na=False)
    ev["t"] = pd.to_datetime(ev["event_utc"])
    return ev


def reports(target):
    """every invigilator report: (centre code, ISO date, session, local time, workstation, text)"""
    rep = pd.read_excel(os.path.join(target, FILES["incidents"]), sheet_name=None, dtype=str, keep_default_na=False)
    code = {v: k for k, v in CODE_CENTRE.items()}
    out = []
    for centre, df in rep.items():
        for r in df.itertuples(index=False):
            d = dt.datetime.strptime(r.Date, "%d/%m/%Y").date().isoformat()
            out.append((code[centre], d, r.Session, r.Time, r.Workstation, str(r.Report)))
    return out


def local(d, hm):
    """a report's local date and hh:mm as a UTC timestamp"""
    hh, mm = map(int, hm.split(":"))
    return pd.Timestamp(d) + pd.Timedelta(hours=hh, minutes=mm) - IST


def power_cut(target, ev):
    """the sittings running at the centre when the reported power cut began"""
    hit = set()
    for cc, d, sess, tm, wsx, text in reports(target):
        if "power cut" not in text.lower():
            continue
        cut = local(d, tm)
        sub = ev[(ev["centre_code"] == cc) & (ev["t"].dt.date == cut.date())]
        starts = sub[sub["event"] == "SESSION_START"].set_index("booking_ref")["t"]
        ends = sub[sub["event"] == "SESSION_END"].set_index("booking_ref")["t"]
        for b, t0 in starts.items():
            if t0 <= cut and ends.get(b, cut) > cut:
                hit.add(b)
    return hit


def hall_stops(target, ev):
    """the reports of a whole hall's clocks stopped (a fire alarm, a switch of the building's power): each sitting
    running then is stopped from that time to its own next SESSION_RESUME"""
    stops = {}
    for cc, d, sess, tm, wsx, text in reports(target):
        m = re.search(r"All clocks stopped at (\d\d:\d\d)", text)
        if not m:
            continue
        t = local(d, m.group(1))
        sub = ev[(ev["centre_code"] == cc) & (ev["t"].dt.date == t.date())]
        starts = sub[sub["event"] == "SESSION_START"].set_index("booking_ref")["t"]
        ends = sub[sub["event"] == "SESSION_END"].set_index("booking_ref")["t"]
        res = sub[(sub["event"] == "SESSION_RESUME") & (sub["t"] > t)].groupby("booking_ref")["t"].min()
        for b, t0 in starts.items():
            if t0 < t < ends.get(b, t) and b in res.index:
                stops.setdefault(b, []).append((t, res[b]))
    return stops


def per_form(D, bookings):
    form_of = dict(zip(D["s"]["booking_ref"], D["s"]["form"]))
    win_of = dict(zip(D["s"]["booking_ref"], D["s"]["window"]))
    counts = {f: 0 for f in F27}
    for b in bookings:
        if win_of.get(b, "").startswith("2027") and form_of.get(b) in counts:
            counts[form_of[b]] += 1
    return counts


def ask_a_sets(target, ev=None):
    """the sets a response could build for ask A: each WS_FAIL as logged, inside its sitting, or followed by the
    sitting's stop; the restarts in place (a WS_REBOOT of the sitting's workstation before its resume there); the
    failures, pauses and changes of seat the invigilators reported; the power cut"""
    ev = events(target) if ev is None else ev
    sit = ev[ev["booking_ref"] != ""].sort_values(["t", "event"])
    by_b = {b: g for b, g in sit.groupby("booking_ref")}
    end = sit[sit["event"] == "SESSION_END"].groupby("booking_ref")["t"].max()
    out = {k: set() for k in ("fail_any", "fail_in", "fail_stop", "restarted", "spare_rep", "inplace_rep", "late_rep",
                              "unexplained")}
    for r in sit[sit["event"] == "WS_FAIL"].itertuples(index=False):
        out["fail_any"].add(r.booking_ref)
        if r.t < end.get(r.booking_ref, r.t):
            out["fail_in"].add(r.booking_ref)
        g = by_b[r.booking_ref]
        nxt = g[(g["t"] > r.t) & (g["event"] != "WS_FAIL")]
        if len(nxt) and nxt.iloc[0]["event"] in ("SESSION_RESUME", "SESSION_END"):
            out["fail_stop"].add(r.booking_ref)
    boots = {}
    for r in ev[ev["event"] == "WS_REBOOT"].itertuples(index=False):
        boots.setdefault((r.centre_code, r.workstation), []).append(r.t)
    resumes = sit[sit["event"] == "SESSION_RESUME"]
    for r in resumes.itertuples(index=False):
        if r.workstation.startswith("SP"):
            continue
        g = by_b[r.booking_ref]
        prev = g[g["t"] < r.t]["t"].max()
        if any(prev < t <= r.t for t in boots.get((r.centre_code, r.workstation), [])):
            out["restarted"].add(r.booking_ref)
    at_min = {}
    for r in resumes.itertuples(index=False):
        loc = r.t + IST
        at_min.setdefault((r.centre_code, loc.date().isoformat(), loc.strftime("%H:%M")), []).append(r)
    explained = set()
    for cc, d, sess, tm, wsx, text in reports(target):
        low = text.lower()
        times = re.findall(r"\b(\d\d:\d\d)\b", text)
        sp = re.search(r"\b(SP\d\d)\b", text)
        if "all clocks stopped" in low or "power cut" in low:
            continue
        failure = any(w in low for w in FAILURE_WORDS)
        hits = []
        if times:
            cands = at_min.get((cc, d, times[-1]), [])
            if sp:
                hits = [q for q in cands if q.workstation == sp.group(1)]
            else:
                hits = [q for q in cands if not q.workstation.startswith("SP")]
                if len(hits) > 1 and any(q.workstation == wsx for q in hits):
                    hits = [q for q in hits if q.workstation == wsx]
        for q in hits:
            explained.add(q.booking_ref)
        if not failure:
            continue
        if sp and hits:
            out["spare_rep"] |= {q.booking_ref for q in hits}
        elif hits:
            out["inplace_rep"] |= {q.booking_ref for q in hits}
        elif not sp:
            t = local(d, tm)
            near = sit[(sit["event"] == "WS_FAIL") & (sit["centre_code"] == cc) & (sit["t"] >= t - pd.Timedelta(minutes=1))
                       & (sit["t"] <= t + pd.Timedelta(minutes=5))]
            out["late_rep"] |= set(near["booking_ref"])
    halls = hall_stops(target, ev)
    for r in resumes.itertuples(index=False):
        if r.booking_ref not in explained and r.booking_ref not in halls and not r.workstation.startswith("SP"):
            out["unexplained"].add(r.booking_ref)
    out["power"] = power_cut(target, ev)
    return out


A_ROUTES = {
    "golden": ("fail_stop", "restarted", "spare_rep", "power"),
    "v2_route": ("fail_any", "spare_rep", "inplace_rep", "late_rep", "power"),
    "in_sitting": ("fail_in", "spare_rep", "inplace_rep", "late_rep", "power"),
    "stopped_fail": ("fail_stop", "spare_rep", "inplace_rep", "late_rep", "power"),
    "reboots": ("fail_any", "restarted", "spare_rep", "power"),
    "in_sitting_reboots": ("fail_in", "restarted", "spare_rep", "power"),
    "unexplained": ("fail_stop", "spare_rep", "inplace_rep", "unexplained", "power"),
    "ws_fail_only": ("fail_any",),
    "no_power": ("fail_stop", "restarted", "spare_rep"),
}


def ask_a(target, T=None, D=None, path="golden", sets=None):
    """each 2027 sitting a failure of the candidate's workstation or its power interrupted: a WS_FAIL the sitting stopped
    after (its next event a resume or its end), a restart of its workstation before it resumed there, a failure of a
    computer, keyboard, mouse or screen the invigilators reported with the spare it resumed on, and the sittings running
    at Kochi when the power cut began; pauses, changes of seat and the two hall stops are not failures"""
    D = D or load(target)
    sets = sets or ask_a_sets(target)
    out = set().union(*[sets[k] for k in A_ROUTES[path]])
    return per_form(D, out), out


def net_intervals(ev):
    """each client's logged link state: (booking, workstation) -> intervals from a NET_LOST to its next NET_BACK (or to
    the sitting's end), or from the client's login to a NET_BACK with no NET_LOST before it; and whether another client
    at the centre logged the same loss"""
    st = ev[ev["event"] == "SESSION_START"].groupby("booking_ref")["t"].min()
    en = ev[ev["event"] == "SESSION_END"].groupby("booking_ref")["t"].max()
    login = {}
    for r in ev[ev["event"].isin(["TUTORIAL_START", "SESSION_RESUME"])].sort_values("t").itertuples(index=False):
        login.setdefault((r.booking_ref, r.workstation), r.t)
    net = ev[ev["event"].isin(["NET_LOST", "NET_BACK"])].sort_values("t")
    out = []
    for (b, wsx), g in net.groupby(["booking_ref", "workstation"]):
        if b not in st.index:
            continue
        e0 = en.get(b, st[b])
        opened, lone = None, False
        for r in g.itertuples(index=False):
            if r.event == "NET_LOST":
                if opened is None:
                    opened = r.t
            elif opened is not None:
                out.append(dict(b=b, ws=wsx, cc=r.centre_code, a=opened, z=r.t, lone=False))
                opened = None
            else:
                out.append(dict(b=b, ws=wsx, cc=r.centre_code, a=login.get((b, wsx), st[b]), z=r.t, lone=True))
        if opened is not None:            # down until the client logged off (a finished candidate's too)
            out.append(dict(b=b, ws=wsx, cc=g.iloc[-1]["centre_code"], a=opened, z=max(e0, opened), lone=False))
    # a loss is the centre's when another client there logged a NET row while it lasted
    rows = net[["centre_code", "booking_ref", "workstation", "t"]].values.tolist()
    by_cc = {}
    for cc, b, wsx, t in rows:
        by_cc.setdefault(cc, []).append((t, b, wsx))
    for v in by_cc.values():
        v.sort()
    for iv in out:
        lo, hi = iv["a"] - pd.Timedelta(minutes=2), iv["z"] + pd.Timedelta(minutes=2)
        iv["shared"] = any(lo <= t <= hi and (b, wsx) != (iv["b"], iv["ws"]) for t, b, wsx in by_cc[iv["cc"]])
    return out, st, en


def offline_sets(target, D=None):
    """the sets a response could build for the link item"""
    ev = events(target)
    ivs, st, en = net_intervals(ev)
    halls = hall_stops(target, ev)

    def running(b):
        run = [(st[b], en[b])]
        for a, z in halls.get(b, []):
            nxt = []
            for p, q in run:
                if z <= p or a >= q:
                    nxt.append((p, q))
                    continue
                if p < a:
                    nxt.append((p, a))
                if z < q:
                    nxt.append((z, q))
            run = nxt
        return run

    sets = {k: set() for k in ("golden", "per_booking", "per_booking_stops", "centre_only", "pairs_only", "lost_refs")}
    for iv in ivs:
        b = iv["b"]
        hit_clock = max(st[b], iv["a"]) < min(en[b], iv["z"])
        hit_run = any(max(p, iv["a"]) < min(q, iv["z"]) for p, q in running(b))
        if hit_clock:
            sets["per_booking"].add(b)
        if hit_run:
            sets["per_booking_stops"].add(b)
        if iv["shared"] and hit_clock:
            sets["centre_only"].add(b)
        if iv["shared"] and hit_run:
            sets["golden"].add(b)
            if not iv["lone"]:
                sets["pairs_only"].add(b)
    sets["lost_refs"] = set(ev[ev["event"] == "NET_LOST"]["booking_ref"])
    power = power_cut(target, ev)
    sets["no_power"] = set(sets["golden"])
    for k in ("golden", "per_booking", "per_booking_stops", "centre_only", "pairs_only"):
        sets[k] |= power
    return sets


def ask_b(target, D=None, path="golden", sets=None):
    """each 2027 sitting whose examination clock ran while the centre's link was down, as its client logged the loss:
    a loss one client logged alone is that workstation's own connection, not the centre's link, and a loss inside a hall
    stop (every clock stopped before the link went) ran no clock; the Kochi power cut's minutes on the UPS with the
    router down count"""
    D = D or load(target)
    sets = sets or offline_sets(target, D)
    return per_form(D, sets[path])


def solve(target):
    C = call(target)
    A, _ = ask_a(target, D=C["D"])
    Bk = ask_b(target, D=C["D"])
    return dict(gain=C["gain"], comp=C["comp"], flagged=C["flagged"], routes=C["routes"], ask_a=A, ask_b=Bk)


if __name__ == "__main__":
    tgt = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "target")
    S = solve(tgt)
    for f in F27:
        r = S["routes"][f]
        print("%s gain %.2f (direct %.2f reach %.2f, n %d)  direct %.2f blanksw %.2f same %.2f raw %.2f between %.2f"
              % (f, S["gain"][f], S["comp"][f]["direct"], S["comp"][f]["reach"], S["comp"][f]["n"], r["direct"],
                 r["direct_blanks_wrong"], r["same_item"], r["raw_within"], r["between"]))
    for k in ["golden", "golden_add", "golden_median", "golden_hit", "golden_median_hit", "direct",
              "direct_blanks_wrong", "same_item", "raw_within", "between"]:
        print("%-20s %s" % (k, "".join(f[-1] for f in flagged(S["routes"], k))))
    print("ask A", S["ask_a"])
    print("ask B", S["ask_b"])
