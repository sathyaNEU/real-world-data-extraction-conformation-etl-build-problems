"""task239 exports: what the survey platform, the scanning bureau, HR and the tablets' own log hold about the 2027
Staff Voice survey, written from the world's returns the way each system records them."""
import datetime as dt

import numpy as np
import pandas as pd

import params as P

ONLINE_Q = ["Q1", "Q2"] + ["Q3%s" % c for c in "abcdefghijkl"] + ["Q4%s" % c for c in "abcdef"]
PAPER_Q = ["Q1", "Q2"] + ["Q3_%02d" % k for k in range(1, 13)] + ["Q4_%d" % k for k in range(1, 7)]
PAGES = [2, 8, 14, 20]                    # questions answered by the end of pages 1 to 4


def utc(t):
    return (t - dt.timedelta(hours=P.UTC_OFFSET)).strftime("%Y-%m-%dT%H:%M:%SZ")


class Records:
    def __init__(self, W, seed=P.SEED + 1):
        self.W = W
        self.rng = np.random.default_rng(seed)
        self._sessions()

    # ---- online platform: personal links and site tablets -------------------------------------------------
    def _online_values(self, r):
        """the platform's codes for one return: 1 strongly disagree .. 5 strongly agree, 6 don't know, blank skipped"""
        vals = [str(self.W.m_group[r["member"]] + 1), str(self.W.m_years[r["member"]] + 1)]
        for j, it in enumerate(P.ITEMS):
            s = int(r["scored"][j])
            raw = 6 - s if it[2] else s
            nr = r["nr"][j]
            vals.append("6" if nr == "dk" else ("" if nr in ("skip", "multi") else str(raw)))
        for k, v in enumerate(r["engage"]):
            vals.append(str(v) if self.rng.random() > 0.01 else "")
        return vals

    def _sessions(self):
        W, rng = self.W, self.rng
        rows, ans = [], []
        site_tab = {s: ["%s-T%02d" % (s, k + 1) for k in range(n)] for s, n in P.TABLETS.items()}
        seq = {t: 0 for v in site_tab.values() for t in v}
        online = [r for r in W.rets if r["chan"] in ("personal", "site")]
        # abandoned sessions: personal links never submitted, and site sessions left part way
        idle = np.flatnonzero(W.m_email & ~W.m_resp)
        ab = rng.choice(idle, 1388, replace=False)
        stubs = []
        for m in ab:
            t = P.OPEN + dt.timedelta(minutes=float(rng.uniform(0, (P.CLOSE - P.OPEN).total_seconds() / 60 - 300)))
            stubs.append(dict(member=int(m), chan="personal", time=t.replace(microsecond=0), stub=True,
                              last_page=int(rng.choice([1, 2, 3, 4], p=[0.35, 0.3, 0.25, 0.1])),
                              status="open at close" if t > P.CLOSE - dt.timedelta(days=4) else "abandoned"))
        tabsites = [s for s in P.TABLETS]
        for k in range(117):
            s = tabsites[rng.integers(len(tabsites))]
            d = P.OPEN.date() + dt.timedelta(days=int(rng.integers(0, 28)))
            if d.weekday() >= 5:
                d = d - dt.timedelta(days=2)
            t = dt.datetime.combine(d, dt.time(0)) + dt.timedelta(hours=float(rng.uniform(8, 18.5)))
            if P.REFRESH_OFF <= t < P.REFRESH_ON + dt.timedelta(minutes=20):
                t = t + dt.timedelta(hours=2)
            stubs.append(dict(member=None, chan="site", site=s, time=t.replace(microsecond=0), stub=True,
                              last_page=int(rng.choice([1, 2, 3], p=[0.5, 0.3, 0.2])), status="abandoned"))
        allr = online + stubs
        # start times; a replayed tablet session keeps the tablet's start and reaches the platform later
        starts = []
        for r in allr:
            dur = float(rng.uniform(5, 38)) if r["chan"] == "personal" else float(rng.uniform(4, 16))
            st = r["time"] - dt.timedelta(minutes=dur)
            if r.get("stub"):
                st = r["time"]
            elif st < P.OPEN:
                st = P.OPEN + dt.timedelta(minutes=float(rng.uniform(0, 4)))
                r["time"] = (st + dt.timedelta(minutes=dur)).replace(microsecond=0)
            starts.append(st.replace(microsecond=0))
        recs = []
        for i, r in enumerate(allr):
            st = starts[i]
            ch = r["chan"]
            m = r.get("member")
            rec = dict(session_id="", link_type=ch, inv_code="", tablet_ref="", entered_code="", team_code="",
                       started_utc=utc(st), submitted_utc="", status="submitted", last_page=5)
            created = st
            if ch == "personal":
                rec["inv_code"] = W.m_inv[m]
            else:
                site = r.get("site") or W.site[W.m_team[m]]
                tab = site_tab[site][int(rng.integers(len(site_tab[site])))]
                rec["_tab"] = tab
                if r.get("entered"):
                    rec["entered_code"] = self._typed(W.m_inv[m])
            if r.get("stub"):
                rec["status"] = r["status"]
                rec["last_page"] = r["last_page"]
                if ch == "personal":
                    rec["team_code"] = W.code[W.m_team[m]]
                elif r["last_page"] >= 1 and rng.random() < 0.7:
                    pool = [c for c, s_ in zip(W.code, W.site) if s_ == r["site"]]
                    rec["team_code"] = pool[int(rng.integers(len(pool)))]
                vals = None
            else:
                rec["team_code"] = r["team_code"]
                up = r["time"] + dt.timedelta(seconds=float(rng.uniform(2, 90))) if ch == "site" else r["time"]
                rec["submitted_utc"] = utc(up.replace(microsecond=0))
                vals = self._online_values(r)
                r["received"] = up.replace(microsecond=0)
                if ch == "site":
                    created = up.replace(microsecond=0)
            recs.append((created, rec, vals, r))
            # a tablet that lost its connection re-sent the session when it reconnected
            if (ch == "site" and not r.get("stub") and W.site[W.m_team[m]] in P.SYNC_SITES and not r.get("entered")
                    and P.SYNC_FAULT[0] <= r["time"].date() <= P.SYNC_FAULT[1] and rng.random() < P.P_REPLAY):
                again = dict(rec)
                up2 = (up + dt.timedelta(minutes=float(rng.uniform(3, 300)))).replace(microsecond=0)
                again["submitted_utc"] = utc(up2)
                again["_replay_of"] = rec
                recs.append((up2, again, vals, r))
        # the tablets number their own sessions in the order they were started
        for tab in seq:
            mine = sorted([x for x in recs if x[1].get("_tab") == tab and "_replay_of" not in x[1]],
                          key=lambda x: x[1]["started_utc"])
            for k, x in enumerate(mine):
                x[1]["tablet_ref"] = "%s-%04d" % (tab, k + 1)
        for x in recs:
            if "_replay_of" in x[1]:
                x[1]["tablet_ref"] = x[1]["_replay_of"]["tablet_ref"]
        # the platform numbers sessions as they reach it
        recs.sort(key=lambda x: (x[0], x[1]["started_utc"]))
        # the platform's session numbers are shared with its other surveys, so the 2027 survey's run with gaps
        gaps = np.random.default_rng(P.SEED + 101)
        nxt = 400118
        self.replays = []
        for k, (created, rec, vals, r) in enumerate(recs):
            rng.integers(0, 3)                       # keeps the record stream as it was
            rec["session_id"] = "SV27-%06d" % nxt
            nxt += 1 + int(gaps.poisson(1.6 if 8 <= created.hour < 18 else 0.4))
        for created, rec, vals, r in recs:
            if "_replay_of" in rec:
                self.replays.append((rec["session_id"], rec["_replay_of"]["session_id"]))
            elif not r.get("stub"):
                r["session_id"] = rec["session_id"]
        for created, rec, vals, r in recs:
            out = {k: v for k, v in rec.items() if not k.startswith("_")}
            rows.append(out)
            nq = PAGES[rec["last_page"] - 1] if rec["status"] != "submitted" else len(ONLINE_Q)
            for q in range(nq):
                if vals is None:
                    if 2 <= q < 14:
                        v = str(int(rng.choice([1, 2, 3, 4, 5, 6], p=[0.07, 0.13, 0.2, 0.36, 0.2, 0.04])))
                    elif q < 2:
                        v = str(int(rng.integers(1, 9 if q == 0 else 6)))
                    else:
                        v = str(int(rng.integers(1, 6)))
                else:
                    v = vals[q]
                ans.append((rec["session_id"], ONLINE_Q[q], v))
        S = pd.DataFrame(rows)
        S = S.sort_values("started_utc", kind="stable").reset_index(drop=True)
        A = pd.DataFrame(ans, columns=["session_id", "question", "response"])
        A["_o"] = A["session_id"].map({s: k for k, s in enumerate(S["session_id"])})
        A["_q"] = A["question"].map({q: k for k, q in enumerate(ONLINE_Q)})
        A = A.sort_values(["_o", "_q"], kind="stable").drop(columns=["_o", "_q"]).reset_index(drop=True)
        self.S, self.A = S, A

    def _typed(self, code):
        u = self.rng.random()
        if u < 0.5:
            return code
        if u < 0.75:
            return code.lower()
        if u < 0.9:
            return code[:4] + " " + code[4:]
        return code[:4] + "-" + code[4:]

    def online_sessions(self):
        return self.S.copy()

    def online_answers(self):
        return self.A.copy()

    # ---- paper: the scanning bureau's file and the pack list --------------------------------------------
    def paper(self):
        W, rng = self.W, self.rng
        packs = np.flatnonzero(W.m_pack)
        serial = rng.choice(np.arange(310000, 399999), len(packs), replace=False)
        self.serial = {int(m): int(s) for m, s in zip(packs, serial)}
        rows = []
        pr = [r for r in W.rets if r["chan"] == "paper"]
        pr.sort(key=lambda r: r["time"])
        batch, last_day, n_in = 100, None, 0
        for r in pr:
            day = r["time"].date()
            if day != last_day or n_in >= 48:
                batch += 1
                n_in = 0
                last_day = day
            n_in += 1
            m = r["member"]
            vals = [str(W.m_group[m] + 1), str(W.m_years[m] + 1)]
            for j, it in enumerate(P.ITEMS):
                s = int(r["scored"][j])
                raw_online = 6 - s if it[2] else s
                nr = r["nr"][j]
                if r.get("blank"):
                    vals.append("9")
                elif nr == "dk":
                    vals.append("6")
                elif nr == "skip":
                    vals.append("9")
                elif nr == "multi":
                    vals.append("8")
                else:
                    vals.append(str(raw_online))
            for v in r["engage"]:
                vals.append("9" if r.get("blank") else str(v))
            if r.get("blank"):
                vals[0] = vals[1] = "9"
            rows.append([("B%03d" % batch), self.serial[m], r["time"].strftime("%Y-%m-%d %H:%M")] + vals)
            r["received"] = r["time"]
        cols = ["batch", "form_serial", "scanned_at"] + PAPER_Q
        return pd.DataFrame(rows, columns=cols)

    def packs(self):
        W, rng = self.W, self.rng
        rows = []
        for m in sorted(self.serial, key=lambda x: self.serial[x]):
            d = P.PACKS_POSTED[0] + dt.timedelta(days=int(rng.integers(0, 3)))
            rows.append((self.serial[m], W.m_inv[m], W.m_jul[m], P.PACKS_PRINTED.isoformat(), d.isoformat()))
        return pd.DataFrame(rows, columns=["form_serial", "inv_code", "team_code", "printed", "posted"])

    # ---- HR ------------------------------------------------------------------------------------------------
    def register(self):
        W = self.W
        sname = {s[0]: s[1] for s in P.SITES}
        dname = {d[0]: d[1] for d in P.DIVISIONS}
        rows = []
        for i in np.argsort(W.code):
            rows.append((W.code[i], W.name[i], dname[W.div[i]], dname.get(W.prev_div[i], ""), W.div_since[i],
                         sname[W.site[i]]))
        return pd.DataFrame(rows, columns=["team_code", "team_name", "division", "previous_division",
                                           "division_since", "site"])

    def reorg_map(self):
        W = self.W
        rows = []
        for code, name, d, succ, change in W.jul:
            if change == "unchanged":
                continue
            for i in succ:
                rows.append((code, name, W.code[i], W.name[i], change, P.REORG.isoformat()))
        for i in np.flatnonzero(np.isin(W.kind, ["new", "reissued"])):
            rows.append(("", "", W.code[i], W.name[i], "new team", P.REORG.isoformat()))
        df = pd.DataFrame(rows, columns=["old_code", "old_team_name", "new_code", "new_team_name", "change",
                                         "effective_from"])
        df["_k"] = df["old_code"].where(df["old_code"] != "", df["new_code"])
        return df.sort_values(["_k", "new_code"]).drop(columns="_k").reset_index(drop=True)

    def staff_in_post(self):
        W = self.W
        leave = np.random.default_rng(P.SEED + 303).binomial(W.size, 0.04)    # on long-term leave on 20 August
        rows = [(W.code[i], int(W.size[i]), int(W.size[i] - leave[i])) for i in np.argsort(W.code)]
        return pd.DataFrame(rows, columns=["team_code", "staff_in_post", "invited"])

    def tablet_log(self):
        rng = self.rng
        mdm = np.random.default_rng(P.SEED + 202)          # the device manager's own timing, apart from the records
        rows = []
        sname = {s[0]: s[1] for s in P.SITES}
        for s, n in P.TABLETS.items():
            for k in range(n):
                tab = "%s-T%02d" % (s, k + 1)
                inst = dt.datetime(2027, 8, 19 + int(rng.integers(0, 3)), 10, 0) + dt.timedelta(
                    minutes=int(rng.integers(0, 240)))
                rows.append((tab, sname[s], "installed", inst.strftime("%Y-%m-%d %H:%M")))
                t1 = P.LIST_LOADED + dt.timedelta(minutes=int(rng.integers(0, 50)))
                rows.append((tab, sname[s], "team list loaded", t1.strftime("%Y-%m-%d %H:%M")))
                off = P.REFRESH_OFF + dt.timedelta(minutes=int(mdm.integers(0, 13)))
                rows.append((tab, sname[s], "offline", off.strftime("%Y-%m-%d %H:%M")))
                t2 = P.REFRESH_ON - dt.timedelta(minutes=int(rng.integers(2, 25)))
                rows.append((tab, sname[s], "team list loaded", t2.strftime("%Y-%m-%d %H:%M")))
                on = t2 + dt.timedelta(minutes=int(mdm.integers(1, int((P.REFRESH_ON - t2).total_seconds() // 60) + 1)))
                rows.append((tab, sname[s], "online", on.strftime("%Y-%m-%d %H:%M")))
                t3 = dt.datetime(2027, 10, 5, 9, 0) + dt.timedelta(minutes=int(rng.integers(0, 300)))
                rows.append((tab, sname[s], "collected", t3.strftime("%Y-%m-%d %H:%M")))
        df = pd.DataFrame(rows, columns=["tablet", "site", "event", "at_local"])
        return df.sort_values(["at_local", "tablet"]).reset_index(drop=True)

    def items_2026(self):
        rows = []
        base = [71.4, 63.8, 74.9, 55.2, 83.6, 66.1, 52.7, 85.0, 61.9, 64.3, 70.2, 73.5]
        for (code, wording, neg, *_), b in zip(P.ITEMS, base):
            rows.append((code, wording, b, int(9300 + self.rng.integers(-450, 300))))
        return pd.DataFrame(rows, columns=["item", "wording", "percent_favourable_2026", "answers_2026"])
