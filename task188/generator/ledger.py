"""Day-by-day trading and banking for every member in 2026, written as the core banking system posts it.

Each member gets its own random stream, so a change to one member's parameters never moves another's
records. Cash is received at a teller (the cash portion of a counter deposit, which can also carry
cheques), at a deposit ATM, or in a night deposit bag, which is counted the next business morning at the
branch or, for branches without vault staff, at Regional Cash Services after the armoured car collects it.
"""
import datetime as dt
import math

import numpy as np

import common as C
import world as W

CUTOFF_HOUR = 18          # ATM deposits after 18:00 local, or on a non-business day, post to the next business day
DEPOSIT_DAYS = {"daily": {0, 1, 2, 3, 4}, "mwf": {0, 2, 4}, "twice": {1, 4}, "weekly": {4}}


def _t(d, hour_lo, hour_hi, r):
    """A local time on day d between two hours, to the second."""
    secs = int(r.integers(int(hour_lo * 3600), int(hour_hi * 3600)))
    return dt.datetime(d.year, d.month, d.day) + dt.timedelta(seconds=secs)


class Sim:
    def __init__(self, members, seed=C.SEED):
        self.members = members
        self.seed = seed
        self.postings = []         # dicts, one per posting
        self.cash_events = []      # (member, account, local receipt datetime, cash, channel, place)
        self.night_bags = []       # (bag, member, drop depository, drop local dt, count local dt, cash, counted_at)
        self.used_pid = set()
        self.terminals = {}
        self.depositories = {}
        self.bags = {}             # member number -> list of bag numbers
        self.bag_issue = {}        # bag -> (member, transit, issued date)
        self.loans = {}
        self._facilities()

    # facilities ---------------------------------------------------------------------------------------
    def _facilities(self):
        r = np.random.default_rng(self.seed + 7)
        used = set()
        self.atm_rows = []
        offsite = {"10342": ["Newton Exchange Plaza"], "10611": ["Lansdowne Station Kiosk"],
                   "10729": ["Royal Oak Village"], "11204": ["Willowbrook Crossing"]}
        for b in W.BRANCHES:
            transit = b[0]
            n = 2 if transit in ("10342", "10611", "10729", "10587") else 1
            for k in range(n):
                tid = self._tid(r, used)
                # the new Willowbrook lobby ATM was commissioned the week before the branch opened
                inst = dt.date(2026, 6, 25) if transit == W.LANGLEY_NEW else b[5]
                self.atm_rows.append((tid, "%s branch lobby %s" % (b[1], "AB"[k]), transit, inst, b[6], "Y"))
                self.terminals.setdefault(transit, []).append((tid, inst, b[6]))
            for place in offsite.get(transit, []):
                if transit == W.LANGLEY_NEW:
                    # Langley City's lobby ATM, taken out when the branch closed and put back in service at
                    # Willowbrook Crossing under its own terminal number
                    tid = self.terminals[W.LANGLEY_OLD][0][0]
                    opened = dt.date(2026, 7, 6)
                else:
                    tid = self._tid(r, used)
                    opened = dt.date(2015 + int(r.integers(0, 8)), 3, 1)
                self.atm_rows.append((tid, place, transit, opened, None, "Y"))
                self.terminals.setdefault(transit, []).append((tid, opened, None))
            # a cash-only ATM at the larger branches takes no deposits
            if transit in ("10342", "10729", "10856"):
                self.atm_rows.append((self._tid(r, used), "%s drive-through" % b[1], transit, b[5], b[6], "N"))
        self.depo_rows = []
        usedd = set()
        for b in W.BRANCHES:
            while True:
                did = "ND-%04d" % int(r.integers(1100, 9800))
                if did not in usedd:
                    usedd.add(did)
                    break
            self.depositories[b[0]] = did
            self.depo_rows.append((did, b[0], b[5] if b[5].year >= 2009 else dt.date(2009, 1, 12), b[6]))

    @staticmethod
    def _tid(r, used):
        while True:
            v = "HR%d%s" % (int(r.integers(1000, 9999)), "ABCDEFGHJK"[int(r.integers(10))])
            if v not in used:
                used.add(v)
                return v

    def _pid(self, r):
        while True:
            v = int(r.integers(10**11, 10**12 - 1))
            if v not in self.used_pid:
                self.used_pid.add(v)
                return v

    # helpers ------------------------------------------------------------------------------------------
    def _branch_for(self, m, d):
        h = m.home
        if h == W.LANGLEY_OLD and d > dt.date(2026, 6, 26):
            return W.LANGLEY_NEW
        if h == W.LANGLEY_NEW and d < dt.date(2026, 6, 29):
            return W.LANGLEY_OLD
        return h

    def _open_branches(self, d):
        out = []
        for b in W.BRANCHES:
            if b[5] <= d and (b[6] is None or d <= b[6]):
                out.append(b[0])
        return out

    def post(self, r, m, acct, when_local, eff, code, channel, desc, debit=0.0, credit=0.0,
             transit="", terminal="", cash=None, items=""):
        self.postings.append({
            "posting_id": self._pid(r), "account_number": acct,
            "posted_at_utc": C.local_to_utc(when_local), "effective_date": eff, "transaction_code": code,
            "channel": channel, "transit": transit, "terminal_id": terminal, "description": desc,
            "debit": C.money(debit) if debit else "", "credit": C.money(credit) if credit else "",
            "cash_portion": C.money(cash) if cash is not None else "", "item_count": items,
            "_member": m.number})

    # trading ------------------------------------------------------------------------------------------
    def daily_sales(self, m, r):
        season = W.SEASON[m.trade]
        dow = W.DOW[m.trade]
        closed_holidays = m.trade in ("SAL", "CAF", "CWS")
        raw = []
        for d in C.DAYS:
            w = dow[d.weekday()] * season[d.month - 1]
            if closed_holidays and d in C.HOLIDAYS:
                w = 0.0
            raw.append(w)
        raw = np.array(raw)
        noise = np.exp(r.normal(0, 0.11, len(raw)) - 0.11 ** 2 / 2)
        x = raw * noise
        return x / x.sum() * m.sales

    def run(self):
        for idx, m in enumerate(self.members):
            r = np.random.default_rng(self.seed * 1000 + idx)
            self._member(m, r)
        self.postings.sort(key=lambda p: (p["posted_at_utc"], p["account_number"], p["posting_id"]))
        return self

    def _member(self, m, r):
        sales = self.daily_sales(m, r)
        walk = sales * (1 - m.p)
        plat = sales * m.p
        cash_takings = walk * m.s
        card_gross = walk * (1 - m.s)
        main = m.accounts[0]
        # bags issued to the member for night deposits
        nb = 1 if m.ch_night < 0.15 else (2 if m.ch_night < 0.35 else 3)
        self.bags[m.number] = []
        for _ in range(nb):
            while True:
                bag = int(r.integers(30000, 79999))
                if bag not in self.bag_issue:
                    break
            issued = max(m.since, dt.date(2014, 1, 1)) + dt.timedelta(days=int(r.integers(0, 400)))
            issued = min(issued, dt.date(2025, 12, 1))
            home_at_issue = m.home if m.home != W.LANGLEY_NEW else W.LANGLEY_OLD
            self.bag_issue[bag] = (m.number, home_at_issue, issued)
            self.bags[m.number].append(bag)
        # laundering: placed with the takings on deposit days, spread through the year with a mild drift
        laund_w = np.array([(1.0 + 0.18 * math.sin((i / 365.0) * 2 * math.pi - 0.9)) if d.weekday() < 6 else 0.0
                            for i, d in enumerate(C.DAYS)])
        laund_day = m.launder * laund_w / laund_w.sum() if m.launder > 0 else np.zeros(len(C.DAYS))
        till = 0.0
        pending_cheques = []
        # members taking larger cheques from business customers scan them in the banking app; the rest bring
        # them to the counter with the takings
        chq_share = sum(sh for (_c, sh, how, _d) in m.b2b if how != "eft")
        rdc = chq_share > 0.04 or m.number % 3 == 0
        dep_days = DEPOSIT_DAYS[m.dep_freq]
        acq_name, lag, fee = W.ACQUIRERS[m.acquirer]
        for i, d in enumerate(C.DAYS):
            # card batch for the day's sales
            if card_gross[i] > 0.5:
                settle = C.next_business_day(d, lag)
                net = card_gross[i] * (1 - fee)
                when = _t(settle, 5.4, 6.6, r)
                if m.acquirer == "CASCADIA":
                    desc = "CASCADIA MERCH DEP %s %s" % (d.strftime("%m%d"), m.mid)
                else:
                    desc = "NORTHGATE PAY STLMT %s %s" % (d.strftime("%y-%m-%d"), m.mid)
                self.post(r, m, main, when, settle, "EFTC", "EFT", desc, credit=net)
            till += cash_takings[i] * (1 - m.retain) + laund_day[i]
            if d.weekday() in dep_days and till > 40:
                pending_cheques = self._deposit(m, r, d, till, pending_cheques)
                till = 0.0
            if pending_cheques and C.is_business_day(d) and len(pending_cheques) >= 3:
                # a run of cheques waiting on a member who banks its cash by ATM or night bag goes in alone
                br = self._branch_for(m, d)
                when = _t(d, 9.6, 16.8, r)
                self.post(r, m, main, when, d, "DEP", "TELLER", "BRANCH DEPOSIT", credit=sum(pending_cheques),
                          transit=br, cash=0.0, items=str(len(pending_cheques)))
                pending_cheques = []
            # business customers paying by cheque hand them over in the month
            for (cust, share, how, day) in m.b2b:
                if d.day == day and d.month > 1:
                    amt = m.sales * share / 12.0 * float(np.exp(r.normal(0, 0.18)))
                    inv = int(r.integers(1000, 9999))
                    if how == "eft":
                        eff = C.business_day_on_or_after(d)
                        self.post(r, m, main, _t(eff, 5.6, 6.9, r), eff, "EFTC", "EFT",
                                  "EFT CR %s INV %d" % (cust.upper(), inv), credit=amt)
                    elif rdc:
                        # scanned in the business banking app the same evening, credited the next business day
                        eff = C.next_business_day(d)
                        self.post(r, m, main, _t(d, 18.2, 22.8, r), eff, "MCHQ", "ONLINE", "MOBILE CHEQUE DEPOSIT",
                                  credit=amt, items="1")
                    else:
                        pending_cheques.append(amt)
        # the year-end till is banked on the first business day of 2027 (outside the year)
        self._platforms(m, r, plat)
        self._network(m, r)
        self._other_credits(m, r)
        self._debits(m, r, sales)

    def _deposit(self, m, r, d, amount, cheques):
        """Bank the till on day d through the member's usual channels; returns the cheques still waiting."""
        cheques_left = list(cheques)
        accts = m.accounts
        parts = [(accts[0], amount)]
        if len(accts) > 1 and r.random() < 0.55:
            k = amount * m.second_cash_share * float(r.uniform(0.6, 1.4))
            k = min(k, amount * 0.8)
            parts = [(accts[0], amount - k), (accts[1], k)]
        for acct, amt in parts:
            u = r.random()
            ch = "TELLER" if u < m.ch_counter else ("NIGHT" if u < m.ch_counter + m.ch_night else "ATM")
            if not C.is_business_day(d) and ch == "TELLER":
                ch = "ATM"
            branch = self._branch_for(m, d)
            if ch == "TELLER":
                if r.random() < 0.07:
                    open_now = [b for b in self._open_branches(d) if b != branch]
                    branch = open_now[int(r.integers(len(open_now)))]
                when = _t(d, 9.6, 16.8, r)
                cash = round(amt, 0) if m.trade != "LDY" else round(amt, 2)
                chq = sum(cheques_left) if cheques_left and acct == accts[0] else 0.0
                items = str(len(cheques_left)) if chq else ""
                if chq:
                    cheques_left = []
                code = "COIN" if (m.trade == "LDY" and r.random() < 0.35 and not chq) else "DEP"
                desc = "BRANCH DEPOSIT" if code == "DEP" else "COIN DEPOSIT"
                self.post(r, m, acct, when, d, code, "TELLER", desc, credit=cash + chq, transit=branch,
                          cash=cash, items=items)
                self.cash_events.append((m.number, acct, when, cash, "TELLER", branch))
            elif ch == "ATM":
                tids = [t for (t, a, z) in self.terminals.get(branch, []) if a <= d and (z is None or d <= z)]
                if not tids:
                    tids = [t for (t, a, z) in self.terminals["10342"] if a <= d and (z is None or d <= z)]
                tid = tids[int(r.integers(len(tids)))]
                when = _t(d, 17.2, 23.6, r) if C.is_business_day(d) else _t(d, 10.0, 21.0, r)
                eff = d if (C.is_business_day(d) and when.hour < CUTOFF_HOUR) else C.next_business_day(d)
                cash = float(math.floor(amt / 5.0) * 5.0)
                self.post(r, m, acct, when, eff, "ATMD", "ATM", "ATM DEPOSIT %s" % tid, credit=cash,
                          terminal=tid, cash=cash)
                self.cash_events.append((m.number, acct, when, cash, "ATM", tid))
            else:
                drop_branch = branch
                if r.random() < m.drop_elsewhere:
                    alts = [b for b in self._open_branches(d) if b != branch]
                    drop_branch = alts[int(r.integers(len(alts)))]
                drop = _t(d, 18.5, 23.9, r)
                count_day = C.next_business_day(d)
                if C.is_business_day(d) is False:
                    count_day = C.business_day_on_or_after(d)
                own = W.BR[drop_branch][4]
                count = _t(count_day, 9.2, 11.9, r) if own else _t(count_day, 10.4, 15.2, r)
                bag = self.bags[m.number][int(r.integers(len(self.bags[m.number])))]
                cash = round(amt, 0)
                if own:
                    self.post(r, m, acct, count, count_day, "NDEP", "NIGHT", "NIGHT DEP BAG %d BR" % bag,
                              credit=cash, transit=drop_branch, cash=cash)
                else:
                    self.post(r, m, acct, count, count_day, "NDEP", "NIGHT", "NIGHT DEP BAG %d" % bag,
                              credit=cash, transit=W.CASH_CENTRE[0], cash=cash)
                self.cash_events.append((m.number, acct, count, cash, "NIGHT", drop_branch))
                self.night_bags.append((bag, m.number, self.depositories[drop_branch], drop, count, cash,
                                        "branch" if own else "cash_centre", drop_branch))
        return cheques_left

    def _platforms(self, m, r, plat):
        if not m.platforms:
            return
        split = {"DASHDROP": 1.0} if m.platforms == ["DASHDROP"] else (
            {"PLATEPASS": 1.0} if m.platforms == ["PLATEPASS"] else {"DASHDROP": 0.6, "PLATEPASS": 0.4})
        main = m.accounts[0]
        start = dt.date(2025, 12, 29)
        week = 0
        while True:
            wk0 = start + dt.timedelta(days=7 * week)
            if wk0 > dt.date(2026, 12, 31):
                break
            idx = [(wk0 + dt.timedelta(days=k) - dt.date(2026, 1, 1)).days for k in range(7)]
            gross = sum(plat[i] for i in idx if 0 <= i < 365)
            # the days of the first week that fall in December 2025 traded at about the early-January rate
            gross += float(np.mean(plat[:14])) * sum(1 for i in idx if i < 0)
            for pf, sh in split.items():
                name, wd, comm = W.PLATFORMS[pf]
                pay = wk0 + dt.timedelta(days=7 + wd)
                pay = C.business_day_on_or_after(pay)
                if pay.year != 2026:
                    continue
                net = gross * sh * (1 - comm)
                if net < 1:
                    continue
                desc = ("DASHDROP CANADA PAYOUT WK %s" % wk0.strftime("%Y%m%d") if pf == "DASHDROP"
                        else "PLATEPASS REMIT %s-%s" % (wk0.strftime("%m%d"), (wk0 + dt.timedelta(days=6)).strftime("%m%d")))
                self.post(r, m, main, _t(pay, 5.5, 7.0, r), pay, "EFTC", "EFT", desc, credit=net)
            week += 1

    def _network(self, m, r):
        if m.network_in <= 0:
            return
        main = m.accounts[0]
        names = W.NETWORK_IN[m.role]
        outs = W.NETWORK_OUT[m.role]
        d = dt.date(2026, 1, 6)
        k = 0
        while d.year == 2026:
            nm = names[k % len(names)] if r.random() < 0.7 else names[int(r.integers(len(names)))]
            amt = m.network_in / 50.0 * float(np.exp(r.normal(0, 0.22)))
            eff = C.business_day_on_or_after(d)
            if eff.year == 2026:
                self.post(r, m, main, _t(eff, 5.6, 6.9, r), eff, "EFTC", "EFT",
                          "EFT CR %s INV %d" % (nm.upper(), int(r.integers(2000, 9800))), credit=amt)
            d = d + dt.timedelta(days=int(r.integers(5, 10)))
            k += 1
        # the money leaves as payments to suppliers the network controls
        total_out = (m.launder + m.network_in) * 0.94
        d = dt.date(2026, 1, 8)
        while d.year == 2026:
            nm = outs[int(r.integers(len(outs)))]
            amt = total_out / 60.0 * float(np.exp(r.normal(0, 0.25)))
            eff = C.business_day_on_or_after(d)
            if eff.year == 2026:
                self.post(r, m, main, _t(eff, 9.0, 16.0, r), eff, "EFTD", "ONLINE",
                          "EFT DR %s PMT" % nm.upper(), debit=amt)
            d = d + dt.timedelta(days=int(r.integers(4, 9)))

    def _other_credits(self, m, r):
        main = m.accounts[0]
        if m.loan:
            ld, amt = m.loan
            ln = "LN%07d" % int(r.integers(1_000_000, 9_999_999))
            self.loans[m.number] = (ln, ld, amt)
            eff = C.business_day_on_or_after(ld)
            self.post(r, m, main, _t(eff, 10.0, 15.0, r), eff, "LNADV", "SYSTEM", "LOAN ADVANCE %s" % ln, credit=amt)
        if m.owner_inj > 0:
            n = int(r.integers(1, 4))
            personal = "%s-%07d" % (m.home if m.home != W.LANGLEY_NEW else W.LANGLEY_OLD, int(r.integers(1_000_000, 9_999_999)))
            for _ in range(n):
                d = C.business_day_on_or_after(dt.date(2026, 1, 1) + dt.timedelta(days=int(r.integers(5, 355))))
                self.post(r, m, main, _t(d, 8.0, 21.0, r), d, "TRFC", "ONLINE", "TRF FROM %s" % personal,
                          credit=m.owner_inj / n * float(r.uniform(0.6, 1.4)))
        if len(m.accounts) > 1:
            # sweeps from the second account back to the operating account
            for mo in range(1, 13):
                d = C.business_day_on_or_after(dt.date(2026, mo, 25))
                if r.random() < 0.6:
                    amt = m.sales * m.s * m.second_cash_share / 12.0 * float(r.uniform(0.3, 0.9))
                    self.post(r, m, m.accounts[1], _t(d, 9.0, 17.0, r), d, "TRFD", "ONLINE",
                              "TRF TO %s" % main, debit=amt)
                    self.post(r, m, main, _t(d, 9.0, 17.0, r), d, "TRFC", "ONLINE",
                              "TRF FROM %s" % m.accounts[1], credit=amt)

    def _debits(self, m, r, sales):
        main = m.accounts[0]
        total = float(sales.sum())
        cogs = {"RFS": 0.31, "RQS": 0.33, "CAF": 0.30, "CNV": 0.70, "GRO": 0.66, "BAR": 0.30,
                "SAL": 0.10, "CWS": 0.12, "LDY": 0.10, "MFV": 0.32}[m.trade]
        sup = list(r.choice(W.SUPPLIERS[m.trade], size=min(3, len(W.SUPPLIERS[m.trade])), replace=False))
        wsh = r.dirichlet(np.ones(len(sup)) * 2)
        for j, s in enumerate(sup):
            d = dt.date(2026, 1, 2) + dt.timedelta(days=int(r.integers(0, 6)))
            while d.year == 2026:
                eff = C.business_day_on_or_after(d)
                if eff.year == 2026:
                    amt = total * cogs * wsh[j] / 52.0 * float(np.exp(r.normal(0, 0.15)))
                    self.post(r, m, main, _t(eff, 8.0, 18.0, r), eff, "EFTD", "ONLINE",
                              "EFT DR %s PMT" % str(s).upper(), debit=amt)
                d = d + dt.timedelta(days=7)
        pay = {"SAL": 0.30, "CWS": 0.22, "LDY": 0.14, "CNV": 0.11, "GRO": 0.14}.get(m.trade, 0.29)
        d = dt.date(2026, 1, 9) + dt.timedelta(days=int(r.integers(0, 7)))
        while d.year == 2026:
            eff = C.business_day_on_or_after(d)
            if eff.year == 2026:
                self.post(r, m, main, _t(eff, 6.0, 7.5, r), eff, "EFTD", "EFT", "PAYROLL CEDARLINE PAYROLL BATCH",
                          debit=total * pay / 26.0 * float(np.exp(r.normal(0, 0.06))))
            d = d + dt.timedelta(days=14)
        rent = total * float(r.uniform(0.05, 0.10)) / 12.0
        landlord = W.LANDLORDS[int(r.integers(len(W.LANDLORDS)))]
        for mo in range(1, 13):
            eff = C.business_day_on_or_after(dt.date(2026, mo, 1))
            self.post(r, m, main, _t(eff, 6.0, 7.5, r), eff, "EFTD", "EFT", "PAD %s RENT" % landlord.upper(), debit=rent)
            eff2 = C.business_day_on_or_after(dt.date(2026, mo, 15))
            self.post(r, m, main, _t(eff2, 6.0, 7.5, r), eff2, "EFTD", "EFT", "CANADA REVENUE AGENCY PAYROLL DEDUCTIONS",
                      debit=total * pay * 0.16 / 12.0 * float(np.exp(r.normal(0, 0.05))))
            eff3 = C.business_day_on_or_after(dt.date(2026, mo, int(r.integers(3, 25))))
            self.post(r, m, main, _t(eff3, 6.0, 7.5, r), eff3, "EFTD", "EFT", "PAD ELECTRIC UTILITY",
                      debit=total * 0.018 / 12.0 * float(np.exp(r.normal(0, 0.18))))
            eff4 = C.business_day_on_or_after(dt.date(2026, mo, 28))
            self.post(r, m, main, _t(eff4, 23.0, 23.9, r), eff4, "FEE", "SYSTEM", "MONTHLY ACCOUNT FEE",
                      debit=float(r.choice([24.95, 34.95, 49.95])))
            if m.loan and dt.date(2026, mo, 1) > m.loan[0]:
                self.post(r, m, main, _t(eff2, 6.0, 7.5, r), eff2, "LNPMT", "SYSTEM", "LOAN PAYMENT %s" % self.loans[m.number][0],
                          debit=m.loan[1] / 48.0)
            if r.random() < 0.7:
                effd = C.business_day_on_or_after(dt.date(2026, mo, int(r.integers(5, 27))))
                self.post(r, m, main, _t(effd, 8.0, 22.0, r), effd, "TRFD", "ONLINE", "TRF TO OWNER ACCOUNT",
                          debit=total * float(r.uniform(0.004, 0.02)))
        for q in range(4):
            eff = C.business_day_on_or_after(dt.date(2026, 3 * q + 1, 28) + dt.timedelta(days=31))
            if eff.year == 2026:
                self.post(r, m, main, _t(eff, 6.0, 7.5, r), eff, "EFTD", "EFT", "CANADA REVENUE AGENCY GST/HST",
                          debit=total * 0.05 * 0.25 * float(np.exp(r.normal(0, 0.1))))
        if r.random() < 0.25:
            for _ in range(int(r.integers(2, 9))):
                d = C.business_day_on_or_after(dt.date(2026, 1, 1) + dt.timedelta(days=int(r.integers(3, 360))))
                br = self._branch_for(m, d)
                self.post(r, m, main, _t(d, 9.7, 16.5, r), d, "CWD", "TELLER", "CASH WITHDRAWAL",
                          debit=float(r.choice([500, 800, 1000, 1500, 2000])), transit=br)
