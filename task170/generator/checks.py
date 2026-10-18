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


def rnd(x):
    return int(C.LOT * round(x / C.LOT))


def edge(x):
    return C.LOT / 2 - abs(x - rnd(x))


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
    upid = Wd["W"]["upid"]
    ok(len(kids_c) == len(kids_p) and len(visits_c) == len(visits_p),
       "R0 the pack's register, read back (layouts joined, crosswalk, June 2024 once, re-sent rows dropped), has the "
       "clean truth's %d children and %d visits" % (len(kids_p), len(visits_p)))
    fam, c = LD.family(kids_p, visits_p)
    famc, cc = LD.family(kids_c, visits_c)
    ok(abs(fam["golden"] - famc["golden"]) < 1e-6, "R0 the golden children's need is the same on the pack and on the "
       "clean truth: %.1f bottles" % fam["golden"])
    ci = DV.call_inputs(t)
    base = ci["adults"] - ci["soh"] - ci["shipped"]
    gold = base + fam["golden"]
    ok(rnd(gold) == fig["order"], "FAM the golden order %.0f rounds to %d" % (gold, fig["order"]))
    ok(edge(gold) >= C.LOT / 4, "FAM the golden sits %.0f bottles inside its step (a quarter step is 1,250)" % edge(gold))
    for k in LD.FAMILY:
        v = fam[k]
        ok(rnd(base + v) == fig["order"] and edge(base + v) >= 750, "FAM %s: children %.0f, order %.0f rounds "
           "to %d (%.0f inside the step, 750 or more)" % (k, v, base + v, rnd(base + v), edge(base + v)))
    for k in LD.ALSO:
        v = fam[k]
        ok(rnd(base + v) == fig["order"], "FAM %s (reported beside the family): children %.0f, order %.0f rounds to "
           "%d (%.0f inside the step)" % (k, v, base + v, rnd(base + v), edge(base + v)))
    for keys in LD.extreme_pairs(fam):
        v = LD.compound(kids_p, visits_p, keys)
        ok(rnd(base + v) == fig["order"] and edge(base + v) >= 500, "FAM the compound choice %s: children %.0f, order "
           "%.0f rounds to %d (%.0f inside the step, 500 or more)" % (" with ".join(keys), v, base + v, rnd(base + v),
                                                                       edge(base + v)))
    sh = LD.shrunk(c)
    for k, v in sorted(sh.items(), key=lambda kv: kv[1]):
        print("INFO  SHR %s: children %.0f, order %d (%s)" % (k, v, rnd(base + v), "in the step" if rnd(base + v) ==
              fig["order"] else "outside the step"))
    tau, Q, kq = K.slope_heterogeneity(c)
    ok(tau > 0.015 and Q / (kq - 1) > 1.5, "SHR the candidates' growth slopes vary between children by more than "
       "their estimation error: tau %.3f kg a month, Q %.0f on %d degrees of freedom" % (tau, Q, kq - 1))
    # one sigma: candidates resampled with replacement
    P, sig = K.P_noisy(c, thr=30.0)
    contrib = (P * c.S_c).sum(1) + C.MAX_MONTHS * (P[:, -1] * c.S_c[:, -1])
    rng = np.random.default_rng(170)
    boots = [contrib[rng.integers(0, len(contrib), len(contrib))].sum() for _ in range(200)]
    sd = float(np.std(boots))
    ok(sd < edge(gold), "FAM a one-sigma move of the switch increment (%.0f bottles, candidates resampled) leaves the "
       "order in its step (%.0f inside)" % (sd, edge(gold)))

    # ------------------------------------------------------------------------------------------------ R1
    v = visits_p
    ok(v.weight.notna().sum() > 500000, "R1 the golden reads the register's weighings at the child-visit grain: %d "
       "weighings" % v.weight.notna().sum())
    heads = []
    for f in files:
        if f.endswith(".csv"):
            heads += next(csv.reader(open(os.path.join(t, f), encoding="utf-8")))
    bad = [h for h in heads if re.search(r"switch|forecast|transition|project", h, re.I)]
    ok(not bad, "R1 no shipped column holds the switch, a forecast or a transition: %s" % (bad or "none"))

    sw_ok = sw_bad = left = 0
    for u, g_ in visits_p.sort_values(["uid", "date"]).groupby("uid"):
        prev = None
        for r_ in g_.itertuples():
            if prev in ("P1-AB3D10", "P1-AB3D50"):
                heavy = r_.weight == r_.weight and r_.weight >= 30.0
                if r_.regimen == C.REG_TLD:
                    sw_ok, sw_bad = sw_ok + heavy, sw_bad + (not heavy)
                elif heavy:
                    left += 1
            prev = r_.regimen
    ok(sw_ok > 1000 and sw_bad == 0 and left == 0, "R1 the register obeys the annex's band as the write-up states it: "
       "%d moves onto TLD, each at a reading of 30.0 kg or more; %d without one; %d readings of 30.0 kg or more left on a "
       "paediatric first line (H6)" % (sw_ok, sw_bad, left))

    # ------------------------------------------------------------------------------------------------ R2
    def order_on(view):
        f2, c2 = LD.family(*view)
        return base + f2["golden"]
    for label, kw in (("the June 2024 visits kept twice", dict(dedupe_overlap=False)),
                      ("the re-sent EPR rows kept", dict(drop_resent=False)),
                      ("the legacy rows not linked through the crosswalk", dict(link_legacy=False))):
        o2 = order_on(PR.register_view(t, **kw))
        ok(rnd(o2) == fig["order"], "R2 %s: order %.0f, still %d" % (label, o2, fig["order"]))
    ok(rnd(base + fam["q1"]) == fig["order"], "R2 collections without a weighing ignored in the schedule: still %d" % fig["order"])
    kk = kids_p.copy()
    pts = {r["upid"]: r for r in csv.DictReader(open(os.path.join(t, PK.F_PTS), encoding="utf-8"))}
    ent = kk.uid.map(lambda u: pts[u]["outcome_entered"])
    kk.loc[[bool(e) and D.fromisoformat(e) > C.COUNT for e in ent], ["outcome", "outcome_date"]] = None
    o2 = order_on((kk, visits_p))
    ok(rnd(o2) == fig["order"], "R2 outcomes entered after the count read as not yet known: order %.0f, still %d" % (o2, fig["order"]))
    ok(sum(1 for p in pts.values() if p["dob_estimated"] == "Y") > 1000, "R2 estimated dates of birth are recorded as "
       "the register holds them (1 July of the year), and the population's age line sits far from the cohort")

    # ------------------------------------------------------------------------------------------------ R3 and the ladder
    rv, info = LD.rivals(c)
    rvc, _ = LD.rivals(cc)
    ok(rnd(base + rvc["smooth_all"]) != fig["order"], "R3a the default path on the clean truth (each child moved when "
       "its growth line through every weighing reaches 30 kg, every filed rule applied) files %d, not %d"
       % (rnd(base + rvc["smooth_all"]), fig["order"]))
    ok(rnd(base + rvc["smooth_all"]) == fig["default_order"], "R3a the default path's order is the write-up's %d" % fig["default_order"])
    ok(rnd(base + famc["golden"]) == fig["order"], "R3b the default path with only the switch read off a scheduled "
       "weighing around the same line files the golden %d" % fig["order"])
    for k in ("band_0.5", "recent_3", "trend", "chain_12", "smooth_12"):
        ok(rnd(base + rvc[k]) != fig["order"], "R3b a lower rung's single correction (%s) leaves the call at %d" % (k, rnd(base + rvc[k])))
    lo, hi = rnd(gold) - C.LOT / 2, rnd(gold) + C.LOT / 2
    for k, val in sorted(rv.items(), key=lambda kv: abs(kv[1] - fam["golden"])):
        if k == "crossing_age_window":
            continue
        o = base + val
        out = o < lo or o >= hi
        ok(out, "LAD %s: children %.0f (%+.0f), order %d, %.0f bottles outside the step" %
           (k, val, val - fam["golden"], rnd(o), (lo - o) if o < lo else (o - hi)))
    ok(rnd(base + rv["mean_curve"]) != fig["order"], "LAD the mean growth curve (each child on the register's median "
       "weight-for-age curve from its own level) files %d" % rnd(base + rv["mean_curve"]))

    bt = LD.backtests(kids_p, visits_p)
    ar = LD.age_rule(c)
    av = {k: v[0] for k, v in ar.items()}
    inside = sorted(k for k, v in av.items() if rnd(base + v) == fig["order"])
    span = (max(av.values()) - min(av.values())) / C.LOT
    ok(span >= 4, "LAD the crossing-age rule (each child switched on reaching the age at which the register's median "
       "weight for age reaches 30 kg) files %d to %d across its %d binnings, %.1f steps apart"
       % (rnd(base + min(av.values())), rnd(base + max(av.values())), len(av), span))
    ok(not [k for k in inside if "interpolated" in k], "LAD the crossing-age rule with the crossing interpolated "
       "between bins misses the step under every look-back and bin width (%s)"
       % ", ".join("%d" % rnd(base + v) for k, v in sorted(av.items()) if "interpolated" in k))
    ok(len(inside) <= 0.3 * len(av), "LAD the crossing-age rule lands in the step under %d of %d binnings, each "
       "where the bin label puts the crossing at %s years" % (len(inside), len(av),
       ", ".join(sorted({"%.2f" % ar[k][1]["F"] for k in inside})) or "no age"))
    e_ca = [100.0 * (b["crossing_age_window"] - b["actual"]) / b["actual"] for b in bt]
    ok(sum(abs(e) >= 30 for e in e_ca) >= 2, "LAD the crossing-age rule out of sample: %s per cent"
       % ", ".join("%+.0f" % e for e in e_ca))

    # ------------------------------------------------------------------------------------------------ OOS
    for b in bt:
        a = b["actual"]
        e = lambda k: 100.0 * (b[k] - a) / a
        ok(abs(e("golden")) <= 6.0, "OOS from %s (%d months): the golden %+.1f%% of the %d bottle-months the register "
           "shows" % (b["origin"], b["months"], e("golden"), a))
        ok(e("smooth_all") <= -25, "OOS from %s: the growth line %+.1f%%" % (b["origin"], e("smooth_all")))
        ok(e("band_0.5") >= 20, "OOS from %s: the band rates %+.1f%%" % (b["origin"], e("band_0.5")))
        ok(e("recent_3") <= -20 and e("trend") <= -25, "OOS from %s: the last three months' switches %+.1f%%, the trend "
           "%+.1f%%" % (b["origin"], e("recent_3"), e("trend")))
        ok(e("noisy_12") >= 25 and e("noisy_monthly") >= 10, "OOS from %s: twelve-month lines %+.1f%%, a weighing "
           "every month %+.1f%% (each over a tenth)" % (b["origin"], e("noisy_12"), e("noisy_monthly")))
        mem = ("thr2995", "win24", "q1", "sig_rms", "sig_diff", "sig_near", "pooled_everyone")
        ok(all(abs(e(k)) <= 10.0 for k in mem), "OOS from %s: the family's members within a tenth (%s)"
           % (b["origin"], ", ".join("%s %+.1f%%" % (k, e(k)) for k in mem)))
        print("INFO  OOS from %s: the MAD scatter, reported beside the family, %+.1f%%" % (b["origin"], e("sig_mad")))
        ok(all(e(k) <= -8.0 for k in LD.SHRUNK), "OOS from %s: slopes pooled or shrunk under-forecast (%s)"
           % (b["origin"], ", ".join("%s %+.1f%%" % (k, e(k)) for k in LD.SHRUNK)))

    # ------------------------------------------------------------------------------------------------ SF
    ok(not any(k.dob == D(2011, 8, 31) for k in kids_p.itertuples()), "SF1 under 15 at the count: no date of birth "
       "on 31 August 2011, so born after it and under 15 select the same children")
    sop = " ".join(p_ for _, ps in DOC.SOP for p_ in ps)
    late = [u for u in c.cand if (C.COUNT - c.last.loc[u, "date"]).days > 92]
    c_late = K.context(kids_p[~kids_p.uid.isin(late)], visits_p)
    o_late = base + K.total(c_late, K.P_noisy(c_late, thr=30.0)[0])[0]
    ok("(no outcome entered)" in sop, "SF2 on treatment is no outcome entered (SOP 4.2); dropping the %d candidates "
       "last seen over three months before the count files %d (%s)"
       % (len(late), rnd(o_late), "same call" if rnd(o_late) == fig["order"] else "ruled out by 4.2"))
    Cm = K.total(c, P)[1]
    half = fam["golden"] - 0.5 * float(((np.diff(np.c_[np.zeros(len(c.cand)), P], axis=1)) * c.S_c).sum())
    ok("one bottle for each patient on the regimen at the end of the month" in sop,
       "SF3 one bottle for each child on TLD at a month's end (SOP 4.1); half a bottle in the switch month would file "
       "%d (%s)" % (rnd(base + half), "same call" if rnd(base + half) == fig["order"] else "ruled out by 4.1"))
    avg_rule = ci["adults"] - C.MAX_MONTHS * ci["adult_months"][-1] + C.MAX_MONTHS * np.mean(ci["adult_months"][4:])
    ok(rnd(avg_rule + fam["golden"] - ci["soh"] - ci["shipped"]) != fig["order"], "SF4 the maximum stock level is six "
       "months of June 2027's forecast (SOP 3.2); six months of the cycle's average files %d"
       % rnd(avg_rule + fam["golden"] - ci["soh"] - ci["shipped"]))
    quar = sum(b["qty"] for b in Wd["S"]["batches"] if b["status"] == "Quarantined")
    ok(rnd(gold - quar) != fig["order"], "SF5 usable stock leaves out the quarantined batch (SOP 3.3): with it %d" % rnd(gold - quar))
    planned = sum(s["qty"] for s in Wd["S"]["ship"] if s["status"] == "Planned")
    ok(rnd(gold - planned) != fig["order"], "SF6 the planned C7 call-off is not on order (SOP 3.3): with it %d" % rnd(gold - planned))
    sep_dec = sum(ci["adult_months"][:4]) + float(sum(Cm[:4]))
    ok(rnd(gold - sep_dec) != fig["order"], "SF7 the window opens on 1 September 2026 (SOP 3.1): from 1 January %d" % rnd(gold - sep_dec))
    due = [x[3] for x in ci["shipments"]]
    ok(all(d_.date() <= D(2026, 12, 31) for d_ in due), "SF8 every confirmed lot is due by 31 December 2026, so "
       "'confirmed delivery on or before the last day of the cycle ordered' (SOP 3.1), due within C6 and due before "
       "the window closes select the same %d lots: same call" % len(due))
    parts = rnd(ci["adults"]) + rnd(fam["golden"]) - ci["soh"] - ci["shipped"]
    ok(rnd(sum(ci["adult_months"]) + C.MAX_MONTHS * ci["adult_months"][-1] + fam["golden"] - ci["soh"] - ci["shipped"])
       == fig["order"], "SF9 the order rounded once at the end (the prompt's last sentence) is %d; rounding the adults' "
       "and the children's parts to 5,000 first files %d (%s)" % (fig["order"], rnd(parts),
       "same call" if rnd(parts) == fig["order"] else "ruled out by the prompt"))
    sec = [u for u, r in c.last.iterrows() if r["regimen"] == "P2-AZ3LR"]
    ok(len(sec) > 50, "SF10 %d children on the paediatric second line move to the adult second line, not TLD (Annex 7.3)" % len(sec))
    ok("the band of the weight recorded at that visit" in " ".join(DOC.DOSING_INTRO), "SF11 the band applies to the "
       "weight recorded at the visit (Annex 7.1), on every route: same call")
    starts = [D.fromisoformat(p_["art_start_date"]) for p_ in pts.values() if p_["art_start_date"]]
    ok(not [d_ for d_ in starts if d_ > C.COUNT], "SF12 patients starting treatment after the count are the "
       "projection's (SOP 4.2); the register holds no child who started after 31 August 2026: same call")
    ages_end = [(D(2027, 6, 30) - c.dob[u]).days / 365.25 for u in c.on + c.cand]

    def under15(uids):
        return np.array([[1.0 if (e - c.dob[u]).days / 365.25 < 15 else 0.0 for e in c.fr.ends] for u in uids])
    o15 = base + K.total(c, P, S_on=c.S_on * under15(c.on), S_c=c.S_c * under15(c.cand))[0]
    ok("whatever their age by then" in sop and sum(a >= 15 for a in ages_end) > 0, "SF13 %d children turn 15 before "
       "30 June 2027 and stay in (SOP 4.2); dropped at their fifteenth birthday they file %d (%s)"
       % (sum(a >= 15 for a in ages_end), rnd(o15), "same call" if rnd(o15) == fig["order"] else "ruled out by 4.2"))
    dep = sum(b["qty"] for b in Wd["S"]["batches"] if b["status"] == "Usable" and b["warehouse"] == "Northern depot")
    ok(rnd(gold + dep) != fig["order"], "SF14 usable stock counts both warehouses (SOP 2.1): the Main warehouse alone files %d" % rnd(gold + dep))

    # ------------------------------------------------------------------------------------------------ ASK
    g, res = CR.sheet(t)
    for k, val in fig["asks"].items():
        ok(g[k] == val, "ASK %s: %d" % (k, val))
    Pk = AS.Pack(t)
    for name, kw in (("the customer master's region", dict(region_route="label")),
                     ("the posting date", dict(date_route="posted")),
                     ("the registry's operational record for a reissued code", dict(region_route="registry_current")),
                     ("refused deliveries counted", dict(refusals="include"))):
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
                 "cracker_refusals_cracked", "cracker_donation_cracked", "label_posted"):
        ok(len(res[name]["hits"]) == 0, "ASK %s keeps %d of %d ask figures" % (name, len(res[name]["hits"]), res[name]["n"]))
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
    ok(fig["adults"] % 100 and fig["soh"] % 100 and fig["shipped"] % 100 and int(gold) % 100,
       "REAL no round headline total (adults %d, stock %d, shipments %d, order before rounding %.0f)"
       % (fig["adults"], fig["soh"], fig["shipped"], gold))
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
            texts.append((f, open(os.path.join(t, f), "rb").read().decode("latin-1")))
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
