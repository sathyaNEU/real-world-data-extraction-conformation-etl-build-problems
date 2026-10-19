"""task270's checks, run by build.py on every build: the input gates; the client's three rules executed on the
generator's clean truth (R1 the raw material ships, R2 each Layer 1 item neutral, R3a the analyst test, R3b the
decisive step alone, R3c no plant); the ladder, the threshold family and the margins on the shipped pack; the semantic
fork rows; the asks tied back to the books, their stops, the forcing of each device and the separation line; the
cracker; the realism sweep; Gate G and the leak greps."""
import collections
import copy
import csv
import datetime as dt
import json
import os
import re

import analysis as A
import books as BK
import common as K
import cracker as CR
import pack as PK
import world as W

N = {"ok": 0, "fail": 0}
FAILS = []
HERE = os.path.dirname(os.path.abspath(__file__))


def check(label, cond, detail=""):
    if cond:
        N["ok"] += 1
    else:
        N["fail"] += 1
        FAILS.append("%s %s" % (label, detail))


def _pdf_text(path):
    from pypdf import PdfReader
    return re.sub(r"\s+", " ", " ".join(p.extract_text() for p in PdfReader(path).pages))


def band(v):
    return sorted(A.top3(v)["band"])


# ------------------------------------------------------------------------------------------------- the clean truth
def clean(w, T=A.T_GOLDEN):
    """The world before any record is written: exposure from the segments, every accident that costs the Society,
    the ones claimed under the 2024 scale, the Step Protection lift and the size-based recovery on the true costs."""
    E = W.exposure(w["segs"])
    Es = collections.defaultdict(float)
    for s in w["segs"]:
        for y in K.ACC_YEARS:
            a, b = max(s["a"], dt.date(y, 1, 1)), min(s["b"], dt.date(y + 1, 1, 1))
            if b > a:
                Es[(s["region"], s["step"], s["protected"])] += (b - a).days / 365.0
    acc = [e for e in w["events"] if e["kind"] in ("AF", "NAF") and e["day"].year in K.ACC_YEARS and W.costs_mutual(e)]
    made = [e for e in acc if e["claimed"]]
    truth = {c: 100.0 * sum(1 for e in acc if e["region"] == c) / E[c] for c in K.CODES}
    rep = {c: 100.0 * sum(1 for e in made if e["region"] == c) / E[c] for c in K.CODES}
    num = collections.Counter((e["protected"]) for e in made if e["step"] in K.PILOT_STEPS)
    den = collections.Counter()
    for (r, s, p), v in Es.items():
        if s in K.PILOT_STEPS:
            den[p] += v
    u = (num[True] / den[True]) / (num[False] / den[False])
    lift = {c: 100.0 * sum(u if (e["step"] in K.PILOT_STEPS and not e["protected"]) else 1.0
                           for e in made if e["region"] == c) / E[c] for c in K.CODES}
    full = [e["cost"] for e in made if e["step"] == 0 or e["protected"]]
    S = sum(1 for x in full if x > T) / len(full)
    rec = {c: 100.0 * sum(1 for e in made if e["region"] == c and e["cost"] > T) / S / E[c] for c in K.CODES}
    absorbed_max = max(e["cost"] for e in acc if not e["claimed"])
    return dict(E=E, truth=truth, rep=rep, lift=lift, rec=rec, u=u, absorbed_max=absorbed_max)


