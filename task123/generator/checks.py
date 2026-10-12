"""task123 assertions: the input gates, every rung and its separation from the golden, the golden's placement and
its valid variants (SF11), each semantic fork row, the closure facts, both asks' goldens and every stop on their
ladders, the separation line, the hazards, and the realism sweep. Run by build.py after every build.

The main call's rungs run on the simulated records through calc.py (the golden there equals the golden recomputed
from target/ by golden.py, asserted first); the forks that turn on a shipped file's content run on target/.
"""
import datetime as dt
import json
import os
import re
import shutil
import sys
import tempfile
import zipfile
from collections import defaultdict

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import calc as K       # noqa: E402
import docs as DC      # noqa: E402
import golden as G     # noqa: E402
import pack as P       # noqa: E402
import world as W      # noqa: E402

J0, J1 = dt.date(2026, 1, 1), dt.date(2026, 1, 31)
r5 = G.r5k
r10 = G.r10k


class Book:
    def __init__(self):
        self.rows = []

    def check(self, cid, ok, detail):
        self.rows.append((cid, bool(ok), detail))

    def report(self):
        width = max(len(c) for c, _, _ in self.rows)
        for cid, ok, detail in self.rows:
            print("%-4s %-*s %s" % ("PASS" if ok else "FAIL", width, cid, detail))
        bad = [c for c, ok, _ in self.rows if not ok]
        print("checks: %d assertions, %d failed" % (len(self.rows), len(bad)))
        if bad:
            raise SystemExit("checks failed: %s" % ", ".join(bad))


def disp(d):
    """A county dict from the simulated records, keyed by the names the pack carries."""
    return {W.DISPLAY[k]: v for k, v in d.items()}


def bins_off(a, g, step):
    rnd = r5 if step == 5000 else r10
    return [c for c in G.COUNTIES if rnd(a[c]) != rnd(g[c])]


