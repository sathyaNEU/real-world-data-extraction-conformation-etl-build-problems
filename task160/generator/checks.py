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
    check("GOLDEN truth 602.0", abs(g - 602.0) < 0.05, g)
    check("GOLDEN pack equals truth", abs(P.golden() - g) < 1e-9, (P.golden(), g))
    check("GOLDEN rounds to 600", K.r50(g) == 600, K.r50(g))
    check("BIN golden at least a quarter bin from the edge", edge(g) >= 12.5, edge(g))
    se = st.stdev(R["north_waves"]) / len(R["north_waves"]) ** 0.5
    check("BIN one sigma of the mean wave leaves the bin unchanged", K.r50(g - se) == 600 and K.r50(g + se) == 600, se)
    fam = R["family"]
    check("C1 nine constructions file 600", len(fam) == 9 and all(K.r50(v) == 600 for v in fam.values()), fam)
    check("C1 every construction a quarter bin inside", min(edge(v) for v in fam.values()) >= 12.5,
          min(edge(v) for v in fam.values()))
    check("C1 shift by shift on the pack", K.r50(st.mean(P.north_waves("shifts"))) == 600, P.north_waves("shifts"))
    routes = {"every member aligned on West and Central's centre": PR.aligned(P, "WC"),
              "every member aligned on West and Central's first surge night": PR.aligned(P, "WCfirst"),
              "the North at West and Central's centre plus the mean lag": PR.placed(P, "WC"),
              "the North at West and Central's centre plus the median lag": PR.placed(P, "WC", agg="median"),
              "the North's first night at West and Central's first plus the mean lag": PR.placed(P, "WC", onset=True),
              "the North from West and Central's wastewater peak": PR.ww_route(P, "WC")}
    for name, v in routes.items():
        check("C1 on the pack, %s, files 600 a quarter bin inside" % name, K.r50(v) == 600 and edge(v) >= 12.5, v)
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
    lse = list(R["lags_se"].values())
    gap = [T.region_mid("WC", w) - T.region_mid("SE", w) for w in C.CLOSED]
    check("TIMING the North 30 to 34 days behind West and Central in every closed winter", min(lags) >= 30.0
          and max(lags) <= 34.0, lags)
    check("TIMING West and Central's gap behind the Southeast moves by more than three weeks", max(gap) - min(gap) > 21, gap)
    check("TIMING the North's lag behind the Southeast moves by more than three weeks", max(lse) - min(lse) > 21, lse)
    check("TIMING pack centres match truth", all(abs(P.region_centre("North", w) - P.region_centre("West and Central", w)
                                                     - R["lags"][w]) < 1e-9 for w in C.CLOSED))
    check("TIMING south's last surge night by 27 December", TM["south_last"] <= D(2026, 12, 27), TM["south_last"])
    check("TIMING North spells five days inside the block weeks", TM["north_first"] >= C.BLOCK_2027[0] + dt.timedelta(days=5)
          and TM["north_last"] <= C.BLOCK_2027[1] - dt.timedelta(days=5), (TM["north_first"], TM["north_last"]))
    wc27 = P.region_centre("West and Central", 2027, upto=C.CENSUS_END)
    lo = D.fromordinal(int(wc27 + min(lags) - 7)) ; hi = D.fromordinal(int(wc27 + max(lags) + 7))
    check("TIMING any closed winter's lag from West and Central's centre at the pull keeps every North spell inside",
          lo >= C.BLOCK_2027[0] and hi <= C.BLOCK_2027[1], (lo, hi))
    wcf = min(P.spells(f, C.season_bounds(2027)[0], C.CENSUS_END)[0][0] for f in P.fids("West and Central"))
    check("TIMING West and Central in surge by the pull, every member", all(P.spells(f, C.season_bounds(2027)[0], C.CENSUS_END)
                                                                        for f in P.fids("West and Central")), wcf)
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
    check("LADDER R0 files 1,850", K.r50(R["R0"]) == 1850, R["R0"])
    check("LADDER R0b files 2,100", K.r50(R["R0b"]) == 2100, R["R0b"])
    check("LADDER R0c files 1,750", K.r50(R["R0c"]) == 1750, R["R0c"])
    check("LADDER R1 files 1,250 (1,050 with the North at its calendar January)", K.r50(R["R1"]) == 1250
          and K.r50(R["R1b"]) == 1050, (R["R1"], R["R1b"]))
    check("LADDER R1c the North timed from the Southeast files 100 (none by first surge nights)", K.r50(R["R1c"]) == 100
          and K.r50(R["R1c_onset"]) == 0, (R["R1c"], R["R1c_onset"]))
    check("LADDER R1d every member aligned on the Southeast files 1,150", K.r50(R["R1d"]) == 1150, R["R1d"])
    check("LADDER R2c files 1,550", K.r50(R["R2c"]) == 1550, R["R2c"])
    check("LADDER R2d files 1,300", K.r50(R["R2d"]) == 1300, R["R2d"])
    check("LADDER R2e files 2,200", K.r50(R["R2e"]) == 2200, R["R2e"])
    check("LADDER R2f files 650 (950 without the tail to 31 December)", K.r50(R["R2f_dec"]) == 650 and K.r50(R["R2f"]) == 950,
          (R["R2f_dec"], R["R2f"]))
    rungs = [R[k] for k in ("R0", "R0b", "R0c", "R1", "R1b", "R1c", "R1c_onset", "R1d", "R2c", "R2d", "R2e", "R2f_dec",
                            "R2f")]
    check("LADDER every rung at least one bin from the golden", all(abs(K.r50(v) - 600) >= 50 for v in rungs),
          [K.r50(v) for v in rungs])
    check("LADDER the golden bracketed", max(K.r50(v) for v in rungs) > 600 and min(K.r50(v) for v in rungs) < 600)
    for name, v in PR.reflex_sweep(P).items():
        check("REFLEX %s misses the golden's bin by a quarter bin or more" % name, v <= 562.5 or v >= 637.5, v)
        if name.split(":")[0] in ("aligned", "eyeballed", "wastewater only"):
            check("REFLEX %s misses the golden's cell by a full bin" % name, v <= 525.0 or v >= 675.0, v)
    check("LADDER R0 on the pack", K.r50(st.mean(P.block_draw(P.fids(), w) for w in C.CLOSED)) == 1850)
    oc = O["carry"]
    check("OOS calendar carried a winter misses by a quarter or more every time", min(abs(v) for v in oc.values()) > 0.25, oc)
    check("OOS North per-wave within 7 per cent", max(abs(v) for v in O["north_loo"].values()) < 0.07, O["north_loo"])
    check("OOS the lag behind West and Central within 2 days of each winter's own", max(abs(v) for v in O["lag_loo"].values()) < 2.0,
          O["lag_loo"])
    check("OOS the lag behind the Southeast misses a winter by more than three weeks",
          max(abs(v) for v in O["lag_loo_se"].values()) > 21, O["lag_loo_se"])

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
    check("R3a the default path on the clean truth files 1,850", K.r50(R["R0"]) == 1850)
    check("R3b the decisive step alone files 600", K.r50(R["R3"]) == 600)
    check("R3b each lower correction alone stays wrong", all(K.r50(R[k]) != 600 for k in ("R1", "R1b", "R1c", "R1d", "R2c", "R2d")))
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
    wc_first = [P.spells(f, C.season_bounds(2027)[0], C.CENSUS_END - dt.timedelta(days=7))[0][0]
                for f in P.fids("West and Central")]
    onset_lag = [PR.anchor(P, "NOfirst", w) - PR.anchor(P, "WCfirst", w) for w in C.CLOSED]
    first_n = D.fromordinal(int(min(wc_first).toordinal() + min(onset_lag)))
    check("R2 provisional census nights dropped leave West and Central's onsets and the North's placement unchanged",
          max(wc_first) <= C.CENSUS_END - dt.timedelta(days=7) and first_n >= C.BLOCK_2027[0]
          and K.r50(PR.placed(P, "WC", onset=True)) == 600, (min(wc_first), first_n))
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
    check("SF7 last winter's funded shifts 0.5 per cent under the register", abs((fund - reg_sh) / reg_sh + 0.0049) < 0.001,
          (fund, reg_sh))
    check("SF8 the as-of: census to 20 December", max(P.cap["census_date"]) == C.CENSUS_END)
    sb = T.block_draw(T.south(), 2027)
    check("SF9 rounding path: regions rounded first the same", sb == 0 and K.r50(K.r50(sb) + K.r50(g)) == K.r50(sb + g) == 600,
          sb)
    check("SF10 five closed winters on the census", min(P.cap["census_date"]) == C.CENSUS_START)
    agn = " ".join(ag.split())
    check("SF11 the block covers every Member in Schedule A, the North from 1 Nov 2026 (the 16 alone file none)",
          "The January Block covers every Member's surge unit for the four weeks" in agn
          and "A Member is a hospital listed in Schedule A, from its Pool start date." in agn
          and sum(1 for h in T.hs if h["name"] in ag) == 24 and K.r50(T.block_draw(T.south(), 2027)) == 0)
    # the reader's and judge's realism and fork items
    dd = pd.read_excel(PR.find(r"data_dictionary\.xlsx", pack), header=None, dtype=str)
    ddt = " ".join(str(v) for v in dd.values.ravel() if isinstance(v, str))
    check("ASK the dictionary files Inland Seas' payroll date as the day a shift ends, for both workbooks",
          sum(1 for v in dd.values.ravel() if v == "The date Inland Seas pays the shift under: the day the shift ends.") == 2)
    det = pd.read_excel(PR.find(r"inland_seas_member_shifts_2025-26\.xlsx", pack), sheet_name="Timesheet detail",
                        header=2, dtype=str)
    check("REAL the queried timesheets carry an order number and request, no query label",
          list(det.columns)[-2:] == ["Order no.", "Request ref"] and not re.search(r"stand-down|declaration|pool", " ".join(
              str(v) for v in det.values.ravel() if isinstance(v, str)), re.I), list(det.columns))
    bo = pd.read_excel(PR.find(r"january_block_orders_.*\.xlsx", pack), dtype=str).iloc[:5]
    shares = [int(c) / int(b) for c, b in zip(bo["crestfield_shifts"], bo["block_shifts"])]
    check("REAL the block orders split unevenly, no two seasons alike", len({round(x, 3) for x in shares}) == 5
          and sum(1 for c, i in zip(bo["crestfield_shifts"], bo["inland_seas_shifts"]) if c == i) == 0, shares)
    book = [int(x) for x in bo["block_shifts"]]
    check("REAL each later block the last January's draw to the nearest 50, the record missing both ways",
          book[0] == PK.FIRST_BLOCK and all(book[i] == K.r50(R["jan"][C.CLOSED[i - 1]]) for i in range(1, 5))
          and any(book[i] > R["jan"][C.CLOSED[i]] for i in range(5)) and any(book[i] < R["jan"][C.CLOSED[i]] for i in range(5)),
          (book, R["jan"]))
    revd = [ln for ln in reg.splitlines() if re.search(r"\d{1,2} [A-Z][a-z]{2} \d{4}$", ln) and not ln.startswith("TPHA")]
    dates = [re.search(r"(\d{1,2} [A-Z][a-z]{2} \d{4})$", ln).group(1) for ln in revd]
    check("REAL every member's plan has its own revision date", len(dates) == 24 and len(set(dates)) >= 22, dates)

    # ------------------------------------------------------------------------------------------ closure axes
    check("AXIS9 no surge shift within three days of either block edge (truth)",
          TM["north_first"] - C.BLOCK_2027[0] >= dt.timedelta(days=3) and C.BLOCK_2027[1] - TM["north_last"] >= dt.timedelta(days=3))
    check("AXIS12 West and Central spells end before the block weeks under the longest closed spell",
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
    check("DEVICE lines counted moves Ask B at every member", nlb == 16, nlb)
    import cracker
    co, pc, pa2, both, leak = cracker.pack_mode(pack, quiet=True)
    check("ASK the cracker misses every Ask A and Ask B figure and both chart figures", co["cracker"][:3] == (0, 0, 0),
          co["cracker"])
    check("ASK pair ceiling 40 or under", pc <= 40.0, pc)
    check("ASK both top responses on the call 45 or under", both <= 45.0, both)
    check("ASK mirror leakage under 35 per cent", leak < 35.0, leak)
    kb, ft, bt, fund, bill = PR.chart_figures(P, PR.ask_lines(P))
    check("ASK C busiest week 12 to 18 January 2026: 902 funded, 928 billed to the pool", (kb, ft, bt) == (10, 902, 928),
          (kb, ft, bt))
    check("ASK C the busiest week clear of the next by 40 shifts or more", ft - sorted(fund.values())[-2] >= 40,
          sorted(fund.values())[-2:])
    for name, kw in (("lines counted", dict(split="line")), ("payroll dates as start dates", dict(isn_date="start"))):
        _, cft, cbt, _, _ = PR.chart_figures(P, PR.ask_lines(P, **kw))
        check("DEVICE %s moves both chart figures" % name, cft != ft and cbt != bt, (cft, cbt))
    check("DEVICE zero device rows in the call's population: the golden unchanged with both agency reports deleted",
          abs(g_cut - g) < 1e-9, (g_cut, g))

    # ------------------------------------------------------------------------------------------ realism
    nw = R["north_waves"]
    check("REAL the North's waves differ every winter", len(set(nw)) == len(nw), nw)
    check("REAL no round headline", g % 50 != 0 and R["R0"] % 50 != 0)
    check("REAL no three members share last winter's funded shifts", max(collections.Counter(fA[f] for f in south).values()) <= 2,
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
