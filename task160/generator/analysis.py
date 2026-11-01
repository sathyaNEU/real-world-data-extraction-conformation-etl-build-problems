"""Every figure the build grades, the rungs of the ladder and the licensed variants, computed from target/ alone."""
import datetime as dt
import os

import numpy as np
import pandas as pd
from openpyxl import load_workbook

FILES = {
    "history": "QRMC_MedAlertHistory_20250101-20261025.csv",
    "background": "QRMC_MSP26_BackgroundLog_20260706-20261025.csv",
    "census": "QRMC_UnitCensus_Daily_20250101-20261025.csv",
    "plan": "QRMC_FY2027_Inpatient_Volume_Plan.xlsx",
    "register": "QRMC_MedAlert_Rule_Register_20261026.xlsx",
    "queue": "CRV_QueueExport_QRMC_20260630-20261001.csv",
    "pocmap": "CRV_PointOfCare_Map_QRMC.csv",
}
EXISTING = ("DDI_SEVERE", "DRUG_ALLERGY", "MAX_DOSE")
DUP, QT = "MSP26_DUP_OPIOID_PRN", "MSP26_QT_COMBO"
BG0, B_END = pd.Timestamp("2026-07-06"), pd.Timestamp("2026-10-26")
LOG0 = pd.Timestamp("2025-01-01")
FC0, FC_WEEKS = pd.Timestamp("2027-01-04"), 13
Q3 = (pd.Timestamp("2026-07-01"), pd.Timestamp("2026-10-01"))
MONTHS = ("2026-07", "2026-08", "2026-09")
SHIFTS = ("Day", "Evening", "Night")


def r100(x):
    return int(np.floor(x / 100.0 + 0.5) * 100)


def shift_of(ts):
    h = ts.hour
    return "Day" if 7 <= h < 15 else ("Evening" if 15 <= h < 23 else "Night")


