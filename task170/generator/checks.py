"""task170 generator checks, run on the cut pack and on the generator's clean truth.

Blocks: GATE (input gates), R (the three rules: R1 raw material, R2 mess neutral, R3a analyst test, R3b decisive step
alone, R3c no plant), FAM (the family of constructions in the golden's step), LAD (every rival out of it), OOS (the
out-of-sample record), SF (the semantic fork table), ASK (the asks, their devices and the pair), SEP (the separation
line), REAL (the realism sweep), DIST (distractors).

    python3 checks.py <target>        exit 0 when every assertion holds"""
from __future__ import annotations

import csv
import datetime as dt
import glob
import json
import os
import re
import sys
import zipfile

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import asks as AS          # noqa: E402
import calc as K           # noqa: E402
import common as C         # noqa: E402
import cracker as CR       # noqa: E402
import deliver as DV       # noqa: E402
import docs as DOC         # noqa: E402
import ladder as LD        # noqa: E402
import pack as PK          # noqa: E402
import pack_read as PR     # noqa: E402

D = dt.date
TASK = os.path.dirname(HERE)
FAILS = []
N = [0]


def ok(cond, label):
    N[0] += 1
    print(("PASS  " if cond else "FAIL  ") + label, flush=True)
    if not cond:
        FAILS.append(label)


def pdf_text(path):
    import subprocess
    return subprocess.run(["pdftotext", "-layout", path, "-"], capture_output=True, text=True).stdout


def pdf_readers(path):
    """The document's text under pdfminer.six, pdfplumber, pypdf (strict and lenient) and poppler's pdftotext, each
    with its whitespace collapsed, and whether pypdf's strict and lenient texts agree."""
    import subprocess
    import warnings
    warnings.filterwarnings("ignore")
    import pdfplumber
    import pypdf
    from pdfminer.high_level import extract_text
    sq = lambda s_: re.sub(r"\s+", " ", s_ or "").strip()
    out = {"pdfminer": sq(extract_text(path))}
    with pdfplumber.open(path) as p_:
        out["pdfplumber"] = sq("\n".join((pg.extract_text() or "") for pg in p_.pages))
    strict = sq("\n".join(pg.extract_text() for pg in pypdf.PdfReader(path, strict=True).pages))
    lenient = sq("\n".join(pg.extract_text() for pg in pypdf.PdfReader(path, strict=False).pages))
    out["pypdf"] = strict
    out["pdftotext"] = sq(subprocess.run(["pdftotext", path, "-"], capture_output=True, text=True).stdout)
    out["strict_equals_lenient"] = strict == lenient
    return out


def rnd(x):
    """Pallets, to the nearest whole pallet (SOP 4.4)."""
    return int(round(x / C.PALLET))


