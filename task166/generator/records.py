"""The shipped records, cut from the clean world, each in the layout of the system that writes it, with the mess
those systems really make (the 2023 ERP cutover's legacy account codes and contributor format, ISBNs with and
without hyphens, credits raised days after the distributor books a delivery in, damaged-in-transit claims credited
beside returns, a re-sent receipts batch, other publishers' copies in returned parcels, a delivery booked in twice,
hurts re-inspected by tote).  Nothing here is authored apart from the world's event lists."""
from __future__ import annotations

import datetime as dt
import os
import sqlite3

import numpy as np
import pandas as pd

import common as K

CUTOVER = dt.date(2023, 2, 6)        # the ERP went live; earlier ledger rows keep the legacy account codes
PANEL_FROM = dt.date(2024, 11, 2)    # the panel extract: weeks ending 2 November 2024 to 31 October 2026
DIST_FROM = dt.date(2024, 11, 1)     # the distributor's returns files cover FY2025 and FY2026

F_LEDGER = "marrowgate_sales_ledger_FY2022-FY2026.sqlite"
F_TITLES = "title_master_2026-10-30.xlsx"
F_ACCOUNTS = "trade_accounts_2026-10-30.csv"
F_RA = "tallowmere_returns_authorisations_FY2025-FY2026.csv"
F_RECEIPTS = "tallowmere_returns_received_FY2025-FY2026.csv"
F_REINSPECT = "tallowmere_hurts_reinspection_FY2026.xlsx"
F_PANEL = "uk_consumer_sales_panel_weekly_FY2025-FY2026.csv"
F_PRINT = "print_orders_FY2025-FY2026.csv"
F_STOCK = "tallowmere_stock_on_hand_2026-10-30.csv"
F_TERMS = "marrowgate_terms_of_trade_2024.pdf"
F_POLICY = "marrowgate_accounting_policies_FY2026.pdf"


def day_date(day):
    return K.DAY0 + dt.timedelta(days=int(day))


def legacy_contributor(name):
    first, last = name.split(" ", 1)
    return "%s, %s" % (last.upper(), first)


def legacy_format(fmt):
    return {"Hardback": "HB", "Trade paperback": "TPB", "Paperback": "PB"}[fmt]


def new_format(fmt):
    return {"Hardback": "Hardback", "Trade paperback": "Trade Paperback", "Paperback": "Paperback"}[fmt]


