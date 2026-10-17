"""Result messages for MMWR weeks 2 and 3 of 2027 as the county platform holds them at 08:00 on Monday 25 January,
the laboratories' weekly aggregate reports, the stream register, the test code list and the distractor series."""
import datetime as dt

import numpy as np
import pandas as pd

import params as P
import sim

DOW_W = np.array([0.08, 0.17, 0.16, 0.16, 0.15, 0.16, 0.12])      # Sunday .. Saturday share of a week's releases
HOUR_W = np.array([0.4, 0.3, 0.3, 0.3, 0.4, 0.8, 2.0, 3.6, 5.0, 6.0, 6.4, 6.4, 6.2, 6.0, 6.0, 5.8, 5.6, 5.2, 4.6,
                   4.0, 3.4, 2.6, 1.8, 1.0])
HOUR_W = HOUR_W / HOUR_W.sum()
CODE = {"flu_A": "RV-FLUA", "flu_B": "RV-FLUB", "flu": "RV-FLU", "rsv": "RV-RSV", "cov": "RV-COV2"}
TARGET = {"RV-FLUA": "Influenza A virus", "RV-FLUB": "Influenza B virus", "RV-FLU": "Influenza A and B virus",
          "RV-RSV": "Respiratory syncytial virus", "RV-COV2": "SARS-CoV-2"}


def utc_naive(local):
    return local - dt.timedelta(hours=P.TZ_OFFSET_H)


def fmt(t):
    return t.strftime("%Y-%m-%d %H:%M:%S")


