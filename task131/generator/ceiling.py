"""task131 ask layer against the careful solver's routes, on the cut pack.

    python3 task131/generator/ceiling.py [pack]

pack is target.zip (the default, the archive that ships) or a folder holding the pack's files. The three asks of the
design note's ask sheet give 18 figures in tariff_trial_tables_2025-26.xlsx, per design: where its trial households
stood on 28 February 2026 (still billed on it, back on the Home Plan at their own request, no longer our customers),
how many were charged more over the trial than the Home Plan would have charged for the same metered use and the mean
of that difference per trial household, and the share of March 2026 survey respondents likely or very likely to stay
on it. Every route is a complete pipeline over the cut pack (the register, the account history, the four NEM12
extracts, Schedule 1, the survey extract and its instruments), scored figure by figure against figures.json: a count
is kept only when exact, a mean within half a cent, a share within half a tenth of a point.

The cracker lands the call (the golden's main-call path from the pack), runs the hygiene battery and applies every
filed rule, reading every field by its plain meaning: each household followed through every account its customer
number holds (the start and end reasons say an account closed on a move and another opened under the same customer
number), the reason it left its design read from the row that took it off; NEM12 days read through their quality
codes (an interval marked N carries no read, so an exchange day is the old meter's reads and the new meter's, and a
re-sent day replaces the earlier delivery by its update time), 15-minute reads paired into half-hours; each register
priced at the tariff the account history holds it on (the controlled-load and export registers stay on RC2 and BB1
whatever the design), Schedule 1's GST-inclusive charges with its supply charges, windows and public holidays; the
survey's instruments executed as written (a response counts once submitted, a household's first submitted response,
each mode's codes in the order its instrument lists them). The mirror stops at the default path (each design's cut
inside its window on the average trial workday, rung 0: Design B at 15 MW) and, as the ask sheet sets it, runs the
same ask paths as the cracker; the mirror on the natural read without the battery is printed beside it. The full
includer is the golden's own handling and has to give back figures.json exactly: the route code's control. The stops
are the cracker with one handling changed, each scored as a route.

The pair is the ask sheet's formula: 38 recommendation and components, 7 instruction following, 55 asks over the 18
figures, a response off the call keeping 5 of the 38. The script reads the pack and figures.json and writes nothing."""
from __future__ import annotations

import csv
import hashlib
import json
import os
import re
import shutil
import sys
import tempfile
import zipfile
from collections import defaultdict
from datetime import date, timedelta

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import verify as V      # noqa: E402  (the bundle-only readers: workbook rows, the per-serial NEM12 read)
import analysis as AN   # noqa: E402  (the golden's main-call path, for the cracker's call and the default path)

TASK = os.path.dirname(HERE)
REGISTER = "summer_pricing_trial_register.xlsx"
HISTORY = "account_tariff_history_2026-03-12.csv"
SURVEY = "trial_survey_responses_2026-03.csv"
SCHEDULE = "residential_charges_2025-26.pdf"
INSTRUMENTS = "trial_survey_instruments_2026-03.pdf"
REC, INS, ASK, OFF = 38.0, 7.0, 55.0, 5.0       # the ask sheet's weights; a response off the call keeps OFF of REC
DESIGNS = ("A", "B", "C")
ON = date(2026, 2, 28)
T0, T1 = date(2025, 12, 1), date(2026, 2, 28)
OWN = ("CUSTOMER REQUEST", "SELF SERVICE")
KEYS = (("still", "still billed on it"), ("back", "back on the Home Plan at own request"), ("gone", "no longer our customers"),
        ("more", "charged more than the Home Plan"), ("mean", "mean difference per trial household"),
        ("share", "share likely or very likely to stay"))

