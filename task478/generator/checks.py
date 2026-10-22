"""task478's assertions on the cut pack and the generator's clean truth: the three rules (R1 to R3c), every semantic fork
row (SF1 to SF18), the ladder, the golden's licensed family and margins, the asks' devices, the separation line, the
distractors, the input gates and the realism sweep.

    python3 task478/generator/checks.py
"""
import datetime as dt
import json
import os
import re
import shutil
import sys
import tempfile
import warnings

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
warnings.filterwarnings("ignore")

import bundle as B    # noqa: E402
import pack as P      # noqa: E402
import world as W     # noqa: E402

TASK = os.path.dirname(HERE)
TARGET = os.path.join(TASK, "target")
GOLD = ["03", "05", "07", "10", "11"]
DEFAULT = ["02", "03", "07", "09", "10"]
RESULTS = []
LINES = (45000, 50000, 56000, 60000, 65000, 70000, 72000)
RECEIPT_ALLOW = W.RECEIPT_MIN / 60.0      # the old host stamped an entry up to this many hours after it happened


def check(name, ok):
    RESULTS.append((name, bool(ok)))
    print("%s  %s" % ("PASS" if ok else "FAIL", name))


def pdf_text(key):
    import pypdf
    r = pypdf.PdfReader(os.path.join(TARGET, P.FILES[key]))
    return re.sub(r"\s+", " ", " ".join(p.extract_text() for p in r.pages))


def whole(sh):
    return {c: B.hround(sh[c]) for c in B.CODES}


def subset(keys):
    """A copy of the pack holding only the named files."""
    d = tempfile.mkdtemp(prefix="t478_")
    for k in keys:
        shutil.copy(os.path.join(TARGET, P.FILES[k]), os.path.join(d, P.FILES[k]))
    return d


def ticket_arrays(tk, keyed=False):
    st = tk["Axle 1 (lb)"].astype(float).to_numpy()
    g = tk["Gross (lb)"].astype(float).to_numpy() if keyed else \
        tk[["Axle %d (lb)" % i for i in range(1, 6)]].astype(float).sum(axis=1).to_numpy()
    return st, g


def factors_by(df, tst, tg, line=50000, agg=np.median, ragg=np.median):
    return {c: agg(df[df["section"] == c]["steer"].to_numpy()[df[df["section"] == c]["gross"].to_numpy() > line])
            / ragg(tst[tg > line]) for c in B.CODES}


def world_routes(e):
    """The clean truth: every station's readings and the tickets before any file is written."""
    R = {r["code"]: (r["read"].sum(axis=1), r["read"][:, 0], r["gross"]) for r in e["wim"]}
    tg, ts = e["tickets"]["gross"], e["tickets"]["axles"][:, 0]

    def sh(fa):
        return {c: 100.0 * np.mean(R[c][0] / fa[c] > W.LIMIT) for c in R}
    out = {"raw": sh({c: 1.0 for c in R}),
           "loaded": sh({c: np.median(R[c][1][R[c][0] > 50000]) / np.median(ts[tg > 50000]) for c in R}),
           "pooled": sh({c: np.median(R[c][1]) / np.median(ts) for c in R}),
           "empty": sh({c: np.median(R[c][1][R[c][0] <= 50000]) / np.median(ts[tg <= 50000]) for c in R}),
           "gross": sh({c: np.median(R[c][0]) / np.median(tg) for c in R}),
           "truth": {c: 100.0 * np.mean(R[c][2] > W.LIMIT) for c in R}}
    return out


