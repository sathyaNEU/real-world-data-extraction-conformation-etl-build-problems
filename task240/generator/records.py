"""task240 records: the files the agency's systems write from the world. Each file draws from its own generator
(seed + 1000 onwards), so nothing here moves the simulated survey or another file."""
import datetime as dt

import numpy as np
import pandas as pd

import params as P


def stamp(t):
    return t.strftime("%Y-%m-%d %H:%M")


class Records:
    def __init__(self, W, seed=P.SEED):
        self.W = W
        self.seed = seed
        self.address = {a["address_id"]: a for a in W.addresses}
        self._roster()
        self._events()

    def rng(self, k):
        return np.random.default_rng([self.seed, 1000 + k])

    # ---------------------------------------------------------------- the analysis files: households, members, weights
    def _roster(self):
        """every member of each responding household: the adults the survey interviewed, then any children under 16
        on the household's roster (in roster order: the adults as the interviewer entered them, then the children)"""
        rng = self.rng(1)
        by_hh = {}
        for x in self.W.adults:
            by_hh.setdefault(x["address_id"], []).append(x)
        rows = []
        for hh in sorted(by_hh):
            ad = by_hh[hh]
            for x in ad:
                rows.append(dict(hh_id=hh, person_no=x["person_no"], age=x["age"], sex=x["sex"],
                                 proxy="Y" if x["proxy"] else "N", pension=x["q_pension"], care=x["q_care"]))
            ages = [x["age"] for x in ad]
            if len(ad) <= 3 and any(25 <= a <= 52 for a in ages):
                k = int(rng.choice(4, p=[0.52, 0.21, 0.19, 0.08]))
                top = min(15, max(ages) - 18)
                kids = sorted((int(rng.integers(0, top + 1)) for _ in range(k)), reverse=True)
                for j, age in enumerate(kids):
                    rows.append(dict(hh_id=hh, person_no=len(ad) + j + 1, age=age, sex=int(rng.integers(1, 3)),
                                     proxy="", pension=-1, care=-1))
        self.members_df = pd.DataFrame(rows)

    def households(self):
        W = self.W
        kids = self.members_df[self.members_df["age"] < 16].groupby("hh_id").size()
        first = {}
        for x in W.adults:
            first.setdefault(x["address_id"], x)
        rows = []
        for hh, x in sorted(first.items()):
            a = self.address[hh]
            ic = a["issues"][-1]["calls"][-1][0]
            n_ad = sum(1 for _ in a["ages"])
            rows.append(dict(hh_id=hh, region=x["region"], stratum=x["region"] + ("-U" if x["urban"] else "-R"),
                             psu=x["psu"], interview_date=ic.date().isoformat(), adults=n_ad,
                             children=int(kids.get(hh, 0)), tenure=x["q_tenure"], arrears=x["q_arrears"]))
        return pd.DataFrame(rows)

    def members(self):
        return self.members_df.copy()

    def weights(self):
        rows = [dict(hh_id=x["address_id"], person_no=x["person_no"], final_weight=round(x["w"], 3)) for x in self.W.adults]
        return pd.DataFrame(rows).sort_values(["hh_id", "person_no"]).reset_index(drop=True)

    # ---------------------------------------------------------------- the sample: issued addresses
    def issued(self):
        rng = self.rng(2)
        psu = {p["psu"]: p for p in self.W.psus}
        rows = []
        for a in self.W.addresses:
            p = psu[a["psu"]]
            kind = rng.choice(["house", "apartment", "row house", "other"],
                              p=[0.55, 0.25, 0.15, 0.05] if a["urban"] else [0.80, 0.05, 0.08, 0.07])
            rows.append(dict(address_id=a["address_id"], psu=a["psu"], region_code=p["old_region"], psu_frame=p["frame"],
                             dwelling=str(kind)))
        return pd.DataFrame(rows).sort_values(["psu", "address_id"]).reset_index(drop=True)

    # ---------------------------------------------------------------- fieldwork: every event, the outcome extract
    def _events(self):
        W, rng = self.W, self.rng(3)
        psu = {p["psu"]: p for p in W.psus}
        ev = []                             # [address, issue, time, type, result, interviewer, received, copy]
        self.when = {}                      # each call's time as the tablet logged it, to the minute
        minute = dt.timedelta(minutes=1)
        runs, rr = {}, self.rng(6)

        def mail_run(day):
            """the office's letters go out in one run a day, logged at that day's run time"""
            if day not in runs:
                runs[day] = dt.datetime.combine(day, dt.time(10)) + dt.timedelta(minutes=int(rr.integers(0, 330)))
            return runs[day]
        for a in W.addresses:
            if a["unworked"]:
                # the advance letter went out with the assignment; nobody called
                p = psu[a["psu"]]
                start = mail_run(p["start"] - dt.timedelta(days=int(rng.integers(4, 9))))
                ev.append([a["address_id"], 1, start, "LETTER", "", "OFFICE", None, False])
                continue
            used = set()
            for iss in a["issues"]:
                calls = iss["calls"]
                start = mail_run((calls[0][0] - dt.timedelta(days=int(rng.integers(4, 9)))).date())
                ev.append([a["address_id"], iss["issue"], start, "LETTER", "", "OFFICE", None, False])
                for j, (t, res) in enumerate(calls):
                    t = t.replace(second=0, microsecond=0)
                    while t in used:
                        t += minute
                    used.add(t)
                    self.when[(a["address_id"], iss["issue"], j)] = t
                    typ = "PHONE" if (j > 0 and res in ("NC", "AP", "RF") and rng.random() < 0.12) else "VISIT"
                    ev.append([a["address_id"], iss["issue"], t, typ, res, iss["interviewer"], None, False])
                    if typ == "VISIT" and res == "NC" and rng.random() < 0.4:
                        tc = t + minute
                        while tc in used:
                            tc += minute
                        used.add(tc)
                        ev.append([a["address_id"], iss["issue"], tc, "CARD", "", iss["interviewer"], None, False])
        for e in ev:
            if e[3] == "LETTER":
                e[6] = e[2] + dt.timedelta(minutes=int(rng.integers(12, 120)))
            else:
                e[6] = e[2] + dt.timedelta(minutes=int(rng.integers(90, 1320)))
        # tablets that synced after the outcome extract: the interview, and any call after the last one that reached
        # the office, arrived in October
        self.late_from = {}
        for a in W.addresses:
            if not a["late_sync"]:
                continue
            fin = a["issues"][-1]
            last_ok = self.when[(a["address_id"], fin["issue"], len(fin["calls"]) - 2)]
            self.late_from[a["address_id"]] = last_ok
            arrive = dt.datetime.combine(dt.date(2027, 10, int(rng.integers(2, 15))), dt.time(0)) + dt.timedelta(
                minutes=int(rng.integers(8 * 60, 18 * 60)))
            for e in ev:
                if e[0] == a["address_id"] and e[1] == fin["issue"] and e[2] > last_ok and e[3] != "LETTER":
                    e[6] = arrive
        # a tablet whose sync failed wrote the day's calls again when it next connected
        by_day = {}
        for i, e in enumerate(ev):
            if e[3] in ("VISIT", "PHONE") and e[6] < dt.datetime(2027, 9, 30):
                by_day.setdefault((e[5], e[2].date()), []).append(i)
        keys = sorted(by_day)
        region_of = {a["address_id"]: a["region"] for a in W.addresses}
        responded = {a["address_id"] for a in W.addresses if not a["unworked"] and a["final"] == 110}
        n_target = int(round(P.P_RESENT * sum(len(v) for v in by_day.values())))
        chosen, n = [], 0
        for kk in rng.permutation(len(keys)):
            if n >= n_target:
                break
            chosen.append(keys[kk])
            n += len(by_day[keys[kk]])
        for r in W.reg:
            if not any(region_of[ev[i][0]] == r and ev[i][0] in responded for kk in chosen for i in by_day[kk]):
                cand = [kk for kk in keys if any(region_of[ev[i][0]] == r and ev[i][0] in responded for i in by_day[kk])]
                chosen.append(cand[int(rng.integers(len(cand)))])
        copies = []
        for kk in chosen:
            last = max(ev[i][6] for i in by_day[kk])
            wrote = last + dt.timedelta(days=int(rng.integers(2, 6)), minutes=int(rng.integers(0, 600)))
            for i in by_day[kk]:
                e = ev[i]
                copies.append([e[0], e[1], e[2], e[3], e[4], e[5], wrote + dt.timedelta(minutes=int(rng.integers(1, 9))),
                               True, wrote])
        ev = [e + [e[2]] for e in ev] + copies
        df = pd.DataFrame(ev, columns=["address_id", "issue_no", "event_time", "event_type", "result", "interviewer_id",
                                       "received_at", "copy", "written"])
        # the tablet numbers each address's events for an issue in the order it writes them
        df = df.sort_values(["address_id", "issue_no", "written", "event_type"], kind="stable").reset_index(drop=True)
        df["event_no"] = df.groupby(["address_id", "issue_no"]).cumcount() + 1
        # the office numbers records as they arrive
        df = df.sort_values(["received_at", "address_id", "issue_no", "event_no"], kind="stable").reset_index(drop=True)
        ids, nxt = [], 5108231
        for _ in range(len(df)):
            ids.append("E%07d" % nxt)
            nxt += 1 + int(rng.poisson(0.7))
        df.insert(0, "record_id", ids)
        self.events = df

    def call_records(self):
        df = self.events.copy()
        df["event_time"] = df["event_time"].map(stamp)
        df["received_at"] = df["received_at"].map(stamp)
        return df[["record_id", "address_id", "issue_no", "event_no", "event_time", "event_type", "result",
                   "interviewer_id", "received_at"]]

    def outcomes(self):
        """the outcome file as extracted on 30 September: each worked issue's outcome as the office's case system held
        it, a case still open there carrying the status of its last call to reach the office"""
        rng = self.rng(4)
        rows = []
        for a in self.W.addresses:
            if a["unworked"]:
                continue
            for k, iss in enumerate(a["issues"]):
                code, when = iss["outcome"], iss["calls"][-1][0]
                if a["late_sync"] and k == len(a["issues"]) - 1:
                    synced = [(t, r) for j, (t, r) in enumerate(iss["calls"])
                              if self.when[(a["address_id"], iss["issue"], j)] <= self.late_from[a["address_id"]]]
                    when = synced[-1][0]
                    if any(r == "AP" for _, r in synced):
                        code = 230
                    else:
                        code = 220 if rng.random() >= P.P_UNKNOWN_IF_NOCONTACT else 310
                rows.append(dict(address_id=a["address_id"], issue_no=iss["issue"], interviewer_id=iss["interviewer"],
                                 outcome_code=code, outcome_date=when.date().isoformat()))
        return pd.DataFrame(rows).sort_values(["address_id", "issue_no"]).reset_index(drop=True)

    # ---------------------------------------------------------------- the distractors
    def population(self):
        rows = []
        for r in self.W.pop:
            lo, hi = r["band"]
            band = "%d to %d" % (lo, hi) if hi < 120 else "%d and over" % lo
            rows.append(dict(health_region=r["region"], sex="Male" if r["sex"] == 1 else "Female", age_band=band,
                             population_thousands=r["thousands"]))
        return pd.DataFrame(rows)

    def interviewers(self):
        rng = self.rng(5)
        rows = {}
        for p in self.W.psus:
            rr = rows.setdefault(p["interviewer"], dict(interviewer_id=p["interviewer"], home_region=p["region"],
                                                          psus_assigned=0, hours_claimed=0.0))
            rr["psus_assigned"] += 1
        for rr in rows.values():
            rr["hours_claimed"] = round(rr["psus_assigned"] * float(rng.uniform(26, 41)), 1)
        return pd.DataFrame(sorted(rows.values(), key=lambda r: r["interviewer_id"]))
