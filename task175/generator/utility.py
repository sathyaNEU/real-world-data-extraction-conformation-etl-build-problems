"""Port Ardell Utilities: premises, accounts, meter installs and capacity fee receipts (the clean truth the
asks read). Built from the World's lots, homes and permits; nothing here is read by the main call."""
import numpy as np
import datetime as dt


def C_date(x):
    return dt.date.fromisoformat(str(np.datetime64(x, "D")))
from world import World, AREAS, d

FY26 = (np.datetime64("2025-10-01"), np.datetime64("2026-10-01"))
FY25_START = np.datetime64("2024-10-01")
FEE = {2024: 10870, 2025: 11240, 2026: 11690, 2027: 12160}   # water and sewer capacity fee per single-family ERC, by fiscal year


def fiscal_year(dates):
    y = dates.astype("datetime64[Y]").astype(int) + 1970
    m = dates.astype("datetime64[M]").astype(int) % 12 + 1
    return np.where(m >= 10, y + 1, y)


class Utility:
    def __init__(self, w: World):
        self.w = w
        g = np.random.default_rng([w.seed, 11])
        L = w.L
        N = w.N
        area = L["area"]
        # premises: one per lot in every served area, created when its lines were accepted (core: by unit)
        created = np.full(N, np.datetime64("NaT", "D"))
        unit_core_date = {}
        for u, ai in zip(w.unit_no, w.unit_area):
            if AREAS[ai][0] == "Core":
                unit_core_date[u] = np.datetime64("%d-%02d-%02d" % (int(g.integers(1978, 1996)), int(g.integers(1, 13)), int(g.integers(1, 28))))
        for ai, acc in enumerate(w.area_acc):
            sel = area == ai
            if AREAS[ai][0] == "Core":
                created[sel] = np.array([unit_core_date[u] for u in L["unit"][sel]])
            elif acc is not None and acc <= dt.date(2026, 12, 31):
                created[sel] = np.datetime64(acc.isoformat())
        self.created = created
        self.has_premise = ~np.isnat(created)
        # the phase a premise carries is the phase its area belonged to when the premise was created
        self.phase_now = np.array([AREAS[a][1] for a in area])
        self.phase_stored = np.array([AREAS[a][2] if not np.isnat(c) and c < np.datetime64("2021-07-01") else AREAS[a][1]
                                      for a, c in zip(area, created)])
        # homes: completion (pre-2008 year built, or certificate of occupancy)
        yb = w.yb0
        home_done = np.where(yb > 0, np.array(["%d-06-30" % max(y, 1962) for y in np.where(yb > 0, yb, 2000)], dtype="datetime64[D]"),
                             w.co)
        self.home_done = home_done
        # meter set for permitted homes: 18 to 75 days after the permit
        lag = g.integers(16, 71, size=N)
        self.meter_set = np.where(np.isnat(w.issued), np.datetime64("NaT", "D"), w.issued + lag.astype("timedelta64[D]"))
        # pre-2008 homes: meter set at completion
        self.meter_set = np.where(yb > 0, home_done, self.meter_set)
        # accounts: the first opens at the home's completion (occupancy), turnover every 4 to 14 years
        acc_rows = []
        today = np.datetime64("2026-12-31")
        idx = np.where(~np.isnat(home_done) & (home_done <= today) & self.has_premise)[0]
        start = home_done[idx] + g.integers(3, 40, size=len(idx)).astype("timedelta64[D]")
        for k in range(8):
            ok = start <= today
            if not ok.any():
                break
            dur = (g.gamma(2.2, 1300.0, size=len(idx))).astype(int)
            end = start + dur.astype("timedelta64[D]")
            open_ = end > today
            for i, s, e, o in zip(idx[ok], start[ok], end[ok], open_[ok]):
                acc_rows.append((i, s, None if o else e))
            gap = g.integers(0, 60, size=len(idx))
            start = np.where(ok & ~open_, end + gap.astype("timedelta64[D]"), np.datetime64("2100-01-01", "D"))
        self.accounts = acc_rows
        # AMI change-outs in fiscal 2026: meters at existing homes whose registers failed, replaced through the year
        homes_old = np.where(self.has_premise & ~np.isnat(home_done) & (home_done < np.datetime64("2023-01-01")))[0]
        n_co = 236
        pick = list(g.choice(homes_old, size=n_co, replace=False))
        day0 = np.datetime64("2025-10-06")
        days = list(g.integers(0, 357, size=n_co))
        # every phase sees some exchanges in every quarter (crews work the whole service area)
        qstart = [np.datetime64(d) for d in ("2025-10-06", "2026-01-05", "2026-04-06", "2026-07-06")]
        for ph in ["Core", "1", "2", "3", "4"]:
            cand = homes_old[self.phase_now[homes_old] == ph]
            for k in range(4):
                have = sum(1 for i, dd in zip(pick, days) if self.phase_now[i] == ph and
                           qstart[k] <= day0 + np.timedelta64(int(dd), "D") < qstart[k] + np.timedelta64(84, "D"))
                while have < 2:
                    i = int(g.choice(cand))
                    if i in pick:
                        continue
                    pick.append(i)
                    days.append(int((qstart[k] - day0).astype(int)) + int(g.integers(0, 80)))
                    have += 1
        self.changeouts = (np.array(pick), day0 + np.array(days).astype("timedelta64[D]"))
        # meter size: one-inch services (fire sprinklers, larger homes) on about one new home in six
        self.size1 = g.random(N) < 0.17
        # meters pulled when a build stalls and set again when work resumes: the head-end logs the second set too
        first_acc = {}
        for (i, s_, e_) in acc_rows:
            if i not in first_acc or s_ < first_acc[i]:
                first_acc[i] = s_
        lo, hi = np.datetime64("2024-10-01"), np.datetime64("2026-09-30")
        cand = np.where(self.has_premise & (yb == 0) & ~np.isnat(self.meter_set) & (self.meter_set >= lo) & (self.meter_set < hi))[0]
        rs_lot, rs_day = [], []
        for i in cand:
            if g.random() < 0.055:
                d = self.meter_set[i] + np.timedelta64(int(g.integers(45, 221)), "D")
                lim = min(first_acc.get(int(i), np.datetime64("2100-01-01")), hi)
                if d < lim:
                    rs_lot.append(int(i)); rs_day.append(d)
        qs = [np.datetime64(x) for x in ("2025-10-01", "2026-01-01", "2026-04-01", "2026-07-01", "2026-10-01")]
        for ph in ["Core", "1", "2", "3", "4"]:
            pool = [int(i) for i in cand if self.phase_now[i] == ph]
            for k in range(4):
                have = sum(1 for i, d in zip(rs_lot, rs_day) if self.phase_now[i] == ph and qs[k] <= d < qs[k + 1])
                tries = 0
                while have < 2 and tries < 5000:
                    tries += 1
                    i = pool[int(g.integers(0, len(pool)))]
                    if i in rs_lot:
                        continue
                    d = qs[k] + np.timedelta64(int(g.integers(0, 88)), "D")
                    lim = min(first_acc.get(i, np.datetime64("2100-01-01")), hi)
                    if self.meter_set[i] + np.timedelta64(40, "D") <= d < lim:
                        rs_lot.append(i); rs_day.append(d); have += 1
        self.resets = (np.array(rs_lot), np.array(rs_day, dtype="datetime64[D]"))
        self._second_premises(np.random.default_rng([w.seed, 29]))
        # capacity fee receipts: paid with the permit, at the fee of the permit's fiscal year
        self._receipts(g)

    def _second_premises(self, g):
        """when work resumes on a stalled build the meter order goes through the cashier's counter, which sets up a
        premise from the service order unless the clerk reopens the stub; the stub keeps the first set in the head-end
        log and goes back to STUB, and the home's account opens on the counter's premise"""
        lots, days = self.resets
        ms = self.meter_set

        def cell(x):
            x = np.datetime64(x, "D")
            if not (FY26[0] <= x < FY26[1]):
                return None
            m = int(x.astype("datetime64[M]").astype(int) % 12) + 1
            return ((m - 10) % 12) // 3

        cells = [(self.phase_now[i], cell(dd)) for i, dd in zip(lots, days)]
        first = [(self.phase_now[i], cell(ms[i])) for i in lots]
        newp = g.random(len(lots)) < 0.7
        PH = ["Core", "1", "2", "3", "4"]
        for _ in range(60):
            changed = False
            for ph in PH:
                for k in range(4):
                    here = [j for j, c in enumerate(cells) if c == (ph, k)]
                    n_new = sum(1 for j in here if newp[j])
                    out = sum(1 for j, c in enumerate(first) if newp[j] and c == (ph, k) and cells[j] != c)
                    inn = sum(1 for j in here if newp[j] and first[j] != cells[j])
                    if n_new == 0 or inn == out:
                        free = [j for j in here if not newp[j]]
                        if free:
                            newp[free[int(g.integers(0, len(free)))]] = True
                        else:
                            j = here[int(g.integers(0, len(here)))]
                            newp[j] = not newp[j]
                        changed = True
            if not changed:
                break
        self.reset_newprem = newp
        self.prem2 = {int(i): dd - np.timedelta64(int(g.integers(2, 12)), "D") for i, dd, nw in zip(lots, days, newp) if nw}

    def _receipts(self, g):
        w = self.w
        sel = np.where(~np.isnat(w.issued) & (w.issued >= np.datetime64("2025-08-01")) & self.has_premise)[0]
        # builders: production builders pay several permits on one receipt
        wts = np.r_[np.full(12, 0.24 / 12), np.full(128, 0.76 / 128)]
        self.builder = g.choice(140, size=w.N, p=wts)
        rows = []
        order = sel[np.argsort(w.issued[sel], kind="stable")]
        paid = set()
        payments = []
        for k, lot in enumerate(order):
            if lot in paid:
                continue
            day = w.issued[lot]
            same = [lot]
            if self.builder[lot] < 12:   # production builders pay the week's permits on one receipt
                for o in order[k + 1:k + 60]:
                    if (w.issued[o] - day) > np.timedelta64(6, "D") or len(same) >= 4:
                        break
                    if o not in paid and self.builder[o] == self.builder[lot]:
                        same.append(o)
            paid.update(same)
            rdate = max(w.issued[x] for x in same) + np.timedelta64(int(g.integers(0, 4)), "D")
            fee = FEE[int(fiscal_year(np.array([rdate]))[0])]
            amts = [int(round(fee * (2.5 if self.size1[x] else 1.0))) for x in same]
            payments.append((rdate, same, amts, "UTL" if g.random() < 0.12 else "BLD"))
        # receipt numbers run by drawer and day (YYDDD-NNN); the export does not carry the drawer
        payments.sort(key=lambda p: (p[0], p[3], p[1][0]))
        used = {}
        for rdate, same, amts, drawer in payments:
            dd = C_date(rdate)
            key = (dd, drawer)
            n = used.get(key, 0) + 1
            if drawer == "UTL":
                # the second drawer's sequence restarts each day too; a number already issued at the first drawer
                # that day is shared only by a payment of the same amount from another payer, else it moves on
                while True:
                    other = [p for p in rows if p[0] == "%s-%03d" % (dd.strftime("%y") + "%03d" % dd.timetuple().tm_yday, n)]
                    if not other or (len(same) == 1 and len(other) == 1 and other[0][4] == amts[0]
                                     and self.builder[other[0][2]] != self.builder[same[0]]):
                        break
                    n += 1
            used[key] = n
            rno = "%s%03d-%03d" % (dd.strftime("%y"), dd.timetuple().tm_yday, n)
            for x, am in zip(same, amts):
                rows.append((rno, rdate, int(x), am, sum(amts), len(same), drawer))
        self.receipts = rows

    def connections_fy26(self):
        """new single-family connections in fiscal 2026: first meter set at a premise, by phase and fiscal quarter"""
        w = self.w
        ms = self.meter_set
        new = self.has_premise & ~np.isnat(ms) & (ms >= FY26[0]) & (ms < FY26[1]) & (w.yb0 == 0)
        q = ((ms.astype("datetime64[M]").astype(int) % 12 + 3) % 12) // 3   # Oct-Dec 0 ... Jul-Sep 3
        return new, q


if __name__ == "__main__":
    w = World()
    u = Utility(w)
    new, q = u.connections_fy26()
    ph = u.phase_now
    for p in ["Core", "1", "2", "3", "4"]:
        print(p, [int(((ph == p) & new & (q == k)).sum()) for k in range(4)])
    print("changeouts", len(u.changeouts[0]), "accounts", len(u.accounts), "receipt lines", len(u.receipts))
