"""task160 checks: every figure the design note and the write-up stand on, asserted on the clean truth and on the cut
pack. Labels R1 to R3c are the client's three rules executed (dataset-generation 7.1); SF1 to SF10 the semantic fork
table; LADDER the rungs; C1 the convergence family; BIN the rounding edges; DEVICE the ask layer's separation."""
from __future__ import annotations

import collections
import datetime as dt
import json
import os
import re
import statistics as st
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import pdfplumber  # noqa: E402

import calc as K  # noqa: E402
import common as C  # noqa: E402
import pack_read as PR  # noqa: E402
import pack as PK  # noqa: E402
import docs as DOC  # noqa: E402

D = dt.date
RESULTS = []


def check(label, ok, detail=""):
    RESULTS.append((label, bool(ok), detail))


def edge(v, u=50):
    return u / 2.0 - abs(v - u * round(v / u))


def pdf_text(path):
    with pdfplumber.open(path) as pdf:
        return "\n".join(p.extract_text() or "" for p in pdf.pages)


def main(pack=None):
    pack = pack or C.TARGET
    PR.PACK = pack
    T = K.Truth()
    R = K.rungs(T)
    O = K.out_of_sample(T)
    TM = K.timing_2027(T)
    P = PR.Pack(pack)

    # ------------------------------------------------------------------------------------------ input gates
    files = sorted(os.listdir(pack))
    check("GATE files >= 10", len(files) >= 10, len(files))
    fmts = {f.rsplit(".", 1)[-1] for f in files}
    check("GATE formats >= 3", len(fmts) >= 3, sorted(fmts))
    big = [f for f in files if f.endswith(".csv") and sum(1 for _ in open(os.path.join(pack, f))) - 1 >= 25000]
    check("GATE a 25,000-row file", bool(big), big)
    check("GATE two distractors", len(PK.DISTRACTORS) >= 2 and all(d in files for d in PK.DISTRACTORS), PK.DISTRACTORS)
    check("GATE no file name names the stump", not any(re.search(r"distract|lag|wave|stump|trap|decoy|answer", f)
                                                       for f in files), files)

    # ------------------------------------------------------------------------------------------ the golden
    g = R["R3"]
    check("GOLDEN truth 602.4", abs(g - 602.4) < 0.05, g)
    check("GOLDEN pack equals truth", abs(P.golden() - g) < 1e-9, (P.golden(), g))
    check("GOLDEN rounds to 600", K.r50(g) == 600, K.r50(g))
    check("BIN golden at least a quarter bin from the edge", edge(g) >= 12.5, edge(g))
    se = st.stdev(R["north_waves"]) / len(R["north_waves"]) ** 0.5
    check("BIN one sigma of the mean wave leaves the bin unchanged", K.r50(g - se) == 600 and K.r50(g + se) == 600, se)
    fam = R["family"]
    check("C1 eight constructions file 600", all(K.r50(v) == 600 for v in fam.values()), fam)
    check("C1 every construction a quarter bin inside", min(edge(v) for v in fam.values()) >= 12.5,
          min(edge(v) for v in fam.values()))
    check("C1 shift by shift on the pack", K.r50(st.mean(P.north_waves("shifts"))) == 600, P.north_waves("shifts"))
    fA0, _, _ = PR.ask_figures(P, PR.ask_lines(P))
    sth = P.fids("Southeast") + P.fids("West and Central")
    fund = sum(fA0[f] for f in sth)
    a26, b26 = C.season_bounds(2026)
    for how, base in (("nights", sum(P.draw_nights(f, a26, b26) for f in sth)),
                      ("shifts", sum(P.draw_shifts(f, a26, b26) for f in sth))):
        sc = st.mean(P.north_waves(how)) * fund / base
        check("C1 the North scaled by last winter's funded shifts against the staffing draw (%s) files 600" % how,
              K.r50(sc) == 600 and edge(sc) >= 12.5, (sc, fund, base))

    # ------------------------------------------------------------------------------------------ timing
    lags = list(R["lags"].values())
    check("TIMING lags 37 to 40 days", min(lags) >= 37.0 and max(lags) <= 40.0, lags)
    check("TIMING pack centres match truth", all(abs(P.region_centre("North", w) - P.region_centre("Southeast", w)
                                                     - R["lags"][w]) < 1e-9 for w in C.CLOSED))
    check("TIMING south's last surge night by 27 December", TM["south_last"] <= D(2026, 12, 27), TM["south_last"])
    check("TIMING North spells a week inside the block weeks", TM["north_first"] >= C.BLOCK_2027[0] + dt.timedelta(days=7)
          and TM["north_last"] <= C.BLOCK_2027[1] - dt.timedelta(days=7), (TM["north_first"], TM["north_last"]))
    se27 = T.region_mid("SE", 2027)
    lo = D.fromordinal(int(se27 + min(lags) - 8)) ; hi = D.fromordinal(int(se27 + max(lags) + 8))
    check("TIMING any closed winter's lag keeps every North spell inside", lo >= C.BLOCK_2027[0] and hi <= C.BLOCK_2027[1],
          (lo, hi))
    check("TIMING the North never in a closed January block", all(R["jan"][w] == T.block_draw(T.south(), w) for w in C.CLOSED))
    def into(w):
        return T.region_mid("SE", w) - C.season_bounds(w)[0].toordinal()
    check("TIMING this winter earliest on file by 3 weeks", all(into(w) - into(2027) >= 20 for w in C.CLOSED),
          [into(w) - into(2027) for w in C.CLOSED])
    ww = json.load(open(os.path.join(pack, PK.F_WW)))

    def rise(reg):
        def m(a, b):
            v = [r["concentration_copies_per_l"] / r["pmmov_copies_per_l"] for r in ww["results"]
                 if r["sewershed_id"].startswith("WW-" + reg) and r["target"] == "Influenza A" and a <= r["sample_date"] <= b
                 and r["concentration_copies_per_l"] is not None]
            return st.mean(v)
        return m("2026-12-04", "2026-12-17") / m("2026-10-01", "2026-11-15")
    rz = {g: rise(g) for g in ("SE", "WC", "NO")}
    check("TIMING the North's wastewater flat at the as-of while the south's has risen tenfold",
          rz["NO"] < 1.3 and rz["SE"] > 10 and rz["WC"] > 10, rz)

    # ------------------------------------------------------------------------------------------ the ladder
    check("LADDER R0 files 2,850", K.r50(R["R0"]) == 2850, R["R0"])
    check("LADDER R0b files 3,700", K.r50(R["R0b"]) == 3700, R["R0b"])
    check("LADDER R0c files 2,550", K.r50(R["R0c"]) == 2550, R["R0c"])
    check("LADDER R1 files none", K.r50(R["R1"]) == 0 and K.r50(R["R1b"]) == 0, (R["R1"], R["R1b"]))
    check("LADDER R2c files 2,250", K.r50(R["R2c"]) == 2250, R["R2c"])
    check("LADDER R2d files 950", K.r50(R["R2d"]) == 950, R["R2d"])
    check("LADDER R2e files 4,450", K.r50(R["R2e"]) == 4450, R["R2e"])
    check("LADDER R2f files 650 (1,050 without the tail to 31 December)", K.r50(R["R2f_dec"]) == 650 and K.r50(R["R2f"]) == 1050,
          (R["R2f_dec"], R["R2f"]))
    rungs = [R[k] for k in ("R0", "R0b", "R0c", "R1", "R1b", "R2c", "R2d", "R2e", "R2f_dec", "R2f")]
    check("LADDER every rung at least one bin from the golden", all(abs(K.r50(v) - 600) >= 50 for v in rungs),
          [K.r50(v) for v in rungs])
    check("LADDER the golden bracketed", max(K.r50(v) for v in rungs) > 600 and min(K.r50(v) for v in rungs) < 600)
    for name, v in PR.reflex_sweep(P).items():
        check("REFLEX %s misses the golden's bin by a quarter bin or more" % name, v <= 562.5 or v >= 637.5, v)
    check("LADDER R0 on the pack", K.r50(st.mean(P.block_draw(P.fids(), w) for w in C.CLOSED)) == 2850)
    oc = O["carry"]
    check("OOS calendar carried a winter misses 38 to 213 per cent",
          round(min(abs(v) for v in oc.values()) * 100) == 38 and round(max(abs(v) for v in oc.values()) * 100) == 213, oc)
    check("OOS North per-wave within 7 per cent", max(abs(v) for v in O["north_loo"].values()) < 0.07, O["north_loo"])
    check("OOS lag within 1.7 days", max(abs(v) for v in O["lag_loo"].values()) < 1.7, O["lag_loo"])

    # ------------------------------------------------------------------------------------------ three rules
    check("R1 the golden reads the census nights of every North member in five winters",
          len(P.fids("North")) == 8 and all(len(P.spells(fid, *C.season_bounds(w))) == 1 for fid in P.fids("North")
                                            for w in C.CLOSED))
    heads = []
    for f in files:
        if f.endswith(".csv"):
            heads += open(os.path.join(pack, f)).readline().strip().lower().split(",")
    check("R1 no shipped column holds the deciding quantity", not any(re.search(r"lag|wave|draw|forecast|expected_shift", h)
                                                                     for h in heads), heads)
    check("R3a the default path on the clean truth files 2,850", K.r50(R["R0"]) == 2850)
    check("R3b the decisive step alone files 600", K.r50(R["R3"]) == 600)
    check("R3b each lower correction alone stays wrong", K.r50(R["R1"]) != 600 and K.r50(R["R2c"]) != 600
          and K.r50(R["R2d"]) != 600)
    # R2: each Layer 1 item mishandled leaves the call
    w_old = [sum(T.draw_grid(h["facility_id"], *C.season_bounds(w)) for h in T.region("NO")) for w in (2025, 2026)]
    check("R2 legacy export dropped: the new system's two winters file 600", K.r50(st.mean(w_old)) == 600, w_old)
    leg = PR.find(r"capacity_reports_legacy_.*\.csv", pack)
    import pandas as pd
    old = pd.read_csv(leg, dtype=str)
    north_members = set(P.roster.loc[P.roster["region"] == "North", "member_no"])
    dup_surge = old[(old["submission"] == "R") & old["surge_status"].notna() & old["member_no"].isin(north_members)]
    check("R2 resubmissions kept twice move the North by under a shift a wave", len(dup_surge) * 14 / 5.0 < 12.5, len(dup_surge))
    def north_shifted(days):
        out = []
        for w in C.CLOSED:
            a, b = C.season_bounds(w)
            n = 0
            for fid in P.fids("North"):
                g = P.grid[fid]
                x = P.cap[P.cap["facility_id"] == fid]
                for d, lv in zip(x["census_date"], x["level"]):
                    dd = d + dt.timedelta(days=days) if d < C.NEW_SYSTEM else d
                    if lv and a <= dd <= b:
                        n += g[lv - 1]
            out.append(n)
        return out
    check("R2 legacy report date read as the census date leaves every wave", north_shifted(1) == north_shifted(0),
          (north_shifted(1), north_shifted(0)))
    check("R2 provisional census nights dropped leave the North inside the block",
          T.region_mid("SE", 2027) - 3 + min(lags) - 8 >= C.BLOCK_2027[0].toordinal())
    import tempfile
    cut = (PK.F_CRS, PK.F_ISN25, PK.F_ISN26, PK.F_WW, PK.F_OUTLOOK, PK.F_BLOCKS, PK.F_SURVEY, DOC.F_RATES)
    with tempfile.TemporaryDirectory() as tdir:
        for fn in files:
            if fn not in cut:
                os.symlink(os.path.join(os.path.abspath(pack), fn), os.path.join(tdir, fn))
        g_cut = PR.Pack(tdir).golden()
    check("R2 the call reads no agency line, wastewater or outlook (DEVICE)", abs(g_cut - P.golden()) < 1e-9,
          (g_cut, P.golden()))
    check("R3c no repeated block: no two members share a census series",
          len({tuple(r["census"] for r in T.truth[h["facility_id"]][:400]) for h in T.hs}) == 24)
    bo = pd.read_excel(PR.find(r"january_block_orders_.*\.xlsx", pack), dtype=str)
    docs_tx = " ".join(pdf_text(os.path.join(pack, fn)) for fn in (DOC.F_AGREEMENT, DOC.F_REGISTER, DOC.F_RATES))
    check("R3c no decoy: no document states a 2027 block figure",
          bo.iloc[-1].isna().sum() >= 1 and not re.search(r"\b\d[,\d]{2,5}\s+(?:agency\s+)?(?:RN\s+)?shifts", docs_tx),
          re.findall(r"\b\d[,\d]{2,5}\s+(?:agency\s+)?(?:RN\s+)?shifts", docs_tx)[:5])

    # ------------------------------------------------------------------------------------------ semantic forks
    ag = pdf_text(os.path.join(pack, DOC.F_AGREEMENT))
    check("SF1 the block weeks", "Monday 4 January to Sunday 31" in ag and "January 2027." in ag)
    check("SF2 the expected draw", "expected draw over the Block weeks" in ag)
    check("SF3 what the pool funds", "staff a Member's surge unit and start while the Member's surge" in ag)
    check("SF4 Schedule A lists 24 members, the North from 1 Nov 2026",
          sum(1 for h in T.hs if h["name"] in ag) == 24 and ag.count("1 Nov 2026") == 8)
    check("SF5 a shift is one nurse for one scheduled shift", "one nurse for one scheduled shift" in ag)
    check("SF6 declared times or census nights the same block", K.r50(fam["mean of five waves (shift by shift)"]) == 600)
    reg = pdf_text(os.path.join(pack, DOC.F_REGISTER))
    check("SF7 the register's staffing read from the pack", P.grid == {h["facility_id"]: h["grid"] for h in T.hs})
    S1 = [s for s in T.shifts if D(2025, 11, 1) <= s["start"].date() <= D(2026, 3, 31)]
    fund = sum(1 for s in S1 if K.W.funded(s, T.iv))
    reg_sh = sum(T.draw_shifts(h["facility_id"], *C.season_bounds(2026)) for h in T.south())
    check("SF7 last winter's funded shifts 0.3 per cent under the register", abs((fund - reg_sh) / reg_sh + 0.0035) < 0.001,
          (fund, reg_sh))
    check("SF8 the as-of: census to 20 December", max(P.cap["census_date"]) == C.CENSUS_END)
    sb = T.block_draw(T.south(), 2027)
    check("SF9 rounding path: regions rounded first the same", sb == 0 and K.r50(K.r50(sb) + K.r50(g)) == K.r50(sb + g) == 600,
          sb)
    check("SF10 five closed winters on the census", min(P.cap["census_date"]) == C.CENSUS_START)

    # ------------------------------------------------------------------------------------------ closure axes
    check("AXIS9 no surge shift within three days of either block edge (truth)",
          TM["north_first"] - C.BLOCK_2027[0] >= dt.timedelta(days=3) and C.BLOCK_2027[1] - TM["north_last"] >= dt.timedelta(days=3))
    check("AXIS12 West and Central spells end by 27 December under the longest closed spell",
          all(T.spell(h["facility_id"], 2027)[0] + dt.timedelta(days=max(
              (T.spell(h["facility_id"], w)[1] - T.spell(h["facility_id"], w)[0]).days for w in C.CLOSED)) < C.BLOCK_2027[0]
              for h in T.region("WC")))
    check("AXIS16 one facility id per member number", P.roster["member_no"].is_unique and P.roster["facility_id"].is_unique)

    # ------------------------------------------------------------------------------------------ the asks
    south = P.fids("Southeast") + P.fids("West and Central")
    fA, fB, wk = PR.ask_figures(P, PR.ask_lines(P))
    tA = collections.Counter(s["facility_id"] for s in S1 if K.W.funded(s, T.iv))
    tB = collections.Counter(s["facility_id"] for s in S1 if s["bill"] == "POOL" and not K.W.funded(s, T.iv))
    check("ASK A pack equals truth", all(fA[f] == tA[f] for f in south), [(fA[f], tA[f]) for f in south])
    check("ASK B pack equals truth", all(fB[f] == tB[f] for f in south))
    for name, kw in (("lines counted", dict(split="line")), ("payroll dates as start dates", dict(isn_date="start")),
                     ("both", dict(split="line", isn_date="start"))):
        cA, cB, _ = PR.ask_figures(P, PR.ask_lines(P, **kw))
        check("DEVICE %s moves every Ask A figure" % name, all(cA[f] != fA[f] for f in south))
        if "payroll" in name or name == "both":
            check("DEVICE %s moves every Ask B figure" % name, all(cB[f] != fB[f] for f in south))
    mA, mB, _ = PR.ask_figures(P, PR.ask_lines(P), by_census=True)
    pm = {x["facility_id"] for _, x in P.decl.iterrows() if x["level_to"] == 0 and x["t"].strftime("%H:%M") == "14:45"
          and D(2025, 11, 1) <= x["t"].date() <= D(2026, 3, 31) and x["facility_id"] in south}
    check("DEVICE the census night's level for the day moves Ask A and B exactly at the afternoon stand-downs",
          {f for f in south if mA[f] != fA[f]} == pm == {f for f in south if mB[f] != fB[f]} and len(pm) >= 1,
          (sorted(pm), [f for f in south if mA[f] != fA[f]]))
    lA, lB, _ = PR.ask_figures(P, PR.ask_lines(P, split="line"))
    nlb = sum(lB[f] != fB[f] for f in south)
    check("DEVICE lines counted moves Ask B at 15 of the 16 members", nlb == 15, nlb)
    import cracker
    co, pc, pa2, pb1, leak = cracker.pack_mode(pack, quiet=True)
    check("ASK the cracker misses every Ask A and Ask B figure and the busiest week", co["cracker"][:3] == (0, 0, 0),
          co["cracker"])
    check("ASK pair ceiling 40 or under", pc <= 40.0, pc)
    check("ASK pair 40 or under with A2 cracked", pa2 <= 40.0, pa2)
    check("ASK pair 40 or under with B1 cracked", pb1 <= 40.0, pb1)
    check("ASK mirror leakage under 35 per cent", leak < 35.0, leak)
    tot = collections.Counter()
    for (k, a), v in wk.items():
        tot[k] += v
    check("ASK C busiest week 1,554 in the week of 19 January", max(tot.values()) == 1554 and tot[11] == 1554, sorted(tot.items()))
    check("DEVICE zero device rows in the call's population: the golden unchanged with both agency reports deleted",
          abs(g_cut - g) < 1e-9, (g_cut, g))

    # ------------------------------------------------------------------------------------------ realism
    nw = R["north_waves"]
    check("REAL the North's waves differ every winter", len(set(nw)) == len(nw), nw)
    check("REAL no round headline", g % 50 != 0 and R["R0"] % 50 != 0)
    check("REAL last winter's funded shifts differ at every member", len({fA[f] for f in south}) == len(south),
          sorted(fA[f] for f in south))
    check("REAL no member's census series repeats another's over the closed winters",
          len({tuple(P.cap.loc[P.cap["facility_id"] == f, "census"]) for f in P.fids()}) == 24)
    for fn in (DOC.F_AGREEMENT, DOC.F_REGISTER, DOC.F_RATES):
        tx = pdf_text(os.path.join(pack, fn))
        check("READ %s extracted" % fn, len(tx) > 400, len(tx))
        check("REAL %s has no em dash" % fn, chr(0x2014) not in tx and chr(0x2013) not in tx)
    check("READ the agreement's positive control", "The Pool funds the agency RN shifts" in ag)
    check("READ the register's positive control", "Rouge Park Hospital" in reg and "Agency staffing is the agency RN shifts" in reg)
    check("DATES no wastewater result posted after the pull", max(r["posted"] for r in ww["results"]) <= "2026-12-21")
    cr = P.crestfield()
    check("DATES no Crestfield line ends after the pull", max(cr["shift_end_utc"]) <= "2026-12-21T11:40:00Z", max(cr["shift_end_utc"]))
    check("DATES documents dated before the pull", DOC.AGREEMENT_DATE < C.AS_OF and DOC.REGISTER_DATE < C.AS_OF
          and DOC.RATES_DATE < C.AS_OF)
    return RESULTS


if __name__ == "__main__":
    res = main(sys.argv[1] if len(sys.argv) > 1 else None)
    bad = [r for r in res if not r[1]]
    for lab, ok, det in res:
        print("%s  %s%s" % ("PASS" if ok else "FAIL", lab, "" if ok else "   " + str(det)[:300]))
    print("%d checks, %d FAIL" % (len(res), len(bad)))
    sys.exit(1 if bad else 0)