def books_truth(bk):
    """The asks' answers from the books themselves (before any file is written)."""
    n = {c: 0 for c in K.CODES}
    cost = {c: 0.0 for c in K.CODES}
    for g in bk["glass"]:
        if g["customer"]:
            continue
        if g["network"]:
            if g["booked"].year == 2025:
                n[g["region"]] += 1
                cost[g["region"]] += g["net"] + round(g["net"] * 0.2, 2) + g["calib"] + round(g["calib"] * 0.2, 2)
        elif g["claim"] is not None and g["claim"]["notified"].year == 2025:
            c = g["claim"]
            day = c["notified"].date()
            d = BK.term_on(bk["_terms"][g["term"]], day)[0]
            r = W.district_region(d, day)
            n[r] += 1
            cost[r] += c["paid"] + c["outstanding"]
    glass = dict(n=n, avg={c: cost[c] / n[c] for c in K.CODES})
    proceeds = collections.defaultdict(float)
    for s in bk["salvage"]:
        proceeds[id(s["claim"])] += s["proceeds"]
    tn = {c: 0 for c in K.CODES}
    tc = {c: 0.0 for c in K.CODES}
    for th in bk["thefts"]:
        if th["day"].year != 2025 or not th["claims"]:
            continue
        inc = sum(c["paid"] + c["outstanding"] for c in th["claims"])
        if inc <= 0:
            continue
        tn[th["region"]] += 1
        tc[th["region"]] += inc - sum(proceeds[id(c)] for c in th["claims"])
    theft = dict(n=tn, avg={c: tc[c] / tn[c] for c in K.CODES})
    return glass, theft


# ------------------------------------------------------------------------------------------------- readings
def ladder(P, **kw):
    E = {k[0]: v for k, v in PK.exposure(P, K.ACC_YEARS).items()}
    skipped = []
    Acl = A.accident_claims(P, skipped=skipped, **kw)
    _, R0 = A.reported(E, Acl)
    _, _, R2 = A.recovered(E, Acl)
    return dict(R0=R0, R2=R2, skipped=len(skipped))


def variant(P, name):
    Q = copy.copy(P)
    if name == "mid-term adjustments ignored":
        Q["terms"] = [dict(t, mtas=[]) for t in P["terms"]]
    elif name == "the current region map throughout":
        rm = copy.copy(P["rmap"])
        rm.by = {d: [(dt.date(2019, 1, 1), dt.date(2099, 12, 31), v[-1][2])] for d, v in P["rmap"].by.items()}
        rm.changes = []
        Q["rmap"] = rm
    elif name == "the legacy expiry date read as the day cover ends":
        Q["terms"] = [dict(t, end=min(t["end"], t["expiry"] - dt.timedelta(days=1))) if t["sys"] == "L" else t
                      for t in P["terms"]]
    elif name == "cancellations ignored":
        Q["terms"] = [dict(t, end=t["expiry"]) for t in P["terms"]]
    elif name == "the crosswalk ignored":
        Q["xw"] = {}
    else:
        raise KeyError(name)
    if "terms" in Q and Q["terms"] is not P["terms"]:
        by_ref = {}
        for t in Q["terms"]:
            by_ref.setdefault(t["ref"], []).append(t)
        for v in by_ref.values():
            v.sort(key=lambda t: t["start"])
        Q["by_ref"] = by_ref
    return Q


