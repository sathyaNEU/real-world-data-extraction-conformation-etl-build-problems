"""task177 pack: every file under target/, cut from the world. The records here are what Daily Lantern Media's systems
export: the campaign tool's two lists, the CRM snapshot, the legacy billing system's invoice lines (on each
subscription's own day), the subscriptions platform's invoices and lines (UTC), the identifier crosswalk, the
subscription events, the offers engine's acceptances (UTC) and the email platform's log (UTC)."""
from __future__ import annotations

import datetime as dt
import json
import os

import numpy as np

import common as C
import world as W


def _dmy(d):
    return d.strftime("%d/%m/%Y")


def _utc_iso(t):
    return t.strftime("%Y-%m-%dT%H:%M:%SZ")


RUNS = [(dt.date(2026, 10, 1), dt.date(2026, 10, 31)), (dt.date(2026, 11, 1), dt.date(2026, 11, 30)),
        (dt.date(2026, 12, 1), dt.date(2026, 12, 31)), (dt.date(2027, 1, 1), dt.date(2027, 1, 31))]


def bill_line(s, mi, run, pend):
    """the platform line for subscription s in bill run mi, and whether it is the subscription's own first bill
    (raised on its start day); None before the subscription starts"""
    s0 = s["start"]
    if s0 > pend:
        return None
    if s["kind"] == "addon":
        code, name, price = C.ADDON_CODE, "Puzzles add-on", C.ADDON_PRICE
    else:
        code, name, price = C.PLAN_CODE[s["plan"]], "%s monthly" % s["plan"], C.PRICE[s["plan"]]
    if s0 >= C.MOVE and s0 >= run:            # joins on the platform this month: from its start day
        dn = (pend - s0).days + 1
        return (s["sub"], code, "%s (from %s)" % (name, s0.strftime("%d %b")), s0, pend,
                round(price * dn / pend.day, 2)), True
    if mi == 0 and s0 < C.MOVE:                 # the first platform bill runs on from the last legacy period
        k = s["dom"]
        st = dt.date(2026, 10, 1) if k == 1 else C.month_day(2026, 10, k)
        days = (pend - st).days + 1
        return (s["sub"], code, "%s (from %s)" % (name, st.strftime("%d %b")), st, pend,
                round(price * days / 31, 2)), False
    return (s["sub"], code, name, run, pend, price), False


