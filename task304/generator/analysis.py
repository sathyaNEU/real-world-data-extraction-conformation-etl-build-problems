"""task304 architecture 4: every rung and every graded figure, computed from target/ alone.

Nothing here reads the generator's world; it reads the files the organisation shipped, the way an analyst would.
"""
import datetime as dt
import json
import math
import os
import re
import zoneinfo
from collections import defaultdict

import pandas as pd

from io_util import pdf_text, read_csv, read_xlsx

TZ = {"BRL-BNE1": "Australia/Brisbane", "BRL-SYD2": "Australia/Sydney", "BRL-MEL1": "Australia/Melbourne",
      "BRL-ADL1": "Australia/Adelaide", "BRL-PER1": "Australia/Perth", "BRL-NTL1": "Australia/Sydney"}
HUB_OF_WCS = {"BRL-BNE1": "Larapinta", "BRL-SYD2": "Eastern Creek", "BRL-MEL1": "Truganina", "BRL-ADL1": "Wingfield",
              "BRL-PER1": "Kewdale", "BRL-NTL1": "Beresfield"}
TZ_SITE = {v: TZ[k] for k, v in HUB_OF_WCS.items()}
HUBS = ["Larapinta", "Eastern Creek", "Truganina", "Wingfield", "Kewdale", "Beresfield"]
REF_START, REF_END = dt.date(2026, 10, 12), dt.date(2026, 11, 8)
VEND_SITE = {"Brolga Larapinta DC": "Larapinta", "Brolga Eastern Creek DC": "Eastern Creek", "Brolga Truganina": "Truganina",
             "Brolga Wingfield": "Wingfield", "Brolga Kewdale DC": "Kewdale", "Brolga Beresfield": "Beresfield"}
AUDIO_SITE = {"BNE - Larapinta": "Larapinta", "SYD - Eastern Creek": "Eastern Creek", "MEL - Truganina": "Truganina",
              "ADL - Wingfield": "Wingfield", "PER - Kewdale": "Kewdale", "NTL - Beresfield": "Beresfield"}


def lex(t, Li, Lf, La, work=7.0, brk=1.0):
    t = min(max(t, 0.0), work)
    return 10 * math.log10((t * 10 ** (Li / 10) + (work - t) * 10 ** (Lf / 10) + brk * 10 ** (La / 10)) / 8.0)


