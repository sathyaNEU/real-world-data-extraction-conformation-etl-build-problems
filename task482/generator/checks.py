"""task482 architecture 16: the generator's checks on the built pack (python3 task482/generator/checks.py).

The world's truth against the golden, the ladder (R0, R1, R1b, the decisive R2), every semantic fork of the design
note's table (SF1 to SF14) converging on the golden's call, the asks' devices and margins, and the input gates."""
import datetime as dt
import json
import os
import re
import sys
import zipfile

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
T = os.path.join(TASK, "target")
sys.path.insert(0, HERE)
import golden as G   # noqa: E402
import params as P   # noqa: E402
import world as W    # noqa: E402

FAILS = []
N = [0]


def check(name, ok, detail=""):
    N[0] += 1
    print("%s %-64s %s" % ("PASS" if ok else "FAIL", name, detail))
    if not ok:
        FAILS.append(name)


def call_of(d, fam):
    prem, earn = G.premium(fam, d["calloff"])
    return prem, tuple(earn)


def main():
    res = G.solve(T)
    d, fam, beta = res["d"], res["fam"], res["beta"]
    golden_call = (res["premium"], tuple(res["earning"]))
    w = W.simulate()
    truth = W.family_truth(w)

    # ------------------------------------------------------------------ the world against the golden
    check("C1 the golden's call is the world's", golden_call == call_of(d, {f: dict(intensity=truth[f])
                                                                         for f in G.FAMILIES}),
          "golden %s, truth %s" % (golden_call, {f: round(truth[f], 4) for f in G.FAMILIES}))
    check("C2 golden intensities within 0.003 of the truth for the billet and the ingot",
          all(abs(fam[f]["intensity"] - truth[f]) < 0.003 for f in ("BIL6063", "BIL6082", "INGLM25")),
          str({f: round(fam[f]["intensity"] - truth[f], 4) for f in G.FAMILIES}))
    check("C3 the regression reads the processes' own rates within 5 per cent",
          abs(beta["melt"] / P.MELT_KWH_PER_T - 1) < 0.05 and abs(beta["h1"] / P.H1_KW - 1) < 0.05 and
          abs(beta["m3"] / P.M3_KWH_PER_T - 1) < 0.05 and abs(beta["t1"] / P.T1_KW - 1) < 0.08,
          "melt %.0f, H1 %.0f, M3 %.0f, T1 %.0f; R2 %.4f" % (beta["melt"], beta["h1"], beta["m3"], beta["t1"],
                                                             res["r2"]))
    prod_truth = w["truth"]["produced"]
    check("C4 production read from the lots is the world's (last result, passed)",
          all(abs(d["prod"][f] - prod_truth[f]) < 0.6 for f in G.FAMILIES),
          str({f: round(d["prod"][f] - prod_truth[f], 3) for f in G.FAMILIES}))
    check("C5 the metered energy is the world's within 0.05 per cent",
          abs(d["kwh"].sum() / w["truth"]["metered_kwh"] - 1) < 5e-4,
          "%.0f against %.0f kWh" % (d["kwh"].sum(), w["truth"]["metered_kwh"]))

    # ------------------------------------------------------------------ the ladder
    m = G.mass_allocation(d)
    r0 = call_of(d, m)
    check("C6 R0 (mass allocation) puts every family under the limit and pays 480,700", r0[0] == 480700,
          "%s at %.4f" % (r0, m["BIL6063"]["intensity"]))
    y, x = res["y"], res["x"]
    r1, _ = G.attribute(d, beta, h1="tonnes")
    check("C7 R1 (the homogenizing furnace's gas shared by tonnes) pays 456,000", call_of(d, r1)[0] == 456000,
          "%s, 6082 at %.4f" % (call_of(d, r1), r1["BIL6082"]["intensity"]))
    b1b, _ = G.fit(y, x, ("melt", "m3", "h1_t", "t1"))
    r1b, _ = G.attribute(d, b1b, h1="tonnes", h1_driver="h1_t")
    check("C8 R1b (a tonnes regressor for the furnace) pays 456,000", call_of(d, r1b)[0] == 456000,
          "%s, 6082 at %.4f" % (call_of(d, r1b), r1b["BIL6082"]["intensity"]))
    check("C9 R2 (decisive: the furnace by its loads' hours) is the golden at 342,000",
          golden_call == (342000, ("BIL6063", "INGLM25")), str(golden_call))
    check("C10 6082 is the family the decisive step moves (under in R1, over in R2)",
          r1["BIL6082"]["intensity"] <= G.LIMIT < fam["BIL6082"]["intensity"],
          "%.4f against %.4f" % (r1["BIL6082"]["intensity"], fam["BIL6082"]["intensity"]))
    check("C11 no family within 0.015 of the limit on the golden",
          min(abs(fam[f]["intensity"] - G.LIMIT) for f in G.FAMILIES) > 0.015,
          str({f: round(fam[f]["intensity"] - G.LIMIT, 4) for f in G.FAMILIES}))

    # ------------------------------------------------------------------ the semantic forks, each converging on the call
    def same(name, fam2, detail=""):
        c = call_of(d, fam2)
        check(name, c == golden_call, "%s %s" % (c, detail))

    # SF1 the local year against the UTC year: UTC days
    dd = dict(d)
    yu = np.zeros(365)
    for t, k in zip(d["starts"], d["kwh"]):
        yu[(t.date() - dt.date(2026, 1, 1)).days] += k
    bu, _ = G.fit(yu, x)
    same("SF1 days and the year read in UTC give the same call", G.attribute(d, bu)[0])
    # SF2 electricity is not fuel the works burned (SCR-2 section 2); the requirement's own words
    scr2 = open(os.path.join(T, P.FILES["scr2"]), "rb").read()
    import pdfplumber
    txt = " ".join((p.extract_text() or "") for p in pdfplumber.open(os.path.join(T, P.FILES["scr2"])).pages)
    txt = re.sub(r"\s+", " ", txt)
    check("SF2 SCR-2 files the fuel the works burned and natural gas at its billed energy",
          "fuel the works burned" in txt and "Natural gas is taken at the energy the gas supplier billed" in txt
          and len(scr2) > 0, "section 2 and section 4")
    # SF3 one average calorific value for the year
    cv_bar = float(np.mean([p["cv"] for p in d["per"]]))
    dd3 = dict(d)
    k = 0
    kk = np.array(d["kwh"])
    for i, t in enumerate(d["starts"]):
        while not (d["per"][k]["a"] <= t < d["per"][k]["b"]):
            k += 1
        kk[i] = kk[i] * cv_bar / d["per"][k]["cv"]
    dd3["kwh"] = kk
    y3 = np.zeros(365)
    for t, v in zip(d["starts"], kk):
        y3[G.DAY_INDEX[G.local_date(t)]] += v
    b3, _ = G.fit(y3, x)
    same("SF3 one average calorific value gives the same call", G.attribute(dd3, b3)[0])
    # SF4 the exact imperial factor against the bill's 2.83
    ex = W.utc(P.METER_EXCHANGE_LOCAL)
    dd4 = dict(d)
    dd4["kwh"] = np.array([v * (2.831685 / 2.83 if t < ex else 1.0) for t, v in zip(d["starts"], d["kwh"])])
    y4 = np.zeros(365)
    for t, v in zip(d["starts"], dd4["kwh"]):
        y4[G.DAY_INDEX[G.local_date(t)]] += v
    b4, _ = G.fit(y4, x)
    same("SF4 hundreds of cubic feet at 2.831685 give the same call", G.attribute(dd4, b4)[0])
    # SF5 production at the first result, and every inspected tonne
    import csv
    first, every = {}, {f: 0.0 for f in G.FAMILIES}
    seen = set()
    for r in csv.DictReader(open(os.path.join(T, P.FILES["lots"]), encoding="utf-8")):
        fam_ = G.PRODUCT[r["Product"]]
        if r["Lot"] not in seen:
            seen.add(r["Lot"])
            every[fam_] += int(r["Net kg"]) / 1000.0
            first[r["Lot"]] = (fam_, r["Result"], int(r["Net kg"]) / 1000.0)
    p_first = {f: 0.0 for f in G.FAMILIES}
    for fam_, res_, t_ in first.values():
        if res_ == "PASS":
            p_first[fam_] += t_
    for label, prod in (("first result", p_first), ("every lot inspected", every)):
        dd5 = dict(d)
        dd5["prod"] = prod
        same("SF5 production at the %s gives the same call" % label, G.attribute(dd5, beta)[0])
    # SF6 the gas burned on rejected lots taken out of the families' numerators (pro rata to the tonnes rejected)
    rej = {f: every[f] - d["prod"][f] for f in G.FAMILIES}
    fam6 = {}
    for f in G.FAMILIES:
        share = d["prod"][f] / (d["prod"][f] + rej[f])
        fam6[f] = dict(intensity=fam[f]["intensity"] * share)
    same("SF6 rejected lots' gas removed from the numerator gives the same call", fam6)
    # SF7 pilot flames while a process runs counted to the processes by their running hours
    fam7 = {}
    base_pilot = beta["const"] * 365
    run_h = {"BIL6063": 0.0, "BIL6082": 0.0, "INGLM25": 0.0, "CSTLM25": 0.0}
    for h in d["heats"]:
        run_h[h["family"]] += (h["b"] - h["a"]).total_seconds() / 3600.0
    for ld in d["h1"]:
        run_h[ld["family"]] += (ld["b"] - ld["a"]).total_seconds() / 3600.0
    run_h["CSTLM25"] += sum((b["b"] - b["a"]).total_seconds() / 3600.0 for b in d["t1"])
    tot_h = sum(run_h.values())
    allp = sum(d["prod"].values())
    for f in G.FAMILIES:
        kwh = fam[f]["kwh"] - base_pilot * d["prod"][f] / allp + base_pilot * run_h[f] / tot_h
        fam7[f] = dict(intensity=kwh * G.CO2 / 1000.0 / d["prod"][f])
    same("SF7 pilot gas counted to the processes by running hours gives the same call", fam7)
    # SF8 heating degree days on 18 C, on 14 C, and none
    for base in (18.0, 14.0):
        yb, xb = G.daily(d, hdd_base=base)
        bb, _ = G.fit(yb, xb)
        same("SF8 heating degree days on %.0f C give the same call" % base, G.attribute(d, bb)[0])
    bn, _ = G.fit(y, x, hdd=False)
    same("SF8 no heating term gives the same call", G.attribute(d, bn)[0])
    # SF9 the regression's grain: weekly, and the days a process ran
    n = 364 // 7
    yw = y[:n * 7].reshape(n, 7).sum(1)
    xw = {k_: v[:n * 7].reshape(n, 7).sum(1) for k_, v in x.items()}
    bw, _ = G.fit(yw, xw)
    same("SF9 a weekly regression gives the same call", G.attribute(d, bw)[0])
    mask = (x["melt"] + x["m3"] + x["h1"] + x["t1"]) > 0
    bm, _ = G.fit(y[mask], {k_: v[mask] for k_, v in x.items()})
    same("SF9 the days a process ran give the same call", G.attribute(d, bm)[0])
    # SF10 melting gas spread by tonnes produced
    same("SF10 melting by tonnes produced gives the same call", G.attribute(d, beta, melt="produced")[0])
    # SF11 the re-keyed heats kept
    import openpyxl
    wb = openpyxl.load_workbook(os.path.join(T, P.FILES["furnaces"]), read_only=True, data_only=True)
    heats_all = []
    for sheet in ("M1 casthouse", "M2 casthouse"):
        for r in list(wb[sheet].iter_rows(values_only=True))[1:]:
            heats_all.append(dict(furnace=sheet[:2], heat=r[0], family=G.ALLOY[str(r[1])], a=G.to_utc(r[2]),
                                  b=G.to_utc(r[3]), t=float(r[4]), lot=r[5]))
    dups = len(heats_all) - len(d["heats"])
    dd11 = dict(d)
    dd11["heats"] = heats_all
    y11, x11 = G.daily(dd11)
    b11, _ = G.fit(y11, x11)
    same("SF11 the re-keyed heats kept give the same call", G.attribute(dd11, b11)[0], "(%d re-keyed rows)" % dups)
    check("SF11 the furnace logs carry re-keyed heats", dups > 10, "%d rows" % dups)
    # SF12 the call-offs: the months summed equal the schedule's totals (asserted in golden.read_calloffs)
    check("SF12 the call-offs read from the schedule are SCR-2's tonnes",
          d["calloff"] == P.CALLOFF_2027, str(d["calloff"]))
    # SF13 the limit read inclusive or exclusive: no family on it
    check("SF13 at or under the limit, or under it: no family on 0.235",
          all(abs(fam[f]["intensity"] - G.LIMIT) > 1e-3 for f in G.FAMILIES), "")
    # SF14 firing hours read as naive local differences
    dd14 = dict(d)
    dd14["h1"] = [dict(ld, b=ld["a"] + ((ld["b"].astimezone(G.LON).replace(tzinfo=None) -
                                          ld["a"].astimezone(G.LON).replace(tzinfo=None)))) for ld in d["h1"]]
    same("SF14 hours from the logs' local stamps unconverted give the same call", G.attribute(dd14, beta)[0])

    # ------------------------------------------------------------------ the asks
    built = __import__("build")
    visits = None
    try:
        visits = built.weighbridge(w, os.devnull, os.devnull)
    except Exception as e:  # pragma: no cover
        check("A0 the weighbridge truth regenerates", False, repr(e))
    if visits is not None:
        truth_a = {g: {q: 0.0 for q in G.QUARTERS} for g in G.GRADES}
        truth_b = {q: 0.0 for q in G.QUARTERS}
        orders_ok = True
        for v in visits:
            q = G.quarter(v["day"])
            ws = v["weights"]
            if v["kind"] == "scrap1" and v["lines"][0]["status"] == "Accepted":
                truth_a[v["lines"][0]["grade"]][q] += (ws[0] - ws[-1]) / 1000.0
            elif v["kind"] == "scrap2":
                for k_, gg in enumerate(v["order"]):
                    truth_a[gg][q] += (ws[k_] - ws[k_ + 1]) / 1000.0
                big = max(v["lines"], key=lambda ln: ln["actual"])
                small = min(v["lines"], key=lambda ln: ln["actual"])
                orders_ok &= big["declared"] > small["declared"]
            elif v["kind"] in ("dross1", "dross2"):
                truth_b[q] += (ws[-1] - ws[-2]) / 1000.0
        check("A1 ask A (scrap by grade and quarter) is the weighbridge's truth to the kilogram",
              all(abs(res["ask_a"][g][q] - truth_a[g][q]) < 1e-6 for g in G.GRADES for q in G.QUARTERS), "")
        check("A2 every two-grade note declares its bigger tip bigger (the match is forced)", orders_ok, "")
        check("A3 ask B (dross by quarter) is the weighbridge's truth", all(abs(res["ask_b"][q] - truth_b[q]) < 1e-6
                                                                           for q in G.QUARTERS), "")
        n2 = sum(1 for v in visits if v["kind"] == "scrap2")
        n1 = sum(1 for v in visits if v["kind"] == "scrap1")
        nd2 = sum(1 for v in visits if v["kind"] == "dross2")
        nd = sum(1 for v in visits if v["kind"] in ("dross1", "dross2"))
        check("A4 two-grade loads are a quarter or more of deliveries", n2 / float(n1 + n2) > 0.2,
              "%d of %d" % (n2, n1 + n2))
        check("A5 a third or more of the dross lifts first unload returned metal", nd2 / float(nd) > 0.25,
              "%d of %d" % (nd2, nd))
        resets = [v for v in visits if v["day"] >= P.WB_RESET]
        check("A6 the weighbridge's tickets restart at 1 on the new indicator", resets and resets[0]["ticket"] == 1,
              "first ticket after %s is %d" % (P.WB_RESET, resets[0]["ticket"]))
    a_dec = G.scrap(T, split="declared")
    kept_a = sum(1 for g in G.GRADES for q in G.QUARTERS if round(a_dec[g][q]) == round(res["ask_a"][g][q]))
    b_fl = G.dross(T, combined="first_last")
    kept_b = sum(1 for q in G.QUARTERS if round(b_fl[q]) == round(res["ask_b"][q]))
    check("A7 the cracker's route (declared split, first and last weighing) misses ask A", kept_a <= 3,
          "keeps %d of 16" % kept_a)
    check("A8 the cracker's route misses ask B", kept_b == 0, "keeps %d of 4" % kept_b)
    vals = [res["ask_a"][g][q] for g in G.GRADES for q in G.QUARTERS] + [res["ask_b"][q] for q in G.QUARTERS]
    check("A9 no ask figure on an exact half tonne", all(abs((v % 1.0) - 0.5) > 0.011 for v in vals),
          "closest %.3f" % min(abs((v % 1.0) - 0.5) for v in vals))

    # ------------------------------------------------------------------ the input gates and the files
    names = sorted(os.listdir(T))
    exts = {n.rsplit(".", 1)[-1] for n in names}
    check("G1 ten or more files in three or more formats", len(names) >= 10 and len(exts) >= 3,
          "%d files, %s" % (len(names), sorted(exts)))
    big = max(sum(1 for _ in open(os.path.join(T, n), encoding="utf-8")) - 1 for n in names if n.endswith(".csv"))
    check("G2 a file of 25,000 rows or more", big >= 25000, "%d rows" % big)
    meta = json.load(open(os.path.join(TASK, "metadata.json")))
    check("G3 two or more named distractors, none named in a file name as one",
          len(meta["distractors"]) >= 2 and all("distract" not in n for n in names), str(meta["distractors"]))
    check("G4 every file has a source, a date and a licence in metadata.json",
          sorted(f["name"] for f in meta["files"]) == names and all(f.get("source") and f.get("date") and
                                                                    f.get("license") for f in meta["files"]), "")
    dash = []
    for n in names:
        b = open(os.path.join(T, n), "rb").read()
        if n.endswith((".xlsx", ".docx")):
            b = b"".join(zipfile.ZipFile(os.path.join(T, n)).read(i) for i in zipfile.ZipFile(os.path.join(T, n))
                         .namelist())
        if chr(0x2014).encode() in b:
            dash.append(n)
    check("G5 no em dash in any file", not dash, str(dash))
    stamps = {}
    for n in names:
        if n.endswith(".pdf"):
            m_ = re.findall(rb"/CreationDate\s*\((D:[^)]*)\)", open(os.path.join(T, n), "rb").read())
            stamps[n] = m_[0] if m_ else b""
        if n.endswith(".xlsx"):
            core = zipfile.ZipFile(os.path.join(T, n)).read("docProps/core.xml")
            stamps[n] = re.findall(rb"<dcterms:created[^>]*>([^<]*)<", core)[0]
    check("G6 every workbook and PDF carries its own creation stamp", len(set(stamps.values())) == len(stamps),
          str({k: v.decode() for k, v in stamps.items()}))
    lic = [n for n in names if "lorem" in open(os.path.join(T, n), "rb").read().decode("latin-1").lower()]
    check("G7 no placeholder text", not lic, str(lic))
    after = []
    for n in names:
        if n.endswith(".csv"):
            for line in open(os.path.join(T, n), encoding="utf-8"):
                if re.search(r"\b2027-0[2-9]|\b2027-1|/0[2-9]/2027|/1[0-2]/2027", line):
                    after.append(n)
                    break
    check("G8 no record dated after the package's January 2027", not after, str(after))

    print("%d checks, %d failed" % (N[0], len(FAILS)))
    return 1 if FAILS else 0


if __name__ == "__main__":
    sys.exit(main())
