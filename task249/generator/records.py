"""The exports, written from the World's truth with each system's own habits.

Platform (MAT-R attempts, exposure log): UTC timestamps, logits and standard errors to three decimals, one row per
attempt, an interrupted attempt and its completed attempt under one booking reference (a fresh reference for the
restart from release 5.3.2). QA's synthetic monitoring suite runs its regression script through the production
platform early each Monday of the season, so its sittings sit in the export beside the candidates' (its identities are
not in the candidate register). Client results feed (shares): IST in the Indian day-month-year
form, one row per share event, the 14 August re-send, Paisaghar Lending's campuses under PGL until the client record
moved. Selection-day operations (2028 shortlists, the case log): dates as the operations team keeps them. The 2028
equivalence study: IST, two dates per volunteer."""
import datetime as dt
import numpy as np
import pandas as pd
import params as P
import exposure as X

RESEND_FROM, RESEND_TO = dt.date(2028, 8, 10), dt.date(2028, 8, 14)
RELEASE = dt.datetime(2028, 7, 9, 22, 0, tzinfo=P.IST)
SUITE_WEEKS = (dt.date(2028, 7, 3), dt.date(2028, 7, 10), dt.date(2028, 7, 17), dt.date(2028, 7, 24))
SUITE_PER_WEEK = 1600
SUITE_N = SUITE_PER_WEEK * 4
MERGE_DAY = dt.date(2028, 9, 2)
CASE_SEED = 118
BANK_SEED = 14
LATE_REG = 7400


def suite_script(bank):
    """QA's regression script for the synthetic suite: sixteen operational items from the middle of the bank's range,
    one a position with the content areas in rotation, the same in every suite sitting"""
    r = np.random.default_rng(P.SEED + 19)
    script = []
    for k in range(16):
        idx = np.where((bank["area"] == X.AREAS[k % 3]) & (bank["b"] > -1.1) & (bank["b"] < 0.7))[0]
        script.append(int(r.choice(np.setdiff1d(idx, script))))
    return np.array(script)


def ist(d, minute):
    return dt.datetime(d.year, d.month, d.day, 0, 0, tzinfo=P.IST) + dt.timedelta(minutes=int(minute))


def naive_utc(t):
    return t.astimezone(P.UTC).replace(tzinfo=None)