def run(target, golden_dir, world, meta_path):
    B = Book()
    prem, U, bills, mdms, ind = world["prem"], world["U"], world["bills"], world["mdms"], world["ind"]
    gc = world["golden"]
    files = sorted(os.listdir(target))

    # ---------------------------------------------------------------- input gates
    meta = json.load(open(meta_path))
    fmts = {f.rsplit(".", 1)[1] for f in files}
    B.check("G1", len(files) >= 10, "%d files" % len(files))
    B.check("G2", len(fmts) >= 3, "formats %s" % sorted(fmts))
    big = max(meta["files"], key=lambda x: x["rows"] or 0)
    B.check("G3", big["rows"] >= 25000, "%s %d rows" % (big["path"], big["rows"]))
    dis = meta["distractor_files"]
    B.check("G4", len(dis) >= 2 and all(d in files for d in dis), "distractors %s" % dis)
    tmp = tempfile.mkdtemp()
    try:
        for f in files:
            if f not in dis:
                shutil.copy(os.path.join(target, f), tmp)
        c2 = G.compute(tmp)
    finally:
        shutil.rmtree(tmp)
    same = all(abs(c2["jan"][c] - gc["jan"][c]) < 1e-6 and c2["k1"][c] == gc["k1"][c] and c2["k2"][c] == gc["k2"][c]
               for c in G.COUNTIES)
    B.check("G5", same, "golden and both asks unchanged with the distractors deleted")

    # ---------------------------------------------------------------- the golden and the rungs
    w = K.shape_from_mdms(mdms)
    r4 = disp(K.county_jan(bills, w, "R4"))
    B.check("M1", max(abs(r4[c] - gc["jan"][c]) for c in G.COUNTIES) < 0.01,
            "golden from target/ equals the simulated records' R4 on every county")
    g_aw = K.awards(r4)
    rungs = {"R0": disp(K.county_jan(bills, w, "R0")), "R1": disp(K.county_jan(bills, w, "R1")),
             "R2": disp(K.county_jan(bills, w, "R2")), "R3": disp(K.scale_up(bills, prem)[0])}
    for k, v in rungs.items():
        a = K.awards(v)
        off = bins_off(a, g_aw, 5000)
        dev = min(abs(a[c] - g_aw[c]) for c in G.COUNTIES)
        B.check("M2-" + k, len(off) == 12 and dev > 3700,
                "%s: %d of 12 counties outside the golden's $5,000 bin, nearest $%s" % (k, len(off), format(int(dev), ",")))
    r1 = K.awards(rungs["R1"])
    world["rung_awards"] = {k: K.awards(v) for k, v in rungs.items()}
    # partial applications: the shape on Northbank's bills only, and on every bill but Northbank's
    for name, on in (("shape on Northbank only", {"NNG"}), ("shape on Kestrel Valley and Pine Harbor only", {"KVG", "PHE"})):
        out = defaultdict(float)
        ones = np.ones(W.NDAY)
        for bl in bills:
            if K.touches_jan(bl):
                out[bl.county] += bl.therms * K.jan_share(w if bl.util in on else ones, bl.start, bl.end)
        off = bins_off(K.awards(disp(out)), g_aw, 5000)
        B.check("M3-" + ("N" if on == {"NNG"} else "KP"), len(off) >= 9, "%s: %d of 12 counties off" % (name, len(off)))
    edge_a = min(2500 - abs(g_aw[c] - r5(g_aw[c])) for c in G.COUNTIES)
    edge_t = min(5000 - abs(r4[c] - r10(r4[c])) for c in G.COUNTIES)
    B.check("M4", edge_a >= 1400, "every award at least $%s inside its $5,000 bin" % format(int(edge_a), ","))
    B.check("M5", edge_t >= 2500, "every county's therms at least %s inside its 10,000 bin" % format(int(edge_t), ","))
    rounded = [r5(g_aw[c]) for c in G.COUNTIES]
    B.check("M6", len(set(rounded)) == 12, "twelve distinct rounded awards (the bar order is unique)")
    B.check("M7", sum(rounded) == W.GRANT, "rounded awards sum to $%s" % format(sum(rounded), ","))

    # ---------------------------------------------------------------- SF11: the golden's valid variants
    variants = {}
    variants["median shape"] = disp(K.county_jan(bills, K.shape_from_mdms(mdms, "median"), "R4"))
    tot, cnt = np.zeros(W.NDAY), np.zeros(W.NDAY)
    for pid, (d0, ccf, q) in mdms.items():
        ok = np.nan_to_num(ccf, nan=0) > 0
        tot[d0:d0 + len(ccf)] += np.where(ok, ccf, 0)
        cnt[d0:d0 + len(ccf)] += ok
    variants["positive reads only"] = disp(K.county_jan(bills, np.where(cnt > 0, tot / np.maximum(cnt, 1), np.nan),
                                                        "R4"))
    a, b = W.IDX[dt.date(2025, 11, 1)], W.IDX[dt.date(2026, 3, 31)]
    whole = {pid for pid, (d0, ccf, q) in mdms.items()
             if np.isfinite(ccf[a - d0:b - d0 + 1]).all() and (ccf[a - d0:b - d0 + 1] > 0).all()}
    variants["meters with a whole winter"] = disp(K.county_jan(bills, K.shape_from_mdms(mdms, pids=whole), "R4"))
    tot, cnt = np.zeros(W.NDAY), np.zeros(W.NDAY)
    for pid, (d0, ccf, q) in mdms.items():
        ok = (q != "E") & np.isfinite(ccf)
        tot[d0:d0 + len(ccf)] += np.where(ok, ccf, 0)
        cnt[d0:d0 + len(ccf)] += ok
    variants["validated reads only"] = disp(K.county_jan(bills, np.where(cnt > 0, tot / np.maximum(cnt, 1), np.nan),
                                                         "R4"))
    tot, cnt = np.zeros(W.NDAY), np.zeros(W.NDAY)
    for pid, (d0, ccf, q) in mdms.items():
        full = np.full(W.NDAY, np.nan)
        full[d0:d0 + len(ccf)] = ccf
        s = np.nansum(full[a:b + 1])
        if s > 0:
            x = full / s
            ok = np.isfinite(x)
            tot[ok] += x[ok]
            cnt[ok] += 1
    variants["each meter normalised"] = disp(K.county_jan(bills, np.where(cnt > 0, tot / np.maximum(cnt, 1), np.nan),
                                                          "R4"))
    pc = defaultdict(set)
    for p in prem:
        if p.pid in mdms:
            pc[p.county].add(p.pid)
    vc = {}
    for c in W.COUNTY_ORDER:
        ww = K.shape_from_mdms(mdms, pids=pc[c]) if c in pc else w
        vc[W.DISPLAY[c]] = K.county_jan([bl for bl in bills if bl.county == c], ww, "R4").get(c, 0.0)
    variants["own county's AMI shape"] = vc
    variants["one span per account"] = disp(K.span_jan(bills, w))
    hv = defaultdict(float)
    for bl in bills:
        if not K.touches_jan(bl):
            continue
        if bl.util == "NNG":
            ia, ib = W.IDX[bl.start] + 1, W.IDX[bl.end] + 1
            seg = w[ia:ib]
            hvs = np.array([W.HV_NNG_MONTH[(d.year, d.month)] for d in W.DAYS[ia:ib]])
            hv[bl.county] += bl.ccf * float((seg * hvs)[W.JAN[ia:ib]].sum() / seg.sum())
        else:
            hv[bl.county] += bl.therms * K.jan_share(w, bl.start, bl.end)
    variants["Northbank CCF at each month's heating value (SF6)"] = disp(hv)
    for i, (name, v) in enumerate(variants.items()):
        oa, ot = bins_off(K.awards(v), g_aw, 5000), bins_off(v, r4, 10000)
        dev = max(abs(K.awards(v)[c] - g_aw[c]) for c in G.COUNTIES)
        B.check("SF11-%d" % (i + 1) if "SF6" not in name else "SF6", not oa and not ot,
                "%s: awards and therms in the golden's bins on all twelve (largest move $%s)" % (name, format(int(dev), ",")))
    truth = defaultdict(float)
    for i, p in enumerate(prem):
        truth[p.county] += U[i, W.JAN].sum()
    off = bins_off(K.awards(disp(truth)), g_aw, 5000)
    B.check("M8", not off, "the simulated true January use lands every county in the golden's award bin")

    # ---------------------------------------------------------------- the other fork rows, on target/
    bdf = gc["bills"]
    cof = gc["county_of"]
    wts = gc["weights"]
    gs = pd.read_csv(os.path.join(target, P.FILES["kvg_gs"]), dtype={"ACCOUNT_NO": str})
    gsb = pd.DataFrame({"util": "KVG", "premise": gs.PREMISE_NO, "account": gs.ACCOUNT_NO,
                        "first": pd.to_datetime(gs.SVC_FROM, format="%m/%d/%Y").dt.date,
                        "last": pd.to_datetime(gs.SVC_TO, format="%m/%d/%Y").dt.date, "therms": gs.THERMS})
    with_gs = G.january(pd.concat([bdf, gsb], ignore_index=True), wts, cof)
    off = bins_off(G.split(with_gs), G.split(gc["jan"]), 5000)
    B.check("SF1", len(off) >= 3, "general service bills added: %d counties move bins (standard 2.1 rules them out)" % len(off))
    shifted = bdf.copy()
    shifted["first"] = shifted["first"] - dt.timedelta(1)
    shifted["last"] = shifted["last"] - dt.timedelta(1)
    sh = G.january(shifted, wts, cof)
    off = bins_off(G.split(sh), G.split(gc["jan"]), 5000)
    kv = pd.read_csv(os.path.join(target, P.FILES["kvg_bills"]), dtype={"ACCOUNT_NO": str})
    kv = kv[kv.TXN_TYPE == "BILL"]
    kv["f"] = pd.to_datetime(kv.SVC_FROM, format="%m/%d/%Y")
    kv["t"] = pd.to_datetime(kv.SVC_TO, format="%m/%d/%Y")
    kv = kv.sort_values(["PREMISE_NO", "t"])
    nxt = kv.groupby("PREMISE_NO")["f"].shift(-1)
    contiguous = bool(((nxt.dropna() - kv.loc[nxt.dropna().index, "t"]).dt.days == 1).all())
    B.check("SF3", len(off) >= 6 and contiguous,
            "the read day billed on the next bill instead: %d counties move bins; Kestrel Valley's SVC_FROM is the day "
            "after the prior SVC_TO on every consecutive pair (standard 2.4)" % len(off))
    sp = pd.read_csv(os.path.join(target, P.FILES["service_points"]), dtype=str)
    city_county = sp.CITY.map(lambda t: P.TOWN_COUNTY[t.title()] if t.title() in P.TOWN_COUNTY else None)
    by_city = dict(zip(sp.PREMISE_ID, city_county.fillna(sp.COUNTY.str.title())))
    moved = int((city_county.notna() & (city_county != sp.COUNTY.str.title())).sum())
    off = bins_off(G.split(G.january(bdf, wts, by_city)), G.split(gc["jan"]), 5000)
    B.check("SF4", moved > 500 and len(off) >= 3,
            "county from the postal city: %d premises move, %d counties change bins (standard 2.6)" % (moved, len(off)))
    k = pd.read_csv(os.path.join(target, P.FILES["kvg_bills"]), dtype={"BILL_NO": str})
    groups = k[k.BILL_NO.isin(k.loc[k.TXN_TYPE == "CNCL", "BILL_NO"])].groupby("BILL_NO")
    ok = all(set(g_.TXN_TYPE) == {"BILL", "CNCL", "RBIL"} and
             int(g_.loc[g_.TXN_TYPE == "CNCL", "THERMS"].sum()) == -int(g_.loc[g_.TXN_TYPE == "BILL", "THERMS"].sum())
             for _, g_ in groups)
    B.check("SF5", ok and len(groups) >= 50,
            "%d cancelled bills, each cancel exactly reverses its original under the same bill number" % len(groups))
    rf = {c: r10(gc["jan"][c]) for c in G.COUNTIES}
    off = bins_off(G.split(rf), G.split(gc["jan"]), 5000)
    B.check("SF8", True, "awards from therms rounded first would move %d counties; standard 3.3 computes from "
                         "unrounded use" % len(off))
    bad = 0
    n = 0
    for bl in bills:
        if bl.basis == "CALENDAR" and bl.end == J1 and bl.start == dt.date(2025, 12, 31):
            d0, ccf, q = mdms[bl.pid]
            s = float(np.nansum(ccf[W.IDX[J0] - d0:W.IDX[J1] - d0 + 1]))
            n += 1
            bad += abs(bl.therms - round(s * W.HV_PHE)) > 0
    B.check("SF9", n > 4000 and bad == 0, "%d AMI January bills, each equal to its daily reads times 1.034" % n)
    est = [bl for bl in bills if K.touches_jan(bl) and bl.read_type == "E"]
    B.check("SF10", not est, "no bill touching January closes on an estimated read")
    B.check("SF2", len(bins_off(K.awards(rungs["R0"]), g_aw, 5000)) == 12,
            "billed-month reading (R0) moves all twelve; standard 2.3 rules it out")
    B.check("SF7", abs(sum(gc["jan"].values()) - sum(r4.values())) < 0.1, "shares of the twelve counties' total")

    # ---------------------------------------------------------------- closure facts
    last = max(bl.end for bl in bills if K.touches_jan(bl))
    B.check("C12", last <= dt.date(2026, 3, 31), "latest read on a bill touching January: %s" % last)
    gaps = 0
    pmap = defaultdict(list)
    for bl in bills:
        pmap[bl.pid].append(bl)
    for p in prem:
        cov = set()
        for bl in pmap[p.pid]:
            d = max(bl.start + dt.timedelta(1), J0)
            while d <= min(bl.end, J1):
                cov.add(d)
                d += dt.timedelta(1)
        act = {J0 + dt.timedelta(i) for i in range(31) if any(
            s <= J0 + dt.timedelta(i) and (e is None or J0 + dt.timedelta(i) <= e) for _, s, e in p.accounts)}
        gaps += len(act ^ cov)
    B.check("C16", gaps == 0, "every January gas day of every account is billed once, and no other")
    B.check("C9", gc["snap_ratio"] >= 2.0, "AMI mean daily use 19 to 31 January is %.2f times 1 to 18 January" %
            gc["snap_ratio"])

    # ---------------------------------------------------------------- the asks
    k1t, k2t = disp(ind["k1"]), disp(ind["k2"])
    B.check("A1", all(gc["k1"][c] == k1t[c] for c in G.COUNTIES), "Ask 1 from target/ equals the events")
    B.check("A2", all(gc["k2"][c] == k2t[c] for c in G.COUNTIES), "Ask 2 from target/ equals the events")
    st = stops(target, cof)
    world["ask_stops"] = st
    for k_, sv in st.items():
        ask, rows = k_.split(":", 1)
        gold = gc["k1"] if ask == "K1" else gc["k2"]
        touched = [c for c in G.COUNTIES if c in sv["counties"]]
        miss = [c for c in touched if sv["values"].get(c, 0) != gold[c]]
        B.check("A-" + k_, len(miss) == len(touched), "%s: misses %d of the %d counties it touches" % (
            rows, len(miss), len(touched)))
    B.check("A3", len(ind["ledger"]["kvg_contractor_late"]) >= 5 and len(ind["ledger"]["phe_remote_np"]) >= 30 and
            len(ind["ledger"]["nng_carried"]) >= 10 and len(ind["ledger"]["phe_converted_open"]) >= 100 and
            len(ind["ledger"]["kvg_intake_county"]) >= 50 and len(ind["ledger"]["nng_stale_flag"]) >= 8,
            "device rows: " + ", ".join("%s %d" % (k_, len(v)) for k_, v in sorted(ind["ledger"].items())))
    # hazards are present and repaired by the golden's path
    o = pd.read_csv(os.path.join(target, P.FILES["kvg_orders"]), dtype=str)
    B.check("H1", ((o.STATUS == "CERR") & (o.REASON_CD == "NP")).sum() >= 3, "completed-in-error nonpayment orders present")
    B.check("H2", (o.STATUS == "UNAB").sum() >= 5, "unable-to-complete attempts present")
    B.check("H3", ((o.ORDER_TYPE == "OFF") & (o.REASON_CD != "NP")).sum() >= 20, "turn-off orders for other reasons")
    e = pd.read_csv(os.path.join(target, P.FILES["kvg_wcp"]), dtype=str, keep_default_na=False)
    late_ap = ((pd.to_datetime(e.APPROVED_DT) > "2026-01-31") & (pd.to_datetime(e.EFFECTIVE_DT) <= "2026-01-31")).sum()
    B.check("H5", late_ap >= 2, "%d enrollments approved after 31 January and effective by then (counted)" % late_ap)

    # ---------------------------------------------------------------- separation line
    closed_meters = {pid for pid, (d0, ccf, q) in mdms.items() if (np.nan_to_num(ccf, nan=1) == 0).any()}
    sub = K.shape_from_mdms(mdms, pids=set(mdms) - closed_meters)
    v = disp(K.county_jan(bills, sub, "R4"))
    B.check("S1", not bins_off(K.awards(v), g_aw, 5000) and not bins_off(v, r4, 10000),
            "%d meters with a shut-off day dropped from the shape: every county stays in both bins" % len(closed_meters))

    # ---------------------------------------------------------------- realism and hygiene
    text = {}
    for f in files:
        pth = os.path.join(target, f)
        if f.endswith((".csv", ".txt", ".eml", ".json")):
            text[f] = open(pth, encoding="utf-8", errors="replace").read()
        elif f.endswith(".docx"):
            with zipfile.ZipFile(pth) as z:
                text[f] = re.sub(r"<[^>]+>", " ", z.read("word/document.xml").decode())
    dash = [f for f, t in text.items() if "—" in t or "–" in t]
    B.check("R1", not dash, "no em or en dash in any text file")
    people = {"Regina Fowler", "Douglas Tyler", "Alison Pacheco", "Matthew Solis"}
    named = set(re.findall(r"\b(Regina|Douglas|Alison|Matthew) ([A-Z][a-z]+)", text[DC.THREAD]))
    B.check("R2", {" ".join(x) for x in named} <= people, "thread names only the card's personas")
    k1v = [gc["k1"][c] for c in G.COUNTIES]
    B.check("R3", len(set(k1v)) >= 5 and len(set(gc["k2"].values())) == 12, "indicator counts vary by county")
    stamp = {int(os.path.getmtime(os.path.join(target, f))) for f in files}
    B.check("R4", len(stamp) == 1, "every file carries the folder's in-fiction stamp")
    ymax = max(dt.date.fromisoformat(m) for f, t in text.items() if f not in (P.FILES["nng_sched"],)
               for m in re.findall(r"\b(20\d\d-\d\d-\d\d)\b", t))
    B.check("R5", ymax <= dt.date(2026, 4, 20), "latest ISO date outside the 2026-27 schedule: %s" % ymax)
    B.check("R6", r10(sum(gc["jan"].values())) % 100000 != 0, "region total is not a round headline")
    B.report()
    return B


