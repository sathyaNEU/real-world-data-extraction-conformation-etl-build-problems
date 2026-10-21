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
def ask_a(target, T=None, D=None):
    j = lambda k: os.path.join(target, FILES[k])
    ev = pd.read_csv(j("events"), dtype=str, keep_default_na=False)
    ev["t"] = pd.to_datetime(ev["event_utc"])
    seat = pd.read_csv(j("seat"), dtype=str)
    D = D or load(target)
    form_of = dict(zip(D["s"]["booking_ref"], D["s"]["form"]))
    win_of = dict(zip(D["s"]["booking_ref"], D["s"]["window"]))
    out = set()
    # a failure belongs to the sitting that started on that workstation before it, that day
    st = ev[ev["event"] == "SESSION_START"]
    for r in ev[ev["event"] == "WS_FAIL"].itertuples():
        c = st[(st["centre_code"] == r.centre_code) & (st["workstation"] == r.workstation) & (st["t"] <= r.t)
               & (st["t"].dt.date == r.t.date())]
        if len(c):
            out.add(c.sort_values("t").iloc[-1]["booking_ref"])
    # the Kochi power cut: every sitting at the centre running at 11:05 local on that date
    rep = pd.read_excel(j("incidents"), sheet_name=None, dtype=str)
    for centre, df in rep.items():
        for r in df.itertuples(index=False):
            if "Power cut" not in str(r.Report):
                continue
            d = dt.datetime.strptime(r.Date, "%d/%m/%Y").date()
            hh, mm = map(int, r.Time.split(":"))
            cut = pd.Timestamp(dt.datetime(d.year, d.month, d.day, hh, mm)) - pd.Timedelta(hours=5, minutes=30)
            code = {v: k for k, v in CODE_CENTRE.items()}[centre]
            sub = ev[(ev["centre_code"] == code) & (ev["t"].dt.date == cut.date())]
            starts = sub[sub["event"] == "SESSION_START"].set_index("booking_ref")["t"]
            ends = sub[sub["event"] == "SESSION_END"].set_index("booking_ref")["t"]
            for b, t0 in starts.items():
                if t0 <= cut and ends.get(b, cut) > cut:
                    out.add(b)
    counts = {f: 0 for f in F27}
    for b in out:
        if win_of.get(b, "").startswith("2027") and form_of.get(b) in counts:
            counts[form_of[b]] += 1
    return counts, out


# ------------------------------------------------------------------ ask B: sittings that ran partly offline
def ask_b(target, D=None, path="golden"):
    """each 2027 sitting whose examination clock ran while its workstation had lost the centre's link: a NET_LOST to
    the next NET_BACK on that workstation, or to the sitting's end when the link did not come back while it ran,
    overlapping the sitting's SESSION_START to SESSION_END"""
    j = lambda k: os.path.join(target, FILES[k])
    D = D or load(target)
    ev = pd.read_csv(j("events"), dtype=str, keep_default_na=False)
    ev["t"] = pd.to_datetime(ev["event_utc"])
    st = ev[ev["event"] == "SESSION_START"].groupby("booking_ref")["t"].min()
    en = ev[ev["event"] == "SESSION_END"].groupby("booking_ref")["t"].max()
    net = ev[ev["event"].isin(["NET_LOST", "NET_BACK"])].sort_values(["centre_code", "workstation", "t"])
    hit = set()
    for (cc, ws), g in net.groupby(["centre_code", "workstation"]):
        rows = list(g.itertuples(index=False))
        for k, r in enumerate(rows):
            if r.event != "NET_LOST":
                continue
            b = r.booking_ref
            if b not in st.index:
                continue
            nxt = next((q for q in rows[k + 1:] if q.event == "NET_BACK" and q.booking_ref == b), None)
            s0, e0 = st[b], en.get(b, st[b])
            if path == "lost_refs":
                hit.add(b)
                continue
            if path == "lost_within":
                if s0 <= r.t <= e0:
                    hit.add(b)
                continue
            if nxt is None:
                if path == "pairs_only":
                    continue
                hi = e0
            else:
                hi = nxt.t
            if max(s0, r.t) < min(e0, hi):
                hit.add(b)
    form_of = dict(zip(D["s"]["booking_ref"], D["s"]["form"]))
    win_of = dict(zip(D["s"]["booking_ref"], D["s"]["window"]))
    counts = {f: 0 for f in F27}
    for b in hit:
        if win_of.get(b, "").startswith("2027") and form_of.get(b) in counts:
            counts[form_of[b]] += 1
    return counts


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