class Records:
    def __init__(self, w):
        self.w = w
        self.rng = np.random.default_rng(P.SEED + 7)
        self._ids()
        self._attempts()
        self._exposure()
        self._shares()
        self._shortlists()
        self._cases()
        self._study()

    # ------------------------------------------------------------------ identifiers
    def _ids(self):
        w, r = self.w, self.rng
        pool = r.choice(np.arange(1000000, 8999999), w.N + SUITE_N, replace=False)
        self.cand_id = np.array(["MC%07d" % v for v in pool[:w.N]])
        self.suite_id = np.array(["MC%07d" % v for v in pool[w.N:]])
        bk = r.choice(np.arange(100000, 999999), w.N + SUITE_N + 6000, replace=False)
        self.booking = np.array(["BK28-%06d" % v for v in bk[:w.N]])
        self.suite_bk = np.array(["BK28-%06d" % v for v in bk[w.N:w.N + SUITE_N]])
        self.spare_bk = ["BK28-%06d" % v for v in bk[w.N + SUITE_N:]]
        self.short_code = {c["cid"]: c["short"] for c in w.colleges}
        # registered but never sat (registered for the season, applied nowhere)
        self.reg_date = np.array([dt.date(2028, 6, 1) + dt.timedelta(days=int(v)) for v in r.integers(0, 40, w.N)])

    # ------------------------------------------------------------------ MAT-R attempts (platform export)
    def _attempts(self):
        w, r = self.w, self.rng
        sit = np.where(w.applied)[0]
        rows = []
        dev_p = {"T1": [0.18, 0.78, 0.04], "T2": [0.22, 0.72, 0.06], "T3": [0.30, 0.62, 0.08], "T4": [0.34, 0.56, 0.10]}
        devs = ["desktop", "laptop", "tablet"]
        p_int = {"lab": 0.016, "desktop": 0.027, "laptop": 0.046, "tablet": 0.097}
        switch = {"desktop": ([0.0, 0.8, 0.2], 0.18), "laptop": ([0.85, 0.0, 0.15], 0.31), "tablet": ([0.3, 0.7, 0.0], 0.64)}
        for i in sit:
            d = w.sit_date[i]
            start = ist(d, w.sit_minute[i])
            if w.lab[i]:
                dev, pi = "desktop", p_int["lab"]
            else:
                dev = devs[int(r.choice(3, p=dev_p[w.cand_tier[i]]))]
                pi = p_int[dev]
            if w.applied[i] and w.restart_u[i] < pi:
                k = int(w.restart_items[i])
                e1 = start + dt.timedelta(seconds=int(k * r.uniform(48, 95)))
                rows.append(dict(i=i, att=1, start=start, end=e1, status="interrupted", items=k, dev=dev))
                dev2 = dev
                if not w.lab[i]:
                    pw, ps = switch[dev]
                    if r.random() < ps:
                        dev2 = devs[int(r.choice(3, p=pw))]
                start = e1 + dt.timedelta(minutes=int(r.integers(4, 95)))
                # from release 5.3.2 a restart is issued a fresh booking reference as a first attempt
                fresh = self.spare_bk.pop() if start >= RELEASE else None
                rows.append(dict(i=i, att=1 if fresh else 2, start=start,
                                 end=start + dt.timedelta(seconds=int(16 * r.uniform(52, 88))),
                                 status="completed", items=16, dev=dev2, bk=fresh))
            else:
                rows.append(dict(i=i, att=1, start=start, end=start + dt.timedelta(seconds=int(16 * r.uniform(52, 88))),
                                 status="completed", items=16, dev=dev))
        self.att = rows
        # QA's synthetic monitoring suite: after each Sunday-night patch window it runs 1,600 sittings early on the
        # Monday (01:00 to 04:00 IST) through the production platform, each under a college code drawn from the
        # register so traffic looks like the season's
        cols = [c["short"] for c in w.colleges]
        self.suite = []
        for j in range(SUITE_N):
            d = SUITE_WEEKS[j // SUITE_PER_WEEK]
            start = ist(d, int(r.integers(60, 240)))
            est = float(r.normal(0.1, 0.9))
            self.suite.append(dict(cand=self.suite_id[j], bk=self.suite_bk[j], col=cols[int(r.integers(0, len(cols)))],
                                   start=start, end=start + dt.timedelta(seconds=int(16 * r.uniform(18, 34))),
                                   est=est, dev=devs[int(r.integers(0, 2))], week=j // SUITE_PER_WEEK))

    def attempts_frame(self):
        w = self.w
        recs = []
        for a in self.att:
            i = a["i"]
            done = a["status"] == "completed"
            recs.append((a.get("bk") or self.booking[i], a["att"], self.cand_id[i], self.short_code[w.cand_college[i]],
                         naive_utc(a["start"]), naive_utc(a["end"]), a["status"], a["items"],
                         float(w.u_est[i]) if done else np.nan, float(w.u_se[i]) if done else np.nan,
                         int(round(P.SCALE_MID + P.SCALE_PER_LOGIT * w.u_est[i])) if done else None,
                         a["dev"], "5.3.2" if a["start"] >= RELEASE else "5.3.1"))
        for q in self.suite:
            est = round(q["est"], 3)
            se = round(float(P.se_online(est)) * float(np.exp(self.rng.normal(0, 0.025))), 3)
            recs.append((q["bk"], 1, q["cand"], q["col"], naive_utc(q["start"]), naive_utc(q["end"]), "completed", 16,
                         est, se, int(round(P.SCALE_MID + P.SCALE_PER_LOGIT * est)), q["dev"],
                         "5.3.2" if q["start"] >= RELEASE else "5.3.1"))
        df = pd.DataFrame(recs, columns=["booking_ref", "attempt_no", "candidate_id", "college_code", "started_utc",
                                         "ended_utc", "attempt_status", "items_shown", "theta_logit", "se_logit",
                                         "scale_score", "device", "platform_release"])
        df["scale_score"] = df["scale_score"].astype("Int64")
        return df.sort_values(["started_utc", "booking_ref", "attempt_no"], kind="stable").reset_index(drop=True)

    def register_frame(self):
        """every registration of the season; besides the candidates in the world, registrants who never booked"""
        w = self.w
        recs = [(self.cand_id[i], self.short_code[w.cand_college[i]], self.reg_date[i].isoformat()) for i in range(w.N)]
        r = np.random.default_rng(P.SEED + 31)
        used = set(self.cand_id.tolist()) | set(self.suite_id.tolist())
        sizes = np.array([c["size"] for c in w.colleges], float)
        extra = []
        while len(extra) < LATE_REG:
            v = "MC%07d" % int(r.integers(1000000, 8999999))
            if v not in used:
                used.add(v)
                extra.append(v)
        cols = r.choice(len(w.colleges), LATE_REG, p=sizes / sizes.sum())
        days = r.integers(0, 40, LATE_REG)
        recs += [(v, w.colleges[int(c)]["short"], (dt.date(2028, 6, 1) + dt.timedelta(days=int(d))).isoformat())
                 for v, c, d in zip(extra, cols, days)]
        df = pd.DataFrame(recs, columns=["candidate_id", "college_code", "registered_on"])
        return df.sort_values(["registered_on", "candidate_id"], kind="stable").reset_index(drop=True)

    # ------------------------------------------------------------------ exposure log
    def _exposure(self):
        w, r = self.w, self.rng
        self.bank = X.bank(np.random.default_rng(P.SEED + BANK_SEED))
        tier_start = {"T1": 0.85, "T2": 0.3, "T3": -0.2, "T4": -0.6}
        fe = np.array([w.u_est[a["i"]] for a in self.att])
        ni = np.array([a["items"] for a in self.att])
        st = np.array([tier_start[w.cand_tier[a["i"]]] for a in self.att])
        self.adm = X.administer_all(r, fe, ni, self.bank, st)
        self.suite_script = suite_script(self.bank)
        self.suite_adm = np.tile(self.suite_script, (len(self.suite), 1))

    def exposure_frame(self):
        ids = self.bank["id"]
        B, A, Pn, I, T = [], [], [], [], []
        for k, a in enumerate(self.att):
            i = a["i"]
            items = self.adm[k][: a["items"]]
            span = (a["end"] - a["start"]).total_seconds() / max(len(items), 1)
            for p, it in enumerate(items):
                B.append(a.get("bk") or self.booking[i]); A.append(a["att"]); Pn.append(p + 1); I.append(ids[it])
                T.append(naive_utc(a["start"] + dt.timedelta(seconds=int(p * span))))
        for q, items in zip(self.suite, self.suite_adm):
            span = (q["end"] - q["start"]).total_seconds() / 16
            for p, it in enumerate(items):
                B.append(q["bk"]); A.append(1); Pn.append(p + 1); I.append(ids[it])
                T.append(naive_utc(q["start"] + dt.timedelta(seconds=int(p * span))))
        df = pd.DataFrame({"booking_ref": B, "attempt_no": A, "position": Pn, "item_id": I, "shown_utc": T})
        return df.sort_values(["shown_utc", "booking_ref", "attempt_no", "position"], kind="stable").reset_index(drop=True)

    def bank_frame(self):
        """the operational bank, the items retired before the 2028 season and the pretest pool the replacements come
        from (calibrated on pretest forms, not administered in MAT-R)"""
        b = self.bank
        df = pd.DataFrame({"item_id": b["id"], "content_area": b["area"], "difficulty_b": b["b"],
                           "discrimination_a": b["a"], "introduced": b["intro"], "status": "operational"})
        r = np.random.default_rng(P.SEED + 17)
        taken = set(b["id"].tolist())
        extra = []
        for status, n, intro in (("retired", 23, ("2024-07-01", "2025-06-30", "2026-06-29")), ("pretest", 41, ("2028-06-26",))):
            for _ in range(n):
                v = "R%04d" % int(r.integers(1000, 9999))
                while v in taken:
                    v = "R%04d" % int(r.integers(1000, 9999))
                taken.add(v)
                extra.append((v, str(r.choice(X.AREAS)), round(float(r.normal(-0.3, 1.0)), 3),
                              round(float(np.exp(r.normal(0.12, 0.25))), 2), str(r.choice(intro)), status))
        df = pd.concat([df, pd.DataFrame(extra, columns=df.columns)], ignore_index=True)
        return df.sort_values("item_id").reset_index(drop=True)

    # ------------------------------------------------------------------ results shared with client accounts
    def _shares(self):
        w, r = self.w, self.rng
        nvk = w.acc["NVK"]
        cols = sorted(set(w.cand_college[nvk["members"]].tolist()))
        self.pgl_cols = set(r.choice(cols, size=max(4, len(cols) // 3), replace=False).tolist())
        recs = []
        for i, code in w.apps:
            a = w.acc[code]
            sd = w.sit_date[i]
            if a["f28"] in ("D1", "S"):
                when = ist(sd, int(r.integers(13 * 60, 19 * 60)))
            elif a["f28"] == "L":
                when = ist(sd + dt.timedelta(days=int(r.integers(9, 40))), int(r.integers(8 * 60, 23 * 60)))
            else:
                when = ist(sd + dt.timedelta(days=int(r.integers(14, 56))), int(r.integers(8 * 60, 23 * 60)))
            acct = code
            if code == "NVK" and w.cand_college[i] in self.pgl_cols and when.date() < MERGE_DAY:
                acct = "PGL"
            ch = "campus drive" if a["f28"] in ("D1", "S", "L") else "careers page"
            recs.append([self.cand_id[i], acct, when, ch, "withdrawn" if r.random() < 0.021 else "active"])
        extra = []
        for row in recs:
            if RESEND_FROM <= row[2].date() <= RESEND_TO and r.random() < 0.62:
                extra.append([row[0], row[1], dt.datetime(2028, 8, 14, 21, 5, tzinfo=P.IST) + dt.timedelta(minutes=int(r.integers(0, 140))), row[3], row[4]])
        allr = recs + extra
        sid = r.choice(np.arange(10000000, 99999999), len(allr), replace=False)
        self.shares = [["SH%08d" % s] + row for s, row in zip(sid, allr)]

    def shares_frame(self):
        recs = [(s[0], s[1], s[2], s[3].strftime("%d/%m/%Y %H:%M"), s[4], s[5]) for s in self.shares]
        df = pd.DataFrame(recs, columns=["share_id", "candidate_id", "account_code", "shared_at_ist", "channel", "share_status"])
        key = pd.to_datetime(df["shared_at_ist"], format="%d/%m/%Y %H:%M")
        return df.assign(_k=key).sort_values(["_k", "share_id"], kind="stable").drop(columns="_k").reset_index(drop=True)

    # ------------------------------------------------------------------ 2028 shortlists, selection days and cases
    def _shortlists(self):
        w, r = self.w, self.rng
        rows = []
        for code, sl in w.short28.items():
            a = w.acc[code]
            for rank, i in enumerate(sl, 1):
                f = a["f28"]
                if f in ("D1", "S"):
                    day, venue = w.sit_date[i] + dt.timedelta(days=2), "campus"
                elif f == "L":
                    day, venue = dt.date(2028, 9, 4) + dt.timedelta(days=int(r.integers(0, 22))), "campus"
                else:
                    day = dt.date(2028, 10, 9) + dt.timedelta(days=int(r.integers(0, 40)))
                    venue = str(r.choice(["Bengaluru centre", "Pune centre", "Hyderabad centre"]))
                u = r.random()
                outcome = "attended" if u < 0.87 else ("no show" if u < 0.95 else ("rescheduled" if u < 0.98 else "withdrew"))
                acct = code
                if code == "NVK" and w.cand_college[i] in self.pgl_cols and day < MERGE_DAY:
                    acct = "PGL"
                rows.append(dict(acct=acct, i=i, rank=rank, day=day, venue=venue, outcome=outcome))
        self.sl_rows = rows

    def _cases(self):
        """a proxy sitting is found at the first selection day the candidate attends (most of the time) by the
        photo and ID check; a second account whose selection day falls while that case is still open opens its own
        case on the same sitting; once a case confirms, the result is voided and later selection days see the
        candidate as voided; a candidate may appeal, and the desk logs the appeal as a case of its own, opened after
        the sitting's last decision and decided by the desk (overturned or confirmed); a few cases are decided
        inconclusive before the desk's final decision; a handful of genuine candidates are opened on a look-alike
        and cleared. Case references run in the order cases are opened."""
        w, r = self.w, np.random.default_rng(P.SEED + CASE_SEED)
        by_cand = {}
        for s in self.sl_rows:
            by_cand.setdefault(s["i"], []).append(s)
        cases = []
        self.void_win = {}
        for i, lst in by_cand.items():
            lst = sorted(lst, key=lambda s: s["day"])
            att = [s for s in lst if s["outcome"] == "attended"]
            if not att:
                continue
            if w.proxy[i]:
                if r.random() > 0.84:
                    continue
                first = att[0]
                closed = first["day"] + dt.timedelta(days=int(r.integers(4, 21)))
                appeal = r.random() < 0.20
                incon = r.random() < 0.12
                if incon:
                    cases.append(dict(i=i, acct=first["acct"], opened=first["day"], finding="inconclusive",
                                      closed=first["day"] + dt.timedelta(days=int(r.integers(2, 4)))))
                cases.append(dict(i=i, acct=first["acct"], opened=first["day"], finding="confirmed impersonation", closed=closed))
                last = closed
                for s in att[1:]:
                    if s["day"] < closed and s["acct"] != first["acct"]:
                        c2 = s["day"] + dt.timedelta(days=int(r.integers(3, 15)))
                        cases.append(dict(i=i, acct=s["acct"], opened=s["day"], finding="confirmed impersonation", closed=c2))
                        last = max(last, c2)
                if appeal:
                    a_open = last + dt.timedelta(days=int(r.integers(2, 21)))
                    a_dec = a_open + dt.timedelta(days=int(r.integers(7, 31)))
                    over = r.random() < 0.55
                    cases.append(dict(i=i, acct=first["acct"], opened=a_open, desk=True, closed=a_dec,
                                      finding="overturned on appeal" if over else "confirmed on appeal"))
                    self.void_win[i] = (closed, a_dec if over else None)
                else:
                    self.void_win[i] = (closed, None)
            elif r.random() < 0.0024:
                s = att[0]
                cases.append(dict(i=i, acct=s["acct"], opened=s["day"], finding="cleared",
                                  closed=s["day"] + dt.timedelta(days=int(r.integers(2, 15)))))
        # one reference per case, in the order the cases were opened; a case's decisions share its reference
        keyed = {}
        for c in cases:
            keyed.setdefault((c["i"], c["acct"], c["opened"], c.get("desk", False)), []).append(c)
        order = sorted(keyed, key=lambda k: (k[2], int(self.cand_id[k[0]][2:]), k[1], k[3]))
        for n, k in enumerate(order, 1):
            for c in keyed[k]:
                c["ref"] = n
        # voided results: selection days inside the void window list the candidate as voided
        for s in self.sl_rows:
            v = self.void_win.get(s["i"])
            if v is not None and s["day"] > v[0] and (v[1] is None or s["day"] <= v[1]):
                s["outcome"] = "result voided"
        self.cases = cases

    def shortlists_frame(self):
        recs = [(s["acct"], self.cand_id[s["i"]], s["rank"], s["day"].strftime("%d-%b-%Y"), s["venue"], s["outcome"])
                for s in self.sl_rows]
        return pd.DataFrame(recs, columns=["account_code", "candidate_id", "shortlist_rank", "selection_day", "venue", "outcome"])

    def cases_frame(self):
        """the booking reference is typed by the account's selection-day lead; the centre-run accounts' leads leave it
        blank (their case sheet has no booking field); the desk keys it on the cases it opens itself"""
        centre = {a[0] for a in P.ACCOUNTS if a[5] == "C"}
        recs = [("IC-28-%04d" % c["ref"], c["opened"], c["acct"], self.cand_id[c["i"]],
                 "" if (c["acct"] in centre and not c.get("desk")) else self.booking[c["i"]], c["finding"], c["closed"])
                for c in self.cases]
        df = pd.DataFrame(recs, columns=["case_ref", "opened", "account_code", "candidate_id", "booking_ref",
                                         "finding", "decided"])
        return df.sort_values(["decided", "case_ref"], kind="stable").reset_index(drop=True)

    # ------------------------------------------------------------------ the equivalence study
    def _study(self):
        w, r = self.w, self.rng
        s = w.study
        m = len(s["theta"])
        base = dt.date(2028, 10, 16)
        self.st_rows = []
        vid = r.choice(np.arange(10000, 99999), m, replace=False)
        for k in range(m):
            d0 = base + dt.timedelta(days=int(r.integers(0, 12)))
            t0 = ist(d0, int(r.integers(9 * 60, 16 * 60)))
            d1 = d0 + dt.timedelta(days=int(s["gap"][k]))
            t1 = ist(d1, int(r.integers(9 * 60, 17 * 60)))
            att = bool(s["attended"][k])
            self.st_rows.append(("EQ-%05d" % vid[k], self.short_code[int(s["col"][k])], t0.strftime("%Y-%m-%d %H:%M"),
                                 float(s["u"][k]), float(s["u_se"][k]),
                                 t1.strftime("%Y-%m-%d %H:%M") if att else "",
                                 float(s["v"][k]) if att else np.nan, float(s["v_se"][k]) if att else np.nan))

    def study_frame(self):
        df = pd.DataFrame(self.st_rows, columns=["volunteer_id", "college_code", "mat_r_started_ist", "mat_r_logit",
                                                 "mat_r_se", "mat_v_started_ist", "mat_v_logit", "mat_v_se"])
        return df.sort_values(["mat_r_started_ist", "volunteer_id"], kind="stable").reset_index(drop=True)
