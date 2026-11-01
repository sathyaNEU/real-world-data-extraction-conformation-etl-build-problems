"""task146 architecture 2: Trentmoor Building Society's instant-access savings book, November 2021 to November 2026.

The world simulates savings pots (a member's money) month by month. A pot sits in one account at a time; when its
member takes up the spring's new Loyalty Saver issue the Society closes the old account and opens the new one in the
same overnight batch with the same amount (the core system cannot convert an account between issues). Pots also leave
the Society (closed and paid out), fund a fixed-rate bond from a closing payment, and move up and down with deposits,
withdrawals and interest. Everything is deterministic from SEED.
"""
import calendar
import datetime as dt

import numpy as np

SEED = 146079
START = dt.date(2021, 11, 30)
END = dt.date(2026, 11, 30)
PRODUCTS = ("ES", "LS", "IS", "YS")
NAME = {"ES": "Easy Saver", "LS": "Loyalty Saver", "IS": "Easy Access Cash ISA", "YS": "Young Saver"}
EXIT = {"ES": 0.0150, "LS": 0.0105, "IS": 0.0072, "YS": 0.0046}      # monthly hazard of leaving the Society
BOND = {"ES": 0.0026, "LS": 0.0031, "IS": 0.0, "YS": 0.0}            # monthly hazard of a bond funded on closing
SWITCH = {"ES": 0.27, "LS": 0.38}                                     # take-up of each spring's new issue
DRIFT = {"ES": -0.0035, "LS": -0.0022, "IS": -0.0012, "YS": 0.0040}   # members' net deposits less withdrawals
VOL = {"ES": 0.050, "LS": 0.040, "IS": 0.030, "YS": 0.045}
NEW = {"ES": 38, "LS": 31, "IS": 16, "YS": 9}                         # new pots a month (new money)
INIT = {"ES": 1650, "LS": 900, "IS": 820, "YS": 310}
MEAN0 = {"ES": 76000.0, "LS": 92000.0, "IS": 45000.0, "YS": 7900.0}
RATE = {"ES": 0.0135, "LS": 0.0210, "IS": 0.0185, "YS": 0.0250}       # base annual rates at the start
BANK = [0.0025 + min(0.0500, max(0.0, 0.0011 * (m - 1))) for m in range(61)]   # a stylised Bank Rate path


def month_ends():
    out, y, m = [], START.year, START.month
    while True:
        d = dt.date(y, m, calendar.monthrange(y, m)[1])
        out.append(d)
        if d >= END:
            return out
        m += 1
        if m == 13:
            y, m = y + 1, 1


MONTHS = month_ends()


def issue_of(d):
    """The Loyalty Saver issue on sale on date d (each issue launches on 1 April)."""
    return "LS%02d" % ((d.year if d.month >= 4 else d.year - 1) % 100)


class Pot:
    __slots__ = ("pid", "product", "issue", "bal", "acct", "chain", "alive", "seg")

    def __init__(self, pid, product, issue, bal, seg):
        self.pid, self.product, self.issue, self.bal, self.seg = pid, product, issue, bal, seg
        self.acct, self.chain, self.alive = None, [], True


