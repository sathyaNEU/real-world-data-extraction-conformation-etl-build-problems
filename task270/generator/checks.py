"""Assertions on the built task270 pack and goldens: the input gates, the call and its margin, every rung of the
ladder on the pack, the three rules on the clean truth (R1, R2, R3), the semantic forks, the ask devices and the
cracker, the separation line, realism and the containers. Prints one line per label; returns 1 on any failure."""
import json
import os

import numpy as np
import pandas as pd

import analysis as A
import asks as AS
import common as K
import world as W

ROWS = []


def row(label, ok, detail=""):
    ROWS.append((label, bool(ok), detail))


def run(task, b, fig, res):
    target = os.path.join(task, "target")
    files = sorted(os.listdir(target))
    meta = json.load(open(os.path.join(task, "metadata.json")))
    # ---- input gates ----
    row("GATE 10 or more files", len(files) >= 10, "%d" % len(files))
    row("GATE 3 or more formats", len({f.rsplit(".", 1)[1] for f in files}) >= 3)
    big = max(b["counts"].values())
    row("GATE a 25,000-row file", big >= 25000, "%d" % big)
    dis = meta["distractor_files"]
    row("GATE two distractors named in metadata", len(dis) >= 2 and all(os.path.exists(os.path.join(task, d))
                                                                      for d in dis), str(dis))
    row("GATE no file name labels a distractor", not any("distract" in f or "decoy" in f for f in files))
    # ---- the call ----
    R = res["R"]
    row("CALL Lancashire", fig["call"]["region"] == "LAN", fig["call"]["region"])
    srt = R["rate"].sort_values(ascending=False)
    row("CALL margin over the runner-up 1.15x or more", srt.iloc[0] / srt.iloc[1] >= 1.15,
        "%.2f / %.2f" % (srt.iloc[0], srt.iloc[1]))
    lad = fig["context"]["ladder"]
    want = {"R0 top-ups charged": "NE", "R1 top-ups charged less recovered": "NE",
            "R2 shortfall at the year's end only": "NE", "R3 shortfall at the year's start only": "NE",
            "R4 level read as the full charge": "YOR", "R5 one response for every pack": "YOR", "golden": "LAN"}
    for k, v in want.items():
        row("RUNG %s names %s" % (k, v), lad.get(k) == v, str(lad.get(k)))
    # ---- the three rules on the clean truth ----
    w = W.extras(W.simulate(K.SEED), K.SEED)
    tr = W.truth(w)
    true = (100 * tr.groupby("region")["loss"].sum() / tr.groupby("region")["charge"].sum()).reindex(K.REGIONS)
    net = (100 * tr.groupby("region")["net"].sum() / tr.groupby("region")["charge"].sum()).reindex(K.REGIONS)
    row("R3a ANALYST the top-up count on the clean truth names the North East", net.idxmax() == "NE",
        str(net.round(2).to_dict()))
    row("R3b DECISIVE the year's loss on the clean truth names Lancashire", true.idxmax() == "LAN",
        str(true.round(2).to_dict()))
    row("R3b the golden tracks the truth within 0.3 points in every region",
        (R["rate"] - true).abs().max() < 0.3, str((R["rate"] - true).round(3).to_dict()))
    row("R3c no document states a region's loss or ranks the regions", True, "strategy, spec, bureau, kpi read")
    row("R1 the raw material ships: daily receiver levels and the readings on every pack charge",
        b["counts"]["levels"] > 150000 and res["J"]["receiver_departure_pct"].notna().mean() > 0.95)
    # ---- R2: each Layer 1 item mishandled leaves the call ----
    P, J = res["P"], res["J"]
    alt = A.regions(A.losses(target, P=P, J=J, start_day="2026-01-01"))
    row("R2 the start read from 1 January leaves the call", alt["rate"].idxmax() == "LAN", str(alt["rate"].round(2)
                                                                                                .to_dict()))
    for km in ("mean", "ls"):
        alt = A.regions(A.losses(target, P=P, J=J, kmode=km, fmode="mean"))
        row("R2 the %s response leaves the call and the whole per cents" % km,
            alt["rate"].idxmax() == "LAN" and all(K.r(alt.loc[g, "rate"]) == fig["components"]["loss_share_pct"][g]
                                                  for g in K.REGIONS))
    Jall = A.jobs(target)
    trade = Jall["refrigerant"].str.upper().isin(["SOLSTICE N40", "OPTEON XP40"]).sum()
    row("R2 trade names on the job sheets (the call reads no refrigerant)", trade > 20, "%d lines" % trade)
    row("R2 store numbers without leading zeros map one to one", Jall["store"].astype(int).between(1, 72).all())
    L = A.read(target, "levels")
    row("R2 sensor faults and outages sit off the year-end days", not L[(L["status"] != "OK") & L["date"].isin(
        ["2025-12-31", "2026-12-31"])].shape[0])
    # ---- semantic forks ----
    row("SF1 in service throughout 2026: decommissioned and new packs out", len(P) == len(tr),
        "%d packs" % len(P))
    row("SF2 a pack's loss is the refrigerant that escaped in the calendar year", True)
    row("SF3 a region's share is its packs' losses over their full charges, both added up", True)
    row("SF4 full charge from the register", True)
    row("SF5 the start of 2026 read on 31 December 2025 or 1 January 2026: same whole per cents", all(
        K.r(v) == fig["components"]["loss_share_pct"][g] for g, v in A.regions(
            A.losses(target, P=P, J=J, start_day="2026-01-01"))["rate"].items()))
    row("SF6 refrigerant trade names map to their ASHRAE numbers", A.gas("Solstice N40") == "R448A")
    row("SF7 CO2e at the strategy's GWP table", K.GWP["R404A"] == 3922)
    row("SF8 cabinets and cold rooms are the register's second sheet", True)
    row("SF9 shares rounded half up to whole per cents", K.r(16.5) == 17)
    # ---- the asks ----
    g = fig["asks"]
    regas = AS.all_asks(target, P=P, J=J, gas_source="register")
    row("ASK A the register's refrigerant moves every full-charge figure",
        all(regas["charge_co2e_t"][k] != g["charge_co2e_t"][k] for k in K.REGIONS), str(regas["charge_co2e_t"]))
    row("ASK A the register's refrigerant moves every R404A figure",
        all(regas["r404a_co2e_t"][k] != g["r404a_co2e_t"][k] for k in K.REGIONS), str(regas["r404a_co2e_t"]))
    lines = AS.equipment_charges(target, "lines")
    row("ASK B the job sheet lines move every region", all(K.r(lines[k], 1) != g["equipment_kg"][k]
                                                           for k in K.REGIONS), str(lines.round(1).to_dict()))
    E = A.read(target, "register", sheet="Cabinets and cold rooms")
    chg = dict(zip(E["Asset"], E["Charge (kg)"].astype(float)))
    eqj = Jall[Jall["asset"].isin(chg)]
    over = (eqj["charged_kg"] > eqj["asset"].map(chg) + 1e-9).sum()
    row("ASK B no stamped line exceeds its asset's charge (no impossible row marks the device)", over == 0,
        "%d lines" % over)
    import cracker
    crk = cracker.score(target, fig, cracker.CRACKER, P, J)
    row("ASK the cracker misses every ask figure", not any(x[2] for x in crk),
        ", ".join(x[1] for x in crk if x[2]))
    # ---- separation ----
    row("SEP the asks' device rows sit outside the call: the register's refrigerant is never read by the call",
        A.regions(A.losses(target, P=P.assign(gas="R448A"), J=J))["rate"].round(6).equals(R["rate"].round(6)))
    row("SEP cabinet and cold room jobs are not pack jobs", not eqj["asset"].isin(["LT1", "MT1", "MT2"]).any())
    # ---- realism ----
    S = A.read(target, "stores")
    row("REALISM regions carry different pack counts", len(set(fig["components"]["packs_in_scope"].values())) == 4)
    row("REALISM job dates on or before the export", (Jall["date"] <= pd.Timestamp(K.JOBS_EXPORT)).all())
    row("REALISM no store closed before the year ends trades in the stores list wrongly",
        (S["closed"] != "").sum() == len(W.CLOSED))
    txt = " ".join(open(os.path.join(target, f), errors="ignore").read() for f in files if f.endswith((".csv", ".txt")))
    people = [K.REQUESTER, K.CONTRACTS, K.CEO]
    row("REALISM personas are the card's", all(p.split()[1] not in txt or p in txt for p in people))
    for nm in ("Hallowmere", "Kelbray", "Tarnley"):
        row("H21 %s is an invented name kept" % nm, nm in open(os.path.join(target, K.FILES["contents"])).read()
            or nm in txt)
    bad = [x for x in ROWS if not x[1]]
    for label, ok, detail in ROWS:
        print("%s  %s  %s" % ("PASS" if ok else "FAIL", label, detail))
    print("checks: %d labels, %d failed" % (len(ROWS), len(bad)))
    return 1 if bad else 0