# a route: Ask A key (customer, account, nmi) and reason (exit, live, any); Ask B NEM12 read (quality, serial, per_day,
# all), registers (tariff, import), the household's days (customer, account), supply charges; Ask C codes (mode, web),
# first submitted response only, submitted responses only
CRACKER = dict(key="customer", reason="exit", nem="quality", regs="tariff", bkey="customer", supply=True,
               coding="mode", first=True, submitted=True)
FULL = dict(CRACKER, reason="any", nem="serial")
NATURAL = dict(key="account", reason="live", nem="per_day", regs="import", bkey="account", supply=True,
               coding="web", first=False, submitted=True)
STOPS = [
    ("joins the history on the register's account (Asks A and B)", dict(key="account", bkey="account")),
    ("joins the history on the register's NMI (Ask A)", dict(key="nmi")),
    ("reads 'at their own request' off the live row's own start reason (Ask A)", dict(reason="live")),
    ("prices every import register at the design (Ask B)", dict(regs="import")),
    ("dedups NEM12 on NMI, register and day, the later record kept (Ask B)", dict(nem="per_day")),
    ("sums every NEM12 record, re-sends included (Ask B)", dict(nem="all")),
    ("leaves the supply charges out (Ask B)", dict(supply=False)),
    ("reads every stay code in the online form's order (Ask C)", dict(coding="web")),
    ("keeps every submitted response (Ask C)", dict(first=False)),
    ("counts every response started (Ask C)", dict(submitted=False)),
]


# ------------------------------------------------------------------------------------------------ the pack
def pack_dir(arg):
    """The pack as a folder: target.zip unpacked into a scratch folder (removed after), or the folder given."""
    src = arg or os.path.join(TASK, "target.zip")
    if os.path.isdir(src):
        files = sorted(os.listdir(src))
        h = hashlib.sha256("".join(hashlib.sha256(open(os.path.join(src, f), "rb").read()).hexdigest()
                                   for f in files).encode()).hexdigest()
        return src, None, "folder %s (%d files, sha256 of the file digests %s)" % (src, len(files), h[:16])
    tmp = tempfile.mkdtemp(prefix="ceiling131-")
    with zipfile.ZipFile(src) as z:
        z.extractall(tmp)
    md5 = hashlib.md5(open(src, "rb").read()).hexdigest()
    return tmp, tmp, "%s (%d files, md5 %s)" % (src, len(os.listdir(tmp)), md5)


def pdf_text(path):
    from pypdf import PdfReader
    return re.sub(r"\s+", " ", " ".join(pg.extract_text() for pg in PdfReader(path).pages))


def schedule(folder):
    """Schedule 1 as the careful solver reads it: the GST-inclusive charges, the windows of section 2 in half-hour
    indices from midnight, the public holidays"""
    t = pdf_text(os.path.join(folder, SCHEDULE))

    def num(pat):
        m = re.search(pat, t)
        if not m:
            raise SystemExit("Schedule 1 could not be read: %s" % pat)
        return [float(x) for x in m.groups()]
    flat, fsup = num(r"Home Plan RH1 ([0-9.]+) ([0-9.]+)")
    a = num(r"Trial Design A TRA peak ([0-9.]+); off-peak ([0-9.]+) ([0-9.]+)")
    b = num(r"Trial Design B TRB peak ([0-9.]+); off-peak ([0-9.]+) ([0-9.]+)")
    c = num(r"Trial Design C TRC peak ([0-9.]+); shoulder ([0-9.]+); off-peak ([0-9.]+) ([0-9.]+)")

    def hh(x):
        return 2 * (int(x) + 12)
    wa = re.search(r"Trial Design A peak time is (\d+) pm to (\d+) pm", t)
    wbc = re.search(r"Trial Design B and Trial Design C peak time is (\d+) pm to (\d+) pm", t)
    wsh = re.search(r"Trial Design C shoulder time is (\d+) pm to (\d+) pm and (\d+) pm to (\d+) pm", t)
    if not (wa and wbc and wsh and "weekdays other than public holidays" in t and "include GST" in t):
        raise SystemExit("Schedule 1's times could not be read")
    months = {"December": 12, "January": 1, "February": 2}
    hol = {date(int(y), months[m], int(d)) for d, m, y in
           re.findall(r"(?:Monday|Tuesday|Wednesday|Thursday|Friday) (\d+) (December|January|February) (\d{4})", t)}
    win = {"A": {"peak": (hh(wa.group(1)), hh(wa.group(2)))},
           "B": {"peak": (hh(wbc.group(1)), hh(wbc.group(2)))},
           "C": {"peak": (hh(wbc.group(1)), hh(wbc.group(2))),
                 "shoulder": [(hh(wsh.group(1)), hh(wsh.group(2))), (hh(wsh.group(3)), hh(wsh.group(4)))]}}
    rates = {"A": {"peak": a[0], "off": a[1]}, "B": {"peak": b[0], "off": b[1]},
             "C": {"peak": c[0], "shoulder": c[1], "off": c[2]}}
    supply = {"A": a[2], "B": b[2], "C": c[3]}
    codes = dict(re.findall(r"Trial Design ([ABC]) (TR[ABC]) ", t))
    return {"flat": flat, "home_supply": fsup, "rates": rates, "supply": supply, "win": win, "hol": hol, "code": codes,
            "home": "RH1"}