class Records:
    """Clean tables keyed the way the systems key them, plus the shipped (messy) versions."""

    def __init__(self, W):
        self.W = W
        self.acc = {a.aid: a for a in W.accounts}
        self.wbi = {w.wid: w for w in W.works}
        r = K.rng("records")
        # the distributor's own consignor references for Marrowgate's accounts
        self.consignor = {}
        used = set()
        for a in W.accounts:
            stem = "".join(ch for ch in a.name.upper() if ch.isalpha())[:3]
            while True:
                ref = "%s%03d" % (stem, int(r.integers(1, 999)))
                if ref not in used:
                    used.add(ref)
                    break
            self.consignor[a.aid] = ref
        # accounts opened after the cutover have no legacy code
        self.opened_after = {a.aid for a in W.accounts if a.channel == "Independent" and r.random() < 0.15}
        self._titles()
        self._ledger()
        self._distributor()
        self._panel()
        self._distractors()

    # ------------------------------------------------------------------------------------------------------------
    def _titles(self):
        W, r = self.W, K.rng("titles")
        rp = K.rng("titles-paperback")
        cover = {"crime": ["A Thriller", "A Mystery"], "literary": ["A Novel"], "commercial": ["A Novel", "A Love Story"]}
        rows = []
        for e in W.eds:
            w = self.wbi[e.wid]
            title = e.title
            if (not e.is_first) and e.fmt == "Paperback" and w.retitle == "same" and rp.random() < 0.5 and w.kind in cover:
                title = "%s: %s" % (e.title, cover[w.kind][int(rp.integers(len(cover[w.kind])))])
            legacy = e.pub < dt.date(2023, 1, 1)          # records created in the old bibliographic system
            if e.pub > K.YEAR_END:
                status = "Forthcoming"
            elif e.pub < dt.date(2016, 1, 1) and r.random() < 0.35:
                status = "Out of print"
            elif e.fmt == "Hardback" and e.succ_pub and e.succ_pub < dt.date(2025, 6, 1) and r.random() < 0.6:
                status = "Out of print"
            else:
                status = "Active"
            rows.append(dict(eid=e.eid - 1, isbn13=e.isbn, title=title,
                             contributor=legacy_contributor(e.contributor) if legacy else e.contributor,
                             imprint=w.imprint, format=legacy_format(e.fmt) if legacy else new_format(e.fmt),
                             fmt=e.fmt, pub_date=e.pub, rrp_gbp=e.rrp, status=status, wid=e.wid))
        self.titles = pd.DataFrame(rows)

    def _acct_ref(self, aid, day):
        a = self.acc[aid]
        if day_date(day) < CUTOVER and aid not in self.opened_after:
            return a.legacy
        return a.code

    def _ledger(self):
        W = self.W
        isbn = {i: e.isbn for i, e in enumerate(W.eds)}
        rrp = {i: e.rrp for i, e in enumerate(W.eds)}
        start = (K.EXTRACT_FROM - K.DAY0).days
        end = (K.YEAR_END - K.DAY0).days
        inv = []
        self.inv_day = {}
        for (no, wk, wd, aid, eid, q, pr) in W.invoices:
            day = 7 * wk + wd
            self.inv_day[no] = day
            if not (start <= day <= end):
                continue
            if aid in self.opened_after and day_date(day) < dt.date(2023, 3, 1):
                continue
            disc = round(1 - pr / rrp[eid], 4)
            inv.append(dict(invoice_no="SI%08d" % no, invoice_day=day, aid=aid, eid=eid, isbn13=isbn[eid], qty=q,
                            unit_rrp=rrp[eid], discount_pct=round(100 * disc, 1), net_value=round(q * pr, 2), net_price=pr))
        self.invoices = pd.DataFrame(inv)
        cr = []
        for (no, day, aid, eid, q, invno, pr, ra, reason) in W.credits:
            if not (start <= day <= end):
                continue
            if aid in self.opened_after and day_date(self.inv_day[invno]) < dt.date(2023, 3, 1):
                continue                    # the account's trade before it was opened on the new system is not in this ledger
            cr.append(dict(credit_no="CN%07d" % no, credit_day=day, aid=aid, eid=eid, isbn13=isbn[eid], qty=q,
                           net_value=round(q * pr, 2), invoice_no="SI%08d" % invno, inv_day=self.inv_day[invno],
                           reason=reason, ra_no=("RA%06d" % ra) if ra else "", net_price=pr))
        self.credits = pd.DataFrame(cr)

    def _distributor(self):
        W, r = self.W, K.rng("distributor")
        isbn = {i: e.isbn for i, e in enumerate(W.eds)}
        start = (DIST_FROM - K.DAY0).days
        end = (K.LAST_DATA - K.DAY0).days
        ra = []
        for (no, day, aid, eid, q, lapsed) in W.returns:
            if start <= day <= end:
                ra.append(dict(ra_no="RA%06d" % no, ra_day=day, aid=aid, eid=eid, isbn13=isbn[eid], qty_authorised=q,
                               lapsed=lapsed))
        self.ra = pd.DataFrame(ra)
        rec = []
        tote_no = 310000
        totes = {}
        for (rc, dl, ra_no, aid, eid, day, q, s, h, u) in W.receipts:
            if not (start <= day <= end):
                continue
            tote = ""
            if h > 0:
                key = (eid, day // 7)
                if key not in totes:
                    tote_no += 1 + int(r.integers(0, 4))
                    totes[key] = tote_no
                tote = "T%06d" % totes[key]
            rec.append(dict(line_id=rc, delivery_no="D%07d" % dl, day=day, aid=aid, ra_no="RA%06d" % ra_no, eid=eid,
                            isbn13=isbn[eid], qty=q, saleable=s, hurt=h, unsaleable=u, tote=tote, ours=True))
        self.receipts = pd.DataFrame(rec)
        # re-inspection of hurts, a tote at a time, one to four weeks after the tote is closed
        ri = []
        if len(self.receipts):
            hh = self.receipts[self.receipts.hurt > 0].groupby("tote").agg(eid=("eid", "first"), hurt=("hurt", "sum"),
                                                                           last=("day", "max")).reset_index()
            for t in hh.itertuples():
                dday = int(t.last) + int(r.integers(7, 29))
                while day_date(dday).weekday() >= 5:
                    dday += 1
                pulped = int(r.binomial(int(t.hurt), 0.56))
                ri.append(dict(tote=t.tote, eid=int(t.eid), isbn13=isbn[int(t.eid)], day=dday, qty_inspected=int(t.hurt),
                               qty_restocked=int(t.hurt) - pulped, qty_pulped=pulped))
        self.reinspect = pd.DataFrame(ri)

    def _panel(self):
        W = self.W
        w0 = K.week_of(PANEL_FROM)
        rows = []
        isbn = [e.isbn for e in W.eds]
        for wk in range(w0, K.W_CUT + 1):
            col = W.panel[:, wk]
            nz = np.nonzero(col)[0]
            we = K.date_of(wk, 5)      # the panel's week ends on the Saturday
            for i in nz:
                rows.append((we, isbn[i], int(col[i])))
        self.panel = pd.DataFrame(rows, columns=["week_ending", "isbn13", "units"])

    def _distractors(self):
        W, r = self.W, K.rng("distractors")
        rows = []
        for i, e in enumerate(W.eds):
            if e.pub < dt.date(2024, 6, 1) and r.random() > 0.25:
                continue
            if e.pub > dt.date(2027, 4, 30):
                continue
            first = e.pub - dt.timedelta(days=int(r.integers(35, 70)))
            if first <= K.YEAR_END and first >= dt.date(2024, 11, 1):
                rows.append(dict(isbn13=e.isbn, po_date=first, kind="First printing",
                                 qty=int(round(e.strength * float(r.uniform(0.7, 1.3)) / 250.0)) * 250 + 1000,
                                 printer=str(r.choice(["Halden Print Group", "Corsley & Rudd Printers", "Wexcombe Press Services"]))))
            if e.pub < dt.date(2026, 6, 1) and r.random() < 0.3:
                rd = e.pub + dt.timedelta(days=int(r.integers(60, 400)))
                if dt.date(2024, 11, 1) <= rd <= K.YEAR_END:
                    rows.append(dict(isbn13=e.isbn, po_date=rd, kind="Reprint",
                                     qty=int(r.choice([1000, 1500, 2000, 3000, 5000])),
                                     printer=str(r.choice(["Halden Print Group", "Corsley & Rudd Printers"]))))
        self.print_orders = pd.DataFrame(rows).sort_values(["po_date", "isbn13"]).reset_index(drop=True)
        st = []
        for i, e in enumerate(W.eds):
            if e.pub > K.YEAR_END + dt.timedelta(days=90) or (e.pub < dt.date(2014, 1, 1) and r.random() < 0.5):
                continue
            base = max(0, int(e.strength * float(r.uniform(0.05, 0.4))))
            st.append(dict(isbn13=e.isbn, saleable=base, awaiting_inspection=int(r.integers(0, 40)) if base else 0,
                           reserved=int(r.integers(0, max(1, base // 10)))))
        self.stock = pd.DataFrame(st)


# ----------------------------------------------------------------------------------------------------------------
# Writers


def write_ledger(path, R):
    if os.path.exists(path):
        os.remove(path)
    con = sqlite3.connect(path)
    con.execute("PRAGMA page_size=4096")
    con.execute("""CREATE TABLE invoice_lines (invoice_no TEXT, invoice_date TEXT, account_ref TEXT, isbn TEXT,
                   qty INTEGER, unit_rrp REAL, discount_pct REAL, net_value REAL)""")
    con.execute("""CREATE TABLE credit_lines (credit_no TEXT, credit_date TEXT, account_ref TEXT, isbn TEXT,
                   qty INTEGER, net_value REAL, against_invoice TEXT, reason_code TEXT, ra_ref TEXT)""")
    rows = []
    for t in R.invoices.itertuples():
        d = day_date(t.invoice_day)
        isb = K.hyphenate(t.isbn13) if d < CUTOVER else t.isbn13
        rows.append((t.invoice_no, d.isoformat(), R._acct_ref(t.aid, t.invoice_day), isb, int(t.qty), float(t.unit_rrp),
                     float(t.discount_pct), float(t.net_value)))
    con.executemany("INSERT INTO invoice_lines VALUES (?,?,?,?,?,?,?,?)", rows)
    rows = []
    for t in R.credits.itertuples():
        d = day_date(t.credit_day)
        isb = K.hyphenate(t.isbn13) if d < CUTOVER else t.isbn13
        rows.append((t.credit_no, d.isoformat(), R._acct_ref(t.aid, t.credit_day), isb, int(t.qty), float(t.net_value),
                     t.invoice_no, t.reason, t.ra_no))
    con.executemany("INSERT INTO credit_lines VALUES (?,?,?,?,?,?,?,?,?)", rows)
    con.execute("CREATE INDEX ix_inv_no ON invoice_lines(invoice_no)")
    con.execute("CREATE INDEX ix_cr_inv ON credit_lines(against_invoice)")
    con.commit()
    con.execute("VACUUM")
    con.close()
    return len(R.invoices) + len(R.credits)


# ----------------------------------------------------------------------------------------------------------------
# The distributor's files, with what its systems do to them


CARTON = {"Chain": 40, "Wholesale": 40, "Supermarket": 30}     # copies to a returns carton from a hub or a depot


def shipped_receipts(R):
    """The returns-received export as Tallowmere sends it: one row per line of each delivery reference booked in.
    What its goods-in does: a consignment from a chain hub or a wholesale or supplier depot is booked carton by carton,
    each carton under its own delivery reference; a parcel from a client's account can hold another publisher's
    copies, booked on the delivery and sent on; an account now and then sends more copies of a title than its
    authorisation allows, booked as received and held for collection; a delivery is now and then booked in a second
    time by another goods-in clerk, the second booking never reversed; and one day's export was sent again inside
    the next file."""
    r = K.rng("receipts-mess")
    rec = R.receipts.sort_values(["day", "delivery_no", "line_id"]).reset_index(drop=True)
    ra_key = {(x.ra_no, x.eid): int(x.qty_authorised) for x in R.ra.itertuples()}
    ra_key = {(x.ra_no, x.eid): int(x.qty_authorised) for x in R.ra.itertuples()}
    units = []                      # [day, order key, rows, second booking, carton]
    for dl, g in rec.groupby("delivery_no", sort=False):
        aid = int(g.aid.iloc[0])
        cap = CARTON.get(R.acc[aid].channel)
        rows = g.to_dict("records")
        if cap is None or int(g.qty.sum()) <= cap:
            units.append([int(g.day.iloc[0]), (dl, 0), [dict(t) for t in rows], False, False])
            continue
        fill = lambda: cap - int(r.integers(0, 9))          # a packer fills a carton by space, not by count
        cartons, cur, room = [], [], fill()
        for t in rows:
            q, gr = int(t["qty"]), [int(t["saleable"]), int(t["hurt"]), int(t["unsaleable"])]
            while q > 0:
                take = min(q, room)
                gs = r.multivariate_hypergeometric(gr, take) if take < q else np.array(gr)
                cur.append(dict(t, qty=take, saleable=int(gs[0]), hurt=int(gs[1]), unsaleable=int(gs[2])))
                gr = [gr[0] - int(gs[0]), gr[1] - int(gs[1]), gr[2] - int(gs[2])]
                q -= take
                room -= take
                if room == 0:
                    cartons.append(cur)
                    cur, room = [], fill()
        if cur:
            cartons.append(cur)
        for k, c in enumerate(cartons):
            units.append([int(g.day.iloc[0]), (dl, k), c, False, True])
    ch = lambda u: R.acc[int(u[2][0]["aid"])].channel
    cellof = lambda u: "%s|%d-Q%d" % (ch(u), K.fy_of(day_date(u[0])), K.fy_quarter(day_date(u[0])))
    genuine = {}
    for u in units:
        for t in u[2]:
            k = (t["ra_no"], t["eid"])
            genuine[k] = genuine.get(k, 0) + int(t["qty"])
    sig = lambda u: tuple(sorted((t["ra_no"], t["eid"], int(t["qty"]), int(t["saleable"]), int(t["hurt"]), int(t["unsaleable"]))
                                 for t in u[2] if t["eid"] >= 0))
    twins = {}
    for u in units:
        twins[sig(u)] = twins.get(sig(u), 0) + 1
    # authorisation lines on which two units carry identical lines: no second booking or over-send is placed there
    twin_lines = {(a, e) for sg, n in twins.items() if n > 1 for a, e, *_ in sg}
    lines_of = lambda u: {(t["ra_no"], t["eid"]) for t in u[2] if t["eid"] >= 0}
    by_cell = {}
    for i, u in enumerate(units):
        by_cell.setdefault(cellof(u), []).append(i)
    other_isbn = [K.isbn13("97818914%04d" % int(x)) for x in r.integers(0, 9999, 60)]
    extra = []
    for c in sorted(by_cell):
        idx = by_cell[c]
        # another publisher's copies in a parcel
        for i in r.permutation(idx)[:min(len(idx), 1 + int(r.integers(0, 3)) + (2 if len(idx) > 400 else 0))]:
            t0 = units[i][2][0]
            q = int(r.integers(1, 7))
            hh = int(r.binomial(q, 0.06))
            units[i][2].append(dict(t0, eid=-1, isbn13=str(r.choice(other_isbn)), qty=q, saleable=q - hh, hurt=0, unsaleable=hh,
                                    tote="", ours=False))
        # more copies sent than authorised, on a line of an ordinary parcel delivered in full
        cand = [i for i in idx if not units[i][4] and not (lines_of(units[i]) & twin_lines)]
        n_over = 1 + int(r.integers(0, 3)) + (1 if len(idx) > 400 else 0)
        done = 0
        for i in r.permutation(cand):
            if done >= n_over:
                break
            ours = [t for t in units[i][2] if t["eid"] >= 0]
            t = ours[int(r.integers(0, len(ours)))]
            k = (t["ra_no"], t["eid"])
            if genuine.get(k, 0) != ra_key.get(k) or t.get("over"):
                continue
            plus = int(r.integers(1, 4))
            t["qty"] = int(t["qty"]) + plus
            t["saleable"] = int(t["saleable"]) + plus
            t["over"] = plus
            genuine[k] += plus
            done += 1
        # a second booking of a delivery whose lines had all come in full
        ok = [i for i in idx if not (lines_of(units[i]) & twin_lines) and not any(t.get("over") for t in units[i][2])
              and all(genuine.get((t["ra_no"], t["eid"]), -1) == ra_key.get((t["ra_no"], t["eid"])) for t in units[i][2] if t["eid"] >= 0)
              and int(sum(t["qty"] for t in units[i][2])) <= 60]
        k_d = min(len(ok), 1 + int(r.random() < 0.6) + (1 if len(idx) > 400 else 0))
        for i in r.permutation(ok)[:k_d]:
            u = units[i]
            day = u[0] + int(r.choice([0, 0, 1, 1, 2]))
            while day_date(day).weekday() >= 5:
                day += 1
            extra.append([day, None, [dict(t) for t in u[2]], True, u[4], int(i)])
    # delivery references: one sequence, in the order goods-in booked the units each day; a second booking falls
    # anywhere after the first on the same day, or anywhere in a later day's bookings
    pos = {}
    for d, grp in pd.Series(range(len(units))).groupby([u[0] for u in units]):
        ii = sorted(grp.values, key=lambda i: units[i][1])
        for j, i in enumerate(ii):
            pos[i] = (j + 0.5) / len(ii)
    allu = units + [e[:4] + [e[4]] for e in extra]
    for j, e in enumerate(extra):
        src = e[5] if len(e) > 5 else None
        pos[len(units) + j] = float(r.uniform(pos[src], 1.0)) if (src is not None and units[src][0] == e[0]) else float(r.random())
    order = sorted(range(len(allu)), key=lambda i: (allu[i][0], pos[i]))
    ref = 9100000
    out = []
    for i in order:
        ref += 1 + int(r.integers(0, 3))
        for t in allu[i][2]:
            t2 = dict(t)
            t2["delivery_no"] = "D%07d" % ref
            t2["day"] = allu[i][0]
            t2["double"] = bool(allu[i][3])
            t2.setdefault("over", 0)
            out.append(t2)
    out = pd.DataFrame(out)
    out["over"] = out["over"].fillna(0).astype(int)
    out["resent"] = False
    days = sorted(out.day.unique())
    pick = [d for d in days if dt.date(2026, 3, 1) <= day_date(d) <= dt.date(2026, 3, 31)]
    if pick:
        cnt = out[out.day.isin(pick)].groupby("day").size()
        d0 = int(cnt.idxmax())
        dup = out[out.day == d0].copy()
        dup["resent"] = True
        out = pd.concat([out, dup], ignore_index=True)
    out["_o"] = range(len(out))
    out = out.sort_values(["day", "delivery_no", "resent", "_o"]).drop(columns="_o").reset_index(drop=True)
    return out


def shipped_reinspection(R):
    """Hurts re-inspection, a tote at a time.  A big tote is sometimes worked in two sessions (two rows that add up
    to the tote); a tote is sometimes counted again after a query, the recount written as a fresh row that stands
    in place of the first (the same tote, the full quantity, a later date)."""
    r = K.rng("reinspect-mess")
    rows = []
    sheet0 = (dt.date(2025, 11, 1) - K.DAY0).days
    last = (K.LAST_DATA - K.DAY0).days
    for t in R.reinspect.sort_values(["day", "tote"]).itertuples():
        base = dict(tote=t.tote, isbn13=t.isbn13, eid=t.eid, kind="whole")
        inside = (t.day + 18 < sheet0) or (sheet0 <= t.day and t.day + 18 <= last)
        if not inside:
            rows.append(dict(base, day=t.day, qty_inspected=t.qty_inspected, qty_restocked=t.qty_restocked, qty_pulped=t.qty_pulped))
            continue
        if t.qty_inspected >= 6 and r.random() < 0.22:
            q1 = int(r.integers(2, t.qty_inspected - 1))
            p1 = int(round(t.qty_pulped * q1 / t.qty_inspected))
            rows.append(dict(base, day=t.day, qty_inspected=q1, qty_restocked=q1 - p1, qty_pulped=p1, kind="session1"))
            d2 = t.day + int(r.integers(1, 8))
            rows.append(dict(base, day=d2, qty_inspected=t.qty_inspected - q1, qty_restocked=t.qty_inspected - q1 - (t.qty_pulped - p1),
                             qty_pulped=t.qty_pulped - p1, kind="session2"))
        elif t.qty_inspected >= 3 and r.random() < 0.12:
            # a first count, later queried and recounted: the recount stands
            p0 = int(min(t.qty_inspected, max(0, t.qty_pulped + int(r.choice([-2, -1, 1, 2])))))
            rows.append(dict(base, day=t.day, qty_inspected=t.qty_inspected, qty_restocked=t.qty_inspected - p0, qty_pulped=p0,
                             kind="superseded"))
            d2 = t.day + int(r.integers(3, 15))
            rows.append(dict(base, day=d2, qty_inspected=t.qty_inspected, qty_restocked=t.qty_restocked, qty_pulped=t.qty_pulped,
                             kind="recount"))
        else:
            rows.append(dict(base, day=t.day, qty_inspected=t.qty_inspected, qty_restocked=t.qty_restocked, qty_pulped=t.qty_pulped))
    out = pd.DataFrame(rows)
    while True:
        bad = out.day.map(lambda d: day_date(d).weekday() >= 5)
        if not bad.any():
            break
        out.loc[bad, "day"] += 1
    return out.sort_values(["day", "tote"]).reset_index(drop=True)


def _xlsx(path, sheets, widths=None, freeze=True):
    """sheets: list of (name, header, rows, number_formats by column index)."""
    from openpyxl import Workbook
    from openpyxl.styles import Font
    wb = Workbook()
    wb.remove(wb.active)
    for name, header, rows, fmts in sheets:
        ws = wb.create_sheet(name)
        ws.append(header)
        for c in ws[1]:
            c.font = Font(bold=True)
        for row in rows:
            ws.append(list(row))
        for col, f in (fmts or {}).items():
            for cell in ws.iter_cols(min_col=col + 1, max_col=col + 1, min_row=2, max_row=ws.max_row):
                for c in cell:
                    c.number_format = f
        if freeze:
            ws.freeze_panes = "A2"
        for i, h in enumerate(header):
            ws.column_dimensions[chr(65 + i) if i < 26 else "A" + chr(65 + i - 26)].width = max(10, min(46, len(str(h)) + 4 + (18 if h in ("title", "contributor") else 0)))
    wb.save(path)


def write_all(out, R):
    n = {}
    n[F_LEDGER] = write_ledger(os.path.join(out, F_LEDGER), R)
    # trade accounts
    rows = []
    for a in sorted(R.W.accounts, key=lambda a: a.code):
        rows.append((a.code, "" if a.aid in R.opened_after else a.legacy, a.name, a.channel, a.terms,
                     {"Export": "IE" if a.name.startswith(("Liffey", "Kerrigan", "Abbey Street")) else "XX"}.get(a.channel, "GB")))
    for i, row in enumerate(rows):
        if row[5] == "XX":
            nm = row[2]
            cc = "SE" if "AB" in nm else "NL" if "BV" in nm else "DE" if "GmbH" in nm else "FR" if "SARL" in nm else \
                "AU" if "Pty" in nm or "Southern Cross" in nm else "NZ" if "NZ" in nm else "MT" if "Malta" in nm else "AE"
            rows[i] = row[:5] + (cc,)
    K.write_csv(os.path.join(out, F_ACCOUNTS), ["account_code", "legacy_account_no", "account_name", "channel", "terms", "country"], rows)
    n[F_ACCOUNTS] = len(rows)
    # title master
    t = R.titles.sort_values(["pub_date", "isbn13"])
    trows = [(x.isbn13, x.title, x.contributor, x.imprint, x.format, x.pub_date, x.rrp_gbp, x.status) for x in t.itertuples()]
    _xlsx(os.path.join(out, F_TITLES), [("Titles", ["isbn13", "title", "contributor", "imprint", "format", "pub_date", "rrp_gbp",
                                                    "status"], trows, {5: "dd/mm/yyyy", 6: "0.00"})])
    n[F_TITLES] = len(trows)
    # returns authorisations: one row per title authorised
    ra = R.ra.sort_values(["ra_day", "ra_no", "isbn13"])
    rows = [(x.ra_no, day_date(x.ra_day).isoformat(), R.acc[x.aid].code, K.hyphenate(x.isbn13), int(x.qty_authorised)) for x in ra.itertuples()]
    K.write_csv(os.path.join(out, F_RA), ["ra_number", "date_issued", "customer_account", "isbn", "qty_authorised"], rows, crlf=True)
    n[F_RA] = len(rows)
    # returns received
    S = shipped_receipts(R)
    R.shipped_rec = S
    rows = [(x.delivery_no, day_date(x.day).strftime("%d/%m/%Y"), R.consignor[x.aid], x.ra_no, K.hyphenate(x.isbn13), int(x.qty),
             int(x.saleable), int(x.hurt), int(x.unsaleable), x.tote) for x in S.itertuples()]
    K.write_csv(os.path.join(out, F_RECEIPTS), ["delivery_ref", "received", "consignor", "ra_ref", "isbn", "qty_received",
                                                "grade_saleable", "grade_hurt", "grade_unsaleable", "hurts_tote"], rows, crlf=True)
    n[F_RECEIPTS] = len(rows)
    # hurts re-inspection, a sheet a month, the layout gaining a reason column from August 2026
    I = shipped_reinspection(R)
    R.shipped_ri = I
    sheets = []
    I = I[I.day <= (K.LAST_DATA - K.DAY0).days]
    for (y, m), g in I.groupby(I.day.map(lambda d: (day_date(d).year, day_date(d).month))):
        if (y, m) < (2025, 11):
            continue
        late = (y, m) >= (2026, 8)
        hdr = ["tote", "isbn", "inspected", "qty_inspected", "restocked", "pulped"] + (["inspector"] if late else [])
        rr = []
        ri = K.rng("inspectors", y, m)
        for x in g.itertuples():
            row = [x.tote, K.hyphenate(x.isbn13), day_date(x.day), int(x.qty_inspected), int(x.qty_restocked), int(x.qty_pulped)]
            if late:
                row.append(str(ri.choice(["JH", "PK", "SM", "AD", "LT"], p=[0.3, 0.25, 0.2, 0.15, 0.1])))
            rr.append(row)
        sheets.append((dt.date(y, m, 1).strftime("%b %Y"), hdr, rr, {2: "dd/mm/yyyy"}))
    _xlsx(os.path.join(out, F_REINSPECT), sheets)
    n[F_REINSPECT] = sum(len(s[2]) for s in sheets)
    # consumer panel
    p = R.panel
    rows = [(we.isoformat(), isb, u) for we, isb, u in p.itertuples(index=False)]
    K.write_csv(os.path.join(out, F_PANEL), ["week_ending", "isbn13", "units_uk_retail"], rows)
    n[F_PANEL] = len(rows)
    # distractors
    po = R.print_orders
    rows = [(x.isbn13, x.po_date.isoformat(), x.kind, int(x.qty), x.printer) for x in po.itertuples()]
    K.write_csv(os.path.join(out, F_PRINT), ["isbn13", "order_date", "order_type", "qty", "printer"], rows)
    n[F_PRINT] = len(rows)
    st = R.stock
    rows = [(K.hyphenate(x.isbn13), int(x.saleable), int(x.awaiting_inspection), int(x.reserved)) for x in st.itertuples()]
    K.write_csv(os.path.join(out, F_STOCK), ["isbn", "on_hand_saleable", "returns_awaiting_inspection", "allocated_to_orders"], rows, crlf=True)
    n[F_STOCK] = len(rows)
    return n