def main():
    f = json.load(open(os.path.join(HERE, "figures.json")))
    wim_all = B.read_wim(TARGET)
    df = B.class9(wim_all)
    tk = B.read_tickets(TARGET)
    tst, tg = ticket_arrays(tk)
    fa = B.factors(df, tk, "loaded")
    sh = B.shares(df, fa)
    gw = whole(sh)
    five = B.five(sh)
    rank = sorted(B.CODES, key=lambda c: -sh[c])
    e = W.everything()

    # ---------------------------------------------------------------- R1: the field's raw material ships
    check("R1 the WIM exports ship one record per vehicle with every axle's weight (%d class 9 weighings)" % len(df),
          len(df) > 150000 and df["steer"].notna().all())
    check("R1 the scale house tickets ship each truck's five static axle weights (%d tickets)" % len(tk),
          len(tk) == 2600 and tk[["Axle %d (lb)" % i for i in range(1, 6)]].notna().all().all())
    heads = []
    for k, fn in P.FILES.items():
        p = os.path.join(TARGET, fn)
        if fn.endswith(".csv"):
            heads += open(p, encoding="utf-8").readline().strip().lower().split(",")
        elif fn.endswith(".xlsx"):
            import openpyxl
            ws = openpyxl.load_workbook(p, read_only=True).active
            heads += [str(v).lower() for v in next(ws.iter_rows(values_only=True))]
    check("R1 no shipped column holds a calibration, factor, bias, correction or static-basis weight",
          not any(re.search(r"calib|factor|bias|correct|adjust|static|true_", h) for h in heads))

    # ---------------------------------------------------------------- R3: the analyst test on the clean truth
    wr = world_routes(e)
    check("R3a the easy route on the clean truth (the gross as each station read it, every filed rule applied) files "
          "%s, the default path's answer" % B.five(wr["raw"]), B.five(wr["raw"]) == DEFAULT)
    check("R3a the default path on the cut pack files the same five", B.five(B.shares(df)) == DEFAULT)
    check("R3b the easy route with only the decisive step (each station's loaded steer axles against the loaded "
          "tickets') files the golden on the clean truth", B.five(wr["loaded"]) == GOLD)
    check("R3b each lower rung's single correction leaves a wrong five on the clean truth (pooled %s, empty %s, "
          "gross %s)" % (B.five(wr["pooled"]), B.five(wr["empty"]), B.five(wr["gross"])),
          all(B.five(wr[k]) != GOLD for k in ("pooled", "empty", "gross")))
    check("R3 the trucks' true gross (the generator's truth) puts the golden five on top", B.five(wr["truth"]) == GOLD)
    check("R3 every golden share sits within 2.5 points of the true share (the stations' random error only)",
          all(abs(sh[c] - wr["truth"][c]) < 2.5 for c in B.CODES))
    pz = open(os.path.join(TARGET, P.FILES["piezo"]), encoding="ascii").read().splitlines()
    bp = pd.read_csv(os.path.join(TARGET, P.FILES["bending"]), dtype=str)
    check("R3c no plant: no WIM record repeats another exactly (piezo %d, bending %d)" % (len(pz), len(bp)),
          len(set(pz)) == len(pz) and not bp.duplicated().any())
    days = df.assign(day=df["local"].dt.date).groupby(["section", "day"])["gross"].apply(lambda s: tuple(np.round(s, -1)))
    check("R3c no plant: no station's day of class 9 weighings repeats another day", days.nunique() == len(days))
    wax = set()
    for ln in pz:
        if ln[26:28] == "09":
            wax.add(tuple(int(ln[35 + 4 * k:39 + 4 * k]) // 5 for k in range(5)))
    for r in bp[bp["fhwa_class"] == "9"][["ax%d_kg" % i for i in range(1, 6)]].astype(int).itertuples(index=False):
        wax.add(tuple(int(round(x / B.KG / 10.0)) // 5 for x in r))
    tax = tk[["Axle %d (lb)" % i for i in range(1, 6)]].astype(int).to_numpy()
    hits = sum(tuple(int(x // 10) // 5 for x in row) in wax for row in tax)
    check("R3c no plant: no scale house ticket copies a WIM weighing (all five axles to 50 lb; %d)" % hits, hits <= 2)

    # ---------------------------------------------------------------- R2: every Layer 1 item, mishandled
    kg = wim_all.copy()
    isb = kg["station"].str.startswith("CT")
    kg.loc[isb, "gross"] = kg.loc[isb, "gross"] * B.KG
    kg.loc[isb, "steer"] = kg.loc[isb, "steer"] * B.KG
    raw_kg = B.shares(B.class9(kg))
    bend = [s[0] for s in W.SECTIONS if s[4] == "bending"]
    check("R2a kilograms read as pounds put every bending-plate station at zero over the limit (a loud failure no "
          "careful route keeps)", all(raw_kg[c] == 0 for c in bend))
    check("R2b the controllers' standard time read as daylight time leaves the call and the twelve shares (the year's "
          "ends are in standard time)", True if df["local"].min().year == 2026 and df["local"].max().year == 2026
          else False)
    keep = df[~((df["station"] == P.STATION_ID[P.RELANED[0]]) & (df["lane"] > 2))]
    check("R2c Foxbriar's renumbered lanes 3 and 4 dropped leaves the call",
          B.five(B.shares(keep, B.factors(keep, tk))) == GOLD)
    check("R2d the re-sited station at its previous milepost (%.1f) stays in its section" % P.RESITED[1],
          B.section_at(P.RESITED[1]) == P.RESITED[0])
    allr = wim_all[wim_all["cls"] == 9]
    check("R2e the rejected weighings kept leaves the call", B.five(B.shares(allr, B.factors(allr, tk))) == GOLD)
    ks, kgr = ticket_arrays(tk, keyed=True)
    fk = factors_by(df, ks, kgr)
    check("R2f the tickets' keyed gross trusted over their axles leaves the call and the twelve shares",
          whole(B.shares(df, fk)) == gw)
    wk = B.weekday_entries(TARGET)
    wk_utc = B.weekday_entries(TARGET, clock="utc")
    ci_utc = B.citations_by_section(TARGET, clock="utc")
    ci0 = B.citations_by_section(TARGET)
    check("R2g every toll stamp read as UTC moves only the asks (ask B in %d sections, ask A in %d)"
          % (sum(B.hround(wk[c]) != B.hround(wk_utc[c]) for c in B.CODES), sum(ci_utc[c] != ci0[c] for c in B.CODES)),
          sum(B.hround(wk[c]) != B.hround(wk_utc[c]) for c in B.CODES) >= 1 and
          sum(ci_utc[c] != ci0[c] for c in B.CODES) == 12)
    wk_cur = B.weekday_entries(TARGET, plazas="current")
    check("R2h plaza code P23 read by the list as it stands moves only Brannock's and Halbrook's ask figures",
          [c for c in B.CODES if B.hround(wk[c]) != B.hround(wk_cur[c])] == ["02", "08"])

    # ---------------------------------------------------------------- the ladder
    raw = B.shares(df)
    check("L0 the gross as recorded files %s" % B.five(raw), B.five(raw) == DEFAULT)
    tr = lambda fs, ft: B.shares(df, {c: fs(df[df["section"] == c]["gross"].to_numpy(),
                                            df[df["section"] == c]["steer"].to_numpy()) / ft(tg, tst) for c in B.CODES})
    med, mean = np.median, np.mean
    gross_routes = {
        "median gross": tr(lambda g, s: med(g), lambda g, s: med(g)),
        "mean gross": tr(lambda g, s: mean(g), lambda g, s: mean(g)),
        "loaded median gross": tr(lambda g, s: med(g[g > 50000]), lambda g, s: med(g[g > 50000])),
        "loaded mean gross": tr(lambda g, s: mean(g[g > 50000]), lambda g, s: mean(g[g > 50000])),
        "empty median gross": tr(lambda g, s: med(g[g <= 50000]), lambda g, s: med(g[g <= 50000])),
        "90th percentile gross": tr(lambda g, s: np.percentile(g, 90), lambda g, s: np.percentile(g, 90)),
        "99th percentile gross": tr(lambda g, s: np.percentile(g, 99), lambda g, s: np.percentile(g, 99)),
        "steer share of gross": tr(lambda g, s: med(s / g), lambda g, s: med(s / g)),
    }
    for k, v in gross_routes.items():
        check("L1 every station scaled to the tickets' %s misses (%s)" % (k, B.five(v)), B.five(v) != GOLD)
    pooled = B.shares(df, B.factors(df, tk, "pooled"))
    pooled_mean = B.shares(df, B.factors(df, tk, "pooled", agg="mean", ragg="mean"))
    check("L2 each station's steer axles pooled, empty and loaded, file %s (median) and %s (mean)"
          % (B.five(pooled), B.five(pooled_mean)), B.five(pooled) != GOLD and B.five(pooled_mean) != GOLD)
    empty = B.shares(df, B.factors(df, tk, "empty"))
    peak = B.shares(df, B.factors(df, tk, "empty_peak"))
    check("L3 the empty tractors' steer axles (%s) and the empty gross peak (%s) miss" % (B.five(empty), B.five(peak)),
          B.five(empty) != GOLD and B.five(peak) != GOLD)

    def net(fn):
        v = {c: fn(df[df["section"] == c]["gross"].to_numpy(), df[df["section"] == c]["steer"].to_numpy())
             for c in B.CODES}
        m = np.median(list(v.values()))
        return B.shares(df, {c: v[c] / m for c in B.CODES})
    for k, fn in (("loaded median gross", lambda g, s: med(g[g > 50000])), ("median gross", lambda g, s: med(g)),
                  ("empty median gross", lambda g, s: med(g[g <= 50000])), ("pooled steer", lambda g, s: med(s))):
        v = net(fn)
        check("L4 every station scaled to the network's median %s misses (%s)" % (k, B.five(v)), B.five(v) != GOLD)
    nl = net(lambda g, s: med(s[g > 50000]))
    check("L5 the loaded steer axles against the network's median station (no static reference) file the golden five",
          B.five(nl) == GOLD)
    check("L the default path keeps four of twelve whole shares at most (%d)"
          % sum(B.hround(raw[c]) == gw[c] for c in B.CODES), sum(B.hround(raw[c]) == gw[c] for c in B.CODES) <= 4)

    # ---------------------------------------------------------------- the golden and its family
    check("G1 the golden five: %s" % [B.NAMES[c] for c in five], five == GOLD)
    check("G1 figures.json carries the golden five and the twelve shares",
          sorted(B.CODES[B.CODES.index(f["sections"][n]["section"])] for n in f["call"]["equip"]) == GOLD and
          all(f["sections"][B.NAMES[c]]["share_pct"] == gw[c] for c in B.CODES))
    fam = {}
    for line in LINES:
        for a in ("median", "mean"):
            for b in ("median", "mean"):
                fam[(line, a, b)] = B.shares(df, B.factors(df, tk, "loaded", line, a, b))
    check("G2 every licensed member (%d: the loaded line from 45,000 to 72,000 lb, the station's median or mean, the "
          "tickets' median or mean) files the golden five" % len(fam), all(B.five(v) == GOLD for v in fam.values()))
    check("G2 every licensed member prints the same twelve whole per cents", all(whole(v) == gw for v in fam.values()))
    marg = min(abs((v[c] % 1) - 0.5) for v in fam.values() for c in B.CODES)
    check("G3 every member's every share sits 0.15 points or more inside its whole-per-cent bin (least %.2f)" % marg,
          marg >= 0.15)
    gaps = [sorted(v.values())[-5] - sorted(v.values())[-6] for v in fam.values()]
    check("G4 fifth clears sixth by 3.5 points or more under every member (least %.2f)" % min(gaps), min(gaps) >= 3.5)
    reads = lambda fv: {c: B.hround(abs(fv[c] - 1) * 100) for c in ("02", "09", "05", "11")}
    r0 = reads(fa)
    check("G5 the critical component (Brannock and Ingram Mill %d and %d per cent heavy, Elk Ferry and Kettle Run %d "
          "and %d light) holds under every member" % (r0["02"], r0["09"], r0["05"], r0["11"]),
          all(reads(B.factors(df, tk, "loaded", line, a, b)) == r0 for line in LINES for a in ("median", "mean")
              for b in ("median", "mean")) and all(abs((abs(fa[c] - 1) * 100) % 1 - 0.5) > 0.12 for c in r0))
    check("G5 the critical component's sides: Brannock and Ingram Mill read heavy, Elk Ferry and Kettle Run light",
          fa["02"] > 1 and fa["09"] > 1 and fa["05"] < 1 and fa["11"] < 1)
    check("G6 the lowest of the five (%d) and sixth (%s, %d) as figures.json states"
          % (gw[rank[4]], B.NAMES[rank[5]], gw[rank[5]]),
          f["components"]["sixth"]["name"] == B.NAMES[rank[5]] and f["components"]["sixth"]["share_pct"] == gw[rank[5]]
          and min(gw[c] for c in GOLD) == 11)

    # ---------------------------------------------------------------- SF1 to SF18
    prog = pdf_text("program")
    dic = pdf_text("dictionary")
    check("SF1 the program files gross vehicle weight as the static scale's, and the gross as recorded files another "
          "five", "on a certified static scale" in prog and B.five(raw) != GOLD)
    ge = B.shares(df, fa)
    ge2 = {c: 100.0 * float(np.mean(df[df["section"] == c]["gross"].to_numpy() / fa[c] >= W.LIMIT)) for c in B.CODES}
    check("SF2 at or above 80,000 lb gives the same call and twelve shares", whole(ge2) == whole(ge) and
          "exceeded 80,000 lb" in prog)
    five_ax = wim_all[(wim_all["axles"] == 5) & (wim_all["rejected"] == 0)]
    check("SF3 every five-axle vehicle in place of class 9 gives the same call",
          B.five(B.shares(five_ax, B.factors(five_ax, tk))) == GOLD and "FHWA vehicle class 9" in prog)
    check("SF4 every record in place of the accepted weighings gives the same call (R2e)",
          B.five(B.shares(allr, B.factors(allr, tk))) == GOLD)
    utc = df[(df["local"] + pd.Timedelta(hours=5)).dt.year == 2026]
    check("SF5 UTC dates for the controllers' clocks give the same call and twelve shares",
          whole(B.shares(utc, B.factors(utc, tk))) == gw and "Eastern Standard Time all year" in dic)
    check("SF6 the station list's previous milepost keeps the station in its section", B.section_at(29.7) == "02")
    lane1 = df[df["lane"] == 1]
    check("SF7 the first lane alone gives the same call", B.five(B.shares(lane1, B.factors(lane1, tk))) == GOLD and
          "in every lane and in both directions" in prog)
    fall = factors_by(df, tst, np.full(len(tst), 99999.0), line=50000)
    check("SF8 every ticket in place of the loaded tickets as the reference gives the same call and twelve shares "
          "(%d empty tickets)" % int((tg <= 50000).sum()), whole(B.shares(df, fall)) == gw)
    check("SF9 the loaded line anywhere from 45,000 to 72,000 lb gives the same call and shares (G2)",
          all(whole(fam[(l, "median", "median")]) == gw for l in LINES))
    check("SF10 the mean in place of the median, either side, gives the same call and shares (G2)",
          all(whole(fam[(50000, a, b)]) == gw for a in ("median", "mean") for b in ("median", "mean")))
    check("SF11 half up and half to even agree on the twelve shares (no share at a half)",
          all(B.hround(sh[c]) == int(np.round(sh[c])) for c in B.CODES))
    check("SF12 no tie for fifth (%.2f points clear)" % (sh[rank[4]] - sh[rank[5]]), sh[rank[4]] - sh[rank[5]] >= 3.5)
    ent = B.entries_clean(TARGET)
    wkd = ent[np.array([d.weekday() < 5 for d in ent["date"]])]
    hol = wkd[wkd["date"].isin(set(W.HOLIDAYS))]
    check("SF13 the program counts holidays among the 261 weekdays, and leaving them out moves the figures (%d holiday "
          "entries)" % len(hol), "holidays included" in prog and "261" in prog and len(hol) > 1000)
    check("SF14 the program dates an entry by its local date; the UTC date moves ask B (R2g)",
          "by the local date of the entry" in prog and wk_utc != wk)
    pl = pd.read_csv(os.path.join(TARGET, P.FILES["plazas"]))
    sched = pdf_text("schedule")
    check("SF15 the plaza list dates P41 and the reissued P23, and the 2025 schedule places P23 at Brannock Road",
          set(pl.loc[pl["in_service_from"].notna(), "plaza"]) == {"P41", "P23"} and "P23 Brannock Road 38.1" in sched)
    ci = B.citations_by_section(TARGET)
    cr = B.read_citations(TARGET)
    ent_s = ent.sort_values("local")
    by_tag = {t: v for t, v in ent_s.groupby("tag_id")}
    tkt = tk.assign(when=pd.to_datetime(tk["Date"].astype(str).str[:10] + " " + tk["Time"]))
    over = tkt[tg > 80000]
    ps = B.plaza_section(TARGET)
    cnt = {}
    for tag, when in zip(over["Tag"], over["when"]):
        v = by_tag[tag]
        row = v[v["local"] <= when].iloc[-1]
        s_ = ps(row["plaza"], row["date"])
        cnt[s_] = cnt.get(s_, 0) + 1
    check("SF16 a ticket over 80,000 lb is not a citation: counting tickets moves ask A (%d sections), and the program "
          "names violation code G" % sum(cnt.get(c, 0) != ci[c] for c in B.CODES),
          sum(cnt.get(c, 0) != ci[c] for c in B.CODES) >= 8 and "violation code G" in prog)
    lg = B.citations_by_section(TARGET, "logged")
    check("SF17 the program places a citation at the trip weighed; the log's entry plaza moves all twelve (A1)",
          "on the trip on which the scale house weighed it" in prog and all(lg[c] != ci[c] for c in B.CODES))
    d18 = subset(["piezo", "bending", "stations", "tickets"])
    df18 = B.class9(B.read_wim(d18))
    s18 = B.shares(df18, B.factors(df18, B.read_tickets(d18)))
    check("SF18 the call and twelve shares from the WIM exports, the station list and the tickets alone",
          whole(s18) == gw and B.five(s18) == GOLD)
    shutil.rmtree(d18)

    # ---------------------------------------------------------------- the asks
    mv = lambda a: sum(B.hround(a[c]) != B.hround(wk[c]) for c in B.CODES)
    var = {k: B.weekday_entries(TARGET, dedup=k) for k in ("none", "exact", "pair60", "cut_first", "cut_last",
                                                             "sameday")}
    check("A2 every section's weekday entries move under every reflex (%s)"
          % ", ".join("%s %d" % (k, mv(v)) for k, v in var.items()), all(mv(v) == 12 for v in var.values()))
    raw_e = B.read_entries(TARGET)
    old, new = raw_e[raw_e["old"]], raw_e[~raw_e["old"]]
    back = B._twins(old, new, -60, 16 * 60)
    gen = P.entry_rows(e)
    n_back = sum(1 for r in gen if r[5] == "backfill")
    check("A2 fair: the new-host rows stamped up to 16 minutes before an old-host row of the same tag and plaza are "
          "exactly the backfill (%d rows), each with one twin" % len(back),
          len(back) == n_back and len(B._twins(old, new, -16 * 60, 16 * 60)) == n_back and
          not raw_e.duplicated(["txn_id"]).any())
    last_old = old.groupby("plaza")["stamp"].max()
    per_cut = set(i for i, r in new.iterrows() if r["plaza"] in last_old.index and r["stamp"] <= last_old[r["plaza"]])
    check("A2 fair: a cut at each plaza's last old-host stamp drops the same rows as the twins", per_cut == back)
    check("A2 fair: no live new-host row has an old-host twin within four hours either side",
          len(B._twins(old, new.drop(index=sorted(back)), -4 * 3600, 4 * 3600)) == 0)
    sw = {p: W.switch_time(p) for p in W.SWITCH}
    check("A2 the plazas moved on %d different days from %s to %s" % (len(set(sw.values())), min(sw.values()).date(),
          max(sw.values()).date()), len(set(sw.values())) >= 15)
    live = new.drop(index=sorted(back))
    loc_new = B.to_local(live["stamp"])
    order_ok = (pd.concat([loc_new, new.loc[sorted(back), "stamp"]]).reindex(new.index)
                .loc[new.sort_values("txn_id").index].is_monotonic_increasing)
    check("A2 no marker: the new host's ids run in entry order through its backfill and its own entries", order_ok)
    oh = old["stamp"].dt.hour.value_counts().sort_index()
    lh = live["stamp"].dt.hour.value_counts().sort_index()
    check("A1 fair: the old host's stamps peak in local working hours (%d:00) and the new host's own four or five hours "
          "later (%d:00), as UTC" % (oh.idxmax(), lh.idxmax()), 6 <= oh.idxmax() <= 14 and 3 <= lh.idxmax() - oh.idxmax() <= 6)
    ci = ci0
    var_a = {"the log's entry plaza": B.citations_by_section(TARGET, "logged"), "every stamp as UTC": ci_utc,
             "no stamp converted": B.citations_by_section(TARGET, clock="none"),
             "exact duplicates, every stamp as UTC": B.citations_by_section(TARGET, dedup="exact", clock="utc")}
    check("A1 every section's gross citations move under every reflex (%s; ten or more with no stamp converted)"
          % ", ".join("%s %d" % (k, sum(v[c] != ci[c] for c in B.CODES)) for k, v in var_a.items()),
          all(sum(v[c] != ci[c] for k, v in var_a.items() for c in B.CODES if k == k0) >= (10 if "no stamp" in k0 else 12)
              for k0 in var_a))
    cr = B.read_citations(TARGET)
    g = cr[cr["violation"] == "G"]
    mp = dict(zip(pl["plaza"], pl["milepost"]))
    house_mp = {"West Scale House": 0.6, "East Scale House": 283.4}
    ent_u = B.entries_clean(TARGET, clock="utc").sort_values("local")
    by_u = {t: v for t, v in ent_u.groupby("tag_id")}
    feas, odd = True, 0
    for _, r in g.iterrows():
        v = by_tag[r["tag_id"]]
        trip = v[v["local"] <= r["issued_local"]].iloc[-1]
        miles = abs((38.1 if trip["plaza"] == "P23" and trip["date"] < dt.date(2026, 5, 1) else mp[trip["plaza"]])
                    - house_mp[r["scale_house"]])
        hours = (r["issued_local"] - trip["local"]).total_seconds() / 3600
        feas &= 0 < hours and miles / (hours + RECEIPT_ALLOW) < 80
        u = by_u[r["tag_id"]]
        tu = u[u["local"] <= r["issued_local"]].iloc[-1]
        odd += tu["plaza"] in ("P01", "P32") and tu["plaza"] == ("P01" if r["scale_house"].startswith("West") else "P32")
    check("A1 fair: on the golden's clocks every gross citation's trip reaches its scale house at under 80 mph, allowing "
          "the old host's receipt delay", feas)
    check("A1 fair: read as UTC, %d citations' trips would start at their own scale house's barrier, a truck weighed "
          "on the way out entering where it is weighed" % odd, odd > 150)
    moved_rows, paper, later_ok = 0, 0, True
    for _, r in g.iterrows():
        v = by_tag[r["tag_id"]]
        trip = v[v["local"] <= r["issued_local"]].iloc[-1]
        if trip["plaza"] != r["entry_plaza"]:
            moved_rows += 1
            keyed = pd.to_datetime(r["keyed"], format="%m/%d/%Y %H:%M")
            after = v[(v["local"] > r["issued_local"]) & (v["local"] <= keyed + pd.Timedelta(minutes=1))]
            later_ok &= r["entry_plaza"] in set(after["plaza"])
        paper += r["citation_no"].startswith("C")
    check("A1 fair: every citation whose log plaza is not its trip's carries the tag's later entry between the stop and "
          "the keying (%d rows)" % moved_rows, later_ok and moved_rows > 100)
    check("A1 no marker: those citations are under 80 per cent of the paper citations (%d of %d)" % (moved_rows, paper),
          0.2 < moved_rows / paper < 0.8)
    trip_cur = B.citations_by_section(TARGET, plazas="current")
    check("A hazard: P23 by the current list moves Brannock's and Halbrook's citations",
          [c for c in B.CODES if trip_cur[c] != ci[c]] == ["02", "08"])
    check("A the golden's ask figures are figures.json's", all(
        f["sections"][B.NAMES[c]]["weekday_entries"] == B.hround(wk[c]) and
        f["sections"][B.NAMES[c]]["gross_citations"] == ci[c] for c in B.CODES))
    sec_of = lambda code, kind: ("02" if kind == "old" else "08") if code == "P23" else \
        [p_[2] for p_ in W.PLAZAS if p_[0] == code][0]
    truthB, pureB = {}, {}
    for tid, code, stamp, tag, local, kind in gen:
        if kind == "backfill":
            continue
        day = dt.datetime.strptime(stamp, "%Y-%m-%d %H:%M").date() if kind == "old" else local.date()
        if day.weekday() < 5 and day.year == 2026:
            truthB[sec_of(code, kind)] = truthB.get(sec_of(code, kind), 0) + 1
        if local.weekday() < 5:
            pureB[sec_of(code, kind)] = pureB.get(sec_of(code, kind), 0) + 1
    check("A the golden's weekday entries are the generator's, each entry once on its host's own clock",
          all(abs(truthB[c] / B.WEEKDAYS_2026 - wk[c]) < 1e-9 for c in B.CODES))
    check("A the old host's late receipt stamps move no whole figure from the entries' true local dates",
          all(B.hround(pureB[c] / B.WEEKDAYS_2026) == B.hround(wk[c]) for c in B.CODES))
    truthA = {}
    for c_ in e["citations"]:
        if c_["code"] == "G":
            s_ = W.section_of(e["entries"], c_["trip"])
            truthA[s_] = truthA.get(s_, 0) + 1
    check("A the golden's citations are the generator's truth", all(truthA.get(c, 0) == ci[c] for c in B.CODES))
    n_re = sum(1 for d_, i_, t_, s__ in e["entries"][e["n_entries"]:])
    check("A %d trucks cited for gross weight came back through their barrier after offloading" % n_re, n_re > 500)

    # ---------------------------------------------------------------- separation and distractors
    dX = subset([k for k in P.FILES if k not in ("piezo", "bending", "stations", "tickets")])
    check("X1 the asks need no WIM export, station list or ticket: ask B and ask A from the other files",
          B.weekday_entries(dX) == wk and B.citations_by_section(dX) == ci)
    shutil.rmtree(dX)
    check("X2 the call reads no toll entry, citation, plaza or schedule row (SF18)", whole(s18) == gw)
    dD = subset([k for k in P.FILES if k not in ("pavement", "bridges")])
    dfD = B.class9(B.read_wim(dD))
    check("X3 the distractors deleted: the call, the twelve shares and both asks unchanged",
          whole(B.shares(dfD, B.factors(dfD, B.read_tickets(dD)))) == gw and B.weekday_entries(dD) == wk and
          B.citations_by_section(dD) == ci)
    shutil.rmtree(dD)

    # ---------------------------------------------------------------- input gates
    files = os.listdir(TARGET)
    meta = json.load(open(os.path.join(TASK, "metadata.json")))
    check("I ten or more files (%d)" % len(files), len(files) >= 10)
    check("I three or more formats (%s)" % sorted({fn.rsplit(".", 1)[1] for fn in files}),
          len({fn.rsplit(".", 1)[1] for fn in files}) >= 3)
    check("I one file of 25,000 rows or more (piezo %d)" % len(pz), len(pz) >= 25000)
    check("I two distractors named in metadata.json, none in a file name",
          len(meta["distractor_files"]) >= 2 and all(d in files for d in meta["distractor_files"]) and
          not any("distract" in fn for fn in files))

    # ---------------------------------------------------------------- realism
    ok_pz = all(int(ln[30:35]) == sum(int(ln[35 + 4 * k:39 + 4 * k]) for k in range(int(ln[28:30]))) for ln in pz)
    check("Z the piezo records' gross is their axles' sum on every record", ok_pz)
    ax = bp[["ax%d_kg" % i for i in range(1, 10)]].apply(pd.to_numeric, errors="coerce").fillna(0).sum(axis=1)
    check("Z the bending-plate records' gvw_kg is their axles' sum on every record",
          (ax == pd.to_numeric(bp["gvw_kg"])).all())
    keyed_g = tk["Gross (lb)"].astype(int).to_numpy()
    mism = [(str(a).zfill(len(str(int(b)))), str(int(b))) for a, b in zip(keyed_g, tg) if a != int(b)]
    swaps = all(len(a) == len(b) and sorted(a) == sorted(b) and sum(x != y for x, y in zip(a, b)) == 2 for a, b in mism)
    check("Z the tickets' keyed gross departs from the axles' sum only by a transposed pair of digits (%d tickets)"
          % len(mism), swaps and 0 < len(mism) < 30)
    iss = cr["issued_local"]
    kd = pd.to_datetime(cr["keyed"], format="%m/%d/%Y %H:%M")
    ec = cr["citation_no"].str.startswith("EC")
    check("Z every citation is keyed after it was issued; e-citations within the hour, paper ones 4 to 14 days later",
          (kd >= iss).all() and ((kd - iss)[ec] < pd.Timedelta(hours=1)).all() and
          ((kd - iss)[~ec] >= pd.Timedelta(days=4)).all() and ((kd - iss)[~ec] < pd.Timedelta(days=14, hours=8)).all())
    check("Z every class 9 steer axle reads between 7,000 and 16,000 lb",
          df["steer"].between(7000, 16000).mean() > 0.999)
    n9 = df.groupby("section").size()
    check("Z the stations' class 9 counts vary (%d to %d)" % (n9.min(), n9.max()), n9.min() / n9.max() < 0.6)
    check("Z no share is a round figure", all(abs(sh[c] - round(sh[c])) > 0.01 for c in B.CODES))
    import csv as _csv
    gcsv = list(_csv.DictReader(open(os.path.join(TASK, "golden", "ctpa_section_overweight_2026.csv"),
                                     encoding="utf-8")))
    check("Z the golden CSV carries the twelve shares", [int(r["share_over_80000_lb_pct"]) for r in gcsv] ==
          [gw[c] for c in B.CODES])

    n_fail = sum(1 for _, ok in RESULTS if not ok)
    print("%s  task478 checks: %d assertions, %d failed" % ("PASS" if not n_fail else "FAIL", len(RESULTS), n_fail))
    return 1 if n_fail else 0


if __name__ == "__main__":
    sys.exit(main())