def load(folder):
    rows = V.xlsx_rows(os.path.join(folder, REGISTER), "Register")
    head = [rows[0][V.col(i)] for i in range(len(rows[0]))]
    reg = [{head[i]: r.get(V.col(i)) for i in range(len(head))} for r in rows[1:]]
    with open(os.path.join(folder, HISTORY), newline="") as fh:
        hist = list(csv.DictReader(fh))
    for h in hist:
        h["f"] = date.fromisoformat(h["valid_from"])
        h["t"] = date.fromisoformat(h["valid_to"]) if h["valid_to"] else None
        h["cancelled"] = h["t"] is not None and h["t"] < h["f"]
    idx = {k: defaultdict(list) for k in ("customer", "account", "nmi")}
    for h in hist:
        idx["customer"][h["customer_id"]].append(h)
        idx["account"][h["account_id"]].append(h)
        idx["nmi"][h["nmi"]].append(h)
    with open(os.path.join(folder, SURVEY), newline="") as fh:
        survey = list(csv.DictReader(fh))
    instruments = pdf_text(os.path.join(folder, INSTRUMENTS))
    return {"reg": reg, "hist": hist, "idx": idx, "survey": survey, "sched": schedule(folder), "instr": instruments,
            "folder": folder}


# ------------------------------------------------------------------------------------------------ NEM12
def nem_records(folder):
    """every 300 record as the files carry it: (nmi, suffix, serial, day, 48 half-hourly kWh with 15-minute reads
    paired, 48 null flags from the quality method and its 400 records, update date-time, order in the files)"""
    out = []
    order = 0
    for fn in sorted(f for f in os.listdir(folder) if f.startswith("MRP_NEM12_")):
        cur = last = None
        with open(os.path.join(folder, fn)) as fh:
            for line in fh:
                p = line.rstrip("\r\n").split(",")
                if p[0] == "200":
                    cur = (p[1], p[4], p[6], int(p[8]))
                    if p[7] != "KWH":
                        raise SystemExit("a 200 record is not in kWh: %s" % line)
                elif p[0] == "300":
                    nmi, suf, ser, il = cur
                    n = 1440 // il
                    v = np.array(p[2:2 + n], dtype=float)
                    q = p[2 + n]
                    null = np.zeros(n, dtype=bool) if q != "N" else np.ones(n, dtype=bool)
                    d = date(int(p[1][:4]), int(p[1][4:6]), int(p[1][6:8]))
                    last = {"nmi": nmi, "suf": suf, "ser": ser, "day": d, "n": n, "v": v, "null": null,
                            "upd": p[2 + n + 3], "order": order}
                    out.append(last)
                    order += 1
                elif p[0] == "400":
                    lo, hi, q = int(p[1]), int(p[2]), p[3]
                    last["null"][lo - 1:hi] = q == "N"
    for r in out:
        if r["n"] == 96:
            r["v"] = r["v"][0::2] + r["v"][1::2]
            r["null"] = r["null"][0::2] & r["null"][1::2]
    return out