class Records:
    """the world and every row the exports carry, built once"""

    def __init__(self):
        self.ly = W.last_year()
        self.ty, self.held, self.ex = W.this_year(self.ly)
        rng = C.stream("records")
        self.rng = rng
        self._offers_and_email()
        self._lbs_invoices()
        self._recentre_goodwill()
        self._sp_invoices()
        self._events()

    # ------------------------------------------------------------------------------------- goodwill credits
    def _recentre_goodwill(self):
        """goodwill credits (two pounds on a bill) re-centre this year's list billing cells inside their hundreds:
        a few hundred credits a month across the list, moved by at most a few dozen in any month and plan"""
        T = self.ty
        rc = C.stream("ty_recentre")
        loyal = T.loyal_month.values.copy()
        plan = T.plan.values
        subs = [dict(sub=T.sp_sub.iat[i], plan=plan[i], start=T.start.iat[i], dom=int(T.dom.iat[i]), kind="list")
                for i in range(len(T))]
        shift = {}
        for mi, (run, pend) in enumerate(RUNS):
            amt = np.array([np.nan if r is None else r[0][5] for r in (bill_line(s, mi, run, pend) for s in subs)])
            billed = ~np.isnan(amt)
            for pl in C.PLANS:
                sel = (plan == pl) & billed
                base = float(np.round(amt[sel], 2).sum())
                g = int(((loyal == mi) & sel).sum())
                ds = sorted(range(-40, 41), key=lambda x: (abs(x), x))
                good = [x for x in ds if C.edge(base - 2.0 * (g + x), 100) >= 30]
                x = good[0] if good else max(ds, key=lambda x: C.edge(base - 2.0 * (g + x), 100))
                if x > 0:
                    pool = np.where(sel & (loyal == -1))[0]
                    loyal[rc.choice(pool, x, replace=False)] = mi
                elif x < 0:
                    pool = np.where(sel & (loyal == mi))[0]
                    loyal[rc.choice(pool, -x, replace=False)] = -1
                shift[(mi, pl)] = x
        T["loyal_month"] = loyal
        self.goodwill_shift = shift

    # ---------------------------------------------------------------------------------------- legacy billing
    def _lbs_invoices(self):
        ly, ty, rng = self.ly, self.ty, self.rng
        rows = []          # (date, subscription_ref, line_type, item_code, applied_ref, amount_pence)
        cases = rng.choice(np.arange(4000000, 4999999), 3 * len(ly), replace=False)
        ci = 0
        L = ly
        lbs = L.lbs.values; plan = L.plan.values; bills = L.bills.values; end = L.end_bill.values
        acc = L.accepted.values; chan = L.channel.values; disc = L.disc_bills.values; desk = L.desk_bills.values
        restart = L.restart_day.values; loyal = L.loyal_bill.values
        for i in range(len(L)):
            price = int(round(C.PRICE[plan[i]] * 100))
            last = 5 if end[i] < 0 else min(end[i], 5)       # December 2025 (0) to April 2026 (4)
            pay_bills = list(range(0, last))
            for j in pay_bills:
                b = bills[i][j]
                rows.append((b, lbs[i], "SUB", C.PLAN_CODE[plan[i]], "", price))
                if j in disc[i]:
                    code = C.OFFER_CODE_APP if chan[i] == "app" else C.OFFER_CODE_WEB
                    rows.append((b, lbs[i], "DISC", code, self.acc_ref[i], -int(round(price * C.OFFER_SHARE))))
                if j in desk[i]:
                    rows.append((b, lbs[i], "DISC", C.DESK_CODE, "CS-%07d" % cases[ci], -int(round(price * C.OFFER_SHARE))))
                    ci += 1
                if loyal[i] == j:
                    rows.append((b, lbs[i], "CRED", C.LOYAL_CODE, "CS-%07d" % cases[ci], -200))
                    ci += 1
            if restart[i] is not None and restart[i] <= dt.date(2026, 4, 30):
                rd = restart[i]
                k = rd.day
                y, m = rd.year, rd.month
                d0 = rd
                while d0 <= dt.date(2026, 4, 30):
                    rows.append((d0, lbs[i], "SUB", C.PLAN_CODE[plan[i]], "", price))
                    y, m = C.add_months(dt.date(y, m, 1), 1)
                    d0 = C.month_day(y, m, k)
        # this year's list: August and September 2026 bills on each subscription's day, the add-ons' too, and the
        # legacy system's last run on 1 October for the day-1 subscriptions in the batches it still held
        T = ty
        t_dom, t_plan, t_lbs = T.dom.values, T.plan.values, T.lbs.values
        t_dupn, t_add, t_adom, t_albs, t_dupa = (T.dup_news.values, T.has_addon.values, T.addon_dom.values,
                                                 T.addon_lbs.values, T.dup_addon.values)
        ap = int(round(C.ADDON_PRICE * 100))
        t_start = T.start.values
        for i in range(len(T)):
            if t_start[i] >= C.MOVE:
                continue
            k = int(t_dom[i])
            price = int(round(C.PRICE[t_plan[i]] * 100))
            for (y, m) in ((2026, 8), (2026, 9)):
                b = C.month_day(y, m, k)
                if b >= t_start[i]:
                    rows.append((b, t_lbs[i], "SUB", C.PLAN_CODE[t_plan[i]], "", price))
            if t_dupn[i]:
                rows.append((C.LBS_LAST, t_lbs[i], "SUB", C.PLAN_CODE[t_plan[i]], "", price))
            if t_add[i]:
                ka = int(t_adom[i])
                for (y, m) in ((2026, 8), (2026, 9)):
                    rows.append((C.month_day(y, m, ka), t_albs[i], "SUB", C.ADDON_CODE, "", ap))
                if t_dupa[i]:
                    rows.append((C.LBS_LAST, t_albs[i], "SUB", C.ADDON_CODE, "", ap))
        # the other plan subscriptions on this year's accounts were billed by the legacy system too; they are not on
        # either list, so their bills take invoice numbers but are not in the pull
        n_pull = len(rows)
        X = self.ex
        for j in np.where(X.legacy.values)[0]:
            k = int(X.dom.iat[j])
            price = int(round(C.PRICE[X.plan.iat[j]] * 100))
            for (y, m) in ((2026, 8), (2026, 9)):
                b = C.month_day(y, m, k)
                if b >= X.start.iat[j]:
                    rows.append((b, X.lbs.iat[j], "SUB", C.PLAN_CODE[X.plan.iat[j]], "", price))
            if X.dup.iat[j]:
                rows.append((C.LBS_LAST, X.lbs.iat[j], "SUB", C.PLAN_CODE[X.plan.iat[j]], "", price))
        # overlap members' LY-era rows are already in from last year's list
        order = sorted(range(len(rows)), key=lambda j: (rows[j][0], rows[j][1], {"SUB": 0, "DISC": 1, "CRED": 2}[rows[j][2]]))
        out, inv_no, seen = [], {}, 0
        gaps = rng.integers(1, 9, len(rows))      # the pull is a part of the system's invoices
        for j in order:
            d, sub, lt, code, ref, amt = rows[j]
            key = (d, sub)
            if key not in inv_no:
                seen += int(gaps[j])
                inv_no[key] = "IN%08d" % (30410000 + seen)
            if j < n_pull:
                out.append((inv_no[key], sub, _dmy(d), lt, code, ref, amt, "Z", "PAID"))
        self.lbs_rows = out
        self.lbs_inv = inv_no       # (date, subscription_ref) -> invoice number

    # ------------------------------------------------------------------------------------ subscriptions platform
    def _sp_invoices(self):
        """one invoice per account in each 1st-of-month run, its lines one per subscription billed (the plan, the
        Puzzles add-on, another plan the account pays for); a subscription that joins on the platform has its first
        bill raised on its start day; credit notes on 14 October for the bills both systems raised for October"""
        T, X, rng = self.ty, self.ex, self.rng
        runs = RUNS
        # the subscriptions on each account, the account holder's own first
        subs = {}          # account -> list of dicts

        def item(sub, plan, start, dom, kind):
            return dict(sub=sub, plan=plan, start=start, dom=int(dom), kind=kind)

        for i in range(len(T)):
            acct = T.sp_acct.iat[i]
            subs.setdefault(acct, [])
        for j in range(len(X)):
            if X.kind.iat[j] == "payer":
                subs[X.sp_acct.iat[j]].append(item(X.sp_sub.iat[j], X.plan.iat[j], X.start.iat[j], X.dom.iat[j], "other"))
        self.list_row = {}
        for i in range(len(T)):
            acct = T.sp_acct.iat[i]
            subs[acct].append(item(T.sp_sub.iat[i], T.plan.iat[i], T.start.iat[i], T.dom.iat[i], "list"))
            self.list_row[T.sp_sub.iat[i]] = i
            if T.has_addon.iat[i]:
                subs[acct].append(dict(sub=T.addon_sp.iat[i], plan=None, start=T.start.iat[i], dom=int(T.addon_dom.iat[i]),
                                       kind="addon"))
        for j in range(len(X)):
            if X.kind.iat[j] == "second":
                subs[X.sp_acct.iat[j]].append(item(X.sp_sub.iat[j], X.plan.iat[j], X.start.iat[j], X.dom.iat[j], "other"))
        loyal = dict(zip(T.sp_sub.values, T.loyal_month.values))

        inv, credits, n_inv = [], [], 0
        accts = sorted(subs)
        for mi, (run, pend) in enumerate(runs):
            for acct in accts:
                own_docs = {}             # start day -> lines of the subscriptions that joined that day
                main = []
                for s in subs[acct]:
                    r = bill_line(s, mi, run, pend)
                    if r is None:
                        continue
                    ln, own = r
                    extra = []
                    if s["kind"] == "list" and loyal.get(s["sub"], -1) == mi:
                        extra = [(s["sub"], C.LOYAL_CODE, "Goodwill credit", run, pend, -2.00)]
                    if own:
                        # a joiner's first bill is raised on its start day, with an add-on taken the same day
                        own_docs.setdefault(ln[3], []).extend([ln] + extra)
                    else:
                        main += [ln] + extra
                docs = []
                if main:
                    docs.append((dt.datetime(run.year, run.month, run.day, 0, 5), main, run))
                for d0 in sorted(own_docs):
                    docs.append((dt.datetime(d0.year, d0.month, d0.day, 0, 5), own_docs[d0], d0))
                for t0, ls, pstart in docs:
                    n_inv += 1
                    iid = "INV-%07d" % (5200000 + n_inv)
                    issued = C.to_utc(t0 + dt.timedelta(seconds=int(rng.integers(0, 3300))))
                    total = round(sum(x[5] for x in ls), 2)
                    lj = json.dumps([{"line": li, "subscription_id": x[0], "item": x[1], "text": x[2],
                                      "from": x[3].isoformat(), "to": x[4].isoformat(), "amount": "%.2f" % x[5]}
                                     for li, x in enumerate(ls, 1)], separators=(",", ":"))
                    inv.append((iid, acct, ls[0][0], "invoice", _utc_iso(issued), pstart.isoformat(), pend.isoformat(),
                                "%.2f" % total, "0", "", "paid", lj))
        # credit notes on 14 October: each account the legacy system also billed for October, every such bill on it
        dup = {}
        for i in range(len(T)):
            a_ = T.sp_acct.iat[i]
            if T.dup_news.iat[i]:
                dup.setdefault(a_, []).append((T.lbs.iat[i], C.PRICE[T.plan.iat[i]]))
            if T.dup_addon.iat[i]:
                dup.setdefault(a_, []).append((T.addon_lbs.iat[i], C.ADDON_PRICE))
        for j in range(len(X)):
            if X.dup.iat[j]:
                dup.setdefault(X.sp_acct.iat[j], []).append((X.lbs.iat[j], C.PRICE[X.plan.iat[j]]))
        first_sub = {}
        for r in inv:
            if r[5] == "2026-10-01" and r[1] not in first_sub:
                first_sub[r[1]] = r[2]
        cn = 0
        for a_ in sorted(dup):
            covered = sorted(self.lbs_inv[(C.LBS_LAST, ref)] for ref, _ in dup[a_])
            amt = round(sum(p for _, p in dup[a_]), 2)
            cn += 1
            local = dt.datetime(2026, 10, 14, 11, 0) + dt.timedelta(seconds=int(rng.integers(0, 7200)))
            credits.append(("CRN-%06d" % (88000 + cn), a_, first_sub[a_], "credit_note", _utc_iso(C.to_utc(local)),
                            "2026-10-01", "2026-10-31", "%.2f" % -amt, "0", ";".join(covered), "refunded", "[]"))
        self.sp_inv = sorted(inv + credits, key=lambda r: (r[4], r[0]))

    # ------------------------------------------------------------------------------------------------ events
    def _events(self):
        ly, ty, rng = self.ly, self.ty, self.rng
        xw = {}                      # LBS ref -> (SP sub, SP account, batch) for subscriptions alive at the move
        ly_alive_oct = (ly.end_bill < 0) | (ly.end_bill >= 10)         # still subscribed when billing moved
        sp_ids = W.ids(C.stream("ly_sp"), len(ly), "S", 9, 410000000)
        sp_acc = W.ids(C.stream("ly_spa"), len(ly), "A", 8, 64300000)
        batches = C.stream("ly_batch").integers(1, 13, len(ly))
        over = ty[ty.from_ly]
        over_map = dict(zip(over.lbs, zip(over.sp_sub, over.sp_acct, over.batch)))
        lbs_v = ly.lbs.values
        for i in np.where(ly_alive_oct.values)[0]:
            ref = lbs_v[i]
            if ref in over_map:
                continue
            xw[ref] = (sp_ids[i], sp_acc[i], "MIG-%02d" % batches[i])
        for i in range(len(ty)):
            if not ty.legacy.iat[i]:
                continue
            xw[ty.lbs.iat[i]] = (ty.sp_sub.iat[i], ty.sp_acct.iat[i], ty.batch.iat[i])
            if ty.has_addon.iat[i]:
                xw[ty.addon_lbs.iat[i]] = (ty.addon_sp.iat[i], ty.sp_acct.iat[i], ty.batch.iat[i])
        self.xwalk = xw
        ev = []
        reasons = np.array(["price", "not reading enough", "switching title", "money is tight", "other"])
        endb = ly.end_bill.values; bills = ly.bills.values; lbs = ly.lbs.values; Tarm = ly["T"].values
        dd = ly.d.values; rst = ly.restart_day.values
        for i in np.where(endb >= 0)[0]:
            j = int(endb[i])
            b = bills[i][j]
            lag = int(rng.integers(1, 8))
            req = b - dt.timedelta(lag)
            if j == 2:
                req = max(req, C.LY_LIST + dt.timedelta(1)) if Tarm[i] == 1 and dd[i] > 1 else max(req, C.LY_LIST)
            end = b - dt.timedelta(1)
            key, sysname = lbs[i], "legacy"
            if b >= C.MOVE:
                key, sysname = self.xwalk.get(lbs[i], (lbs[i],))[0], "platform"
            why = reasons[int(rng.integers(0, len(reasons)))]
            ev.append((key, sysname, "cancel_requested", req.isoformat(), why))
            ev.append((key, sysname, "access_ended", end.isoformat(), ""))
            rd = rst[i]
            if rd is not None and rd <= C.PULL.date():          # a restart after the pull is not in it yet
                ev.append((key, sysname, "restarted", rd.isoformat(), ""))
        self.events = sorted(ev, key=lambda r: (r[3], r[0], r[2]))

    # ----------------------------------------------------------------------------------- offers and email (UTC)
    def _offers_and_email(self):
        ly, rng = self.ly, self.rng
        acc_rows, mail = [], []
        # app users whose app identity was replaced after they accepted (a re-login creates a new app user id;
        # the CRM keeps the current one)
        self.rekeyed = set()
        old_ids = W.ids(C.stream("old_app"), len(ly), "U", 8, 56000000)
        ev = []          # (utc time, LY index, key, channel, first acceptance?)
        for i in np.where(ly.accepted.values)[0]:
            day0 = ly.acc_day.iat[i]
            first_hour = dt.time(9, 35) if day0 == C.LY_LIST else dt.time(7, 0)
            span = int((dt.datetime.combine(day0, dt.time(22, 0)) - dt.datetime.combine(day0, first_hour)).total_seconds())
            t = dt.datetime.combine(day0, first_hour) + dt.timedelta(seconds=int(rng.integers(0, span)))
            ch = ly.channel.iat[i]
            if ch == "app":
                key = ly.app_user.iat[i]
                if rng.random() < 0.22:
                    key = old_ids[i]
                    self.rekeyed.add(i)
            else:
                key = ly.crm.iat[i]
            ev.append((C.to_utc(t), i, key, ch, True))
            if ly.also_email.iat[i]:
                t2 = t + dt.timedelta(minutes=int(rng.integers(20, 2000)))
                ev.append((C.to_utc(t2), i, ly.crm.iat[i], "email", False))
        ev.sort(key=lambda e: (e[0], e[1], not e[4]))
        self.acc_ref = {}
        for n_, (t, i, key, ch, first) in enumerate(ev):
            ref = "OE26-%06d" % (104201 + 7 * n_ + int(rng.integers(0, 7)))
            if first:
                self.acc_ref[i] = ref
            acc_rows.append((ref, "JAN26-HALF2", key, ch, _utc_iso(t), "accepted"))
        self.offers = acc_rows
        mi = 0
        crm, opened = ly.crm.values, ly.opened.values
        for i in np.where(ly["T"].values == 1)[0]:
            mi += 1
            sent = dt.datetime(2026, 1, 31, 9, 30) + dt.timedelta(seconds=int(rng.integers(0, 2400)))
            mid = "M26%07d" % (1100000 + mi)
            if rng.random() < 0.035:
                mail.append((mid, crm[i], "JAN26-HALF2", "bounced", _utc_iso(C.to_utc(sent + dt.timedelta(seconds=40)))))
                continue
            mail.append((mid, crm[i], "JAN26-HALF2", "delivered", _utc_iso(C.to_utc(sent + dt.timedelta(seconds=20)))))
            if opened[i]:
                ot = sent + dt.timedelta(minutes=int(rng.integers(5, 6 * 24 * 60)))
                mail.append((mid, crm[i], "JAN26-HALF2", "opened", _utc_iso(C.to_utc(ot))))
                if rng.random() < 0.28:
                    mail.append((mid, crm[i], "JAN26-HALF2", "clicked",
                                 _utc_iso(C.to_utc(ot + dt.timedelta(seconds=int(rng.integers(5, 600)))))))
        self.mail = sorted(mail, key=lambda r: (r[4], r[0]))


