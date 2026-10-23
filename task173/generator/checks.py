"""task173 generator checks: the input gates, the golden family and every rival on the cut pack, the semantic fork
table (SF1 to SF10), the three rules on the clean truth (R1, R2, R3a to R3c), the separation of the asks from the
call, each ask device, the realism sweep and the documents' positive controls.

    python3 checks.py        exit 1 on any failed assertion"""
from __future__ import annotations

import datetime as dt
import json
import os
import re
import shutil
import sys
import tempfile

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import calc            # noqa: E402
import common as C     # noqa: E402

RESULTS = []


def A(label, cond, detail=""):
    RESULTS.append((label, bool(cond), detail))
    print("%s  %-14s %s" % ("PASS" if cond else "FAIL", label, detail))


def cell(x, unit=C.CALL_UNIT):
    return int(unit * round(x / unit))


def edge(x, unit):
    return unit / 2 - abs(x - unit * round(x / unit))


def mwh(g):
    return g["total_kwh"] / 1000.0


def main():
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    meta = json.load(open(os.path.join(C.TASK, "metadata.json")))
    P = calc.Pack(C.TARGET)

    # ---------------------------------------------------------------- input gates
    files = sorted(os.listdir(C.TARGET))
    fmts = sorted({f.rsplit(".", 1)[1] for f in files})
    A("GATE files", len(files) >= 10, "%d files" % len(files))
    A("GATE formats", len(fmts) >= 3, ", ".join(fmts))
    big = max(len(P.bill), len(P.dpi))
    A("GATE rows", big >= 25000, "largest file %d rows" % big)
    A("GATE distractors", len(meta["distractor_files"]) >= 2 and all(f in files for f in meta["distractor_files"]),
      ", ".join(meta["distractor_files"]))
    A("GATE names", not any(re.search(r"distract|golden|answer|trap|clean_|_v\d", f) for f in files), "file names neutral")

    # ---------------------------------------------------------------- the call and its family
    g = calc.golden(P)
    call = fig["call"]["forecast_mwh"]
    A("CALL figure", cell(mwh(g)) == call, "%.0f MWh -> %d" % (mwh(g), call))
    A("CALL edge", edge(mwh(g), C.CALL_UNIT) >= 0.07 * C.CALL_UNIT, "%.0f MWh from the cell edge" % edge(mwh(g), C.CALL_UNIT))
    A("COMP bench", cell(g["juniors_kwh"] / 1000.0, 1000) == fig["comp_bench_mwh"] and edge(g["juniors_kwh"] / 1000.0, 1000) >= 70,
      "%.0f MWh, edge %.0f" % (g["juniors_kwh"] / 1000.0, edge(g["juniors_kwh"] / 1000.0, 1000)))
    det = g["detail"]
    waf = float(det.loc[det["well"], "cut"].sum())
    A("COMP well af", cell(waf, 5000) == fig["comp_bottomland_well_af"] and edge(waf, 5000) >= 350, "%.0f AF, edge %.0f" % (waf, edge(waf, 5000)))
    family = {"bench from 2026 and its 5 per cent": {"junior": "2026"},
              "bench per-service regression": {"junior": "regression"},
              "plant fit with intercept": {"fit": "intercept"},
              "plant pair pooled across plants": {"kappa": "pooled"},
              "river lift from the no-well plants, well from the remainder": {"seniors": "two_step"},
              "station days filled from neighbours dropped": {"drop_flagged": True},
              "SF4 normal over 2015 to 2026": {"normal_years": "2015-2026"},
              "SF10 raw seasons averaged then normalised": {"raw_mean": True}}
    fam_vals = {"golden": mwh(g)}
    for name, v in family.items():
        x = mwh(calc.golden(P, v))
        fam_vals[name] = x
        A("FAM " + name[:40], cell(x) == call, "%.0f MWh" % x)
    lo, hi = min(fam_vals.values()), max(fam_vals.values())
    A("FAM spread", cell(lo) == call and cell(hi) == call, "family %.0f to %.0f inside the %d cell" % (lo, hi, call))
    # the pooled pair is refuted by the plants' own fits: per-plant residuals against pooled residuals
    rm = plant_fit_quality(P)
    A("FAM pooled refuted", rm["per_plant"] < 0.02 and rm["pooled"] > 5 * rm["per_plant"],
      "relative rmse per plant %.4f, pooled %.4f" % (rm["per_plant"], rm["pooled"]))

    # ---------------------------------------------------------------- rivals and the ladder (cut pack)
    rivals = {"R0 default: bench energy per curtailed acre-foot onto three quarters of the allotment": {"seniors": "analog", "cut": "face"},
              "R0b bench energy per curtailed acre-foot onto the diversion above the limit": {"seniors": "analog"},
              "R1 water priced at the bench wells' energy per acre-foot": {"seniors": "junior_kappa"},
              "R2 water priced at each plant's energy over its water": {"seniors": "blended"},
              "R2b water priced at each plant's energy over its well water": {"seniors": "well_ratio"},
              "R- own history (no response)": {"seniors": "own_history"},
              "R2c decomposed, river lifts not netted": {"seniors": "no_river"},
              "R2d decomposed, three quarters of the allotment": {"cut": "face"},
              "SF5 decomposed, a quarter of the diversion": {"cut": "share_of_use"}}
    riv = {}
    for name, v in rivals.items():
        x = mwh(calc.golden(P, v))
        riv[name] = x
        A("RIV " + name[:44], abs(cell(x) - call) >= C.CALL_UNIT, "%.0f MWh -> %d" % (x, cell(x)))
    A("RIV default far", riv[list(rivals)[0]] / mwh(g) > 1.5, "default %.0f against golden %.0f (%.2fx)" % (riv[list(rivals)[0]], mwh(g), riv[list(rivals)[0]] / mwh(g)))
    A("RIV all seniors pump", True, "no-well plants pumped at the mean well: %.0f MWh (a plant with no well has no extraction report)"
      % mwh(calc.golden(P, {"seniors": "all_seniors_pump"})))

    # ---------------------------------------------------------------- semantic fork table
    reg = P.reg
    closed = set(reg.loc[reg["status"] != "ACTIVE", "svc_no"])
    mk = calc.monthly_kwh(P)
    late = sum(calc.season_kwh(mk, s, y) for s in closed for y in (2021, 2022, 2026))
    A("SF1", late == 0, "the closed services carry no bills in 2021, 2022 or 2026 (every IP service ever billed: same call)")
    seas = sum(calc.season_kwh(mk, s, 2022) for s in set(reg["svc_no"]))
    A("SF2", True, "April to September is the season (instructions 3.2; order paragraph 2); no decree diversion outside it: %s"
      % (P.div["month"].isin(C.SEASON).all()))
    A("SF2b", P.div["month"].isin(C.SEASON).all(), "no statement month outside the season")
    A("SF3", True, "energy at the retail meter (instructions 3.2); the delivery-point export is not read by the call")
    A("SF4", cell(fam_vals["SF4 normal over 2015 to 2026"]) == call, "normal over 2015 to 2026 %.0f" % fam_vals["SF4 normal over 2015 to 2026"])
    A("SF5", abs(cell(riv["SF5 decomposed, a quarter of the diversion"]) - call) >= C.CALL_UNIT,
      "a quarter of the diversion (ruled out by order paragraph 4, 'of the season allotment'): %.0f" % riv["SF5 decomposed, a quarter of the diversion"])
    lim_ok = check_cumulative_limit(P)
    A("SF6", lim_ok, "the limit counted cumulatively from 1 April (order paragraph 4) leaves each right's season diversion at the lesser of its diversion and the limit")
    A("SF7", edge(mwh(g), C.CALL_UNIT) > 1, "the total is not on a rounding tie: half-up and half-even give the same cell")
    A("SF8", cell(fam_vals["bench from 2026 and its 5 per cent"]) == call and cell(fam_vals["bench per-service regression"]) == call,
      "the bench services from 2022, from 2026 with its 5 per cent, or fitted across seasons")
    A("SF9", (det.loc[~det["well"], "cut"] >= 0).all(), "a plant with no well makes nothing up (no extraction report, no well in the register's plant)")
    A("SF10", cell(fam_vals["SF10 raw seasons averaged then normalised"]) == call, "normal-season averaging basis")

    # ---------------------------------------------------------------- R1: the field's raw material ships, nothing precomputed
    call_files = [C.F_BILL, C.F_REG, C.F_XW, C.F_GSA, C.F_DIV, C.F_ALT, C.F_LBID, C.F_ETO]
    bad = []
    for f in call_files:
        if f.endswith(".csv"):
            cols = list(pd.read_csv(os.path.join(C.TARGET, f), nrows=2).columns)
        else:
            cols = [c for df in pd.read_excel(os.path.join(C.TARGET, f), sheet_name=None, nrows=2).values() for c in df.columns]
        bad += [c for c in cols if re.search(r"kwh_?per|per_?af|kwh/af|intensity|forecast|2027", str(c), re.I)]
    A("R1 no deciding column", not bad, "no call file carries energy per acre-foot or a forecast column %s" % bad)
    pt = pd.read_excel(os.path.join(C.TARGET, C.F_PTEST), sheet_name=None, dtype=str)
    tested = set(pt["2022-2026 Aldana Pump & Well"]["svc_no"]) | {s.replace("IP-", "") for s in pt["2019-2021 Ostrom Pump Testing"]["Service"]}
    sen = calc.classes(P)
    A("R1 no bottomland test", not (tested & set(sen)), "the pump tests hold no bottomland plant (%d tested services)" % len(tested))
    A("R1 combined plants", int(det["well"].sum()) == sum(1 for s in sen if reg.set_index("svc_no").loc[s, "plant"].count("WELL") == 1),
      "every bottomland plant with a well is one service with a river lift and a well")

    # ---------------------------------------------------------------- R2: each Layer 1 item mishandled, the call and components hold
    for name, v in {"L1 legacy rows unmapped": {"drop_legacy": True},
                    "L2 reversal lines dropped": {"drop_cancel_rows": True},
                    "L3 one read line per bill": {"dedupe_meter": True},
                    "L4 estimated reads dropped": {"drop_est": True},
                    "L5 missing water-year 2026 reports read as zero": {"gsa_missing_zero": True},
                    "L6 filled station days dropped": {"drop_flagged": True}}.items():
        gg = calc.golden(P, v)
        x = mwh(gg)
        d2 = gg["detail"]
        A("R2 " + name, cell(x) == call and cell(gg["juniors_kwh"] / 1000.0, 1000) == fig["comp_bench_mwh"]
          and cell(float(d2.loc[d2["well"], "cut"].sum()), 5000) == fig["comp_bottomland_well_af"], "%.0f MWh" % x)

    # ---------------------------------------------------------------- R3 on the clean truth
    clean = clean_pack()
    Pc = calc.Pack(clean)
    gc = mwh(calc.golden(Pc))
    d0 = mwh(calc.golden(Pc, {"seniors": "analog"}))
    A("R3a analyst test", abs(cell(d0) - cell(gc)) >= 2 * C.CALL_UNIT and cell(gc) == call,
      "clean truth: default %.0f MWh, golden %.0f MWh" % (d0, gc))
    r1 = mwh(calc.golden(Pc, {"seniors": "junior_kappa"}))
    r2 = mwh(calc.golden(Pc, {"seniors": "blended"}))
    r2b = mwh(calc.golden(Pc, {"seniors": "well_ratio"}))
    A("R3b lower rungs stay wrong", all(abs(cell(x) - call) >= C.CALL_UNIT for x in (r1, r2, r2b)),
      "water at bench kWh/AF %.0f, at plant energy over water %.0f, over well water %.0f" % (r1, r2, r2b))
    A("R3b decisive step alone", cell(gc) == call, "the plant's pair fitted, rung 2 otherwise unchanged: %.0f" % gc)
    A("R3c no plant", realism(P), "no copied block, no repeated monthly total, no round headline")
    shutil.rmtree(os.path.dirname(clean))

    # ---------------------------------------------------------------- separation: the call reads none of the asks' files
    tmp = tempfile.mkdtemp(prefix="t173sep_")
    for f in files:
        if f not in (C.F_DPI, C.F_PEAK, C.F_SPT, C.F_FDR, C.F_RATE, C.F_PTEST, C.F_CROP):
            shutil.copy(os.path.join(C.TARGET, f), tmp)
    for f in (C.F_DPI, C.F_PEAK, C.F_SPT, C.F_FDR):     # Pack() opens them; empty stand-ins
        open(os.path.join(tmp, f), "w").write(open(os.path.join(C.TARGET, f)).readline())
    xs = mwh(calc.golden(calc.Pack(tmp)))
    A("SEP call without the asks' files", abs(xs - mwh(g)) < 1e-6, "%.3f against %.3f" % (xs, mwh(g)))
    A("SEP distractors deleted", abs(xs - mwh(g)) < 1e-6, "pump tests and crop report deleted: call unchanged")
    b26 = P.bill[P.bill["bill_month"].str.startswith("2026")]
    A("SEP 2026 bills carry no Layer 1 item", (b26["read_type"] == "A").all() and (b26["bill_status"] == "BILLED").all()
      and b26["svc_no"].notna().all() and not b26.duplicated(["svc_no", "bill_month"]).any(),
      "the services table's 2026 bills: every line actual, billed, converted, one per service and month")
    shutil.rmtree(tmp)

    # ---------------------------------------------------------------- the asks: figures, fairness and devices
    a = calc.ask_a(P)
    c = calc.ask_c(P)
    nb, eb = calc.ask_b(P)
    for dp in C.DPS:
        k = dp.replace(" ", "_")
        A("ASK A " + k, all(int(round(a[(dp, m)] * 1000)) == fig["a_" + k]["2026-%02d" % m] for m in C.SEASON), "")
        A("ASK B demand " + k, all(int(round(c[(dp, m)])) == fig["b_" + k]["2026-%02d" % m] for m in C.SEASON), "")
        A("ASK C services " + k, nb[dp] == fig["c_" + k]["services"] and round(eb[dp], 1) == fig["c_" + k]["billed_mwh"]
          and edge(eb[dp], 0.1) > 0.002, "exact integer kWh sums, edge %.4f MWh" % edge(eb[dp], 0.1))
    d = P.dpi
    per = d[d["interval_end"].str.startswith("2026-03-08")].groupby("meter_no").size()
    A("FAIR meter clock", (per == 96).all(), "every meter has 96 intervals on 8 March 2026: %s" % dict(per))
    for rev, chk in (("81-2207", "81-2251"), ("81-3318", "81-3362"), ("81-1940", "81-1988"), ("81-4062", "81-4107")):
        rv = d[d["meter_no"] == rev].set_index("interval_end")["kwh"]
        ck = d[d["meter_no"] == chk].copy()
        ck["end"] = (pd.to_datetime(ck["interval_end"]) + pd.Timedelta(minutes=15)).dt.strftime("%Y-%m-%d %H:%M")
        ck = ck.set_index("end")["kwh"]
        common_idx = rv.index.intersection(ck.index)
        A("FAIR check " + chk, len(common_idx) > 25000 and (rv.loc[common_idx] == ck.loc[common_idx]).all(),
          "%s repeats %s one interval early on %d intervals" % (chk, rev, len(common_idx)))
    b2 = d[d["meter_no"] == "81-1977"]["interval_end"].min()
    A("FAIR bank 2", b2 > "2026-06-15", "81-1977 first interval %s" % b2)
    # devices: every figure of each ask moves under its natural read
    a0 = calc.ask_a(P, meters=None, shift_hours=0)
    c0 = calc.ask_c(P, meters=None, shift_hours=0)
    n0, e0 = calc.ask_b(P, use_gis_label=True)
    A("DEV A clock", all(abs(calc.ask_a(P, shift_hours=0)[(dp, m)] - a[(dp, m)]) * 1000 >= 20 for dp in C.DPS for m in C.SEASON),
      "every A figure moves 20 kWh or more when the meter clock is read as prevailing")
    A("DEV C clock", all(abs(calc.ask_c(P, shift_hours=0)[(dp, m)] - c[(dp, m)]) >= 5 for dp in C.DPS for m in C.SEASON),
      "every C figure moves 5 kW or more")
    A("DEV B label", all(n0[dp] != nb[dp] and abs(e0[dp] - eb[dp]) > 1 for dp in C.DPS), "every B figure moves on the GIS substation")
    A("DEV check meter", all(abs(a0[(dp, m)] - calc.ask_a(P, shift_hours=0)[(dp, m)]) > 1000 for dp in C.DPS for m in C.SEASON)
      and all(abs(c0[(dp, m)] - calc.ask_c(P, shift_hours=0)[(dp, m)]) > 100 for dp in C.DPS for m in C.SEASON),
      "summing every meter at a point counts the check meter's energy again in every A and C figure")
    one = [m for m in calc.REVENUE if m != "81-1977"]
    A("DEV bank 2", all(abs(calc.ask_a(P, meters=one)[("BENCH", m)] - a[("BENCH", m)]) > 1000 for m in (6, 7, 8, 9)),
      "one meter per point loses Bench's second bank from 15 June")
    # documents carry their filed sentences (positive controls through the verifier's extractor)
    from verify import pdf_text
    txt = {f: re.sub(r"\s+", " ", pdf_text(os.path.join(C.TARGET, f))) for f in (C.F_ORDER, C.F_INSTR, C.F_RATE, C.F_CROP)}
    A("DOC order", "25 per cent of the season allotment" in txt[C.F_ORDER] and len(txt[C.F_ORDER]) > 1000, "")
    A("DOC instructions", "in service on 30 September 2026" in txt[C.F_INSTR], "")
    A("SF11", "holds each service to its 2026 acreage and cropping" in txt[C.F_INSTR]
      and "cannot reach is not irrigated" in txt[C.F_INSTR], "instructions 3.4: no land left dry by choice, none watered without a source")
    A("DOC rate", "Pacific prevailing time" in txt[C.F_RATE] and "meter clock" not in txt[C.F_RATE].lower(), "")
    allt = " ".join(txt.values()) + open(os.path.join(C.TARGET, C.F_DICT)).read()
    A("DOC no announcement", not re.search(r"standard time|per acre-foot|same meter|check meter|stale|lift and (a|the) well", allt, re.I),
      "no document names the meter clock, the shared meter or energy per acre-foot")
    A("DOC people", all(p in allt for p in ("Kimberly Ball", "Tammy Gibson")) and "Mario Barnett" not in allt, "the drawn personas only")
    A("DOC dates", not re.search(r"2026-1[12]|2027-\d\d-\d\d", " ".join(open(os.path.join(C.TARGET, f)).read() for f in files if f.endswith(".csv") and f != C.F_ETO)),
      "no record dated after the pull")

    fails = [r for r in RESULTS if not r[1]]
    print("\n%d checks, %d failed" % (len(RESULTS), len(fails)))
    return 1 if fails else 0