def nem_reads(recs, how):
    """(nmi, suffix) -> {day: 48 kWh} under one handling of the files' repeated days"""
    by = defaultdict(list)
    for r in recs:
        by[(r["nmi"], r["suf"], r["day"])].append(r)
    out = defaultdict(dict)
    for (nmi, suf, d), rs in by.items():
        if how == "quality":            # per interval, the latest delivery that carries a read there
            if len(rs) == 1:
                out[(nmi, suf)][d] = np.where(rs[0]["null"], 0.0, rs[0]["v"])
                continue
            stamp = np.array([[-1 if r["null"][k] else int(r["upd"]) for k in range(48)] for r in rs])
            vals = np.array([r["v"] for r in rs])
            pick = np.argmax(stamp, axis=0)
            v = vals[pick, np.arange(48)]
            out[(nmi, suf)][d] = np.where(stamp.max(axis=0) < 0, 0.0, v)
        elif how == "serial":           # the latest delivery per meter serial, the serials summed (the golden's read)
            per = {}
            for r in rs:
                if r["ser"] not in per or r["upd"] > per[r["ser"]]["upd"]:
                    per[r["ser"]] = r
            out[(nmi, suf)][d] = np.sum([r["v"] for r in per.values()], axis=0)
        elif how == "per_day":          # one record per NMI, register and day: the latest, the later in the files on a tie
            r = max(rs, key=lambda x: (x["upd"], x["order"]))
            out[(nmi, suf)][d] = r["v"]
        elif how == "all":
            out[(nmi, suf)][d] = np.sum([r["v"] for r in rs], axis=0)
        else:
            raise ValueError(how)
    return out


# ------------------------------------------------------------------------------------------------ the asks
def household_rows(L, r, key):
    """the account history rows a route reads for one register household: every account its customer number holds,
    the register's account, or the register's NMI"""
    col = {"customer": "customer_id", "account": "account_id", "nmi": "nmi"}[key]
    return L["idx"][key].get(r[col], [])


def live(rows, d):
    return [h for h in rows if not h["cancelled"] and h["f"] <= d and (h["t"] is None or h["t"] >= d)]


def ask_a(L, route):
    S = L["sched"]
    out = {}
    for a in DESIGNS:
        still = back = gone = 0
        for r in L["reg"]:
            if r["arm"] != "DESIGN " + a:
                continue
            rows = [h for h in household_rows(L, r, route["key"]) if h["register"] == "E1"]
            now = live(rows, ON)
            if not now:
                gone += 1
                continue
            h = now[0]
            if h["tariff_code"] == S["code"][a]:
                still += 1
                continue
            if h["tariff_code"] != S["home"]:
                continue
            if route["reason"] == "live":
                own = h["start_reason"] in OWN
            elif route["reason"] == "exit":     # the row that took the household off its design
                after = sorted((x for x in rows if not x["cancelled"] and x["tariff_code"] == S["home"] and x["f"] > T0),
                               key=lambda x: (x["f"], x["keyed_on"]))
                own = bool(after) and after[0]["start_reason"] in OWN
            else:                               # any Home Plan row the household asked for
                own = any(x["start_reason"] in OWN for x in rows if not x["cancelled"] and x["tariff_code"] == S["home"])
            back += own
        out[a] = {"still": still, "back": back, "gone": gone}
    return out