def run(task, b, fig, res):
    target = os.path.join(task, "target")
    w, bk = b["w"], b["bk"]
    bk["_terms"] = w["terms"]
    P = res["P"]
    gold = ["NWE", "WMI", "YHU"]
    wrong = ["SEA", "WMI", "YHU"]

    # ------------------------------------------------------------------ input gates
    files = sorted(os.listdir(target))
    check("INPUT ten or more files", len(files) >= 10, len(files))
    exts = {f.rsplit(".", 1)[-1] for f in files}
    check("INPUT three or more formats", len(exts) >= 3, exts)
    check("INPUT a file of 25,000 rows or more", max(b["counts"].values()) >= 25000, max(b["counts"].values()))
    check("INPUT every file in the registry is shipped", set(K.FILES.values()) == set(files), set(files) ^ set(K.FILES.values()))
    meta = json.load(open(os.path.join(task, "metadata.json")))
    check("INPUT two or more distractors named in metadata", len(meta["distractors"]) >= 2)
    for d in meta["distractors"]:
        check("INPUT distractor shipped " + d, d in files)
        check("INPUT distractor not named for its role " + d, "distract" not in d.lower())
    check("INPUT every file has provenance", set(meta["provenance"]) >= set(files))
    contents = open(os.path.join(target, K.FILES["contents"]), encoding="utf-8").read()
    listed = {l.strip() for l in contents.splitlines() if l.strip() and not l.startswith(" ") and "." in l
              and not l.startswith("Pricing")}
    check("INPUT contents lists every other file (H9)", listed == set(files) - {K.FILES["contents"]},
          listed ^ (set(files) - {K.FILES["contents"]}))
    texts = {k: _pdf_text(os.path.join(target, K.FILES[k])) for k in ("scale", "basis", "guide")}
    for k in ("pol_legacy", "pol_platform", "crosswalk", "mta", "clm_legacy", "clm_platform", "glass", "salvage",
              "regions"):
        check("INPUT the data guide names %s" % K.FILES[k], K.FILES[k] in texts["guide"].replace(" ", ""))

    # ------------------------------------------------------------------ R3a and R3b on the clean truth
    cl = clean(w)
    check("R3a the analyst test: the reported frequency on the clean truth files the wrong band", band(cl["rep"]) == wrong,
          band(cl["rep"]))
    check("R3a the Step Protection lift on the clean truth keeps South East in band C", "SEA" in band(cl["lift"]) and
          "NWE" not in band(cl["lift"]), band(cl["lift"]))
    check("R3b the decisive step alone on the clean truth files the golden", band(cl["rec"]) == gold, band(cl["rec"]))
    check("R3 the clean truth's band (every accident that costs the Society) is the golden", band(cl["truth"]) == gold,
          band(cl["truth"]))
    check("R3 the threshold clears every absorbed claim", cl["absorbed_max"] < A.T_GOLDEN, cl["absorbed_max"])
    check("R3 the pack's exposure is the clean truth's", all(abs(res["E"][c] - cl["E"][c]) < 1e-6 for c in K.CODES))
    check("R3 the pack's reported frequency is the clean truth's", all(abs(res["R0"][c] - cl["rep"][c]) < 1e-9
                                                                       for c in K.CODES))
    check("R3 the lift factor on the pack is the clean truth's", abs(res["u"] - cl["u"]) < 1e-9, (res["u"], cl["u"]))

    # ------------------------------------------------------------------ R1: the field's raw material ships
    def hdr(k):
        with open(os.path.join(target, K.FILES[k]), encoding="utf-8") as f:
            return next(csv.reader(f))
    check("R1 the legacy claims carry each claim's amounts, fault and dates",
          {"PAID_AMT", "OS_AMT", "FAULT", "LOSS_DATE", "POLICY_NO"} <= set(hdr("clm_legacy")))
    check("R1 the platform claims carry each claim's amounts, liability and dates",
          {"paid_gbp", "outstanding_gbp", "liability", "loss_date", "policy_number"} <= set(hdr("clm_platform")))
    check("R1 the policy years carry the step and Step Protection",
          {"NCD_STEP", "STEP_PROTECTION"} <= set(hdr("pol_legacy")) and {"ncd_step", "step_protection"} <= set(hdr("pol_platform")))
    for k in ("pol_legacy", "pol_platform", "clm_legacy", "clm_platform", "mta", "glass", "regions", "crosswalk"):
        h = " ".join(hdr(k)).lower().replace("age_band", "age")
        for wd in ("frequency", "absorb", "would", "2027", "band", "unreported"):
            check("R1 no shipped column names the deciding quantity (%s, %s)" % (k, wd), wd not in h)
    check("R1 every 2024 and 2025 accident claim joins a policy year", ladder(P)["skipped"] == 0, ladder(P)["skipped"])

    # ------------------------------------------------------------------ R2: each Layer 1 item is neutral
    for name in ("mid-term adjustments ignored", "the current region map throughout",
                 "the legacy expiry date read as the day cover ends", "cancellations ignored", "the crosswalk ignored"):
        lv = ladder(variant(P, name))
        check("R2 neutral: %s keeps the call%s" % (name, " (SF12)" if name == "cancellations ignored" else ""),
              band(lv["R2"]) == gold, band(lv["R2"]))
        check("R2 neutral: %s keeps the default path wrong" % name, band(lv["R0"]) == wrong, band(lv["R0"]))
        check("R2 neutral: %s keeps the first region below" % name, A.top3(lv["R2"])["below"] == "SEA",
              A.top3(lv["R2"])["below"])
    for name, kw in (("SF1 liability settled only", dict(keep=lambda c: c["liab"] != "P")),
                     ("SF2 paid above nil only", dict(keep=lambda c: c["paid"] > 0)),
                     ("SF2 net of recoveries above nil", dict(keep=lambda c: c["incurred"] - c["rec"] > 0)),
                     ("SF8 by notification date", dict(when="notified"))):
        lv = ladder(P, **kw)
        check("SF %s keeps the call" % name, band(lv["R2"]) == gold, band(lv["R2"]))
        check("SF %s keeps the default path wrong" % name, band(lv["R0"]) == wrong, band(lv["R0"]))
    # the legacy amounts read as pounds: loud (the median accident claim becomes six figures), the reported count
    # (incurred above nil) does not move
    leg = sorted(c["incurred"] for c in P["claims"] if c["sys"] == "L" and c["type"] == "ACC" and c["incurred"] > 0)
    check("R2 the legacy amounts read as pounds are loud: median accident claim over 100,000",
          leg[len(leg) // 2] * 100 > 100000, leg[len(leg) // 2] * 100)
    check("SF6 the claims as recorded (the reported frequency) file another band: the stump, not a reading",
          band(res["R0"]) != gold, band(res["R0"]))
    check("SF7 the Step Protection holders' claims taken as made (recovery on the insured steps only) keep the call",
          band(res["R2i"]) == gold, band(res["R2i"]))
    Q10 = copy.copy(P)
    Q10["claims"] = [dict(c, type="ACC") if c["type"] in ("WSC", "THF", "FIR") else c for c in P["claims"]]
    lv = ladder(Q10)
    check("SF10 windscreen, theft and fire claims counted as accident claims keep the call", band(lv["R2"]) == gold,
          band(lv["R2"]))
    check("SF3 vehicle-years over 365.25 keep the call (a common factor)", band({c: v * 365.25 / 365 for c, v in
                                                                                  res["R2"].items()}) == gold)
    check("SF4 the region at inception is mid-term adjustments ignored (asserted above)", True)
    check("SF9 no tie at the band's edge on the golden", A.top3(res["R2"])["margin"] > 0.05, A.top3(res["R2"])["margin"])
    check("SF11 every claim number is unique across both exports", len({c["no"] for c in P["claims"]}) == len(P["claims"]))
    check("SF5 the remap is in force on the day (two districts, both moved region)",
          {d for d, v in P["rmap"].by.items() if len(v) > 1} == set(K.REMAP))

    # ------------------------------------------------------------------ R3c: no plant
    for k in ("pol_legacy", "pol_platform", "clm_legacy", "clm_platform", "mta", "glass"):
        rows = list(csv.reader(open(os.path.join(target, K.FILES[k]), encoding="utf-8")))[1:]
        body = [tuple(r[1:]) for r in rows]
        runs = sum(1 for i in range(2, len(body)) if body[i] == body[i - 1] == body[i - 2])
        check("R3c no copied block of rows, three alike in a row (%s)" % k, runs == 0, runs)
    for k, t in texts.items():
        for nm in K.NAME.values():
            check("R3c no shipped document names a region (%s, %s)" % (k, nm), nm not in t)

    # ------------------------------------------------------------------ the ladder on the pack
    check("LADDER R0 (reported) files South East, West Midlands, Yorkshire and the Humber", band(res["R0"]) == wrong,
          band(res["R0"]))
    check("LADDER R0's first region below is North West", A.top3(res["R0"])["below"] == "NWE")
    check("LADDER R1 (lift on steps 6 to 9) keeps South East in, North West out", "SEA" in band(res["R1"]) and
          "NWE" not in band(res["R1"]), band(res["R1"]))
    check("LADDER R1b (lift on every step) keeps South East in, North West out", "SEA" in band(res["R1b"]) and
          "NWE" not in band(res["R1b"]), band(res["R1b"]))
    check("LADDER R2 (golden) files North West, West Midlands, Yorkshire and the Humber", band(res["R2"]) == gold)
    check("LADDER R2's first region below is South East", A.top3(res["R2"])["below"] == "SEA")
    check("LADDER R2 recovered only on the insured steps agrees", band(res["R2i"]) == gold, band(res["R2i"]))
    for (T, src), v in sorted(res["grid"].items()):
        check("LADDER the golden band holds at T=%d from %s" % (T, src), band(v) == gold, band(v))
        check("LADDER margin at T=%d from %s is 5 per cent or more" % (T, src), A.top3(v)["margin"] >= 0.05,
              A.top3(v)["margin"])
    pos = {nm: A.top3(res[nm])["order"].index("NWE") for nm in ("R0", "R1", "R1b", "R2")}
    check("LADDER North West is fourth or lower before the decisive step", all(pos[n] >= 3 for n in ("R0", "R1", "R1b")), pos)
    check("LADDER North West is never first on an intermediate rung", pos["R1"] != 0 and pos["R1b"] != 0)
    check("LADDER R0 margin (South East over North West) 5 per cent or more", A.top3(res["R0"])["margin"] >= 0.05,
          A.top3(res["R0"])["margin"])
    check("LADDER R2 margin (North West over South East) 7 per cent or more", A.top3(res["R2"])["margin"] >= 0.07,
          A.top3(res["R2"])["margin"])
    edge = res["R2"]["NWE"] - res["R0"]["NWE"]
    carried = res["R0"]["SEA"] - res["R0"]["NWE"]
    check("LADDER dominance: the decisive step moves North West 1.2 times South East's reported lead", edge >= 1.2 * carried,
          (round(edge, 2), round(carried, 2)))
    holders = [a for a in res["A"] if a["step"] in K.PILOT_STEPS]
    Es = PK.exposure(P, K.ACC_YEARS, by=("step", "prot"))
    big = {p: sum(1 for a in holders if a["prot"] == p and a["incurred"] > A.T_GOLDEN) /
           sum(v for (s, pp), v in Es.items() if s in K.PILOT_STEPS and pp == p) for p in (True, False)}
    check("LADDER the holders claim more often above the threshold too (they bought the add-on): 1.10 times or more",
          big[True] / big[False] >= 1.10, big[True] / big[False])

    # ------------------------------------------------------------------ the asks
    tg, tt = books_truth(bk)
    g, th = res["glass"], res["theft"]
    check("ASK A every region's windscreen claims tie to the books", all(g["n"][c] == tg["n"][c] for c in K.CODES),
          [(c, g["n"][c], tg["n"][c]) for c in K.CODES if g["n"][c] != tg["n"][c]])
    check("ASK A every region's average cost ties to the books", all(abs(g["avg"][c] - tg["avg"][c]) < 0.005
                                                                      for c in K.CODES))
    check("ASK B every region's thefts tie to the books", all(th["n"][c] == tt["n"][c] for c in K.CODES),
          [(c, th["n"][c], tt["n"][c]) for c in K.CODES if th["n"][c] != tt["n"][c]])
    check("ASK B every region's average net cost ties to the books", all(abs(th["avg"][c] - tt["avg"][c]) < 0.005
                                                                          for c in K.CODES))
    # the forcing: the platform's windscreen claims that are the partner's jobs, one to one
    jobs = A.partner_jobs(P)
    feed = A.feed_matches(P, jobs)
    check("ASK A each matched platform claim matches exactly one partner job", all(len(v) == 1 for v in feed.values()))
    h2 = [j for j in jobs.values() if j["booked"] >= K.MIGRATION]
    matched_jobs = {v[0] for v in feed.values()}
    check("ASK A every partner job from 1 July 2025 is on the platform once", len(matched_jobs) == len(h2) == len(feed),
          (len(matched_jobs), len(h2), len(feed)))
    check("ASK A no partner job before 1 July 2025 is a claim", all(j["booked"] >= K.MIGRATION for j in
                                                                    (jobs[v[0]] for v in feed.values())))
    plat_ws = [c for c in P["claims"] if c["type"] == "WSC" and c["sys"] == "P" and c["notified"].year == 2025]
    leg_ws = [c for c in P["claims"] if c["type"] == "WSC" and c["sys"] == "L" and c["notified"].year == 2025]
    check("ASK A the platform's 2025 windscreen claims run four times the legacy system's monthly rate or more",
          len(plat_ws) / 6.0 >= 4 * len(leg_ws) / 6.0, (len(plat_ws), len(leg_ws)))
    check("ASK A no windscreen claim names the partner", all(c["supplier"] != K.PARTNER for c in P["claims"]))
    stops = {
        "partner's jobs and every claim with no supplier (the cracker)": CR.glass_by_source(P, res["E25c"]),
        "the claims exports alone": CR.glass_by_source(P, res["E25c"], partner=False, supplier_split=False),
        "the partner's jobs alone": CR.glass_by_source(P, res["E25c"], claims=False),
    }
    for name, (fq, av) in stops.items():
        miss_f = sum(abs(fq[c] - fig["ask_a"]["frequency"][K.NAME[c]]) >= 0.05 for c in K.CODES)
        miss_a = sum(abs(av[c] - fig["ask_a"]["average"][K.NAME[c]]) >= 0.5 for c in K.CODES)
        check("ASK A stop '%s' misses every frequency" % name, miss_f == 8, miss_f)
        check("ASK A stop '%s' misses six or more averages" % name, miss_a >= 6, miss_a)
    fb, ab = CR.theft_by_claim(P, res["E25"])
    check("ASK B stop 'every theft claim with a cost' misses every frequency",
          sum(abs(fb[c] - fig["ask_b"]["frequency"][K.NAME[c]]) >= 0.05 for c in K.CODES) == 8)
    check("ASK B stop 'every theft claim with a cost' misses every average",
          sum(abs(ab[c] - fig["ask_b"]["average"][K.NAME[c]]) >= 0.5 for c in K.CODES) == 8)
    groups = collections.defaultdict(list)
    for c in P["claims"]:
        if c["type"] == "THF":
            groups[c["police"]].append(c)
    multi = [cs for cs in groups.values() if len(cs) > 1]
    check("ASK B every police reference's claims sit on one policy", all(len({PK.term_for(P, c["ref"], min(x["loss"] for x in cs))["ref"]
                                                                               if PK.term_for(P, c["ref"], min(x["loss"] for x in cs)) else c["ref"]
                                                                               for c in cs}) == 1 for cs in multi))
    cross = [cs for cs in multi if len({c["sys"] for c in cs}) == 2]
    check("ASK B some thefts have their claims on both systems (separators on one)", len(cross) >= 10, len(cross))
    check("ASK B a theft's second claim is dated after its first", all(sorted(c["loss"] for c in cs)[0] <
                                                                        sorted(c["loss"] for c in cs)[1] for cs in multi))
    pols = collections.Counter()
    for ref, cs in groups.items():
        first = min(cs, key=lambda c: (c["loss"], c["no"]))
        if first["loss"].year == 2025 and sum(c["incurred"] for c in cs) > 0:
            t = PK.term_for(P, first["ref"], first["loss"])
            pols[t["ref"]] += 1
    check("ASK B genuine repeat thefts of one car in 2025 exist (the over-cleaning half)", sum(1 for v in pols.values() if v > 1) >= 5,
          sum(1 for v in pols.values() if v > 1))
    sal = collections.Counter(s["sold"].year for s in P["salvage"])
    check("ASK B salvage for 2025 thefts posted in 2026 exists", any(
        s["sold"].year == 2026 and s["cat"] == "Recovered theft" for s in P["salvage"]), sal)

    # ------------------------------------------------------------------ separation
    Q = copy.copy(P)
    Q["claims"] = [c for c in P["claims"] if c["type"] == "ACC"]
    Q["glass"], Q["salvage"] = [], []
    lv = ladder(Q)
    check("SEPARATION the call is identical with every ask record deleted",
          all(abs(lv["R2"][c] - res["R2"][c]) < 1e-12 and abs(lv["R0"][c] - res["R0"][c]) < 1e-12 for c in K.CODES))
    check("SEPARATION no accident claim carries a police reference", all(not c["police"] for c in Q["claims"]))
    check("SEPARATION the asks' devices have zero rows among the accident claims",
          sum(1 for c in res["A"] if c["type"] != "ACC") == 0)

    # ------------------------------------------------------------------ cracker and pair
    cr = CR.run(task, quiet=True)
    check("CRACKER keeps none of the 32 ask figures", cr["cracker_hits"] == 0, cr["cracker_hits"])
    check("CRACKER pair ceiling 40 or under", cr["pair"] <= 40, cr["pair"])
    check("CRACKER mirror leakage under 35 per cent", cr["mirror_hits"] / cr["total"] < 0.35, cr["mirror_hits"])

    # ------------------------------------------------------------------ realism
    for key in ("frequency", "average"):
        for ask in ("ask_a", "ask_b"):
            vals = list(fig[ask][key].values())
            top = collections.Counter(vals).most_common(1)[0][1]
            check("REALISM blind response: one constant hits at most two of eight (%s %s)" % (ask, key), top <= 2, vals)
    for key in ("claims",):
        check("REALISM windscreen claim counts differ by region", len(set(fig["ask_a"][key].values())) == 8)
    check("REALISM theft counts differ by region", len(set(fig["ask_b"]["thefts"].values())) >= 7)
    check("REALISM reported claim counts differ by region", len(set(fig["components"]["reported_claims"].values())) == 8)
    card = json.load(open(os.path.join(os.path.dirname(task), ".claude", "skills", "fingerprint", "cards", "task270.json")))
    allt = " ".join(texts.values())
    for p in card["world"]["people"]:
        check("REALISM persona from the card appears: " + p, p in allt)
    for f in files:
        data = open(os.path.join(target, f), "rb").read()
        for wd in (b"ReportLab", b"openpyxl", b"python-docx", b"matplotlib"):
            check("REALISM no writer's name in %s (%s)" % (f, wd.decode()), wd not in data)
    forward = {"EXPIRY_DATE", "term_end"}
    latest = {}
    for f in files:
        if not f.endswith(".csv"):
            continue
        with open(os.path.join(target, f), encoding="utf-8") as fh:
            rd = csv.reader(fh)
            h = next(rd)
            for row in rd:
                for col, cell in zip(h, row):
                    if col in forward:
                        continue
                    m = re.match(r"^(\d{4})-(\d{2})-(\d{2})", cell) or None
                    if m:
                        d = dt.date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
                    else:
                        m = re.match(r"^(\d{2})/(\d{2})/(\d{4})", cell)
                        if not m:
                            continue
                        d = dt.date(int(m.group(3)), int(m.group(2)), int(m.group(1)))
                    latest[(f, col)] = max(latest.get((f, col), d), d)
    late = {k: v for k, v in latest.items() if v > K.EXTRACT and not (k[0] == K.FILES["glass"] and k[1] == "fitted_date")
            and not (k[0] == K.FILES["regions"])}
    check("REALISM no record after the extract (30 September 2026) outside the forward-dated columns (H16)", not late, late)
    gl = max(v for (f, col), v in latest.items() if f == K.FILES["glass"] and col == "fitted_date")
    check("REALISM the partner's 2025 jobs were fitted by mid-January 2026", gl <= dt.date(2026, 1, 15), gl)
    bad = h21()
    check("H21 invented names clear of real places and firms (none within two edits of one, none containing one)",
          not bad, bad)
    for nm in ("Marrowby", "Lurwick", "Kessling", "Halvorsen", "Pellwyn"):
        check("H21 no retired name survives: " + nm, all(nm.encode() not in open(os.path.join(target, f), "rb").read()
                                                         for f in files))

    # ------------------------------------------------------------------ Gate G and the leak greps
    docs = " ".join(texts.values()).lower() + contents.lower()
    for wd in ("absorb", "hunger", "unreported", "not reported", "small claim", "privately", "threshold", "truncat",
               "incentive", "behaviour", "self-select", "adverse", "pay for it themselves", "would not claim",
               "under-report", "underreport", "deter"):
        check("LEAK no shipped document says '%s'" % wd, wd not in docs)
    for wd in ("registered again", "twice", "duplicate", "same job", "second claim", "found damaged", "recovered damaged",
               "before vat", "excluding vat", "net of vat", "without vat", "booking feed", "repair claim"):
        check("LEAK no shipped document narrates an ask device ('%s')" % wd, not re.search(r"\b%s\b" % wd, docs))
    check("GATE G no shipped file states a frequency by rating region", "per 100" not in " ".join(
        open(os.path.join(target, K.FILES[k]), encoding="utf-8").readline() for k in
        ("pol_legacy", "pol_platform", "clm_legacy", "clm_platform", "regions", "complaints")).lower())

    print("checks: %d passed, %d failed" % (N["ok"], N["fail"]))
    for f in FAILS[:60]:
        print("  FAIL", f)
    return 0 if not FAILS else 1


# the invented names, screened against 5,617 places in Great Britain (h21_reference_places.txt) and the motor
# insurers, glass networks and salvage agents the fiction sits beside
FIRMS = ["Aviva", "Admiral", "Direct Line", "Churchill", "Ageas", "Allianz", "Zurich", "NFU Mutual", "Covea", "Esure",
         "Hastings", "Saga", "Markerstudy", "Sabre", "Ecclesiastical", "Marshmallow", "Hiscox", "Swinton", "Endsleigh",
         "Highway", "Autoglass", "National Windscreens", "Auto Windscreens", "Belron", "Copart", "Synetiq",
         "Silverlake", "Motorhub", "Royal London", "Prudential", "Wesleyan", "Liverpool Victoria", "Cornish Mutual",
         "Engage Mutual", "Police Mutual", "Royal Liver", "Clearview", "Clearwater", "Tremlett", "Fenwick"]
INVENTED = ["Fennacre", "Clearvane", "Tremlow", "Fennacre Mutual", "Clearvane Auto Glass", "Tremlow Vehicle Remarketing"]
GENERIC = {"mutual", "insurance", "society", "auto", "glass", "vehicle", "remarketing", "the", "of", "services",
           "statistics", "service", "private", "motor", "and", "limited", "ltd"}


def _key(name):
    return " ".join(w for w in re.sub(r"[^a-z ]", " ", name.lower()).split() if w not in GENERIC)


def _edits(a, b):
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb)))
        prev = cur
    return prev[-1]


def h21():
    places = [l.strip() for l in open(os.path.join(HERE, "h21_reference_places.txt"), encoding="utf-8") if l.strip()]
    bad = []
    for inv in INVENTED:
        ki = _key(inv)
        for real in places + FIRMS:
            kr = _key(real)
            if not ki or not kr or len(kr) <= 4:
                continue
            if ki == kr or kr in ki or ki in kr or _edits(ki, kr) <= 2:
                bad.append((inv, real))
    return bad