class Pack:
    def __init__(self, target):
        f = {k: os.path.join(target, v) for k, v in FILES.items()}
        wb = load_workbook(f["register"], read_only=True)
        units = list(wb["Units"].iter_rows(min_row=2, values_only=True))
        rules = list(wb["Rules"].iter_rows(min_row=2, values_only=True))
        self.old2code = {r[2]: r[0] for r in units if r and r[0]}
        self.units = [r[0] for r in units if r and r[0]]
        live = [r for r in rules if r and r[0] == DUP and r[4] == "Live"]
        self.pilot = [u.strip() for u in live[0][5].split(",")]
        self.going_live = [u for u in self.units if u not in self.pilot]
        h = pd.read_csv(f["history"], dtype=str, keep_default_na=False)
        self.raw_rows = len(h)
        h["dept"] = h["department"].map(lambda d: self.old2code.get(d, d))
        self.hist_all = h
        h = h.drop_duplicates(subset=[c for c in h.columns if c != "dept"])
        h["t"] = pd.to_datetime(h["alert_dttm"])
        self.hist = h
        bg = pd.read_csv(f["background"], dtype=str, keep_default_na=False)
        bg["t"] = (pd.to_datetime(bg["eval_utc"], utc=True).dt.tz_convert("America/New_York")
                   .dt.tz_localize(None))
        self.bg = bg
        c = pd.read_csv(f["census"], dtype={"department": str})
        c["census_date"] = pd.to_datetime(c["census_date"])
        self.census = c
        wb = load_workbook(f["plan"], read_only=True)
        rows = [r for r in wb["Weekly plan"].iter_rows(min_row=2, values_only=True) if r and r[0]]
        self.plan = pd.DataFrame(rows, columns=["week", "dept", "adm", "pd"])
        self.plan["week"] = pd.to_datetime(self.plan["week"])
        q = pd.read_csv(f["queue"], dtype=str, keep_default_na=False)
        # Each row's clock is read off the alert it carries: a message reaches the queue seconds after its alert
        # fired, so a stamp four hours ahead of the alert history's local time is UTC and one level with it is
        # Eastern already (the rows the new queue platform wrote).
        when = dict(zip(self.hist["alert_id"].astype(int), self.hist["t"]))
        fired = q["alert_ref"].astype(int).map(when)
        naive = pd.to_datetime(q["msg_received_utc"].str.rstrip("Z"))
        q["lead_h"] = (naive - fired).dt.total_seconds() / 3600.0
        utc_row = q["lead_h"] > 2.0
        for col in ("claimed_utc", "closed_utc", "msg_received_utc"):
            conv = pd.to_datetime(q[col], utc=True).dt.tz_convert("America/New_York").dt.tz_localize(None)
            raw = pd.to_datetime(q[col].str.rstrip("Z"))
            q[col.replace("_utc", "_et")] = conv.where(utc_row, raw)
            q[col.replace("_utc", "_su")] = conv
        q["utc_row"] = utc_row
        q["handle_min"] = q["handle_min"].astype(float)
        self.queue = q
        self.pocmap = pd.read_csv(f["pocmap"], dtype=str, keep_default_na=False)

    # ------------------------------------------------------------------ the call
    def pilot_rates(self, window="all", kind="pooled"):
        h = self.hist[self.hist["dept"].isin(self.pilot)]
        if window == "last12":
            h = h[h["t"] >= pd.Timestamp("2025-10-26")]
        elif window == "bg":
            h = h[h["t"] >= BG0]
        elif window == "2025":
            h = h[h["t"] < pd.Timestamp("2026-01-01")]
        if kind == "alone":
            n = h.groupby(["order_id", "alert_dttm"])["alert_id"].transform("count")
            h = h[n == 1]
        d = h[h["alert_rule_id"] == DUP]
        q = h[h["alert_rule_id"] == QT]
        c = (d["user_action"] == "Order removed").mean()
        p = (q["user_action"] == "Overridden").mean()
        return float(c), float(p), len(d), len(q)

    def call(self, rates=("all", "pooled"), b0=BG0, b1=B_END, proj="admissions", combine="product",
             qt_removed="exclude", partner=True, own=True, c=None, p=None, unit_level=False, dedupe=True,
             encounter=False):
        cc, pp, _nd, _nq = self.pilot_rates(*rates)
        c = cc if c is None else c
        p = pp if p is None else p
        h = self.hist if dedupe else self.hist_all.assign(t=pd.to_datetime(self.hist_all["alert_dttm"]))
        hb = h[h["dept"].isin(self.going_live) & (h["t"] >= b0) & (h["t"] < b1)]
        rev = hb[hb["alert_rule_id"].isin(EXISTING) & (hb["user_action"] == "Overridden")]
        bg = self.bg[self.bg["t"] < b1]
        bgw = bg[bg["t"] >= b0]
        removed = set(self.hist.loc[self.hist["user_action"] == "Order removed", "order_id"])
        qt_rows = bgw[bgw["rule_id"] == QT]
        if qt_removed == "exclude":
            qt_rows = qt_rows[~qt_rows["order_id"].isin(removed)]
        dup_orders = set(bg.loc[bg["rule_id"] == DUP, "order_id"])
        qt_orders = set(bg.loc[bg["rule_id"] == QT, "order_id"])
        dup_enc = set(bg.loc[bg["rule_id"] == DUP, "pat_enc_csn_id"])
        d = np.zeros(len(rev))
        if own:
            d += rev["order_id"].isin(dup_orders).to_numpy()
        if partner:
            d += rev["interacting_order_id"].isin(dup_orders).to_numpy()
        qh = rev["order_id"].isin(qt_orders).to_numpy().astype(float)
        if encounter:
            loss = np.where(rev["pat_enc_csn_id"].isin(dup_enc).to_numpy(), c, 0.0)
        elif combine == "product":
            loss = 1.0 - (1.0 - c) ** d * p ** qh
        else:
            loss = np.minimum(1.0, d * c + qh * (1.0 - p))
        rev = rev.assign(loss=loss)
        qt_by = qt_rows.groupby("department").size()
        pre_by = rev.groupby("dept")["loss"].sum()
        cen = self.census[self.census["department"].isin(self.going_live) & (self.census["census_date"] >= b0)
                          & (self.census["census_date"] < b1)]
        weeks = self.plan[(self.plan["week"] >= FC0) & (self.plan["week"] < FC0 + pd.Timedelta(weeks=FC_WEEKS))
                          & self.plan["dept"].isin(self.going_live)]
        days_b = (b1 - b0).days
        out = {"c": c, "p": p, "reviews_B": len(rev), "qt_rows_B": len(qt_rows),
               "qt_add_B": p * len(qt_rows), "pre_B": float(rev["loss"].sum()),
               "adm_B": int(cen["admissions"].sum()), "pd_B": int(cen["midnight_census"].sum()),
               "plan_adm": int(weeks["adm"].sum()), "plan_pd": int(weeks["pd"].sum()), "days_B": days_b}
        out["net_B"] = out["qt_add_B"] - out["pre_B"]
        if unit_level:
            adm_u = cen.groupby("department")["admissions"].sum()
            plan_u = weeks.groupby("dept")["adm"].sum()
            qa = sum(p * qt_by.get(u, 0) * plan_u.get(u, 0) / adm_u[u] for u in self.going_live)
            pr = sum(pre_by.get(u, 0.0) * plan_u.get(u, 0) / adm_u[u] for u in self.going_live)
            scale = None
        else:
            scale = {"admissions": out["plan_adm"] / out["adm_B"], "patient_days": out["plan_pd"] / out["pd_B"],
                     "weeks": FC_WEEKS * 7.0 / days_b}[proj]
            qa, pr = out["qt_add_B"] * scale, out["pre_B"] * scale
        out.update({"scale": scale, "qt_add": qa, "pre": pr, "net": qa - pr})
        return out

    def golden(self):
        return self.call()

    def call_tasks(self):
        """The call read with a queue task, not an overridden alert, as the review (the reading Schedule B 2.1 and 2.3
        rule out): a task is lost only when every alert it carries is lost, and a QT alert opens a task only on an
        order no other overridden alert already brought to the desk."""
        g = self.call()
        c, p = g["c"], g["p"]
        h = self.hist
        hb = h[h["dept"].isin(self.going_live) & (h["t"] >= BG0) & (h["t"] < B_END)]
        rev = hb[hb["alert_rule_id"].isin(EXISTING) & (hb["user_action"] == "Overridden")]
        bg = self.bg[self.bg["t"] < B_END]
        bgw = bg[bg["t"] >= BG0]
        dup_o = set(bg.loc[bg["rule_id"] == DUP, "order_id"])
        qt_o = set(bg.loc[bg["rule_id"] == QT, "order_id"])
        lost = 0.0
        for (_o, _t), grp in rev.groupby(["order_id", "alert_dttm"]):
            o = grp["order_id"].iloc[0]
            keep_own = (1 - c) ** (o in dup_o) * (p if o in qt_o else 1.0)
            all_partner_lost = float(np.prod([c if x in dup_o else 0.0 for x in grp["interacting_order_id"]]))
            lost += (1 - keep_own) + keep_own * all_partner_lost
        removed = set(h.loc[h["user_action"] == "Order removed", "order_id"])
        has_task = set(h.loc[(h["severity"] == "High") & (h["user_action"] == "Overridden"), "order_id"])
        qt_rows = bgw[(bgw["rule_id"] == QT) & ~bgw["order_id"].isin(removed)]
        added = p * float((~qt_rows["order_id"].isin(has_task)).sum())
        return {"added": added * g["scale"], "lost": lost * g["scale"], "net": (added - lost) * g["scale"]}

    def rungs(self):
        g = self.call()
        own = self.call(partner=False)
        full = self.call(c=1.0)
        enc = self.call(encounter=True)
        dup_ack = g["qt_add"] + (1 - g["c"]) * len(self.bg[(self.bg["rule_id"] == DUP)]) * g["scale"]
        return {"R0_silent_mode": g["qt_add"], "R0b_duplicate_alerts_as_reviews": dup_ack,
                "R1_own_order_only": own["net"], "R2_golden": g["net"], "R3_every_duplicate_removed": full["net"],
                "R4_whole_encounter": enc["net"]}

    def variants(self):
        """The standing family: every construction the filed text and the data leave defensible."""
        v = {}
        for w in ("all", "last12", "bg", "2025"):
            for k in ("pooled", "alone"):
                v["rates %s %s" % (w, k)] = self.call(rates=(w, k))
        for proj in ("admissions", "patient_days", "weeks"):
            v["projection %s" % proj] = self.call(proj=proj)
        v["projection by unit"] = self.call(unit_level=True)
        v["base 13 weeks to 25 Oct"] = self.call(b0=pd.Timestamp("2026-07-27"))
        v["base from 13 Jul"] = self.call(b0=pd.Timestamp("2026-07-13"))
        v["base Jul to Sep"] = self.call(b1=pd.Timestamp("2026-10-01"))
        v["additive removal"] = self.call(combine="additive")
        v["QT rows on removed orders kept"] = self.call(qt_removed="include")
        v["boundary duplicates kept"] = self.call(dedupe=False)
        return v

    # ------------------------------------------------------------------ the asks
    def q3_sessions(self, clock="et"):
        """clock 'et': each row's own clock; 'stored_utc': every stamp read as the UTC its column names; 'raw': the
        stamps taken as Eastern with no conversion."""
        q = self.queue
        col = {"et": q["closed_et"], "stored_utc": q["closed_su"],
               "raw": pd.to_datetime(q["closed_utc"].str.rstrip("Z"))}[clock]
        q = q.assign(close_used=col)
        return q[(col >= Q3[0]) & (col < Q3[1])]

    def alert_dept(self):
        h = self.hist.drop_duplicates("alert_id")
        return dict(zip(h["alert_id"].astype(int), h["dept"]))

    def ask_a(self, ward="alert", time="timestamps", clock="et"):
        """Desk hours on reviews from each ward going live, July to September 2026."""
        q = self.q3_sessions(clock)
        if ward == "alert":
            m = self.alert_dept()
            wd = q["alert_ref"].astype(int).map(m)
        else:
            pm = dict(zip(self.pocmap["point_of_care"], self.pocmap["point_of_care"]))
            wd = q["poc_location"].str.split("^").str[1].map(pm)
        if time == "timestamps":
            hrs = (pd.to_datetime(q["closed_utc"].str.rstrip("Z")) - pd.to_datetime(q["claimed_utc"].str.rstrip("Z"))
                   ).dt.total_seconds() / 3600.0
        elif time == "handle_all":
            hrs = q["handle_min"] / 60.0
        else:   # handle minutes on the signed-off session only
            hrs = np.where(q["close_status"] == "Signed off", q["handle_min"] / 60.0, 0.0)
        s = pd.Series(np.asarray(hrs, dtype=float), index=q.index).groupby(wd).sum()
        return {u: float(s.get(u, 0.0)) for u in self.going_live}

    def bundle_size(self):
        h = self.hist[(self.hist["severity"] == "High") & (self.hist["user_action"] == "Overridden")]
        n = h.groupby(["order_id", "alert_dttm"]).size()
        first = h.sort_values("alert_id").drop_duplicates(["order_id", "alert_dttm"])
        return dict(zip(first["alert_id"].astype(int), [int(n[(o, t)]) for o, t in
                                                         zip(first["order_id"], first["alert_dttm"])]))

    def ask_b(self, count="alerts", clock="et", scope="all"):
        """Reviews signed off in each shift of each month, July to September 2026."""
        q = self.q3_sessions(clock)
        q = q[q["close_status"] == "Signed off"]
        if scope == "going_live":
            dept = self.alert_dept()
            q = q[q["alert_ref"].astype(int).map(dept).isin(self.going_live)]
        ts = q["close_used"]
        if count == "alerts":
            bs = self.bundle_size()
            n = q["alert_ref"].astype(int).map(bs).fillna(1).astype(int)
        else:
            n = pd.Series(1, index=q.index)
        key = [(t.strftime("%Y-%m"), shift_of(t)) for t in ts]
        out = {(m, s): 0 for m in MONTHS for s in SHIFTS}
        for k, v in zip(key, n):
            if k in out:
                out[k] += int(v)
        return out


def figures(P):
    g = P.golden()
    a = P.ask_a()
    b = P.ask_b()
    f = {"call_net_change": r100(g["net"]), "qt_reviews_added": r100(g["qt_add"]),
         "current_reviews_removed": r100(g["pre"])}
    for u, v in a.items():
        f["desk_hours_%s" % u] = int(np.floor(v + 0.5))
    for (m, s), v in b.items():
        f["signed_off_%s_%s" % (m, s.lower())] = v
    return f