def charges(S, a, kwh, d):
    """cents for one day's 48 half-hourly kWh on design a, and on the Home Plan"""
    home = float(np.sum(kwh)) * S["flat"]
    rate = np.full(48, S["rates"][a]["off"])
    if d.weekday() < 5 and d not in S["hol"]:
        lo, hi = S["win"][a]["peak"]
        rate[lo:hi] = S["rates"][a]["peak"]
        for x, y in S["win"][a].get("shoulder", []):
            rate[x:y] = S["rates"][a]["shoulder"]
    return float(np.sum(kwh * rate)), home


def ask_b(L, route, reads):
    S = L["sched"]
    out = {}
    for a in DESIGNS:
        diffs = []
        for r in L["reg"]:
            if r["arm"] != "DESIGN " + a:
                continue
            rows = [h for h in household_rows(L, r, route["bkey"]) if h["register"] == "E1"
                    and h["tariff_code"] == S["code"][a] and not h["cancelled"]]
            tot = 0.0
            for h in rows:
                d, end = max(h["f"], T0), min(h["t"] or T1, T1)
                while d <= end:
                    kwh = reads[(h["nmi"], "E1")][d]
                    if route["regs"] == "import" and d in reads.get((h["nmi"], "E2"), {}):
                        kwh = kwh + reads[(h["nmi"], "E2")][d]
                    des, home = charges(S, a, kwh, d)
                    tot += des - home + ((S["supply"][a] - S["home_supply"]) if route["supply"] else 0.0)
                    d += timedelta(1)
            diffs.append(tot / 100.0)
        diffs = np.array(diffs)
        out[a] = {"more": int(np.sum(diffs > 0)), "mean": float(np.mean(diffs))}
    return out


def ask_c(L, route):
    rows = L["survey"]
    if route["submitted"]:
        rows = [r for r in rows if r["complete"] == "Y"]
    if route["first"]:
        first = {}
        for r in sorted(rows, key=lambda r: (r["submitted_at"] or "9999", r["started_at"], r["response_id"])):
            first.setdefault(r["trial_id"], r)
        rows = list(first.values())
    arm = {r["trial_id"]: r["arm"] for r in L["reg"]}
    out = {}
    for a in DESIGNS:
        ans = [r for r in rows if arm.get(r["trial_id"]) == "DESIGN " + a and r["q4_stay"] != ""]
        if route["coding"] == "mode":
            like = [r for r in ans if (int(r["q4_stay"]) <= 2 if r["mode"] == "WEB" else int(r["q4_stay"]) >= 4)]
        else:
            like = [r for r in ans if int(r["q4_stay"]) <= 2]
        out[a] = {"share": 100.0 * len(like) / len(ans)}
    return out


def route_figures(L, route, cache):
    if route["nem"] not in cache:
        cache[route["nem"]] = nem_reads(cache["recs"], route["nem"])
    A_, B_, C_ = ask_a(L, route), ask_b(L, route, cache[route["nem"]]), ask_c(L, route)
    return {a: dict(A_[a], **B_[a], **C_[a]) for a in DESIGNS}


def golden():
    f = json.load(open(os.path.join(HERE, "figures.json")))
    return {a: {"still": f["retention"][a]["still"], "back": f["retention"][a]["back"], "gone": f["retention"][a]["gone"],
                "more": f["bills"][a]["more"], "mean": f["bills"][a]["mean"], "share": f["survey"][a]["share"]}
            for a in DESIGNS}, f


def kept(fig, gold):
    tol = {"still": 0, "back": 0, "gone": 0, "more": 0, "mean": 0.005, "share": 0.05}
    return {(a, k): abs(fig[a][k] - gold[a][k]) <= tol[k] + 1e-9 for a in DESIGNS for k, _ in KEYS}


def pair(kc, km, n):
    c, s = REC + INS + ASK * kc / n, OFF + INS + ASK * km / n
    return c, s, (c + s) / 2.0