# -------------------------------------------------------------------------------------------------- writers
def write_assignment(out, R):
    ly = R.ly
    rng = C.stream("assign_times")
    mins = rng.integers(0, 40, len(ly))
    T = ly["T"].values
    sent = [(dt.datetime(2026, 1, 31, 9, 30) + dt.timedelta(minutes=int(m))).strftime("%d/%m/%Y %H:%M") if t == 1 else ""
            for t, m in zip(T, mins)]
    rows = list(zip(["RET-2026-01"] * len(ly), ly.lbs.values, ly.crm.values, np.where(T == 1, "offer", "holdout"),
                    ["%.3f" % s for s in ly.score.values], ly.band.values, sent))
    rows.sort(key=lambda r: r[1])
    return C.write_csv(os.path.join(out, C.F_ASSIGN), ["list_id", "subscription_ref", "customer_no", "arm", "risk_score",
                                                       "risk_band", "offer_sent_at"], rows)


def write_profile(out, R):
    ly = R.ly
    rows = list(zip(ly.crm.values, ly.lbs.values, ly.plan.values, [s.isoformat() for s in ly.start.values],
                    ly.region.values, ly.device.values, ly.arts.values.astype(int), ly.news.values.astype(int),
                    ly.supp.values.astype(int), ly.pay.values, ly.app_user.values))
    rows.sort(key=lambda r: r[0])
    return C.write_csv(os.path.join(out, C.F_PROFILE), ["customer_no", "subscription_ref", "plan", "started_on", "region",
                                                        "most_used_on", "articles_read_28d", "newsletters",
                                                        "support_contacts_90d", "payment_method", "app_user_id"], rows)


