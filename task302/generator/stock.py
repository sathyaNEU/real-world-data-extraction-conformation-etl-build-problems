"""Stock positions that agree with the sales, day by day.

Distribution-centre lines arrive Monday to Saturday before opening; each delivery brings the line back to its
order-up-to level in whole cases. A spell off the shelf is an order the store missed while the system still showed
stock: the evening count before it finds the shelf empty and corrects the system stock to zero, nothing arrives until
the next order is placed, and the delivery on the day it ends refills the line.
Formula comes from the supplier's weekly visit (Tuesday, Wednesday from 1 September 2025); a missed visit empties the
shelf until the next one. Count corrections set the system stock to zero where the shelf was found empty earlier than
the system expected; small write-offs (damage, expiry) come at random.

    on_hand_at_open[d + 1] = on_hand_at_open[d] - units_sold[d] + adjustment[d] + delivered[d + 1]
"""
import numpy as np

import params as P

CASE = {"W": [12, 6, 2, 12, 2, 12, 12, 12, 12, 12], "F": [6] * 8, "P": [4, 2, 4, 4, 6, 4, 6, 6, 4, 6, 4, 6],
        "G": [6] * 9}


def delivery_days(c):
    dow = P.DAYS.dayofweek.values
    if c == "F":
        tue = (dow == 1) & (P.DAYS < P.FORMULA_DAY_CHANGE)
        wed = (dow == 2) & (P.DAYS >= P.FORMULA_DAY_CHANGE)
        return tue | wed
    return dow != 6


def positions(res, closed, seed=P.SEED_STOCK):
    rng = np.random.default_rng(seed)
    out = {}
    for c, T in res.items():
        U = T["units"]
        O = T["oos"]
        S, L, N = U.shape
        deliv_day = delivery_days(c)
        on = np.zeros((S, L, N), np.int64)
        dl = np.zeros((S, L, N), np.int64)
        adj = np.zeros((S, L, N), np.int64)
        for s in range(S):
            for i in range(L):
                u = U[s, i]
                o = O[s, i]
                case = CASE[c][i]
                mu = max(u[~o].mean(), 0.05)
                gap = 7 if c == "F" else 2
                target = int(np.ceil((gap + 2.5) * mu * 1.6 / case) * case) + case
                stock = target
                for d in range(N):
                    if o[d]:
                        # nothing on hand at opening, nothing arrives: the order was missed
                        if stock != 0:
                            adj[s, i, d - 1] -= stock if d > 0 else 0
                            stock = 0
                        on[s, i, d] = 0
                        continue
                    if d > 0 and o[d - 1]:
                        q = target                      # the restock
                        dl[s, i, d] = q
                        stock += q
                    elif deliv_day[d] and not closed[s, d]:
                        q = max(0, target - stock)
                        q = int(np.ceil(q / case) * case)
                        dl[s, i, d] = q
                        stock += q
                    if stock < u[d]:
                        # an early sell-out the delivery schedule did not cover: an extra drop that morning
                        extra = int(np.ceil((u[d] - stock) / case) * case)
                        dl[s, i, d] += extra
                        stock += extra
                    on[s, i, d] = stock
                    stock -= int(u[d])
                    # damage and expiry write-offs
                    if stock > 0 and rng.uniform() < (0.004 if c != "G" else 0.03):
                        w = int(min(stock, 1 + rng.poisson(0.6 if c != "G" else 1.5)))
                        if d + 1 < N and o[d + 1]:
                            w = 0
                        adj[s, i, d] -= w
                        stock -= w
                    # the day before a spell must close at zero: what is left is a count correction
                    if d + 1 < N and o[d + 1] and stock != 0:
                        adj[s, i, d] -= stock
                        stock = 0
        out[c] = dict(on_hand=on, delivered=dl, adjustment=adj)
    return out


def check(res, pos):
    for c, T in res.items():
        U = T["units"]
        on, dl, adj = pos[c]["on_hand"], pos[c]["delivered"], pos[c]["adjustment"]
        lhs = on[:, :, 1:]
        rhs = on[:, :, :-1] - U[:, :, :-1] + adj[:, :, :-1] + dl[:, :, 1:]
        assert (lhs == rhs).all(), c
        assert ((on == 0) == T["oos"]).all() or True
        assert ((on == 0) & ~T["oos"]).sum() == 0, (c, int(((on == 0) & ~T["oos"]).sum()))
        assert ((on > 0) & T["oos"]).sum() == 0, c
        assert (on - U >= 0).all(), c
    return True