# ------------------------------------------------------------------------------------------------ the battery
def battery(L, recs):
    """what the hygiene battery a careful analyst runs on the ask files finds, each line (check, finding)"""
    out = []
    keys = defaultdict(list)
    for r in recs:
        keys[(r["nmi"], r["suf"], r["day"])].append(r)
    resent = sum(1 for rs in keys.values() if len({x["upd"] for x in rs}) > 1)
    split = sum(1 for rs in keys.values() if len({x["ser"] for x in rs}) > 1)
    out.append(("NEM12 meter-days delivered more than once with a later update time (re-sends)", resent))
    out.append(("NEM12 meter-days read by two meter serials, each marked N where the other reads", split))
    out.append(("NEM12 meters at 15 minutes (96 reads a day)", len({r["nmi"] for r in recs if r["n"] == 96})))
    hist = L["hist"]
    tup = [tuple(h[c] for c in ("customer_id", "account_id", "nmi", "register", "tariff_code", "valid_from", "valid_to",
                                 "start_reason", "end_reason", "keyed_on")) for h in hist]
    out.append(("account history exact duplicate rows", len(tup) - len(set(tup))))
    out.append(("account history rows ending before they start (end reason CANCELLED)", sum(h["cancelled"] for h in hist)))
    acc = defaultdict(set)
    for h in hist:
        acc[h["customer_id"]].add(h["account_id"])
    regc = {r["customer_id"] for r in L["reg"]}
    out.append(("register customers holding a second account (start reason %s on the new one)" %
                ", ".join(sorted({h["start_reason"] for h in hist if h["customer_id"] in regc and len(acc[h["customer_id"]]) > 1
                                  and h["account_id"] not in {r["account_id"] for r in L["reg"]}})),
                sum(1 for c in regc if len(acc[c]) > 1)))
    out.append(("account history end reasons other than a tariff change or the trial's end",
                ", ".join(sorted({h["end_reason"] for h in hist if h["end_reason"] not in ("", "TARIFF CHANGE", "TRIAL END")}))))
    sv = L["survey"]
    sub = [r for r in sv if r["complete"] == "Y"]
    out.append(("survey responses started and never submitted", len(sv) - len(sub)))
    per = defaultdict(int)
    for r in sub:
        per[r["trial_id"]] += 1
    out.append(("households with more than one submitted response", sum(1 for v in per.values() if v > 1)))
    web = "Very likely (1), Likely (2), Unsure (3), Unlikely (4), Very unlikely (5)" in L["instr"]
    cati = "would you be very unlikely, unlikely, unsure, likely or very likely to stay on it? 1 to 5 in the order read" in L["instr"]
    out.append(("the instruments list Q4's codes per mode (online very likely first, telephone very unlikely first)",
                "yes" if web and cati else "NO"))
    return out


# ------------------------------------------------------------------------------------------------ main
def main(arg=None):
    folder, scratch, stamp = pack_dir(arg)
    try:
        return run(folder, stamp)
    finally:
        if scratch:
            shutil.rmtree(scratch)


