"""The generator's assertions on the built pack: the input gates; the register, the keys and every person's stay and
earlier departure as the files give them against the simulation; the call, its rungs and its convergence across the
golden's family; the three-rules block (the analyst test on the clean truth); every row of the semantic fork table;
the asks against the generator's truth with their stops and the separation line; figures.json against the golden
files."""
import collections
import csv
import datetime as dt
import itertools
import json
import math
import os

import numpy as np

import bundle as B
import calibrate as C
import methods as M
import pack as P
import world as W

T5 = ["Aldewolde", "Borgermeer", "Bremvoort", "Dornhaghe", "Zandloo"]
GOLD = sorted(T5 + ["Eekhorst", "Haverstede", "Hilderloo", "Koudenbeek"])
DEFAULT = sorted(T5 + ["Hilderloo", "Molenrade", "Nijdorp"])
RUNG_SETS = {
    "R1 one audit rate": sorted(T5 + ["Dalmeer"]),
    "R2a born abroad": sorted(T5 + ["Molenrade", "Nijdorp"]),
    "R2a' foreign nationality": sorted(T5 + ["Molenrade", "Nijdorp"]),
    "R2b born abroad x years at the address": DEFAULT,
    "R2c current stay": sorted(T5 + ["Hilderloo"]),
    "R2d first settlement x left before": GOLD,
    "R2e left before": sorted(T5 + ["Molenrade", "Nijdorp"]),
    "R2f years at the address x left before": sorted(T5 + ["Eekhorst", "Haverstede", "Koudenbeek", "Molenrade",
                                                           "Nijdorp"]),
    "R2g age and sex": sorted(T5 + ["Dalmeer"]),
    M.GOLDEN: GOLD,
}
LAST_LOCAL_2025 = dt.date(2025, 12, 30)   # a message registered on 31 December leaves in the New Year's night batch


class Checker:
    def __init__(self):
        self.ok = True
        self.n = 0

    def __call__(self, cond, msg):
        self.n += 1
        if not cond:
            self.ok = False
            print("FAIL:", msg)


def names(codes):
    return sorted(W.NAME[m] for m in codes)


def loglik(audit, key):
    rates, pooled = M.fit(audit, key)
    s = 0.0
    for f, a in audit:
        p = rates.get(key(f), pooled)
        if 0 < p < 1:
            s += math.log(p) if a else math.log(1 - p)
    return s


def logit_adjusted(audit, pops, fx):
    X = np.array([[1.0] + fx(f) for f, _ in audit])
    y = np.array([a for _, a in audit], float)
    b = np.zeros(X.shape[1])
    for _ in range(80):
        p = 1 / (1 + np.exp(-X @ b))
        H = X.T @ (X * (p * (1 - p))[:, None]) + 1e-6 * np.eye(X.shape[1])
        step = np.linalg.solve(H, X.T @ (y - p) - 1e-6 * b)
        b += step
        if np.abs(step).max() < 1e-10:
            break
    return {m: len(pop) - float((1 / (1 + np.exp(-np.array([[1.0] + fx(f) for f in pop]) @ b))).sum())
            for m, pop in pops.items()}


def partitions(pk):
    """every contiguous partition of the completed years 0..10+ with the earlier departure: (set, loglik, lumps 9|10)"""
    S_ = 12
    idx = lambda f: 0 if f["stay"] is None else 1 + min(f["stay"], 10)
    A, N = np.zeros((S_, 2)), np.zeros((S_, 2))
    for f, a in pk.audit:
        N[idx(f), f["left"]] += 1
        A[idx(f), f["left"]] += a
    P_ = {m: np.zeros((S_, 2)) for m in pk.codes}
    for m in pk.codes:
        for f in pk.pops[m]:
            P_[m][idx(f), f["left"]] += 1
    pooled = A.sum() / N.sum()
    out = []
    for cuts in itertools.product((0, 1), repeat=10):
        band, b = [0], 1
        for k in range(11):
            band.append(b)
            if k < 10 and cuts[k]:
                b += 1
        band = np.array(band)
        rate, ll = {}, 0.0
        for bb in range(band.max() + 1):
            sel = band == bb
            for l in (0, 1):
                n, a = N[sel, l].sum(), A[sel, l].sum()
                rate[bb, l] = a / n if n else pooled
                if n and 0 < a < n:
                    ll += a * math.log(a / n) + (n - a) * math.log(1 - a / n)
        adj = {m: P_[m].sum() - sum(P_[m][s, l] * rate[band[s], l] for s in range(S_) for l in (0, 1)) for m in pk.codes}
        out.append((names(M.qualifying(adj)), ll, not cuts[9]))
    return out