def main(t):
    meta = json.load(open(os.path.join(TASK, "metadata.json")))
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    files = sorted(os.listdir(t))
    # ------------------------------------------------------------------------------------------------ GATE
    ok(len(files) >= 10, "GATE files: %d (10 or more)" % len(files))
    fmts = sorted({f.rsplit(".", 1)[1] for f in files})
    ok(len(fmts) >= 3, "GATE formats: %s (3 or more)" % ", ".join(fmts))
    big = meta["input_gates"]["largest_file_rows"]
    ok(big >= 25000, "GATE largest file %s: %d rows (25,000 or more)" % (meta["input_gates"]["largest_file"], big))
    ok(len(meta["distractor_files"]) >= 2 and all(f in files for f in meta["distractor_files"]),
       "GATE distractors named in metadata.json and shipped: %s" % ", ".join(meta["distractor_files"]))
    ok(not any("distractor" in f.lower() for f in files), "GATE no file name says distractor")
    man = list(csv.DictReader(open(os.path.join(t, PK.F_MAN), encoding="utf-8")))
    ok(sorted(r["file"] for r in man) == files, "GATE the manifest lists exactly the shipped files")

    # ------------------------------------------------------------------------------------------------ the call
    Wd = PK.make_world()
    PK.place_order(Wd)
    kids_c, visits_c = Wd["kids"], Wd["visits"]
    kids_p, visits_p = PR.register_view(t)
    ok(len(kids_c) == len(kids_p) and len(visits_c) == len(visits_p),
       "R0 the pack's register, read back (layouts joined, crosswalk, June 2024 once, re-sent rows dropped), has the "
       "clean truth's %d children and %d visits" % (len(kids_p), len(visits_p)))
    fam, c = LD.family(kids_p, visits_p)
    famc, cc = LD.family(kids_c, visits_c)
    ok(abs(fam["golden"] - famc["golden"]) < 1e-6, "R0 line 2's golden forecast is the same on the pack and on the "
       "clean truth: %.1f bottles" % fam["golden"])
    ci = DV.call_inputs(t)
    W = C.PALLET
    line2 = fig["call"]
    lo_e, hi_e = (line2 - 0.5) * W, (line2 + 0.5) * W
    ok(rnd(fig["call_unrounded"]) == line2 and abs(fig["call_unrounded"] - fam["golden"]) < 10,
       "FAM line 2 before rounding %d bottles (whole children each month) rounds to %d pallets" % (fig["call_unrounded"], line2))
    # one sigma: the candidates resampled with replacement
    P, sig = K.P_noisy(c)
    contrib = (P * c.S_c).sum(1) + C.MAX_MONTHS * (P[:, -1] * c.S_c[:, -1])
    rng = np.random.default_rng(170)
    boots = [contrib[rng.integers(0, len(contrib), len(contrib))].sum() for _ in range(200)]
    sd = float(np.std(boots))
    need = W / 4 + sd
    print("INFO  one sigma of the switch increment, candidates resampled: %.0f bottles; a quarter pallet with one "
          "sigma is %.0f" % (sd, need))
    for k in LD.FAMILY:
        v = fam[k]
        m = min(v - lo_e, hi_e - v)
        ok(rnd(v) == line2 and m >= need, "FAM %s: %.0f bottles (%+.0f), %d pallets, %.0f inside the pallet (%.0f or more)"
           % (k, v, v - fam["golden"], rnd(v), m, need))
    for keys in LD.extreme_pairs(fam):
        v = LD.compound(kids_p, visits_p, keys)
        m = min(v - lo_e, hi_e - v)
        ok(rnd(v) == line2 and m >= sd, "FAM the compound choice %s: %.0f bottles, %d pallets, %.0f inside (one sigma, "
           "%.0f, or more)" % (" with ".join(keys), v, rnd(v), m, sd))
    sh = LD.shrunk(c)
    for k, v in sorted(sh.items(), key=lambda kv: kv[1]):
        print("INFO  SHR %s: %.0f bottles (%+.0f), %d pallets (%s)" % (k, v, v - fam["golden"], rnd(v),
              "in line 2's pallet" if rnd(v) == line2 else "outside it"))
    tau, Q, kq = K.slope_heterogeneity(c)
    ok(tau > 0.015 and Q / (kq - 1) > 1.5, "SHR the candidates' growth slopes vary between children by more than "
       "their estimation error: tau %.3f kg a month, Q %.0f on %d degrees of freedom" % (tau, Q, kq - 1))

    # ------------------------------------------------------------------------------------------------ R1
    v = visits_p
    ok(v.weight.notna().sum() > 300000, "R1 the golden reads the register's weighings at the child-visit grain: %d "
       "weighings" % v.weight.notna().sum())
    heads = []
    for f in files:
        if f.endswith(".csv"):
            heads += next(csv.reader(open(os.path.join(t, f), encoding="utf-8")))
    bad = [h for h in heads if re.search(r"switch|forecast|transition|project", h, re.I)]
    ok(not bad, "R1 no shipped column holds the switch, a forecast or a transition: %s" % (bad or "none"))
    moves = {30.0: 0, 35.0: 0}
    under = back = 0
    left_post = 0
    for u, g_ in visits_p.sort_values(["uid", "date"]).groupby("uid"):
        prev, waiting = None, False
        for r_ in g_.itertuples():
            thr = K.threshold_at(r_.date)
            heavy = r_.weight == r_.weight and r_.weight >= thr
            if prev in K.PAED1 and r_.regimen == C.REG_TLD:
                if heavy:
                    moves[thr] += 1
                elif not waiting:
                    under += 1
                waiting = False
            elif r_.regimen in K.PAED1 and heavy:
                waiting = True
                if prev in K.PAED1 and r_.date >= K.THR_FROM:
                    left_post += 1
            if prev == C.REG_TLD and r_.regimen in K.PAED1:
                back += 1
            prev = r_.regimen
    ok(moves[35.0] > 500 and moves[30.0] > 500 and under == 0 and back == 0,
       "R1 the register follows the annex in force: %d moves onto TLD at a reading of 35 kg or more before 1 March 2026 "
       "and %d at 30 kg or more since, none without such a reading or a held-back one before it, %d moved back (H6)"
       % (moves[35.0], moves[30.0], back))
    ok(0 < left_post < 0.2 * moves[30.0], "R1 since 1 March 2026, %d first-line readings of 30 kg or more were held "
       "back to the next visit (the register's lag)" % left_post)

    # ------------------------------------------------------------------------------------------------ R2
    def line_on(view):
        f2, c2 = LD.family(*view)
        return f2["golden"]
    for label, kw in (("the June 2024 visits kept twice", dict(dedupe_overlap=False)),
                      ("the re-sent EPR rows kept", dict(drop_resent=False)),
                      ("the legacy rows not linked through the crosswalk", dict(link_legacy=False))):
        o2 = line_on(PR.register_view(t, **kw))
        ok(rnd(o2) == line2, "R2 %s: %.0f bottles, still %d pallets" % (label, o2, line2))
    kk = kids_p.copy()
    pts = {r["upid"]: r for r in csv.DictReader(open(os.path.join(t, PK.F_PTS), encoding="utf-8"))}
    ent = kk.uid.map(lambda u: pts[u]["outcome_entered"])
    kk.loc[[bool(e) and D.fromisoformat(e) > C.COUNT for e in ent], ["outcome", "outcome_date"]] = None
    o2 = line_on((kk, visits_p))
    ok(rnd(o2) == line2, "R2 outcomes entered after the count read as not yet known: %.0f bottles, still %d pallets" % (o2, line2))
    ok(sum(1 for p in pts.values() if p["dob_estimated"] == "Y") > 500, "R2 estimated dates of birth are recorded as "
       "the register holds them (1 July of the year)")

    # ------------------------------------------------------------------------------------------------ R3 and the ladder
    rv, info = LD.rivals(c)
    rvc, _ = LD.rivals(cc)
    ok(rnd(rvc["smooth_all"]) <= line2 - 1, "R3a the default path on the clean truth (each child moved when its growth "
       "line through every weighing reaches 30 kg, every filed rule applied) files %d pallets, %d below %d"
       % (rnd(rvc["smooth_all"]), line2 - rnd(rvc["smooth_all"]), line2))
    ok(rnd(rvc["smooth_all"]) == fig["default_line2"], "R3a the default path is the write-up's %d pallets" % fig["default_line2"])
    ok(rnd(famc["golden"]) == line2, "R3b the default path with only the move read off a scheduled weighing around the "
       "same line files the golden %d pallets" % line2)
    for k in ("band_0.5", "recent_3", "trend", "smooth_12", "lead_shift"):
        ok(rnd(rvc[k]) != line2, "R3b a lower rung's single correction (%s) leaves line 2 at %d pallets" % (k, rnd(rvc[k])))
    for k in LD.MISS:
        val = rv[k]
        ok(val < lo_e or val >= hi_e, "LAD %s: %.0f bottles (%+.0f), %d pallets, %.0f outside line 2's pallet"
           % (k, val, val - fam["golden"], rnd(val), (lo_e - val) if val < lo_e else (val - hi_e)))
    for k, val in sorted(rv.items(), key=lambda kv: kv[1]):
        if k not in LD.MISS:
            print("INFO  LAD %s: %.0f bottles (%+.0f), %d pallets (%s)" % (k, val, val - fam["golden"], rnd(val),
                  "in line 2's pallet" if rnd(val) == line2 else "outside it"))
    ar = LD.age_rule(c)
    av = {k: v_[0] for k, v_ in ar.items()}
    win = {k: v_ for k, v_ in av.items() if k.endswith("window")}
    ok(all(rnd(v_) != line2 for v_ in win.values()), "LAD the crossing-age rule (each child moved on reaching the age "
       "at which the register's median weight for age reaches 30 kg) misses line 2 under all %d binnings that wait for "
       "each child's age (%d to %d pallets)" % (len(win), rnd(min(win.values())), rnd(max(win.values()))))
    inside = sorted(k for k, v_ in av.items() if rnd(v_) == line2)
    print("INFO  LAD the crossing-age rule lands under %d of %d binnings, each moving every child already past the "
          "age at its next visit: %s" % (len(inside), len(av), "; ".join(inside)))

    # ------------------------------------------------------------------------------------------------ OOS
    bt = LD.backtests(kids_p, visits_p)
    for b_ in bt:
        a_ = b_["actual"]
        e = lambda k: 100.0 * (b_[k] - a_) / a_
        ok(b_["threshold"] == 35.0, "OOS from %s (%d months): the window closed under the 35 kg band" % (b_["origin"], b_["months"]))
        ok(abs(e("golden")) <= 15.0, "OOS from %s: the golden %+.1f%% of the %d bottle-months the register shows"
           % (b_["origin"], e("golden"), a_))
        ok(e("smooth_all") <= -45, "OOS from %s: the growth line %+.1f%%" % (b_["origin"], e("smooth_all")))
        mem = ("plain", "thr2995", "win24", "q1", "sig_rms", "sig_diff", "sig_near", "own_sd", "pv", "pv_win24",
               "eb_pred", "noisy_12", "noisy_monthly")
        ok(all(abs(e(k)) <= 20.0 for k in mem), "OOS from %s: every construction that reads the move off a scheduled "
           "weighing within a fifth (%s)" % (b_["origin"], ", ".join("%s %+.1f%%" % (k, e(k)) for k in mem)))
        print("INFO  OOS from %s: shrunk or pooled slopes %s; band rates %+.1f%%, recent switches %+.1f%%"
              % (b_["origin"], ", ".join("%s %+.1f%%" % (k, e(k)) for k in ("eb_plug",) + tuple(LD.SHRUNK)),
                 e("band_0.5"), e("recent_3")))

    # ------------------------------------------------------------------------------------------------ SF
    ok(not any(k.dob == D(2011, 8, 31) for k in kids_p.itertuples()), "SF1 under 15 at the count: no date of birth "
       "on 31 August 2011, so born after it and under 15 select the same children")
    sop = " ".join(p_ for _, ps in DOC.SOP for p_ in ps)
    annex = " ".join(DOC.DOSING_INTRO)
    late = [u for u in c.cand if (C.COUNT - c.last.loc[u, "date"]).days > 92]
    c_late = K.context(kids_p[~kids_p.uid.isin(late)], visits_p)
    o_late = K.total(c_late, K.P_noisy(c_late)[0])[0]
    ok("(no outcome entered)" in sop, "SF2 on treatment is no outcome entered (SOP 4.2); dropping the %d candidates "
       "last seen over three months before the count files %d pallets (%s)"
       % (len(late), rnd(o_late), "same call" if rnd(o_late) == line2 else "ruled out by 4.2"))
    Cm = K.total(c, P)[1]
    half = fam["golden"] - 0.5 * float(((np.diff(np.c_[np.zeros(len(c.cand)), P], axis=1)) * c.S_c).sum())
    ok("one bottle for each patient in care on the regimen at the end of the month" in sop,
       "SF3 one bottle for each child on TLD at a month's end (SOP 4.1); half a bottle in the month of the move would "
       "file %d pallets (%s)" % (rnd(half), "same call" if rnd(half) == line2 else "ruled out by 4.1"))
    avg = fam["golden"] - C.MAX_MONTHS * float(Cm[-1]) + C.MAX_MONTHS * float(np.mean(Cm[4:]))
    ok("six months of their forecast consumption in the last month of the cycle ordered" in sop,
       "SF4 line 2's maximum stock is six months of June 2027's (SOP 4.3); six months of the cycle's average files %d "
       "pallets (%s)" % (rnd(avg), "same call" if rnd(avg) == line2 else "ruled out by 4.3"))
    quar = sum(b["qty"] for b in Wd["S"]["batches"] if b["status"] == "Quarantined")
    l1 = fig["line1_unrounded"]
    ok(rnd(l1 - quar) != fig["line1"], "SF5 usable stock leaves out the quarantined batch (SOP 3.3): with it line 1 "
       "files %d pallets" % rnd(l1 - quar))
    planned = sum(s["qty"] for s in Wd["S"]["ship"] if s["status"] == "Planned")
    ok(rnd(l1 - planned) != fig["line1"], "SF6 the planned C7 call-off is not on order (SOP 3.3): with it line 1 files "
       "%d pallets" % rnd(l1 - planned))
    jan = fam["golden"] - float(sum(Cm[:4]))
    ok(rnd(jan) != line2, "SF7 the window opens on 1 September 2026 (SOP 3.1, 4.3): from 1 January line 2 files %d "
       "pallets" % rnd(jan))
    due = [x[3] for x in ci["shipments"]]
    ok(all(d_.date() <= D(2026, 12, 31) for d_ in due), "SF8 every confirmed lot is due by 31 December 2026, so due "
       "within C6 and due before the window closes select the same %d lots: same call" % len(due))
    parts = rnd(float(sum(Cm))) * W + rnd(C.MAX_MONTHS * float(Cm[-1])) * W
    ok(rnd(fig["call_unrounded"]) == line2, "SF9 line 2 rounded once (SOP 4.4) is %d pallets; its consumption and "
       "maximum stock rounded to pallets first file %d (%s)" % (line2, rnd(parts),
       "same call" if rnd(parts) == line2 else "ruled out by 4.4"))
    sec = [u for u, r in c.last.iterrows() if r["regimen"] == "P2-AZ3LR"]
    ok(len(sec) > 50, "SF10 %d children on the paediatric second line move to the adult second line, not TLD (Annex 7.3)" % len(sec))
    ok("the band of the weight recorded at that visit" in annex, "SF11 the band applies to the weight recorded at the "
       "visit (Annex 7.1), on every route: same call")
    starts = [D.fromisoformat(p_["art_start_date"]) for p_ in pts.values() if p_["art_start_date"]]
    ok(not [d_ for d_ in starts if d_ > C.COUNT], "SF12 patients starting treatment after the count are the "
       "projection's (SOP 4.2); the register holds no child who started after 31 August 2026: same call")
    ages_end = [(D(2027, 6, 30) - c.dob[u]).days / 365.25 for u in c.on + c.cand]

    def under15(uids):
        return np.array([[1.0 if (e - c.dob[u]).days / 365.25 < 15 else 0.0 for e in c.fr.ends] for u in uids])
    o15 = K.total(c, P, S_on=c.S_on * under15(c.on), S_c=c.S_c * under15(c.cand))[0]
    ok("whatever their age by then" in sop and sum(a_ >= 15 for a_ in ages_end) > 0, "SF13 %d children turn 15 before "
       "30 June 2027 and stay in (SOP 4.2); dropped at their fifteenth birthday they file %d pallets (%s)"
       % (sum(a_ >= 15 for a_ in ages_end), rnd(o15), "same call" if rnd(o15) == line2 else "ruled out by 4.2"))
    dep = sum(b["qty"] for b in Wd["S"]["batches"] if b["status"] == "Usable" and b["warehouse"] == "Northern depot")
    ok(rnd(l1 + dep) != fig["line1"], "SF14 usable stock counts both warehouses (SOP 2.1): the Main warehouse alone "
       "files line 1 at %d pallets" % rnd(l1 + dep))
    ok("stays on TLD at later visits, whatever the weight recorded" in annex and back == 0,
       "SF15 a child started on TLD stays on it whatever the weight recorded (Annex 7.1); the register moves none back")
    o35 = K.total(c, K.P_noisy(c, thr=35.0)[0])[0]
    ok("lowers the weight from which TLD is given from 35 kg to 30 kg" in annex and rnd(o35) != line2,
       "SF16 the band for the window is 30 kg (Annex 7, 2026 edition, effective 1 March 2026); the 35 kg band of the "
       "register's earlier moves would file %d pallets" % rnd(o35))
    share = fam["golden"] - ci["soh"] * fam["golden"] / (fam["golden"] + ci["adults"])
    ok("netted on line 1 alone" in sop and rnd(share) != line2, "SF17 the stock and the lots are netted on line 1 alone "
       "(SOP 4.3); netting the children's share on line 2 would file %d pallets" % rnd(share))
    ok("is not counted from the month the patient leaves" in sop and rnd(rv["no_exits"]) == line2,
       "SF18 a child who leaves care is not counted (SOP 4.1); every child kept in care files %.0f bottles, %d pallets: "
       "same call" % (rv["no_exits"], rnd(rv["no_exits"])))

    # ------------------------------------------------------------------------------------------------ ASK
    g, res = CR.sheet(t)
    for k, val in fig["asks"].items():
        ok(g[k] == val, "ASK %s: %d" % (k, val))
    Pk = AS.Pack(t)
    for name, kw in (("the customer master's region", dict(region_route="label")),
                     ("the posting date", dict(date_route="posted")),
                     ("the registry's operational record for a reissued code", dict(region_route="registry_current")),
                     ("refused deliveries counted", dict(refusals="include")),
                     ("every return netted (refusals and short-dated stock alike)", dict(refusals="net_returns"))):
        a2, _ = AS.deliveries(Pk, **kw)
        moved = sum(1 for kk_ in a2 if a2[kk_] != g["delivered %s %s" % kk_])
        ok(moved == 12, "ASK device on deliveries, %s: moves %d of 12 figures" % (name, moved))
    for name, kw in (("the region stamped at submission", dict(region_route="label")),
                     ("the registry's operational record for a reissued code", dict(region_route="registry_current")),
                     ("the CMS product code alone (the partner donation left out)", dict(products="cms_code"))):
        b2, _ = AS.dispensing(Pk, **kw)
        moved = sum(1 for kk_ in b2 if b2[kk_] != g["dispensed %s %s" % kk_])
        ok(moved == 12, "ASK device on dispensing, %s: moves %d of 12 figures" % (name, moved))
    b3, _ = AS.dispensing(Pk, report_route="all")
    ok(sum(1 for kk_ in b3 if b3[kk_] != g["dispensed %s %s" % kk_]) >= 10, "ASK hazard: returned submissions summed "
       "move the dispensing figures (the latest submission is the approved one)")
    for name in ("cracker", "mirror", "cracker_reissue_cracked", "cracker_refusals_and_donation_cracked",
                 "cracker_refusals_cracked", "cracker_donation_cracked", "label_posted", "cracker_returns_netted"):
        ok(len(res[name]["hits"]) == 0, "ASK %s keeps %d of %d ask figures" % (name, len(res[name]["hits"]), res[name]["n"]))
    rn = res["cracker_reissue_cracked_returns_netted"]
    ok(not [h for h in rn["hits"] if h.startswith("delivered")], "ASK the reissued codes cracked with every return "
       "netted keeps %d of the 12 delivery figures (the short-dated stock returns break the tie with the refusals)"
       % len([h for h in rn["hits"] if h.startswith("delivered")]))
    p = CR.pair(res["cracker"]["kept"], res["mirror"]["kept"])
    ok(p <= 40, "ASK pair ceiling %.1f (40 or under)" % p)
    ok(CR.pair(res["cracker"]["kept"], res["cracker"]["kept"], True, True) <= 45, "ASK both top responses on the call: 45.0 or under")
    vals = sorted(fig["asks"].values())
    ok(len(set(vals)) == len(vals), "ASK no two ask figures are equal")

    # ------------------------------------------------------------------------------------------------ SEP
    call_files = {PK.F_LEG, PK.F_EPR, PK.F_PTS, PK.F_CW, PK.F_CODES, PK.F_PROJ, PK.F_STOCK, DOC.F_DOSING, DOC.F_SOP}
    ask_files = {PK.F_DEL, PK.F_POD, PK.F_ACC, PK.F_LMIS, PK.F_REG}
    src = open(os.path.join(HERE, "pack_read.py")).read() + open(os.path.join(HERE, "calc.py")).read()
    ok(not any(f in src for f in ask_files), "SEP the call's computation (pack_read, calc) opens no ask file: zero ask "
       "device rows in the call's population")
    ok(not (call_files & ask_files), "SEP the call's files and the ask files are disjoint")

    # ------------------------------------------------------------------------------------------------ REAL
    proj = DV.call_inputs(t)["adult_months"]
    ok(len(set(proj)) == len(proj), "REAL the projection's national months are all different")
    ok(fig["adults"] % 100 and fig["soh"] % 100 and fig["shipped"] % 100 and fig["call_unrounded"] % 100,
       "REAL no round headline total (adults %d, stock %d, shipments %d, line 2 before rounding %d)"
       % (fig["adults"], fig["soh"], fig["shipped"], fig["call_unrounded"]))
    # the register: ages spread, multi-month dispensing, site scales, season, puberty, the lag
    by_year = kids_p[kids_p.uid.isin(c.on + c.cand)].dob.map(lambda d_: d_.year).value_counts(normalize=True)
    ok(by_year.max() < 0.16 and (by_year > 0.02).sum() >= 10, "REAL the children under 15 spread over %d birth years, "
       "none above %.0f%% of them" % ((by_year > 0.02).sum(), 100 * by_year.max()))
    est = pdf_text(os.path.join(t, DOC.F_EST)).encode()
    n_mid = PK.children_on_art(Wd["W"], C.mi(2026, 6))
    n_reg = int(len(kids_p[(kids_p.dob > D(2011, 6, 30)) & (kids_p.art_start <= D(2026, 6, 30)) &
                           (kids_p.outcome.isna() | (kids_p.outcome_date > D(2026, 6, 30)))]))
    shown = "{:,}".format(int(round(n_mid, -2))).encode()
    ok(shown in est and abs(n_mid - n_reg) < 0.05 * n_mid, "REAL the estimates' children on treatment at mid-2026 "
       "(%s) are the register's children under 15 in care at 30 June 2026 (%d)" % (shown.decode(), n_reg))
    lastv = c.last.reindex(c.on + c.cand)
    ages = np.array([(C.COUNT - c.dob[u]).days / 365.25 for u in lastv.index])
    elig = ages >= 5
    mmd = float((lastv.months.values[elig] >= 2).mean())
    tri = float((lastv.months.values[elig] == 3).mean())
    yr = visits_p[(visits_p.date > D(2024, 8, 31)) & (visits_p.date <= D(2025, 8, 31))]
    pre = float((yr.groupby("uid").months.last() >= 2).mean())
    ok(mmd > 0.55 and pre < mmd, "REAL two- and three-month dispensing: at the count %.0f%% of the children aged five "
       "and over were on two or three months (%.0f%% on three), against %.0f%% a year before" % (100 * mmd, 100 * tri, 100 * pre))
    F_ = K.fitstats(c)
    res = F_["res"]
    fac_of = c.last.facility if "facility" in c.last else None
    mon = np.array([(C.COUNT + dt.timedelta(days=float(x) * K.DPM)).month for x in F_["x"]])
    sea = [float(np.mean(res[mon == m_])) for m_ in range(1, 13)]
    ok(max(sea) - min(sea) > 0.1, "REAL the season shows in the residuals: monthly means %.2f to %.2f kg"
       % (min(sea), max(sea)))
    ok(0.05 < c.lag < 0.2, "REAL the lag: %.1f%% of first readings of 30 kg or more since March 2026 held to the next "
       "visit" % (100 * c.lag))
    wsd = visits_p[visits_p.weight.notna()].groupby("uid").weight.std()
    ok(float((wsd.fillna(1) == 0).mean()) < 0.002, "REAL no child's weighings are a constant stream")
    wts = visits_p.weight.dropna()
    ok(float(wts.min()) >= 2.5 and float(wts.max()) < 120, "REAL every weighing is a plausible child's weight (%.1f to "
       "%.1f kg)" % (float(wts.min()), float(wts.max())))
    sb = [r["signed_by"] for r in csv.DictReader(open(os.path.join(t, PK.F_POD), encoding="utf-8"))]
    top = max(sb.count(x) for x in set(sb)) / len(sb)
    ok(top < 0.4, "REAL the proof of delivery's signer roles vary (top share %.2f)" % top)
    texts = []
    for f in files:
        if f.endswith((".csv", ".json")):
            texts.append((f, open(os.path.join(t, f), encoding="utf-8").read()))
    for f in files:
        if f.endswith(".pdf"):
            texts.append((f, pdf_text(os.path.join(t, f))))
    ok(not any(("\u2014" in s or "\u2013" in s) for _, s in texts), "REAL no em or en dash in a shipped text file")
    ok(not any(re.search(r"\b(fictional|fictitious|constructed for|this exercise|synthetic)\b", s, re.I) for _, s in texts),
       "REAL no shipped file says the pack was built (H24)")
    blob = b""
    for f in files:
        if f.endswith((".xlsx", ".pdf")):
            raw = open(os.path.join(t, f), "rb").read()
            blob += raw
            if f.endswith(".xlsx"):
                with zipfile.ZipFile(os.path.join(t, f)) as z:
                    blob += z.read("docProps/core.xml") + z.read("docProps/app.xml")
    ok(not re.search(rb"openpyxl|ReportLab|reportlab|matplotlib", blob), "REAL no writing library's name in a container (H1)")
    # H25: every shipped document opens with every reader a solver would use, and the decisive sentences read in each
    decisive = {DOC.F_DOSING: ["stays on TLD at later visits, whatever the weight recorded",
                               "lowers the weight from which TLD is given from 35 kg to 30 kg",
                               "the band of the weight recorded at that visit"],
                DOC.F_SOP: ["The TLD order has two lines", "netted on line 1 alone", "(8,064 bottles) to the pallet",
                            "whatever their age by then", "is not counted from the month the patient leaves"],
                DOC.F_EST: ["0-14"]}
    for f, sents in decisive.items():
        got = pdf_readers(os.path.join(t, f))
        miss = {k: [s_ for s_ in sents if s_ not in v_] for k, v_ in got.items() if k != "strict_equals_lenient"}
        ok(not any(miss.values()) and got["strict_equals_lenient"], "REAL %s opens with %s and every decisive "
           "sentence reads in each; strict and lenient text agree (H25)" % (f, ", ".join(sorted(miss))))
    late_rows = []
    for f, col in ((PK.F_EPR, "visit_date"), (PK.F_PTS, "outcome_entered"), (PK.F_POD, "signed_on"),
                   (PK.F_DEL, "posting_date"), (PK.F_VL, "result_date")):
        for r in csv.DictReader(open(os.path.join(t, f), encoding="utf-8")):
            if r[col] and D.fromisoformat(r[col][:10]) > C.PULL:
                late_rows.append((f, r[col]))
    ok(not late_rows, "REAL no record dated after the pull of 2 September 2026 outside the forward-looking columns")
    names = [C.PEOPLE[k] for k in C.PEOPLE]
    card = json.load(open(os.path.join(TASK, "..", ".claude", "skills", "fingerprint", "cards", "task170.json")))
    ok(sorted(names) == sorted(card["world"]["people"]), "REAL the personas are the card's, drawn with guard.py names")

    # ------------------------------------------------------------------------------------------------ DIST
    gen = "".join(open(p_).read() for p_ in glob.glob(os.path.join(HERE, "*.py"))
                  if os.path.basename(p_) in ("calc.py", "asks.py", "pack_read.py", "verify.py", "ladder.py"))
    for f in meta["distractor_files"]:
        ok(f not in gen, "DIST %s is read by no computation of the call or an ask (deleting it changes nothing)" % f)

    print("%d assertions, %d failed" % (N[0], len(FAILS)))
    return 0 if not FAILS else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