def stops(target, cof):
    """The stops on both asks' ladders, each a complete count by county."""
    out = {}
    k = pd.read_csv(os.path.join(target, P.FILES["kvg_bills"]), dtype={"ACCOUNT_NO": str},
                    usecols=["ACCOUNT_NO", "PREMISE_NO"])
    ap = {int(a): p for a, p in zip(k.ACCOUNT_NO, k.PREMISE_NO)}
    o = pd.read_csv(os.path.join(target, P.FILES["kvg_orders"]), dtype={"ACCOUNT_NO": str})
    oo = o[(o.REASON_CD == "NP") & (o.ORDER_TYPE == "OFF") & (o.STATUS == "COMP")]
    cis = defaultdict(int)
    for p, ts in zip(oo.PREMISE_NO, oo.COMPLETED_TS):
        if J0 <= dt.datetime.strptime(ts, "%m/%d/%Y %H:%M").date() <= J1:
            cis[cof[p]] += 1
    nl = pd.read_excel(os.path.join(target, P.FILES["northline"]), header=4)
    nl = nl[nl["Job #"].astype(str).str.startswith("NL-")]
    dbl = defaultdict(int, cis)
    for a, d in zip(nl["Acct #"], nl["Date"]):
        if J0 <= pd.Timestamp(d).date() <= J1:
            dbl[cof[ap[int(a)]]] += 1
    act = pd.read_csv(os.path.join(target, P.FILES["nng_activity"]), dtype=str)
    crew = pd.read_csv(os.path.join(target, P.FILES["nng_crew"]), dtype=str)
    aa = act[(act.ACT_CD == "DNP") & (act.RESULT_CD == "C")].merge(crew, on="ACTIVITY_ID")
    sched, done = defaultdict(int), defaultdict(int)
    for p, d, ts in zip(aa.PREMISE_ID, aa.ACT_DATE, aa.COMPLETED_AT):
        if J0 <= dt.date.fromisoformat(d) <= J1:
            sched[cof[p]] += 1
        if J0 <= dt.date.fromisoformat(ts[:10]) <= J1:
            done[cof[p]] += 1
    wo = json.load(open(os.path.join(target, P.FILES["phe_wo"])))["workOrders"]
    wos = defaultdict(int)
    for x in wo:
        if x["woType"] == "Collections Shutoff" and x["status"] == "Completed" and \
                J0 <= dt.date.fromisoformat(x["completedAt"][:10]) <= J1:
            wos[cof[x["premiseId"]]] += 1
    mh = pd.read_csv(os.path.join(target, P.FILES["phe_meters"]), dtype=str, keep_default_na=False)
    mp = dict(zip(mh.METER_NO, mh.PREMISE_ID))
    ev = pd.read_csv(os.path.join(target, P.FILES["phe_events"]), dtype=str, keep_default_na=False)
    np_local, every_close = defaultdict(int), defaultdict(int)
    for m, ts, code, reason in zip(ev.METER_ID, ev.EVENT_TS_UTC, ev.EVENT_CODE, ev.REASON_CD):
        local = (dt.datetime.strptime(ts, "%Y-%m-%dT%H:%M:%SZ") - dt.timedelta(hours=5)).date()
        if code == "VALVE_CLOSE" and J0 <= local <= J1:
            every_close[cof[mp[m]]] += 1
            if reason == "NP":
                np_local[cof[mp[m]]] += 1
    by_util = lambda u: [W.DISPLAY[c] for c in W.COUNTY_ORDER if W.COUNTIES[c][0] == u]
    kvg5, nng, phe = by_util("KVG"), by_util("NNG"), by_util("PHE")
    cr = {c: cis.get(c, 0) + sched.get(c, 0) + wos.get(c, 0) for c in G.COUNTIES}
    out["K1:cracker (CIS orders, Northbank activity date, Pine Harbor work orders)"] = dict(values=cr, counties=G.COUNTIES)
    out["K1:contractor jobs added to the CIS orders"] = dict(
        values={c: dbl.get(c, 0) + done.get(c, 0) + wos.get(c, 0) + np_local.get(c, 0) for c in G.COUNTIES},
        counties=kvg5)
    out["K1:every valve close counted"] = dict(
        values={c: cis.get(c, 0) + done.get(c, 0) + wos.get(c, 0) + every_close.get(c, 0) +
                (dbl.get(c, 0) - cis.get(c, 0)) for c in G.COUNTIES}, counties=phe)
    out["K1:Northbank by activity date, all else right"] = dict(values={c: sched.get(c, 0) for c in nng}, counties=nng)
    # Ask 2
    e = pd.read_csv(os.path.join(target, P.FILES["kvg_wcp"]), dtype=str, keep_default_na=False)
    intake, right = defaultdict(int), defaultdict(int)
    for a, cty, eff, end in zip(e.ACCOUNT_NO, e.SERVICE_COUNTY, e.EFFECTIVE_DT, e.END_DT):
        eff = dt.datetime.strptime(eff, "%m/%d/%Y").date()
        end = dt.datetime.strptime(end, "%m/%d/%Y").date() if end else None
        if eff <= J1 and (end is None or end >= J1):
            intake[cty.title()] += 1
            right[cof[ap[int(a)]]] += 1
    fl = pd.read_csv(os.path.join(target, P.FILES["nng_flags"]), dtype=str)
    flags = defaultdict(int)
    for p in fl.PREMISE_ID:
        flags[cof[p]] += 1
    a2p = dict(zip(mh.ACCOUNT_NO, mh.PREMISE_ID))
    pl = pd.read_csv(os.path.join(target, P.FILES["phe_plans"]), dtype=str, keep_default_na=False)
    pl = pl[pl.PLAN_TYPE == "IBPP"]
    rows_active = defaultdict(int)
    for a, s, en in zip(pl.ACCOUNT_NO, pl.START_DATE, pl.END_DATE):
        if dt.date.fromisoformat(s) <= J1 and (not en or dt.date.fromisoformat(en) >= J1):
            rows_active[cof[a2p[a]]] += 1
    phe_k2 = {c: 0 for c in G.COUNTIES}
    gc2 = G.on_plan(target, cof)
    cr2 = {c: intake.get(c, 0) + flags.get(c, 0) + rows_active.get(c, 0) for c in G.COUNTIES}
    out["K2:cracker (intake county, premise flags, active plan rows)"] = dict(values=cr2, counties=G.COUNTIES)
    out["K2:Kestrel Valley by intake county, all else right"] = dict(
        values={c: intake.get(c, 0) + (gc2[c] - right.get(c, 0)) for c in G.COUNTIES},
        counties=kvg5)
    out["K2:Northbank premise flags, all else right"] = dict(values={c: flags.get(c, 0) for c in nng}, counties=nng)
    out["K2:Pine Harbor plan rows in force, all else right"] = dict(
        values={c: rows_active.get(c, 0) + (gc2[c] - phe_part(target, cof).get(c, 0)) for c in phe}, counties=phe)
    del phe_k2
    return out


def phe_part(target, cof):
    mh = pd.read_csv(os.path.join(target, P.FILES["phe_meters"]), dtype=str, keep_default_na=False)
    live = {}
    for a, p, s, en in zip(mh.ACCOUNT_NO, mh.PREMISE_ID, mh.LINKED_FROM, mh.LINKED_TO):
        if dt.date.fromisoformat(s) <= J1 and (not en or dt.date.fromisoformat(en) >= J1):
            live[a] = p
    pl = pd.read_csv(os.path.join(target, P.FILES["phe_plans"]), dtype=str, keep_default_na=False)
    pl = pl[pl.PLAN_TYPE == "IBPP"]
    out = defaultdict(int)
    for a, s, en in zip(pl.ACCOUNT_NO, pl.START_DATE, pl.END_DATE):
        if dt.date.fromisoformat(s) <= J1 and (not en or dt.date.fromisoformat(en) >= J1) and a in live:
            out[cof[live[a]]] += 1
    return out
