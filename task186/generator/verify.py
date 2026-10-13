"""Independent verifier: reads only target/ (and the goldens to compare), on its own code path, and recomputes the call,
each brand's share of examined stations found, each brand's regular litres in January, February and March 2026 and
each brand's stations priced by the brand on 1 December 2026; then checks figures.json and both goldens against them.

    python3 task186/generator/verify.py"""
import csv
import datetime as dt
import json
import math
import os
import re
import sys
from collections import Counter, defaultdict

import numpy as np
import openpyxl

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
D0, D1 = dt.date(2025, 1, 1), dt.date(2026, 11, 15)
CHANGE = dt.date(2026, 1, 1)
SCOPE = dt.date(2026, 12, 1)
Q1 = [dt.date(2026, 1, 1), dt.date(2026, 2, 1), dt.date(2026, 3, 1)]


def rd(target, name):
    return os.path.join(target, name)


def find(target, prefix):
    return [f for f in sorted(os.listdir(target)) if f.startswith(prefix)][0]


# ------------------------------------------------------------------------------------------------- clocks
def second_sunday_march(y):
    d = dt.date(y, 3, 1)
    return d + dt.timedelta(days=(6 - d.weekday()) % 7 + 7)


def first_sunday_november(y):
    d = dt.date(y, 11, 1)
    return d + dt.timedelta(days=(6 - d.weekday()) % 7)


def to_local(ts):
    """UTC stamp to local wall time: UTC-4 from 02:00 on the second Sunday in March to 02:00 on the first Sunday in
    November, UTC-5 otherwise (the extract notes)"""
    t = dt.datetime.strptime(ts, "%Y-%m-%dT%H:%M:%SZ")
    on = dt.datetime.combine(second_sunday_march(t.year), dt.time(7, 0))
    off = dt.datetime.combine(first_sunday_november(t.year), dt.time(6, 0))
    return t - dt.timedelta(hours=4 if on <= t < off else 5)


# ------------------------------------------------------------------------------------------------- registers
def load_register(target):
    wb = openpyxl.load_workbook(rd(target, find(target, "station_register")), read_only=True)
    st = {}
    rows = list(wb["Stations"].iter_rows(values_only=True))
    head = rows[0]
    for r in rows[1:]:
        x = dict(zip(head, r))
        for k in ("opened", "closed"):
            if isinstance(x[k], dt.datetime):
                x[k] = x[k].date()
        st[str(x["station_number"])] = x
    hist = defaultdict(list)
    rows = list(wb["Brand history"].iter_rows(values_only=True))
    for r in rows[1:]:
        x = dict(zip(rows[0], r))
        f = x["valid_from"].date() if isinstance(x["valid_from"], dt.datetime) else x["valid_from"]
        t = x["valid_to"].date() if isinstance(x["valid_to"], dt.datetime) else x["valid_to"]
        hist[str(x["station_number"])].append((x["brand_code"], f, t))
    return st, hist


def brand_on(hist, sid, d):
    for b, f, t in hist.get(sid, []):
        if f <= d and (t is None or d <= t):
            return b
    return None


def crosswalk(target):
    with open(rd(target, find(target, "station_renumbering")), encoding="utf-8") as fh:
        return {r["old_number"]: r["new_number"] for r in csv.DictReader(fh)}


def levy_cents(target):
    from pypdf import PdfReader
    text = " ".join(p.extract_text() for p in PdfReader(rd(target, find(target, "carbon_levy"))).pages)
    out = {}
    for y, tonne, gas, dsl in re.findall(r"\b(20\d\d)\s+(\d+)\s+(\d+\.\d\d)\s+(\d+\.\d\d)", text):
        out[int(y)] = float(gas)
    return out