def truth_asks(x):
    """the generator's truth for the two asks, from the simulated messages and the hub's answers"""
    former = {}
    for nr in x["nonres"]:
        former[nr["key"]] = nr["dep"]
    dep = collections.Counter()
    dth = collections.Counter()
    for m, res, _ in x["acks"]:
        if res != "ACCEPTED" or m.get("void") or m["date"].year != 2025 or m["sent"] > LAST_LOCAL_2025:
            continue
        if m["kind"] == "EMI":
            dep[m["mun"]] += 1
        elif m["kind"] == "OVL" and not (m["key"] in former and former[m["key"]] <= m["date"]):
            dth[m["mun"]] += 1
    return dep, dth


def run(target, gdir, x=None, meta_path=None, fig_path=None):
    ck = Checker()
    x = x or P.everything()
    pk = B.Pack(target)
    # ------------------------------------------------------------------------------------------- input gates
    files = sorted(os.listdir(target))
    ck(len(files) >= 10, "ten or more files")
    ck(len({f.rsplit(".", 1)[1] for f in files}) >= 3, "three or more formats")
    with open(os.path.join(target, P.FILES["events"]), encoding="utf-8") as fh:
        ck(sum(1 for _ in fh) - 1 >= 25000, "a file of 25,000 or more rows")
    if meta_path:
        meta = json.load(open(meta_path, encoding="utf-8"))
        ck(len(meta["distractor_files"]) >= 2 and all(f in files for f in meta["distractor_files"]),
           "two or more distractors named in metadata.json")
    # ---------------------------------------------------------------------------- the register and the keys
    ck(len(pk.trailer) == 1 and int(pk.trailer[0]["MUN_CODE"]) == len(pk.register) == sum(W.COUNT.values()),
       "SF2 the trailer's count, the rows and the world's counts agree")
    ck(names(pk.codes) == sorted(W.NAME[m] for m in W.CODES) and W.MERGED[1] in pk.codes
       and not set(r["MUN_CODE"] for r in pk.register) & {c for _, c in W.FORMER},
       "SF4 the 24 municipalities as constituted on 1 January 2026, Ravenmeer one of them")
    ck(min(len(p) for p in pk.pops.values()) >= W.IN_PLAY[0] and max(len(p) for p in pk.pops.values()) <= W.IN_PLAY[1],
       "SF3 every register count between 4,500 and 6,000 (4,561 to 5,944), so the bounds' inclusivity is moot")
    regk = collections.Counter(r["PERSON_KEY"] for r in pk.register)
    ck(max(regk.values()) == 1, "no person key twice in the register extract")
    ck(len({r["PERSON_KEY"] for r in pk.sample}) == len(pk.sample), "no person key twice in the sample")
    ck(len({n["PERSON_KEY"] for n in pk.nonres}) == len(pk.nonres), "no person key twice in the non-resident records")
    ck(not set(regk) & {n["PERSON_KEY"] for n in pk.nonres}, "no registered person among the non-resident records")
    ck(set(pk.hist) == set(regk), "every registered person has a history and nobody else")
    inplay_sampled = {r["PERSON_KEY"] for r in pk.sample if r["MUN_CODE"] in pk.codes}
    ck(inplay_sampled <= set(regk), "the in-play sampled persons are registered persons")
    # ------------------------------------------------------- each person's career as the files give it, vs truth
    truth = {}
    for code in W.CODES:
        for p in x["reg"][code]:
            truth[p["key"]] = p
    feat = {}
    for r in pk.register:
        feat[r["PERSON_KEY"]] = B.features(r, pk.hist.get(r["PERSON_KEY"], []))
    bad = [k for k, f in feat.items() if (f["stay"], f["left"]) != (truth[k]["stay"], truth[k]["left"])]
    ck(not bad, "every registered person's stay and earlier departure from the files equal the truth (%d differ)" % len(bad))
    samp_truth = {p["key"]: p for p in x["sample"]}
    sbad = [r["PERSON_KEY"] for r, (f, a) in zip(pk.sample, pk.audit)
            if (f["stay"], f["left"]) != (samp_truth[r["PERSON_KEY"]]["stay"], samp_truth[r["PERSON_KEY"]]["left"])
            or a != int(samp_truth[r["PERSON_KEY"]]["absent"])]
    ck(not sbad, "every sampled person's career and final result from the files equal the truth (%d differ)" % len(sbad))
    ck(sum(a for _, a in pk.audit) == 206 and len(pk.audit) == W.N_AUDIT, "206 of 12,000 sampled persons not living there")
    # ------------------------------------------------------------------------------------------------ the call
    gold = names(pk.qualifying())
    ck(gold == GOLD, "the call: %s" % gold)
    adj = pk.adjusted()
    below = max((adj[m], W.NAME[m]) for m in pk.codes if adj[m] < 5000)
    above = min((adj[m], W.NAME[m]) for m in pk.codes if adj[m] >= 5000)
    ck(below[1] == "Hilderloo" and above[1] == "Dalmeer" and 5000 - below[0] > 40 and above[0] - 5000 > 38,
       "SF1 nearest municipalities: Hilderloo %.1f under, Dalmeer %.1f over" % (5000 - below[0], above[0] - 5000))
    ck(sorted(W.NAME[m] for m in pk.codes if adj[m] < 5000) == GOLD,
       "SF1 the unrounded comparison files the same nine")
    for name, want in RUNG_SETS.items():
        got = names(pk.qualifying(name))
        ck(got == want, "rung %s files %s" % (name, got))
    llg = loglik(pk.audit, M.RUNGS[M.GOLDEN])
    ck(abs(llg - (-774.4)) < 0.1, "the golden's cells fit at -774.4 (%.1f)" % llg)
    for name in M.RUNGS:
        if RUNG_SETS[name] != GOLD:
            ck(loglik(pk.audit, M.RUNGS[name]) < llg - 10, "the audit fits %s worse than the golden by 10 or more" % name)
    ck(abs(loglik(pk.audit, M.RUNGS["R2b born abroad x years at the address"]) - (-834.4)) < 0.1,
       "the default path's cells fit at -834.4")
    for name in M.VARIANTS:
        ck(names(pk.qualifying(name)) == GOLD, "the golden's family: %s files the nine" % name)
    band, ab = M.band, M.addr_band
    crosses = {
        "stay x left x abroad x address": lambda f: (band(f["stay"]), f["left"], f["abroad"], ab(f["addr"])),
        "stay x left x address x sex": lambda f: (band(f["stay"]), f["left"], ab(f["addr"]), f["sex"]),
        "stay x left x foreign": lambda f: (band(f["stay"]), f["left"], f["foreign"]),
        "stay x left x age": lambda f: (band(f["stay"]), f["left"], min(f["age"] // 10, 8)),
        "stay x left x first settlement": lambda f: (band(f["stay"]), f["left"], band(f["first"])),
        "first settlement x left x abroad x address": lambda f: (band(f["first"]), f["left"], f["abroad"], ab(f["addr"])),
    }
    for name, key in crosses.items():
        ck(names(M.qualifying(M.adjusted(pk.audit, pk.pops, key))) == GOLD, "the golden's family: %s files the nine" % name)
    d = lambda v, ks: [int(v == k) for k in ks]
    logits = {
        "stay bands + left": lambda f: d(band(f["stay"]), (0, 1, 2, 3)) + [f["left"]],
        "stay bands x left": lambda f: [int(band(f["stay"]) == k and f["left"] == l) for k in (0, 1, 2, 3) for l in (0, 1)],
        "stay bands + left + register fields": lambda f: d(band(f["stay"]), (0, 1, 2, 3)) + [f["left"], f["abroad"],
                                                         f["foreign"]] + d(ab(f["addr"]), (1, 2, 3)) +
        d(min(f["age"] // 15, 5), (1, 2, 3, 4, 5)) + [int(f["sex"] == "M")],
        "stay years + left": lambda f: [int(f["stay"] is not None), (f["stay"] or 0), f["left"]],
        "stay bands + left + first bands": lambda f: d(band(f["stay"]), (0, 1, 2, 3)) + [f["left"]] +
        d(band(f["first"]), (1, 2, 3)),
    }
    spread = {}
    for name, fx in logits.items():
        la = logit_adjusted(pk.audit, pk.pops, fx)
        ck(names(M.qualifying(la)) == GOLD, "the golden's family: logit %s files the nine" % name)
        spread[name] = max(abs(la[m] - adj[m]) for m in pk.codes)
    reg_fields = lambda f: [f["abroad"], f["foreign"]] + d(ab(f["addr"]), (1, 2, 3)) + d(min(f["age"] // 15, 5),
                                                                                        (1, 2, 3, 4, 5)) + [int(f["sex"] == "M")]
    ck(names(M.qualifying(logit_adjusted(pk.audit, pk.pops, reg_fields))) == DEFAULT,
       "a logistic fit on every register field files the default path's eight")
    parts = partitions(pk)
    good = [p for p in parts if p[0] == GOLD]
    badp = [p for p in parts if p[0] != GOLD]
    ck(len(good) == 1013 and max(p[1] for p in badp) < llg - 15 and sum(1 for p in badp if p[2]) == 10,
       "1,013 of 1,024 stay partitions with the earlier departure file the nine; of the 11 others ten lump 5-9 with 10+, "
       "and all fit 15 or more below the golden's cells (%d, best of them %.1f)" % (len(good), max(p[1] for p in badp)))
    cellvar = max(abs(pk.adjusted(v)[m] - adj[m]) for v in M.VARIANTS for m in pk.codes)
    ck(cellvar < 4.5 and max(spread.values()) < 50,
       "SF11 the adjusted figure: cell variants within %.1f persons, logits within %.1f; the call fixed" % (
           cellvar, max(spread.values())))
    # ------------------------------------------------------------ three rules: the analyst test on the clean truth
    t_audit = [(C.features(p), int(p["absent"])) for p in x["sample"]]
    t_pops = {code: [C.features(p) for p in x["reg"][code]] for code in W.CODES}
    ck(names(M.qualifying(M.adjusted(t_audit, t_pops, M.RUNGS["R2b born abroad x years at the address"]))) == DEFAULT,
       "analyst test: on the clean truth the register's own fields file the default eight")
    ck(names(M.qualifying(M.adjusted(t_audit, t_pops, M.RUNGS[M.GOLDEN]))) == GOLD,
       "analyst test: on the clean truth the stay with the earlier departure files the nine")
    ck(names(M.qualifying(M.adjusted(t_audit, t_pops, M.RUNGS["R2c current stay"]))) == RUNG_SETS["R2c current stay"],
       "analyst test: the decisive step changed alone (the earlier departure dropped) files the six")
    # --------------------------------------------------------------------------------- semantic fork table
    ck(names(B.Pack(target, annulments=False).qualifying()) == GOLD, "SF7 annulled events kept: the same nine")
    ck(names(B.Pack(target, final_result="first").qualifying()) == GOLD, "SF6 the first result that is not 91: the same nine")
    alt50 = [(f, int(pk.result[r["AUDIT_NO"]] in ("20", "30", "40", "50"))) for (f, _), r in zip(pk.audit, pk.sample)]
    ck(names(M.qualifying(M.adjusted(alt50, pk.pops, M.RUNGS[M.GOLDEN]))) == GOLD, "SF5 result 50 as absent: the same nine")
    inplay = [(f, a) for (f, a), r in zip(pk.audit, pk.sample) if r["MUN_CODE"] in pk.codes]
    ck(names(M.qualifying(M.adjusted(inplay, pk.pops, M.RUNGS[M.GOLDEN]))) != GOLD,
       "SF8 the in-play sampled persons alone file another set (ruled out by report 5)")
    cal_key = M.RUNGS[M.GOLDEN]
    cal = calendar_years(pk)
    ck(names(M.qualifying(M.adjusted(cal[0], cal[1], cal_key))) == GOLD, "SF9 the calendar-year difference: the same nine")
    codes = {e for evs in pk.hist.values() for e, _, _ in evs}
    ck(codes <= {"GEB", "IMM", "EMI", "VER", "ADR", "HUW", "NAT", "OVL"}, "SF10 every event code is on the code list")
    partial = sum(1 for r in pk.register if r["BIRTH_DATE"].endswith("00"))
    ck(partial > 0 and names(pk.qualifying()) == GOLD, "SF12 partial birth dates (%d) leave the golden untouched" % partial)
    # ----------------------------------------------------------------------------------------------- the asks
    tdep, tdth = truth_asks(x)
    gd, gt = pk.departures(), pk.deaths()
    ck(all(gd[m] == tdep[m] for m in pk.codes), "SF13 departures abroad equal the generator's truth")
    ck(all(gt[m] == tdth[m] for m in pk.codes), "SF14 deaths equal the generator's truth")
    vow = collections.Counter(pk.mun(m["SENDER_MUN"]) for m in pk._messages("VOW"))
    ck(all(vow[m] >= 1 for m in pk.codes), "SF15 removals in every municipality, none counted as departures")

    def misses(a, b):
        return all(a[m] != b[m] for m in pk.codes)
    stops_a = {"the annulled departures counted": pk.departures(void="keep"),
               "every departure of a registered person dropped": pk.departures(void="drop_registered"),
               "the hub's UTC year": pk.departures(clock="utc"),
               "the UTC year with the annulled counted": pk.departures(clock="utc", void="keep"),
               "the UTC year with registered persons dropped": pk.departures(clock="utc", void="drop_registered"),
               "every message": pk.departures(acks="all"),
               "persons not departures": pk.departures(dedup=True),
               "any departure date": pk.departures(year=False)}
    for k, v in stops_a.items():
        ck(misses(v, gd), "ask A stop misses all 24: %s" % k)
    nres = pk.departures_nonres()
    ck(sum(1 for m in pk.codes if nres[m] == gd[m]) <= 1, "ask A: the non-resident records' departures miss 23 or more")
    stops_b = {"the annulled deaths counted": pk.deaths(void="keep"),
               "the hub's UTC year": pk.deaths(clock="utc"),
               "the UTC year with the annulled counted": pk.deaths(clock="utc", void="keep"),
               "former residents counted": pk.deaths(residency="none"),
               "every message": pk.deaths(acks="all"),
               "any date of death": pk.deaths(year=False)}
    for k, v in stops_b.items():
        ck(misses(v, gt), "ask B stop misses all 24: %s" % k)
    ck(pk.deaths(residency="no_record") == gt, "ask B: every former resident out gives the golden (no death before a "
                                                "registration ended)")
    # the careful two-error readings
    for clock, void in itertools.product(("local", "utc"), ("exclude", "keep", "drop_registered")):
        for year in (True, False):
            if (clock, void, year) != ("local", "exclude", True):
                ck(misses(pk.departures(clock=clock, void=void, year=year), gd),
                   "ask A reading %s/%s/%s misses all 24" % (clock, void, year))
    for clock, void, res, year in itertools.product(("local", "utc"), ("exclude", "keep"), ("registered", "none"),
                                                   (True, False)):
        if (clock, void, res, year) != ("local", "exclude", "registered", True):
            ck(misses(pk.deaths(clock=clock, void=void, residency=res, year=year), gt),
               "ask B reading %s/%s/%s/%s misses all 24" % (clock, void, res, year))
    # ------------------------------------------------------------------------------ separation and realism
    for code in W.CODES:
        for p in x["reg"][code]:
            for e in p.get("annulled", []):
                if e[0] in ("EMI", "OVL") and e[1].year == 2025:
                    imms = [v[1] for v in p["events"] if v[0] == "IMM"]
                    ck(not imms or e[1] > imms[-1], "an annulled 2025 event after the latest settlement (%s)" % p["key"])
    sent = [m["SENT_AT"] for m in pk.messages]
    ck(all(s[:4] == "2025" and s[11:13] in ("22", "23") for s in sent), "every message logged in 2025 UTC, the night batch")
    ck(len({m["MESSAGE_ID"] for m in pk.messages}) == len(pk.messages) == len(pk.acks), "one acknowledgement per message")
    year_end = sum(1 for m in pk.messages if B.local_date(m["SENT_AT"]).year == 2026)
    ck(year_end >= 48, "the New Year's night batch in every municipality (%d messages)" % year_end)
    # ----------------------------------------------------------------------------------------- figures.json
    if fig_path and gdir:
        fig = json.load(open(fig_path, encoding="utf-8"))
        ck(fig["call"]["names"] == GOLD and fig["call"]["count"] == 9, "figures.json: the call")
        with open(os.path.join(gdir, "adjusted_population_supplement_2027.csv"), encoding="utf-8") as fh:
            rows = list(csv.DictReader(fh))
        by = {x_["gm"]: x_ for x_ in fig["municipalities"]}
        ck(len(rows) == 24 and [r["MUNICIPALITY_CODE"] for r in rows] == sorted(r["MUNICIPALITY_CODE"] for r in rows),
           "the CSV: 24 rows sorted by code")
        for r in rows:
            f_ = by[r["MUNICIPALITY_CODE"]]
            ck(int(r["REGISTERED_20260101"]) == f_["registered"] and int(r["ADJUSTED_POPULATION"]) == f_["adjusted"]
               and int(r["NOT_RESIDENT_ESTIMATE"]) == f_["registered"] - f_["adjusted"]
               and r["QUALIFIES"] == ("Y" if f_["qualifies"] else "N") and int(r["DEPARTURES_ABROAD_2025"]) ==
               f_["departures"] and int(r["DEATHS_2025"]) == f_["deaths"], "the CSV row %s agrees with figures.json" % r[
                "MUNICIPALITY_CODE"])
    print("checks: %d of %d passed" % (ck.n - (0 if ck.ok else 1), ck.n) if ck.ok else "checks: FAILED")
    return ck.ok


def calendar_years(pk):
    """the audit and the populations with the stay as the calendar-year difference to 2026"""
    def recode(r, hist):
        f = B.features(r, hist)
        imms = [d for e, d, _ in hist if e == "IMM"]
        if imms:
            f = dict(f, stay=2026 - imms[-1].year)
        return f
    audit = [(recode(r, pk.shist.get(r["PERSON_KEY"], [])), a) for r, (_, a) in zip(pk.sample, pk.audit)]
    pops = {m: [] for m in pk.codes}
    for r in pk.register:
        pops[r["MUN_CODE"]].append(recode(r, pk.hist.get(r["PERSON_KEY"], [])))
    return audit, pops