def lex_daily_list(ts, Li, Lf, La, avg="energy"):
    vals = [lex(t, Li, Lf, La) for t in ts]
    if avg == "energy":
        return 10 * math.log10(sum(10 ** (v / 10) for v in vals) / len(vals))
    if avg == "arith":
        return sum(vals) / len(vals)
    s = sorted(vals)
    return s[len(s) // 2]


class Pack:
    def __init__(self, target):
        self.t = target
        self._levels()
        self._people()
        self._sessions()

    def p(self, name):
        return os.path.join(self.t, name)

    # ------------------------------------------------------------------ documents
    def _levels(self):
        txt = pdf_text(self.p("noise_survey_report_2026.pdf"))
        self.levels = {}
        for hub in HUBS:
            i = txt.index(hub + " (")
            seg = txt[i:i + 420]
            nums = re.findall(r"\b(\d{2,3}\.\d)\b", seg)
            self.levels[hub] = dict(Li=float(nums[0]), Lf=float(nums[1]), La=float(nums[2]))
        dtxt = pdf_text(self.p("induct_enclosure_design_report_rev2.pdf"))
        for hub in HUBS:
            m = re.search(re.escape(hub) + r" (\d+) (\d{2}\.\d) (\d{2}\.\d) ", dtxt)
            self.levels[hub]["Lp"] = float(m.group(3))
            self.levels[hub]["stations"] = int(m.group(1))

    # ------------------------------------------------------------------ people and shifts
    def _people(self):
        h, rows = read_csv(self.p("hr_employee_list_20261113.csv"))
        ix = {c: i for i, c in enumerate(h)}
        self.emp = {r[ix["payroll_no"]]: dict(site=r[ix["site"]], title=r[ix["position_title"]], kind="EMP") for r in rows}
        h, rows = read_csv(self.p("ta_shift_records_20260928_20261108.csv"))
        ix = {c: i for i, c in enumerate(h)}
        self.shifts = defaultdict(list)     # ref -> [date]
        self.shift_site = {}
        for r in rows:
            if r[ix["status"]] != "WORKED":
                continue
            d = dt.date.fromisoformat(r[ix["work_date"]])
            self.shifts[r[ix["emp_no"]]].append(d)
            self.shift_site[r[ix["emp_no"]]] = r[ix["site"]]
        self.lh = {}
        head, body = read_xlsx(self.p("labour_hire_timesheets_oct_nov_2026.xlsx"), "Tasman Workforce", header_row=3)
        ix = {c: i for i, c in enumerate(head)}
        for r in body:
            ref = r[ix["Worker No"]]
            d = r[ix["Date"]]
            d = d.date() if isinstance(d, dt.datetime) else d
            self.shifts[ref].append(d)
            self.shift_site[ref] = r[ix["Site"]]
            self.lh[ref] = dict(site=r[ix["Site"]], title="Operative (labour hire)", kind="LH")
        head, body = read_xlsx(self.p("labour_hire_timesheets_oct_nov_2026.xlsx"), "Meridian Labour Hire", header_row=2)
        ix = {c: i for i, c in enumerate(head)}
        for r in body:
            ref = r[ix["Worker ID"]]
            we = r[ix["Week ending"]]
            we = we.date() if isinstance(we, dt.datetime) else we
            for k, day in enumerate(["Mon", "Tue", "Wed", "Thu", "Fri"]):
                if r[ix[day]]:
                    self.shifts[ref].append(we - dt.timedelta(days=6 - k))
            self.shift_site[ref] = r[ix["Site"]]
            self.lh[ref] = dict(site=r[ix["Site"]], title="Operative (labour hire)", kind="LH")
        head, body = read_xlsx(self.p("badge_register_20261113.xlsx"), "Badges", header_row=1)
        ix = {c: i for i, c in enumerate(head)}
        self.badges = defaultdict(list)
        for r in body:
            iss = r[ix["Issued"]]
            can = r[ix["Cancelled"]]
            iss = iss.date() if isinstance(iss, dt.datetime) else iss
            can = can.date() if isinstance(can, dt.datetime) else can
            self.badges[str(r[ix["Badge ID"]])].append(dict(type=r[ix["Holder type"]], ref=str(r[ix["Holder ref"]]),
                                                            issued=iss, cancelled=can))

    def holder(self, badge, d):
        for b in self.badges.get(badge, []):
            if b["issued"] <= d and (b["cancelled"] is None or d < b["cancelled"]):
                return b
        return None

    def _sessions(self):
        df = pd.read_csv(self.p("wcs_operator_sessions_export_20261116.csv"), dtype=str)
        df["on"] = pd.to_datetime(df["logon_utc"], utc=True)
        df["off"] = pd.to_datetime(df["logoff_utc"], utc=True)
        df["site"] = df["site_code"].map(HUB_OF_WCS)
        loc_on = []
        for code, on in zip(df["site_code"], df["on"]):
            loc_on.append(on.tz_convert(zoneinfo.ZoneInfo(TZ[code])).tz_localize(None))
        df["local_on"] = loc_on
        df["shift_date"] = [(t - pd.Timedelta(hours=5)).date() for t in df["local_on"]]
        df["utc_date"] = [t.date() for t in df["on"]]
        df["hours"] = (df["off"] - df["on"]).dt.total_seconds() / 3600.0
        refs, kinds = [], []
        for b, d in zip(df["badge_id"], df["shift_date"]):
            h = self.holder(b, d)
            refs.append(h["ref"] if h else None)
            kinds.append(h["type"] if h else None)
        df["ref"] = refs
        df["holder_type"] = kinds
        self.sess = df

    # ------------------------------------------------------------------ exposure
    def workers(self, window=(REF_START, REF_END)):
        out = {}
        for ref, ds in self.shifts.items():
            n = sum(1 for d in ds if window[0] <= d <= window[1])
            if n == 0:
                continue
            info = self.emp.get(ref) or self.lh.get(ref)
            out[ref] = dict(site=self.shift_site[ref], title=info["title"], kind=info["kind"], shifts=n,
                            dates=sorted(d for d in ds if window[0] <= d <= window[1]))
        return out

    def induct_hours(self, tail="keep", date_basis="local", resolve_reissue=True, window=(REF_START, REF_END)):
        s = self.sess[self.sess["holder_type"].isin(["Employee", "Labour hire"])].copy()
        if not resolve_reissue:
            # a reader who maps each badge to its current holder only, ignoring cancelled badges
            cur = {}
            for b, recs in self.badges.items():
                for r in recs:
                    if r["cancelled"] is None:
                        cur[b] = r["ref"]
            s["ref"] = s["badge_id"].map(cur)
            s = s[s["ref"].notna()]
        hours = s["hours"].copy()
        if tail == "trim":
            hours = hours.where(s["logoff_reason"] != "AUTO_TIMEOUT", hours - 10 / 60.0)
        s = s.assign(h=hours)
        dcol = "shift_date" if date_basis == "local" else "utc_date"
        s = s[(s[dcol] >= window[0]) & (s[dcol] <= window[1])]
        per_day = s.groupby(["ref", "shift_date"])["h"].sum()
        tot = s.groupby("ref")["h"].sum()
        return tot.to_dict(), per_day

    def exposure_table(self, tail="keep", date_basis="local", denom="roster", avg="energy", breaks="amenities",
                       resolve_reissue=True, floor_shift=0.0):
        W = self.workers()
        tot, per_day = self.induct_hours(tail=tail, date_basis=date_basis, resolve_reissue=resolve_reissue)
        rows = []
        pdd = per_day.to_dict()
        for ref, w in W.items():
            lv = self.levels[w["site"]]
            Lf = lv["Lf"] + floor_shift
            La = lv["La"] if breaks == "amenities" else Lf
            ih = tot.get(ref, 0.0)
            if denom == "roster":
                n = w["shifts"]
            else:
                days_on = sum(1 for (r, d) in pdd if r == ref)
                n = days_on if days_on > 0 else w["shifts"]
            t = ih / n
            if avg == "energy":
                pre, post = lex(t, lv["Li"], Lf, La), lex(t, lv["Lp"], Lf, La)
            else:
                daily = [pdd.get((ref, d), 0.0) for d in w["dates"]]
                pre = lex_daily_list(daily, lv["Li"], Lf, La, avg)
                post = lex_daily_list(daily, lv["Lp"], Lf, La, avg)
            rows.append(dict(ref=ref, site=w["site"], title=w["title"], kind=w["kind"], shifts=w["shifts"],
                             induct_hours=ih, t=t, pre=pre, post=post))
        return pd.DataFrame(rows)

    @staticmethod
    def counts(tab):
        out = {}
        for hub in HUBS:
            x = tab[tab["site"] == hub]
            out[hub] = dict(pool=int((x["pre"] >= 85.0).sum()), below=int(((x["pre"] >= 85.0) & (x["post"] < 85.0)).sum()),
                            workers=int(len(x)))
        return out

    # ------------------------------------------------------------------ the rungs
    def rung_jobbased(self, tab):
        """R0: AS/NZS 1269.1's job-based strategy: induct titles at the induct area for the seven working hours, every
        other title on the floor; a labour-hire operative signed on to induct joins the induct group."""
        def seg1(title):
            tl = title.lower()
            return ("induct" in tl) or ("induction" in tl) or (tl == "sorter - relief")
        res = {}
        for hub in HUBS:
            x = tab[tab["site"] == hub]
            lv = self.levels[hub]
            pool = below = 0
            for _, r in x.iterrows():
                t = 7.0 if (seg1(r["title"]) or (r["kind"] == "LH" and r["induct_hours"] > 0)) else 0.0
                a, b = lex(t, lv["Li"], lv["Lf"], lv["La"]), lex(t, lv["Lp"], lv["Lf"], lv["La"])
                pool += a >= 85
                below += (a >= 85) and (b < 85)
            res[hub] = dict(pool=int(pool), below=int(below))
        return res

    def rung_signed_on(self, tab):
        """R1: everyone signed on to an induct station in the reference weeks at the induct group's seven hours."""
        res = {}
        for hub in HUBS:
            x = tab[tab["site"] == hub]
            lv = self.levels[hub]
            pool = below = 0
            for _, r in x.iterrows():
                t = 7.0 if r["induct_hours"] > 0 else 0.0
                a, b = lex(t, lv["Li"], lv["Lf"], lv["La"]), lex(t, lv["Lp"], lv["Lf"], lv["La"])
                pool += a >= 85
                below += (a >= 85) and (b < 85)
            res[hub] = dict(pool=int(pool), below=int(below))
        return res

    def rung_title_average(self, tab):
        """R2: each title's average induct hours a shift from the sessions, given to every member."""
        res = {}
        for hub in HUBS:
            x = tab[tab["site"] == hub]
            lv = self.levels[hub]
            pool = below = 0
            for title, g in x.groupby("title"):
                t = g["induct_hours"].sum() / g["shifts"].sum()
                a, b = lex(t, lv["Li"], lv["Lf"], lv["La"]), lex(t, lv["Lp"], lv["Lf"], lv["La"])
                pool += len(g) * (a >= 85)
                below += len(g) * ((a >= 85) and (b < 85))
            res[hub] = dict(pool=int(pool), below=int(below))
        return res

    def station_hours(self):
        """Induct station-hours signed on in the reference weeks by hub (the job-based route's reconciliation)."""
        s = self.sess[(self.sess["shift_date"] >= REF_START) & (self.sess["shift_date"] <= REF_END)]
        return s.groupby("site")["hours"].sum().to_dict()

    # ------------------------------------------------------------------ ask A
    def vending(self, site_basis="history", pack_basis="history", clock="local"):
        doc = json.load(open(self.p("ppe_vending_transactions_2026q3.json"), encoding="utf-8"))
        h, rows = read_csv(self.p("ppe_vending_service_visits_2026q3.csv"))
        ix = {c: i for i, c in enumerate(h)}
        visits = []
        for r in rows:
            d = dt.datetime.strptime(r[ix["visit_date"]], "%d/%m/%Y").date()
            visits.append(dict(date=d, machine=r[ix["machine_id"]], site=VEND_SITE[r[ix["site"]]], type=r[ix["visit_type"]],
                               product=r[ix["product_code"]], uom=r[ix["uom"]]))
        head, body = read_xlsx(self.p("ppe_vending_asset_list_20260930.xlsx"), "Machines", header_row=1)
        mi = {c: i for i, c in enumerate(head)}
        current = {r[mi["Machine ID"]]: VEND_SITE[r[mi["Site"]]] for r in body}
        # each machine's site by date: the site of its visits, moving on its commissioning visit at a new site
        tl = defaultdict(list)
        for v in sorted(visits, key=lambda v: (v["date"], v["type"] != "COMMISSION")):
            if not tl[v["machine"]] or tl[v["machine"]][-1][1] != v["site"]:
                start = v["date"] if tl[v["machine"]] else dt.date(2026, 1, 1)
                tl[v["machine"]].append((start, v["site"]))
        change = {v["machine"]: v["date"] for v in visits if v["type"] == "RANGE CHANGE"}
        out = defaultdict(int)
        for rec in doc["records"]:
            if rec["product_code"] != "EP-01":
                continue
            mach = rec["machine_id"]
            t = dt.datetime.strptime(rec["vend_utc"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=dt.timezone.utc)
            if site_basis == "history":
                site = None
                # site at the vend's UTC date is unambiguous: machines move over weekends with no vends in transit
                for start, s in tl[mach]:
                    if t.date() >= start - dt.timedelta(days=1):
                        site = s
            else:
                site = current[mach]
            if clock == "local":
                lt = t.astimezone(zoneinfo.ZoneInfo(TZ_SITE[site])).replace(tzinfo=None)
            else:
                lt = t.replace(tzinfo=None)
            if pack_basis == "history":
                pairs = 5 if lt.date() >= change[mach] else 1
            else:
                pairs = 5
            out[(site, lt.month)] += pairs
        return dict(out)

    # ------------------------------------------------------------------ ask B
    def audiometry(self, reference="rebuilt", hub_basis="at_retest", confirm=True):
        h, rows = read_csv(self.p("audiometry_results_2025_2026.csv"))
        ix = {c: i for i, c in enumerate(h)}
        tests = defaultdict(list)
        for r in rows:
            tests[r[ix["client_no"]]].append(dict(id=int(r[ix["test_id"]]), date=dt.date.fromisoformat(r[ix["test_date"]]),
                                                  type=r[ix["test_type"]],
                                                  L=[float(r[ix["L_2k"]]), float(r[ix["L_3k"]]), float(r[ix["L_4k"]])],
                                                  R=[float(r[ix["R_2k"]]), float(r[ix["R_3k"]]), float(r[ix["R_4k"]])]))
        head, body = read_xlsx(self.p("audiometry_clients_20261106.xlsx"), "Clients", header_row=1)
        ci = {c: i for i, c in enumerate(head)}
        clients = {r[ci["Client No"]]: dict(emp=str(r[ci["Employee No"]]), ref_test=int(r[ci["Reference test"]])) for r in body}
        th, trows = read_csv(self.p("hr_site_transfers_2026.csv"))
        ti = {c: i for i, c in enumerate(th)}
        transfers = defaultdict(list)
        for r in trows:
            transfers[r[ti["payroll_no"]]].append((dt.datetime.strptime(r[ti["effective_date"]], "%d/%m/%Y").date(),
                                                   r[ti["from_site"]], r[ti["to_site"]]))

        def hub_at(emp, d):
            site = self.emp[emp]["site"]
            if hub_basis == "at_retest" and emp in transfers:
                eff, frm, to = transfers[emp][0]
                return frm if d < eff else to
            return site

        def shift(t, ref):
            return max(sum(t[e][i] - ref[e][i] for i in range(3)) / 3.0 for e in ("L", "R"))

        out = defaultdict(set)
        for c, ts in tests.items():
            ts.sort(key=lambda t: (t["date"], t["id"]))
            emp = clients[c]["emp"]
            if reference == "rebuilt":
                ref = ts[0]
            else:
                ref = next(t for t in ts if t["id"] == clients[c]["ref_test"])
            for i, t in enumerate(ts):
                if t["type"] != "ANNUAL" or shift(t, ref) < 10.0:
                    continue
                if not confirm:
                    if t["date"].year == 2026:
                        out[hub_at(emp, t["date"])].add(emp)
                    continue
                rt = next((u for u in ts[i + 1:] if u["type"] == "RETEST" and 0 < (u["date"] - t["date"]).days <= 30), None)
                if rt is not None and shift(rt, ref) >= 10.0:
                    if rt["date"].year == 2026:
                        out[hub_at(emp, rt["date"])].add(emp)
                    if reference == "rebuilt":
                        ref = rt
        return {hub: len(out.get(hub, set())) for hub in HUBS}


def golden(target):
    pk = Pack(target)
    tab = pk.exposure_table()
    c = pk.counts(tab)
    best = max(HUBS, key=lambda h: c[h]["below"])
    second = sorted(HUBS, key=lambda h: -c[h]["below"])[1]
    return pk, tab, c, best, second