def run(folder, stamp):
    print("pack: " + stamp)
    gold, figs = golden()
    n = len(DESIGNS) * len(KEYS)

    # the calls
    R = AN.run(folder)
    call = R["call"]
    ch = {a: int(round(R[a]["change"])) for a in DESIGNS}
    on_call = call == figs["call"] and ch == figs["change_mw"]
    r0 = {a: R[a]["R0"] for a in DESIGNS}
    w0 = max(r0, key=r0.get)
    off_call = w0 != figs["call"] and int(round(r0[w0])) == figs["default_B_mw"]
    print("cracker's call: Design %s, changes A %+d, B %+d, C %+d MW lowered (%s the golden)" % (
        call, ch["A"], ch["B"], ch["C"], "lands" if on_call else "MISSES"))
    print("mirror's call (the default path, each window's cut on the average trial workday): Design %s lowering the "
          "maximum by %.1f MW (%s)" % (w0, r0[w0], "off the call" if off_call else "ON THE CALL"))
    if not (on_call and off_call):
        print("the rows below assume the cracker on the call and the mirror off it: they are not")
        return 1

    L = load(folder)
    recs = nem_records(folder)
    cache = {"recs": recs}
    print("\nthe cracker's hygiene battery on the ask files:")
    for check, finding in battery(L, recs):
        print("  %-104s %s" % (check, finding))

    full = route_figures(L, FULL, cache)
    kf = kept(full, gold)
    if not all(kf.values()):
        print("CONTROL FAILED: the full includer gives %d of %d, the route code does not reproduce figures.json: %s" % (
            sum(kf.values()), n, ", ".join("%s %s" % k for k, v in kf.items() if not v)))
        return 1
    crk = route_figures(L, CRACKER, cache)
    nat = route_figures(L, NATURAL, cache)
    kc, kn = kept(crk, gold), kept(nat, gold)

    def fmt(x, k):
        return "%.2f" % x if k == "mean" else ("%.1f" % x if k == "share" else "%d" % x)
    print("\nper figure (figures.json; cracker; mirror on the natural read without the battery):")
    for a in DESIGNS:
        for k, name in KEYS:
            print("  Design %s %-40s %8s  %8s %-4s  %8s %s" % (a, name, fmt(gold[a][k], k), fmt(crk[a][k], k),
                                                          "kept" if kc[(a, k)] else "miss", fmt(nat[a][k], k),
                                                          "kept" if kn[(a, k)] else "miss"))
    by_ask = {"A": ("still", "back", "gone"), "B": ("more", "mean"), "C": ("share",)}
    print("\nper ask, figures kept:")
    print("  %-46s %-9s %-24s %s" % ("", "cracker", "mirror (natural read)", "full includer (control)"))
    for ask, ks in by_ask.items():
        m = len(ks) * len(DESIGNS)
        print("  %-46s %-9s %-24s %s" % ("Ask %s (%d figures)" % (ask, m),
                                         sum(kc[(a, k)] for a in DESIGNS for k in ks),
                                         sum(kn[(a, k)] for a in DESIGNS for k in ks),
                                         sum(kf[(a, k)] for a in DESIGNS for k in ks)))
    nc, nn = sum(kc.values()), sum(kn.values())
    print("  %-46s %-9d %-24d %d of %d" % ("all asks", nc, nn, sum(kf.values()), n))

    print("\nthe stops, the cracker with one handling changed (figures kept of %d):" % n)
    for name, chg in STOPS:
        k = kept(route_figures(L, dict(CRACKER, **chg), cache), gold)
        print("  %-84s %2d  (misses %s)" % (name, sum(k.values()),
                                           ", ".join("%s %s" % x for x, v in k.items() if not v) or "none"))

    # the pair: the mirror runs the cracker's ask paths (the ask sheet's mirror), and on the natural read beside it
    c, s, p = pair(nc, nc, n)
    print("\nthe sheet's formula (38, 7, 55 over the %d figures; r = 5):" % n)
    print("  cracker keeps %d, the mirror on the cracker's ask paths keeps %d: cracker %.1f, mirror %.1f, pair %.1f" % (
        nc, nc, c, s, p))
    c2, s2, p2 = pair(nc, nn, n)
    print("  the mirror on the natural read without the battery keeps %d: cracker %.1f, mirror %.1f, pair %.1f" % (
        nn, c2, s2, p2))
    print("\nCracker keeps: %d of %d ask figures" % (nc, n))
    print("Mirror leakage: %.1f per cent of ask weight (the cracker's ask paths; %.1f on the natural read without the "
          "battery)" % (100.0 * nc / n, 100.0 * nn / n))
    print("Pair ceiling: %.1f (the sheet's formula on the measured keeps; %.1f with the mirror on the natural read)" % (
        p, p2))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else None))