def rack_cents(target):
    pub = {}
    with open(rd(target, find(target, "terminal_rack")), encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            if r["product"] == "RUL":
                pub[dt.date.fromisoformat(r["price_date"])] = float(r["rack_cad_per_litre"]) * 100
    out, last = {}, None
    d = min(pub)
    while d <= D1:
        last = pub.get(d, last)
        out[d] = last
        d += dt.timedelta(days=1)
    return out


# ------------------------------------------------------------------------------------------------- the main call
def daily_prices(events, days, closed):
    """time-weighted price over 06:00 to 22:00 local on each day with a price in force at 06:00"""
    out = np.full(len(days), np.nan)
    j, cur = 0, None
    ev = sorted(events)
    for k, d in enumerate(days):
        if closed is not None and d >= closed:
            break
        today = []
        while j < len(ev) and ev[j][0] == d:
            today.append(ev[j][1:])
            j += 1
        start = cur
        for minute, p in today:
            if minute <= 360:
                start = p
        if start is not None:
            tot, t, p = 0.0, 360, start
            for minute, q in today:
                if minute <= 360:
                    continue
                if minute >= 1320:
                    break
                tot += p * (minute - t)
                t, p = minute, q
            tot += p * (1320 - t)
            out[k] = tot / 960.0
        if today:
            cur = today[-1][1]
    return out


def window_changes(m, w=28, need=20):
    ok = ~np.isnan(m)
    cs = np.r_[0.0, np.cumsum(np.where(ok, m, 0.0))]
    cn = np.r_[0, np.cumsum(ok)]
    n = len(m)
    ks = np.arange(w, n - w + 1)
    sa, na = cs[ks + w] - cs[ks], cn[ks + w] - cn[ks]
    sb, nb = cs[ks] - cs[ks - w], cn[ks] - cn[ks - w]
    with np.errstate(invalid="ignore", divide="ignore"):
        ch = sa / na - sb / nb
    ch[(na < need) | (nb < need)] = np.nan
    return ks, ch


def benjamini_hochberg(p, q=0.05):
    p = np.asarray(p)
    o = np.argsort(p, kind="mergesort")
    m = len(p)
    ok = p[o] <= q * np.arange(1, m + 1) / m
    k = int(np.max(np.where(ok)[0]) + 1) if ok.any() else 0
    f = np.zeros(m, bool)
    f[o[:k]] = True
    return f


def main_call(target):
    st, hist = load_register(target)
    xw = crosswalk(target)
    brands = json.load(open(rd(target, find(target, "monitored_brand"))))["brands"]
    codes = [b["brand_code"] for b in brands]
    levy = levy_cents(target)
    rack = rack_cents(target)
    days = [D0 + dt.timedelta(days=k) for k in range((D1 - D0).days + 1)]
    lev = np.array([levy[d.year] for d in days])
    rk = np.array([rack[d] for d in days])
    seen = set()
    events = defaultdict(list)
    with open(rd(target, find(target, "price_change_log")), encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            sid = xw.get(r["station_number"], r["station_number"])
            key = (sid, r["effective_utc"], r["price_cents_per_litre"])
            if key in seen:
                continue                      # a change the platform re-sent after an outage
            seen.add(key)
            t = to_local(r["effective_utc"])
            events[sid].append((t.date(), t.hour * 60 + t.minute, float(r["price_cents_per_litre"])))
    ch = (CHANGE - D0).days
    ex = []
    for sid in sorted(events):
        b = brand_on(hist, sid, CHANGE)
        if b not in codes:
            continue
        price = daily_prices(events[sid], days, st[sid]["closed"])
        m = price / 1.05 - lev - rk
        ks, chg = window_changes(m)
        d = chg[ks == ch][0]
        if np.isnan(d):
            continue
        ref = chg[((ks <= ch - 28) | (ks >= ch + 28)) & ~np.isnan(chg)]
        ex.append((sid, b, float(d), (1 + int(np.sum(ref >= d))) / (len(ref) + 1)))
    found = benjamini_hochberg([x[3] for x in ex])
    share = {}
    for b in codes:
        idx = [i for i, x in enumerate(ex) if x[1] == b]
        share[b] = (int(found[idx].sum()), len(idx))
    top = max(codes, key=lambda b: share[b][0] / share[b][1])
    best = share[top][0] / share[top][1]
    call = top if best >= 0.1 and sum(1 for b in codes if share[b][0] / share[b][1] == best) == 1 else None
    return {"codes": codes, "names": {b["brand_code"]: b["brand"] for b in brands}, "ex": ex, "found": found,
            "share": share, "call": call, "register": st, "history": hist}


# ------------------------------------------------------------------------------------------------- the asks
ABBR = {"st": "street", "rd": "road", "ave": "avenue", "hwy": "highway", "dr": "drive", "ln": "lane"}


def norm(text):
    return " ".join(ABBR.get(w, w) for w in text.replace(",", " ").casefold().split())


def month_end(m):
    return (m + dt.timedelta(days=32)).replace(day=1) - dt.timedelta(days=1)


def litres(target, st, hist, codes):
    latest = {}
    with open(rd(target, find(target, "fuel_sales_survey_returns")), encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            k = (r["survey_reference"], r["reference_month"])
            if k not in latest or int(r["revision"]) > int(latest[k]["revision"]):
                latest[k] = r
    frame, since = {}, {}
    with open(rd(target, find(target, "fuel_sales_survey_frame")), encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            frame[r["survey_reference"]] = r["station_number"]
            since[r["survey_reference"]] = dt.date.fromisoformat(r["on_frame_since"])
    by_site = defaultdict(list)
    for sid, x in st.items():
        by_site[norm(x["street_address"] + " " + x["area"])].append(sid)
    out = defaultdict(int)
    resolved = 0
    for (ref, month), r in latest.items():
        m = dt.date.fromisoformat(month + "-01")
        if m not in Q1:
            continue
        sid = frame[ref]
        if since[ref] > month_end(m):
            # the reference was freed and given to a station that joined the frame after this month: the return is
            # the site it names
            cands = [s for s in by_site[norm(r["site_address"])] if st[s]["opened"] <= month_end(m)]
            assert len(cands) == 1, (ref, month, r["site_address"], cands)
            sid = cands[0]
            resolved += 1
        b = brand_on(hist, sid, max(m, st[sid]["opened"]))
        if b in codes:
            out[(b, m)] += int(r["regular_litres"])
    return {b: [out[(b, m)] for m in Q1] for b in codes}, resolved


def priced_by_brand(target, st, hist, codes):
    """a brand's pricing desk pushes its stations' prices through the API at the same minutes of the day: the push
    times are the minutes of the day at which three or more of the brand's stations submitted regular prices through
    the API in November, and a station is priced by its brand when most of its regular-price changes came at them"""
    pushers = defaultdict(set)
    per = defaultdict(list)
    with open(rd(target, find(target, "price_submissions")), encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            if r["grade"] != "RUL":
                continue
            sid = r["station_number"]
            t = to_local(r["effective_utc"])
            key = (brand_on(hist, sid, t.date()), t.hour * 60 + t.minute)
            if r["channel"] == "API":
                pushers[key].add(sid)
            per[sid].append(key)
    push = {k for k, v in pushers.items() if len(v) >= 3}
    out = {b: 0 for b in codes}
    for sid, keys in per.items():
        b = brand_on(hist, sid, SCOPE)
        closed = st[sid]["closed"]
        if b not in codes or (closed is not None and closed <= SCOPE):
            continue
        if sum(1 for k in keys if k in push) / len(keys) >= 0.5:
            out[b] += 1
    return out


def tens(f, n):
    return int(math.floor(f / n * 10 + 0.5)) * 10


def thousands(x):
    return int(math.floor(x / 1000.0 + 0.5))


# ------------------------------------------------------------------------------------------------- the goldens
def docx_text(path):
    import zipfile
    with zipfile.ZipFile(path) as z:
        xml = z.read("word/document.xml").decode("utf-8")
    paras = []
    for p in re.findall(r"<w:p[ >].*?</w:p>", xml, flags=re.S):
        paras.append("".join(re.findall(r"<w:t(?: [^>]*)?>([^<]*)</w:t>", p)))
    return paras


def main(target=None, golden=None):
    target = target or os.path.join(TASK, "target")
    golden = golden or os.path.join(TASK, "golden")
    mc = main_call(target)
    codes, names, st, hist = mc["codes"], mc["names"], mc["register"], mc["history"]
    lit, resolved = litres(target, st, hist, codes)
    pr = priced_by_brand(target, st, hist, codes)
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    bad = []

    def same(a, b, what):
        if a != b:
            bad.append("%s: verifier %r, figures.json %r" % (what, a, b))
    same(names[mc["call"]] if mc["call"] else "none", fig["call"], "call")
    same(len(mc["ex"]), fig["stations_examined"], "stations examined")
    same(int(mc["found"].sum()), fig["stations_found"], "stations found")
    for b in codes:
        nm = names[b]
        f, n = mc["share"][b]
        same(n, fig["stations_examined_by_brand"][nm], "examined " + nm)
        same(f, fig["stations_found_by_brand"][nm], "found " + nm)
        same("%d" % tens(f, n), fig["share_found_nearest_ten_per_cent"][nm], "share " + nm)
        same(pr[b], fig["priced_by_brand_2026_12_01"][nm], "priced by the brand " + nm)
        for i, m in enumerate(("January 2026", "February 2026", "March 2026")):
            same(thousands(lit[b][i]), fig["regular_litres_thousands"][nm][m], "litres %s %s" % (nm, m))
    same(resolved, 3 * fig["survey_references_reissued"], "returns filed under references reissued later")
    # the memo
    paras = docx_text(os.path.join(golden, "pass_through_inquiry_2027.docx"))
    text = " ".join(paras)
    if names[mc["call"]] not in paras[0] + text[:2000]:
        bad.append("memo does not name the call early")
    for b in codes:
        nm = names[b]
        row = [nm, "%d" % mc["share"][b][1], "%d per cent" % tens(*mc["share"][b])]
        if not any(paras[i:i + 3] == row for i in range(len(paras) - 2)):
            bad.append("memo table row for " + nm)
    import zipfile
    with zipfile.ZipFile(os.path.join(golden, "pass_through_inquiry_2027.docx")) as z:
        if not any(n.startswith("word/media/") for n in z.namelist()):
            bad.append("memo has no chart")
    # the workbook
    wb = openpyxl.load_workbook(os.path.join(golden, "inquiry_scope_2027.xlsx"), read_only=True)
    rows = list(wb["Inquiry scope"].iter_rows(min_row=5, values_only=True))
    got = {r[1]: r for r in rows if r and r[1] in codes}
    for b in codes:
        r = got.get(b)
        if r is None or r[2] != pr[b] or list(r[3:6]) != [thousands(x) for x in lit[b]]:
            bad.append("workbook row " + b)
    if bad:
        raise SystemExit("verify FAILED:\n  " + "\n  ".join(bad))
    sh = ", ".join("%s %d/%d" % (b, mc["share"][b][0], mc["share"][b][1]) for b in codes)
    print("verify: call %s; examined %d, found %d (%s); litres and priced-by-brand for %d brands agree; %d returns "
          "resolved through reissued references; figures.json and both goldens agree" % (
              names[mc["call"]] if mc["call"] else "none", len(mc["ex"]), int(mc["found"].sum()), sh, len(codes),
              resolved))
    return mc, lit, pr


if __name__ == "__main__":
    main(*(sys.argv[1:3] if len(sys.argv) > 2 else []))