class World:
    def __init__(self, seed=SEED):
        self.r = np.random.RandomState(seed)
        self.pots, self.accounts, self.events, self.bonds = [], {}, [], []
        self.balances = {}          # (account, month index) -> pounds
        self.next_acct, self.next_pid = 40311207, 0
        self._run()

    # -- accounts -------------------------------------------------------------
    def _open(self, pot, day, amount, how):
        a = self.next_acct
        self.next_acct += 1 + int(self.r.randint(0, 6))
        code = pot.issue if pot.product == "LS" else pot.product
        self.accounts[a] = {"account": a, "product": pot.product, "issue": code, "opened": day, "closed": None,
                            "pid": pot.pid, "how": how}
        pot.acct = a
        pot.chain.append(a)
        self.events.append((day, "OPEN", a, code, round(amount, 2), how, pot.pid))
        return a

    def _close(self, pot, day, amount, why):
        a = pot.acct
        self.accounts[a]["closed"] = day
        self.events.append((day, "CLOSE", a, self.accounts[a]["issue"], round(amount, 2), why, pot.pid))
        pot.acct = None

    def _new_pot(self, product, day, bal):
        issue = issue_of(day) if product == "LS" else product
        p = Pot(self.next_pid, product, issue, bal, int(self.r.randint(0, 3)))
        self.next_pid += 1
        self.pots.append(p)
        self._open(p, day, bal, "new")
        return p

    # -- the run ----------------------------------------------------------------
    def _run(self):
        r = self.r
        d0 = START
        for prod in PRODUCTS:
            for _ in range(INIT[prod]):
                bal = MEAN0[prod] * float(np.exp(r.normal(-0.6, 1.0)))
                bal = max(25.0, min(bal, 250000.0 if prod != "YS" else 18000.0))
                opened = d0 - dt.timedelta(days=int(r.randint(30, 3600)))
                p = Pot(self.next_pid, prod, "LS21" if prod == "LS" else prod, round(bal, 2), int(r.randint(0, 3)))
                self.next_pid += 1
                self.pots.append(p)
                self._open(p, opened, bal, "new")
        self._snapshot(0)
        for mi in range(1, len(MONTHS)):
            me, prev = MONTHS[mi], MONTHS[mi - 1]
            ndays = (me - prev).days
            spring = me.month in (4, 5)
            for p in list(self.pots):
                if not p.alive:
                    continue
                # deposits, withdrawals and interest over the month
                rate = RATE[p.product] + 0.55 * BANK[mi]
                p.bal *= float(np.exp(r.normal(DRIFT[p.product], VOL[p.product]))) * (1 + rate / 12.0)
                p.bal = round(max(p.bal, 1.0), 2)
                u = r.random_sample()
                if u < EXIT[p.product] * (1.0 + 0.35 * p.seg):
                    day = prev + dt.timedelta(days=int(r.randint(1, ndays + 1)))
                    self._close(p, day, p.bal, "paid")
                    p.alive = False
                    continue
                if u < EXIT[p.product] * (1.0 + 0.35 * p.seg) + BOND[p.product]:
                    day = prev + dt.timedelta(days=int(r.randint(1, ndays + 1)))
                    self._close(p, day, p.bal, "bond")
                    self.bonds.append((day, round(p.bal, 2), p.pid))
                    p.alive = False
                    continue
                if spring and p.product in SWITCH and p.issue != issue_of(me) and not getattr(p, "_sw", None) == me.year:
                    q = SWITCH[p.product] / 2.0     # the window runs over April and May
                    if r.random_sample() < q:
                        day = prev + dt.timedelta(days=int(r.randint(1, ndays + 1)))
                        self._close(p, day, p.bal, "switch")
                        p.product, p.issue = "LS", issue_of(me)
                        self._open(p, day, p.bal, "switch")
            # new money
            for prod in PRODUCTS:
                k = NEW[prod] + (34 if (prod == "IS" and me.month == 4) else 0)
                for _ in range(int(r.poisson(k))):
                    day = prev + dt.timedelta(days=int(r.randint(1, ndays + 1)))
                    bal = MEAN0[prod] * 0.55 * float(np.exp(r.normal(-0.5, 1.0)))
                    bal = round(max(20.0, min(bal, 250000.0 if prod != "YS" else 18000.0)), 2)
                    self._new_pot(prod, day, bal)
            self._snapshot(mi)

    def _snapshot(self, mi):
        for p in self.pots:
            if p.alive and p.acct is not None:
                self.balances[(p.acct, mi)] = p.bal


if __name__ == "__main__":
    w = World()
    import collections
    tot = collections.Counter()
    for (a, mi), b in w.balances.items():
        tot[mi] += b
    print("accounts", len(w.accounts), "pots", len(w.pots), "rows", len(w.balances))
    print("book start %.1fm end %.1fm" % (tot[0] / 1e6, tot[len(MONTHS) - 1] / 1e6))
    ev = collections.Counter((e[1], e[5]) for e in w.events)
    print(ev)