def write_list(out, R):
    ty = R.ty
    rows = list(zip(["RET-2027-01"] * len(ty), ty.sp_sub.values, ty.sp_acct.values, ty.crm.values, ty.plan.values,
                    [s.isoformat() for s in ty.start.values], ty.region.values, ty.device.values,
                    ty.arts.values.astype(int), ty.news.values.astype(int), ty.supp.values.astype(int), ty.pay.values,
                    ["%.3f" % s for s in ty.score.values], ty.band.values))
    rows.sort(key=lambda r: r[1])
    return C.write_csv(os.path.join(out, C.F_LIST), ["list_id", "subscription_id", "account_id", "customer_no", "plan",
                                                     "started_on", "region", "most_used_on", "articles_read_28d",
                                                     "newsletters", "support_contacts_90d", "payment_method",
                                                     "risk_score", "risk_band"], rows)


def write_lbs(out, R):
    return C.write_csv(os.path.join(out, C.F_LBS), ["invoice_no", "subscription_ref", "invoice_date", "line_type",
                                                    "item_code", "applied_ref", "amount_pence", "vat_code", "status"],
                       R.lbs_rows)


def write_sp(out, R):
    return C.write_csv(os.path.join(out, C.F_SPINV), ["invoice_id", "account_id", "subscription_id", "doc_type",
                                                      "issued_at", "period_start", "period_end", "amount_gbp",
                                                      "tax_rate", "covers", "status", "lines"], R.sp_inv, crlf=False)