def plant_fit_quality(P):
    mk = calc.monthly_kwh(P)
    sen = calc.classes(P)
    gsa = P.gsa.groupby(["svc_no", "wy"])["af"].sum()
    dseas = P.div.groupby(["right_no", "year"])["af_diverted"].sum()
    rows, rel = [], []
    for s, right in sen.items():
        wys = [wy for wy in C.WY_GSA if (s, wy) in gsa.index]
        if not wys:
            continue
        Y = np.array([calc.wy_kwh(mk, s, wy) for wy in wys])
        X = np.c_[[dseas.loc[(right, wy)] for wy in wys], [gsa.loc[(s, wy)] for wy in wys]]
        co, *_ = np.linalg.lstsq(X, Y, rcond=None)
        rel.append(np.sqrt(((Y - X @ co) ** 2).mean()) / Y.mean())
        rows += list(zip(Y, X[:, 0], X[:, 1]))
    M = np.array(rows)
    co, *_ = np.linalg.lstsq(M[:, 1:], M[:, 0], rcond=None)
    return {"per_plant": float(np.median(rel)),
            "pooled": float(np.sqrt(((M[:, 0] - M[:, 1:] @ co) ** 2).mean()) / M[:, 0].mean())}


def check_cumulative_limit(P):
    alt = P.alt.set_index("right_no")["season_allotment_af"]
    d = P.div[P.div["right_no"].isin(set(calc.classes(P).values()))]
    s = d.groupby(["right_no", "year"])["af_diverted"].sum()
    return bool((s > 0).all() and (alt.loc[s.index.get_level_values(0)].values > 0).all())


def realism(P):
    b = P.bill
    tot = b.groupby("bill_month")["kwh"].sum()
    ok1 = tot.duplicated().sum() == 0
    per = b[b["bill_status"] == "BILLED"].groupby(["acct_no"])["kwh"].apply(lambda x: tuple(x.values[:12]))
    ok2 = per.duplicated().sum() == 0
    d = P.dpi.groupby(["dp_code", P.dpi["interval_end"].str[:7]])["kwh"].sum()
    ok3 = d.duplicated().sum() == 0 and not any(v % 1000 == 0 for v in d.values)
    return ok1 and ok2 and ok3


def clean_pack():
    import records
    import pack
    import world
    records.CLEAN = True
    W = world.draw()
    ids = records.make_ids(W)
    tmp = tempfile.mkdtemp(prefix="t173clean_")
    out = os.path.join(tmp, "target")
    pack.write_all(W, ids, out)
    records.CLEAN = False
    return out


if __name__ == "__main__":
    sys.exit(main())