class Records:
    def __init__(self, W):
        self.W = W
        self.rng = np.random.default_rng(P.RECORDS_SEED)
        self.rng_week = {wk: np.random.default_rng(s) for wk, s in P.WEEK_SEED.items()}
        self.gaps = {}                   # (lab, week) -> accessions numbered for orders cancelled before testing
        self.truth = {}                  # (lab, virus, week) -> dict of test-level truth

    # ---------------------------------------------------------------- tests of one laboratory and week
    def _week_tests(self, code, week_start, wi, rng, wk):
        lab = P.LAB[code]
        acc_mode, grain, facs = lab[6], lab[7], lab[8]
        T = {v: int(self.W.T[(code, v)][wi]) for v in lab[4]}
        Pn = {v: int(self.W.Pos[(code, v)][wi]) for v in lab[4]}
        nsw = int(max(T.values()) * 1.18)
        swab_tests = [[] for _ in range(nsw)]
        tests = []
        for v in lab[4]:
            idx = rng.choice(nsw, size=T[v], replace=False)
            pos = np.zeros(T[v], bool); pos[rng.choice(T[v], size=Pn[v], replace=False)] = True
            for j, s in enumerate(idx):
                swab_tests[s].append(len(tests))
                tests.append(dict(virus=v, swab=int(s), positive=bool(pos[j])))
        used = [s for s in range(nsw) if swab_tests[s]]
        # patients: one in twenty patients gives a second swab in the week
        npat = int(len(used) * 0.952)
        mrns = rng.choice(np.arange(10_000_000, 99_999_999), size=npat, replace=False)
        pat_of = {}
        order = rng.permutation(used)
        for k, s in enumerate(order):
            pat_of[int(s)] = "%s%d" % (P.PREFIX[code], mrns[k] if k < npat else mrns[int(rng.integers(0, npat))])
        # release time per swab (local), collection before it
        rel = {}
        for s in used:
            day = int(rng.choice(7, p=DOW_W)); hr = int(rng.choice(24, p=HOUR_W)); mi = int(rng.integers(0, 60))
            rel[s] = dt.datetime.combine(week_start, dt.time()) + dt.timedelta(days=day, hours=hr, minutes=mi,
                                                                                 seconds=int(rng.integers(0, 60)))
        # a patient's second swab is taken at least 18 hours after the first
        first = {}
        for s in sorted(used, key=lambda x: rel[x]):
            p = pat_of[s]
            if p in first and (rel[s] - first[p]).total_seconds() < 18 * 3600:
                rel[s] = first[p] + dt.timedelta(hours=18 + int(rng.integers(0, 30)))
                if rel[s] >= dt.datetime.combine(week_start + dt.timedelta(days=7), dt.time()):
                    rel[s] = dt.datetime.combine(week_start + dt.timedelta(days=6), dt.time(23, 50))
            first.setdefault(p, rel[s])
        coll = {s: rel[s] - dt.timedelta(minutes=int(60 * max(1.0, rng.gamma(4.0, P.TAT_H[code] / 4.0)))) for s in used}
        # a patient swabbed twice in the week gives the two specimens at least a day apart (the earlier one waits)
        coll_kept = dict(coll)
        swabs_of = {}
        for s in used:
            swabs_of.setdefault(pat_of[s], []).append(s)
        for ss in swabs_of.values():
            ss = sorted(ss, key=lambda x: coll_kept[x])
            for i in range(len(ss) - 2, -1, -1):
                if coll_kept[ss[i + 1]] - coll_kept[ss[i]] < dt.timedelta(hours=24):
                    coll_kept[ss[i]] = coll_kept[ss[i + 1]] - dt.timedelta(hours=24, minutes=7 * (i + 1))
        # accessions: per test ordered, or one per swab for the panel with add-on tests on new accessions; one order in
        # about 250 is a duplicate cancelled before testing, numbered in sequence with the rest
        base_acc = P.ACC_BASE[code] + (wk - 2) * P.ACC_PER_WEEK
        grng = np.random.default_rng([P.SEED, wk, [l[0] for l in P.LABS].index(code)])
        gaps = []
        out = []
        for s in sorted(used, key=lambda x: coll[x]):
            tlist = swab_tests[s]
            if grng.random() < 1 / 250:
                gaps.append(("%s%07d" % (P.PREFIX[code], base_acc), tlist[0])); base_acc += 1
            if acc_mode == "panel":
                main = "%s%07d" % (P.PREFIX[code], base_acc); base_acc += 1
                for j, ti in enumerate(tlist):
                    t = tests[ti]
                    if j > 0 and rng.random() < 0.12:            # added to the swab after the first run
                        t["accession"] = "%s%07d" % (P.PREFIX[code], base_acc); base_acc += 1
                        t["released"] = rel[s] + dt.timedelta(hours=float(rng.uniform(2, 20)))
                    else:
                        t["accession"] = main; t["released"] = rel[s] + dt.timedelta(minutes=int(rng.integers(0, 4)))
            else:
                for ti in tlist:
                    t = tests[ti]
                    t["accession"] = "%s%07d" % (P.PREFIX[code], base_acc); base_acc += 1
                    t["released"] = rel[s] + dt.timedelta(minutes=int(rng.integers(0, 240)))
            for ti in tlist:
                t = tests[ti]
                end = dt.datetime.combine(week_start + dt.timedelta(days=7), dt.time()) - dt.timedelta(minutes=1)
                t["released"] = min(t["released"], end)
                t["collected"] = coll_kept[s]; t["patient"] = pat_of[s]
                t["facility"] = facs[0] if len(facs) == 1 or rng.random() < 0.92 else facs[1]
                out.append(t)
        self.gaps[(code, wk)] = [dict(accession=a, test=tests[ti]) for a, ti in gaps]
        return out

    # ---------------------------------------------------------------- messages of one test
    def _messages(self, code, t, lost, held_until, week_end, rng):
        grain = P.LAB[code][7]
        v = t["virus"]
        if v == "flu" and grain == "target":
            if t["positive"]:
                a_pos = rng.random() < 0.86
                rows = [("RV-FLUA", "DETECTED" if a_pos else "NOT DETECTED"), ("RV-FLUB", "NOT DETECTED" if a_pos else "DETECTED")]
            else:
                rows = [("RV-FLUA", "NOT DETECTED"), ("RV-FLUB", "NOT DETECTED")]
        else:
            c = CODE["flu"] if v == "flu" else CODE[v]
            res = "DETECTED" if t["positive"] else ("INCONCLUSIVE" if rng.random() < 0.004 else "NOT DETECTED")
            rows = [(c, res)]
        msgs = []
        if lost:
            return msgs
        for c, res in rows:
            if held_until is not None:
                recv = held_until + dt.timedelta(seconds=int(rng.integers(0, 2400)))
            else:
                recv = t["released"] + dt.timedelta(seconds=int(rng.exponential(420)) + 5)
            msgs.append(dict(code=c, result=res, status="F", released=t["released"], received=recv))
        # one test in 130 has a result corrected the same day, sent as a C message; in three of ten the first result
        # was wrong and the correction carries the true one
        if rng.random() < 1 / 130:
            k = int(rng.integers(0, len(msgs)))
            m = dict(msgs[k]); m["status"] = "C"
            if rng.random() < 0.3:
                msgs[k]["result"] = "NOT DETECTED" if m["result"] == "DETECTED" else "DETECTED"
            m["released"] = min(m["released"] + dt.timedelta(minutes=int(rng.integers(20, 300))), week_end)
            m["received"] = max(m["received"], m["released"]) + dt.timedelta(seconds=int(rng.integers(30, 900)))
            msgs.append(m)
        return msgs

    def results(self, weeks=(2, 3)):
        """the platform's result table for weeks 2 and 3 as extracted at 08:00 local on Monday 25 January"""
        W = self.W
        rows = []
        self.week_truth = {}
        for wi, week_start in ((W.cur - 1, P.PREV_WEEK), (W.cur, P.CUR_WEEK)):
            wk = 2 if week_start == P.PREV_WEEK else 3
            if wk not in weeks:
                continue
            rng = self.rng_week[wk]
            monday = dt.datetime.combine(week_start + dt.timedelta(days=8), dt.time())
            for code in [l[0] for l in P.LABS]:
                tests = self._week_tests(code, week_start, wi, rng, wk)
                # the interface holds what is released from Saturday evening and through Sunday, and sends it on Monday
                hold_from = dt.datetime.combine(week_start + dt.timedelta(days=6), dt.time(P.HOLD_FROM[code]))
                sunday_end = dt.datetime.combine(week_start + dt.timedelta(days=1), dt.time())
                flush = monday + dt.timedelta(hours=P.FLUSH_AT[code][0], minutes=P.FLUSH_AT[code][1])
                flush_first = flush - dt.timedelta(days=7)
                week_end = dt.datetime.combine(week_start + dt.timedelta(days=7), dt.time()) - dt.timedelta(minutes=1)
                for t in tests:
                    lost = (wk == 3 and code in P.LOSS and rng.random() < P.LOSS[code]) or rng.random() < P.BG_LOSS
                    out_w2 = P.OUTAGE_W2.get(code) if wk == 2 else None
                    t["outage"] = bool(out_w2 and out_w2[0] <= t["released"] < out_w2[1])
                    lost = lost or t["outage"]
                    held = flush if t["released"] >= hold_from else (flush_first if t["released"] < sunday_end else None)
                    t["lost"] = bool(lost); t["held"] = held is not None and held == flush
                    msgs = self._messages(code, t, lost, held, week_end, rng)
                    for m in msgs:
                        if m["received"] > P.EXTRACT_LOCAL:
                            continue
                        rows.append(dict(week=wk, lab=code, facility=t["facility"], accession=t["accession"],
                                         patient=t["patient"], collected=t["collected"], code=m["code"],
                                         result=m["result"], status=m["status"], released=m["released"],
                                         received=m["received"]))
                    t["in_extract"] = any(m["received"] <= P.EXTRACT_LOCAL for m in msgs)
                self.week_truth[(code, wk)] = tests
            # cancelled tests: ordered, then cancelled before testing (one in 250 orders)
        df = pd.DataFrame(rows)
        return df

    def cancelled(self, df):
        """duplicate orders cancelled before testing (no result), on the accessions numbered for them; the cancellation
        goes through the laboratory's interface like a result: held over the weekend, lost when the interface loses"""
        rng = self.rng
        rows = []
        for (code, wk), gaps in self.gaps.items():
            week_start = P.PREV_WEEK if wk == 2 else P.CUR_WEEK
            monday = dt.datetime.combine(week_start + dt.timedelta(days=8), dt.time())
            hold_from = dt.datetime.combine(week_start + dt.timedelta(days=6), dt.time(P.HOLD_FROM[code]))
            sunday_end = dt.datetime.combine(week_start + dt.timedelta(days=1), dt.time())
            flush = monday + dt.timedelta(hours=P.FLUSH_AT[code][0], minutes=P.FLUSH_AT[code][1])
            out_w2 = P.OUTAGE_W2.get(code) if wk == 2 else None
            for g in gaps:
                t = g["test"]
                rel = max(t["released"] - dt.timedelta(minutes=int(rng.integers(30, 600))),
                          t["collected"] + dt.timedelta(minutes=int(rng.integers(10, 40))))
                if rel < dt.datetime.combine(week_start, dt.time()) or (out_w2 and out_w2[0] <= rel < out_w2[1]):
                    continue
                if wk == 3 and code in P.LOSS and rng.random() < P.LOSS[code]:
                    continue
                if rel >= hold_from:
                    recv = flush + dt.timedelta(seconds=int(rng.integers(0, 2400)))
                elif rel < sunday_end:
                    recv = flush - dt.timedelta(days=7) + dt.timedelta(seconds=int(rng.integers(0, 2400)))
                else:
                    recv = rel + dt.timedelta(seconds=int(rng.exponential(420)) + 5)
                if recv > P.EXTRACT_LOCAL:
                    continue
                c = "RV-FLU" if t["virus"] == "flu" else CODE[t["virus"]]
                if t["virus"] == "flu" and P.LAB[code][7] == "target":
                    c = "RV-FLUA"
                rows.append(dict(week=wk, lab=code, facility=t["facility"], accession=g["accession"], patient=t["patient"],
                                 collected=t["collected"], code=c, result="", status="X", released=rel, received=recv))
        return pd.concat([df, pd.DataFrame(rows)], ignore_index=True)

    def as_stored(self, df):
        """the platform's table: release times in UTC; receipt times as each broker wrote them (local before the
        state hub's broker migration, UTC from it); facility identifiers; random message ids"""
        rng = self.rng
        out = df.copy()
        out["released"] = [fmt(utc_naive(t)) for t in df["released"]]
        out["received"] = [fmt(t if t < P.BROKER_MIGRATION_LOCAL else utc_naive(t)) for t in df["received"]]
        out["collected"] = [fmt(utc_naive(t)) for t in df["collected"]]
        out = out.sort_values(["received", "facility", "accession", "code", "status"], kind="mergesort").reset_index(drop=True)
        out.insert(0, "message_id", ["%012x" % x for x in rng.integers(0, 2 ** 48, size=len(out))])
        out["target"] = out["code"].map(TARGET)
        cols = ["message_id", "facility", "accession", "patient", "collected", "code", "target", "result", "status",
                "released", "received"]
        return out[cols].rename(columns={"facility": "sending_facility", "patient": "patient_mrn",
                                         "collected": "specimen_collected", "code": "test_code",
                                         "status": "result_status"})

    def aggregate_reports(self):
        """each laboratory's weekly report of tests and positives by virus, MMWR 2022-W40 to 2027-W02, with the
        resubmissions a laboratory files when its first count was short"""
        rng = self.rng
        W = self.W
        rows = []
        for code, name, kind, mix, bases, tr, acc, grain, fac in P.LABS:
            for v in bases:
                for i in range(W.cur):
                    y, wk = sim.mmwr_label(W.W[i])
                    due = W.W[i] + dt.timedelta(days=10)
                    sub = due - dt.timedelta(days=int(rng.integers(0, 3)))
                    T, Pp = int(W.T[(code, v)][i]), int(W.Pos[(code, v)][i])
                    sub2 = sub + dt.timedelta(days=int(rng.integers(2, 9)))
                    if rng.random() < 0.025 and sub2 < P.EXTRACT_LOCAL.date():
                        f = rng.uniform(0.55, 0.92)
                        rows.append(dict(lab_id=P.LAB_ID[code], virus=P.VNAME[v], mmwr_year=y, mmwr_week=wk,
                                         tests=int(T * f), positives=int(Pp * f), submitted=sub.isoformat(), version=1))
                        rows.append(dict(lab_id=P.LAB_ID[code], virus=P.VNAME[v], mmwr_year=y, mmwr_week=wk, tests=T,
                                         positives=Pp, submitted=sub2.isoformat(), version=2))
                    else:
                        rows.append(dict(lab_id=P.LAB_ID[code], virus=P.VNAME[v], mmwr_year=y, mmwr_week=wk, tests=T,
                                         positives=Pp, submitted=sub.isoformat(), version=1))
        df = pd.DataFrame(rows).sort_values(["mmwr_year", "mmwr_week", "lab_id", "virus", "version"]).reset_index(drop=True)
        return df

    def register(self):
        labs = []
        for code, name, kind, mix, bases, tr, acc, grain, fac in P.LABS:
            labs.append(dict(lab_id=P.LAB_ID[code], laboratory=name, setting=kind, sending_facility_ids=", ".join(fac),
                             streams=", ".join(P.VNAME[v] for v in bases), electronic_reporting_since=REPORT_SINCE[code]))
        abbr = {"flu": "FLU", "rsv": "RSV", "cov": "COV"}
        codes = lambda c, v: ("RV-FLUA, RV-FLUB" if P.LAB[c][7] == "target" else "RV-FLU") if v == "flu" else CODE[v]
        streams = [dict(stream_id="%s-%s" % (P.LAB_ID[c], abbr[v]), lab_id=P.LAB_ID[c], virus=P.VNAME[v],
                        test_codes=codes(c, v)) for c, v in P.STREAMS]
        return pd.DataFrame(labs), pd.DataFrame(streams)

    @staticmethod
    def code_list():
        rows = [("RV-FLUA", "Influenza A virus RNA, NAAT", "Influenza", "one result per target; read with RV-FLUB as one influenza test"),
                ("RV-FLUB", "Influenza B virus RNA, NAAT", "Influenza", "one result per target; read with RV-FLUA as one influenza test"),
                ("RV-FLU", "Influenza A and B virus RNA, NAAT", "Influenza", "one result for the test"),
                ("RV-RSV", "Respiratory syncytial virus RNA, NAAT", "RSV", "one result for the test"),
                ("RV-COV2", "SARS-CoV-2 RNA, NAAT", "SARS-CoV-2", "one result for the test")]
        return pd.DataFrame(rows, columns=["test_code", "description", "virus", "note"])

    def ed_ili(self):
        """distractor: county emergency department visits and influenza-like-illness visits by week and age group"""
        rng = self.rng
        W = self.W
        C = {(v, g): W.curve(v, g) for v in P.VIRUSES for g in ("child", "adult", "elder")}
        rows = []
        for i in range(W.NW):
            y, wk = sim.mmwr_label(W.W[i])
            for band, g, base in (("0-4", "child", 9200), ("5-17", "child", 11800), ("18-64", "adult", 38500),
                                  ("65+", "elder", 14100)):
                act = 0.55 * C[("flu", g)][i] + 0.25 * C[("cov", g)][i] + 0.2 * C[("rsv", g)][i]
                visits = int(rng.normal(base, base * 0.03) * W.HOL[i] ** 0.3)
                ili = int(rng.binomial(visits, min(0.2, 0.012 + 0.22 * act)))
                rows.append(dict(mmwr_year=y, mmwr_week=wk, age_group=band, ed_visits=visits, ili_visits=ili))
        return pd.DataFrame(rows)

    def state_positivity(self):
        """distractor: the state's public weekly percent positive by region and virus, from the state's sentinel network"""
        rng = self.rng
        W = self.W
        rows = []
        shift = {"Region 1": -1.0, "Region 2": 0.0, "Region 3 (Tamsen)": 0.0, "Region 4": 1.5, "Region 5": 2.5}
        for i in range(W.cur):
            y, wk = sim.mmwr_label(W.W[i])
            if (y, wk) < (2025, 40):
                continue
            for reg, sh in shift.items():
                j = min(max(int(round(i - sh)), 0), W.NW - 1)
                for v in P.VIRUSES:
                    pi = 0.25 * W.curve(v, "child")[j] + 0.6 * W.curve(v, "adult")[j] + 0.15 * W.curve(v, "elder")[j]
                    n = int(rng.integers(900, 2600))
                    rows.append(dict(mmwr_year=y, mmwr_week=wk, region=reg, virus=P.VNAME[v], specimens_tested=n,
                                     percent_positive=round(100 * rng.binomial(n, pi) / n, 1)))
        return pd.DataFrame(rows)


    def admissions(self):
        """distractor: new hospital admissions with influenza, RSV and COVID-19 reported by the county's hospitals"""
        rng = self.rng
        W = self.W
        K = {"flu": 1150.0, "rsv": 1900.0, "cov": 1050.0}
        rows = []
        for i in range(W.cur):
            y, wk = sim.mmwr_label(W.W[i])
            for v in P.VIRUSES:
                act = 0.2 * W.curve(v, "child")[i] + 0.35 * W.curve(v, "adult")[i] + 0.45 * W.curve(v, "elder")[i]
                lam = K[v] * max(act - 0.6 * P.FLOOR[v], 0.002)
                rows.append(dict(mmwr_year=y, mmwr_week=wk, virus=P.VNAME[v], new_admissions=int(rng.poisson(lam)),
                                 hospitals_reporting=int(14 - (rng.random() < 0.08))))
        return pd.DataFrame(rows)


REPORT_SINCE = {"CHH": "2019-03-01", "AH1": "2018-11-15", "AH2": "2019-06-03", "AH3": "2020-01-20", "AH4": "2019-09-09",
                "CM1": "2021-04-12", "CM2": "2021-08-30", "CM3": "2022-02-14", "LTC": "2020-10-05", "REF": "2018-05-21"}