def write_xwalk(out, R):
    rows = sorted((k, v[0], v[1], "2026-10-01", v[2]) for k, v in R.xwalk.items())
    return C.write_csv(os.path.join(out, C.F_XWALK), ["legacy_subscription_ref", "platform_subscription_id",
                                                      "platform_account_id", "migrated_on", "batch"], rows)


def write_events(out, R):
    return C.write_csv(os.path.join(out, C.F_EVENTS), ["subscription_key", "system", "event", "event_date", "reason"],
                       R.events)


def write_offers(out, R):
    return C.write_csv(os.path.join(out, C.F_OFFERS), ["acceptance_ref", "offer", "customer_key", "channel",
                                                       "accepted_at", "status"], R.offers, crlf=False)


def write_email(out, R):
    return C.write_csv(os.path.join(out, C.F_EMAIL), ["message_id", "customer_no", "campaign", "event", "event_at"],
                       R.mail, crlf=False)


def write_survey(out, R):
    """the reader survey's fourth-quarter export (both lists' members among the respondents)"""
    rng = C.stream("survey")
    pool = list(R.ty.crm.values) + list(R.ly.crm.values[R.ly.end_bill.values < 0])
    n = 9200
    who = rng.choice(np.array(pool), n, replace=False)
    days = [dt.date(2026, 10, 5) + dt.timedelta(int(x)) for x in rng.integers(0, 80, n)]
    sat = np.clip(np.round(rng.normal(6.4, 2.1, n)), 0, 10).astype(int)
    lik = np.where(sat <= 3, rng.choice(np.array(["very likely", "likely", "unlikely"]), n, p=[0.45, 0.4, 0.15]),
                   np.where(sat <= 6, rng.choice(np.array(["likely", "unlikely", "very unlikely"]), n, p=[0.3, 0.5, 0.2]),
                            rng.choice(np.array(["unlikely", "very unlikely"]), n, p=[0.35, 0.65])))
    why = rng.choice(np.array(["price", "not enough time to read", "quality of coverage", "app problems", "other news apps",
                               "nothing in particular"]), n, p=[0.27, 0.22, 0.12, 0.08, 0.11, 0.20])
    rows = sorted(zip(who, [d.isoformat() for d in days], sat, lik, why), key=lambda r: (r[1], r[0]))
    return C.write_csv(os.path.join(out, C.F_SURVEY), ["customer_no", "responded_on", "satisfaction",
                                                       "likely_to_cancel_3m", "main_reason"], rows)


_CACHE = {}


def records():
    if "R" not in _CACHE:
        _CACHE["R"] = Records()
    return _CACHE["R"]


def build_pack(out):
    import docs as D
    os.makedirs(out, exist_ok=True)
    R = records()
    n = {}
    n[C.F_ASSIGN] = write_assignment(out, R)
    n[C.F_PROFILE] = write_profile(out, R)
    n[C.F_LIST] = write_list(out, R)
    n[C.F_LBS] = write_lbs(out, R)
    n[C.F_SPINV] = write_sp(out, R)
    n[C.F_XWALK] = write_xwalk(out, R)
    n[C.F_EVENTS] = write_events(out, R)
    n[C.F_OFFERS] = write_offers(out, R)
    n[C.F_EMAIL] = write_email(out, R)
    n[C.F_SURVEY] = write_survey(out, R)
    D.write_note(out)
    D.write_validation(out)
    D.write_plan(out)
    D.write_dictionary(out)
    return n
