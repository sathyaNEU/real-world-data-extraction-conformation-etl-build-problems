"""The files the asks read and the call never does: the vendor's export from the breakfast cereal trial, the
distribution centre's trailer stops with the tills' first and last sale each day, and the distribution centre's
purchase orders with the suppliers' EDI messages and the goods received.

The trial export joins two reports: up to 1 February 2026 the stores' own stock report, which gives the stock on hand
when the store opened, and from 2 February the ordering system's, which gives the stock on hand when it closed.
The stores opened at 6:30 until the chain moved to a 7 am opening on 1 April 2026; the store list carries the current
hours. A purchase order the buyer changes is issued again, and the order export keeps the date it was last issued;
the suppliers' EDI messages keep every issue, the first being the order.
"""
import datetime as dt

import numpy as np
import pandas as pd

import params as P
import records as RC

# ---------------------------------------------------------------------------------------------------------------
# Ask A: the breakfast cereal trial

TRIAL_STORES = [203, 204, 210]                 # Feilding, Levin, Carterton
TRIAL_LIVE = pd.Timestamp("2026-02-02")
TRIAL_DAYS = pd.date_range("2025-11-03", "2026-05-03", freq="D")
CEREAL = ["Harvest Hills Wheat Biscuits 1.2kg", "Harvest Hills Wheat Biscuits 750g", "Harvest Hills Bran Flakes 500g",
          "Harvest Hills Oat Biscuits 1kg", "Kiwi Oat Co Rolled Oats 750g", "Kiwi Oat Co Rolled Oats 1.5kg",
          "Kiwi Oat Co Quick Oats 750g", "Kiwi Oat Co Porridge Sachets 10 Pack", "Morning Crunch Natural Muesli 750g",
          "Morning Crunch Fruit Muesli 750g", "Morning Crunch Toasted Muesli 1kg", "Morning Crunch Clusters 600g",
          "Sunrise Puffs Honey 500g", "Sunrise Puffs Chocolate 500g", "Sunrise Corn Flakes 500g",
          "Sunrise Rice Bubbles 410g", "Ridgeway Wheat Biscuits 1kg", "Ridgeway Rolled Oats 1kg",
          "Ridgeway Toasted Muesli 1kg", "Ridgeway Corn Flakes 500g", "Tui Valley Granola Berry 500g",
          "Tui Valley Granola Nut 500g", "Tui Valley Protein Granola 450g", "Alpine Grain Bircher 500g",
          "Alpine Grain Ancient Grain Flakes 400g", "Alpine Grain Gluten Free Muesli 500g", "Sunrise Fruit Loops 410g",
          "Sunrise Coco Pops 375g", "Harvest Hills Light n Tasty 525g", "Morning Crunch Peanut Butter Clusters 600g",
          "Kiwi Oat Co Steel Cut Oats 1kg", "Tui Valley Keto Granola 400g"]


def trial(rng):
    """The vendor's export for the trial stores' cereal lines: on hand (when the store opened up to 1 February 2026,
    when it closed from 2 February), delivered that morning and units sold. Hidden column: the opening stock."""
    n = len(CEREAL)
    arts = sorted(int(x) for x in rng.choice(np.arange(300000, 399999), n, replace=False))
    rows = []
    for st in TRIAL_STORES:
        lam = np.exp(rng.normal(np.log(3.2), 0.55, n))
        for i in range(n):
            case = int(rng.choice([6, 8, 10, 12]))
            stock, spell = int(np.ceil(lam[i] * 4.0 / case) * case) + case, 0
            for day in TRIAL_DAYS:
                after = day >= TRIAL_LIVE
                dow = day.dayofweek
                target = int(np.ceil(lam[i] * (6.5 if dow == 5 else 4.0) / case) * case) + case
                deliv = 0
                if spell > 0:
                    # an order the store missed: nothing comes until the next order is placed
                    spell -= 1
                    opening = 0
                else:
                    if dow != 6 and stock < target:
                        deliv = int(np.ceil((target - stock) / case) * case)
                    opening = stock + deliv
                demand = int(rng.poisson(lam[i] * (1.12 if dow in (4, 5) else 1.0)))
                sold = min(demand, opening)
                closing = opening - sold
                # manual ordering misses a line more often than the system: the evening count before a missed
                # order finds the shelf empty and the line opens empty until the order is caught
                if spell == 0 and opening > 0 and sold > 0 and rng.uniform() < (0.0058 if after else 0.0150) and \
                        day != TRIAL_LIVE - pd.Timedelta(days=1):
                    spell = 1 + int(rng.poisson(1.3))
                    closing = 0
                rows.append((st, day.date(), arts[i], CEREAL[i], closing if after else opening, deliv, sold, opening))
                stock = closing
    df = pd.DataFrame(rows, columns=["store_no", "date", "article", "description", "on_hand", "delivered",
                                     "units_sold", "_opening"])
    return df.sort_values(["date", "store_no", "article"], kind="stable").reset_index(drop=True)


# ---------------------------------------------------------------------------------------------------------------
# Ask B: trailer stops and the tills' trading day

HOURS_CHANGE = pd.Timestamp("2026-04-01")      # 6:30 opening until 31 March 2026, 7:00 from 1 April
ROUTES = {"A": [201, 202, 203], "B": [204, 212, 213, 214], "C": [205, 206, 207, 208], "D": [209, 210, 211],
          "E": [215, 216], "S1": [223, 221, 222], "S2": [217, 218, 219, 220, 224]}
YEAR = pd.date_range(P.BASE_LO, P.D1, freq="D")


def opening_time(day):
    return dt.time(6, 30) if day < HOURS_CHANGE else dt.time(7, 0)


def trailer_stops(rng, closed):
    """The distribution centre's trailer stops, one row per store a run reached, Monday to Saturday. A run reaches its
    stores between half past three and a quarter past six; a run held up on the road reaches the store it was making
    for at twenty to seven or a little after and the rest after ten past seven; a run that breaks down reaches every
    store after a quarter past seven. The Nelson and Marlborough runs cross on the evening ferry."""
    idx = {no: k for k, no in enumerate(RC.STORE_NO)}
    days = [d for d in YEAR if d.dayofweek != 6]
    early = [d for d in days if d < HOURS_CHANGE]
    # the runs held up: about one in thirty, and at least two before April at every store
    held = {}
    for r, stops in ROUTES.items():
        for d in days:
            if rng.uniform() < 0.032:
                held[(r, d)] = int(rng.integers(0, len(stops)))
        for k in range(len(stops)):
            have = sum(1 for (rr, d), kk in held.items() if rr == r and kk == k and d < HOURS_CHANGE)
            while have < 2:
                d = early[int(rng.integers(0, len(early)))]
                if (r, d) not in held:
                    held[(r, d)] = k
                    have += 1
    rows = []
    run_no = 50001
    trailers = {r: "TR%02d" % (k + 3) for k, r in enumerate(ROUTES)}
    for day in days:
        d = (day - P.D0).days
        for r, stops in ROUTES.items():
            if r.startswith("S"):
                dep = dt.datetime.combine((day - pd.Timedelta(days=1)).date(), dt.time(17, 50)) + \
                    dt.timedelta(minutes=int(rng.integers(0, 40)))
            else:
                dep = dt.datetime.combine(day.date(), dt.time(1, 30)) + dt.timedelta(minutes=int(rng.integers(0, 35)))
            first = dt.datetime.combine(day.date(), dt.time(3, 35)) + dt.timedelta(minutes=int(rng.integers(0, 30)))
            arr = [first]
            for _ in stops[1:]:
                arr.append(arr[-1] + dt.timedelta(minutes=int(rng.integers(20, 44))))
            limit = dt.datetime.combine(day.date(), dt.time(6, 15))
            if arr[-1] > limit:
                arr = [a - (arr[-1] - limit) for a in arr]
            if (r, day) in held:
                k = held[(r, day)]
                arr[k] = dt.datetime.combine(day.date(), dt.time(6, 40)) + dt.timedelta(minutes=int(rng.integers(0, 9)))
                t = dt.datetime.combine(day.date(), dt.time(7, 10))
                for j in range(k + 1, len(arr)):
                    t += dt.timedelta(minutes=int(rng.integers(12, 40)))
                    arr[j] = t
            elif rng.uniform() < 0.045:
                t = dt.datetime.combine(day.date(), dt.time(7, 15)) + dt.timedelta(minutes=int(rng.integers(0, 140)))
                for j in range(len(arr)):
                    arr[j] = t
                    t += dt.timedelta(minutes=int(rng.integers(20, 44)))
            # the driver's handheld stamps the arrival to the second
            arr = [a + dt.timedelta(seconds=int(rng.integers(0, 60))) for a in arr]
            for k, st in enumerate(stops):
                if closed[idx[st], d]:
                    continue
                rows.append([run_no, trailers[r], st, dep, arr[k], int(rng.integers(30, 120))])
            run_no += 1
    df = pd.DataFrame(rows, columns=["run_no", "trailer", "store_no", "departed", "arrived", "cases"])
    for c in ("departed", "arrived"):
        df[c] = pd.to_datetime(df[c]).dt.strftime("%Y-%m-%d %H:%M:%S")
    return df


def trading_days(rng, closed, size):
    """The tills' first and last sale and the transactions each store-day of the twelve months."""
    idx = {no: k for k, no in enumerate(RC.STORE_NO)}
    rows = []
    for day in YEAR:
        d = (day - P.D0).days
        op = opening_time(day)
        for st in RC.STORE_NO:
            if closed[idx[st], d]:
                continue
            first = dt.datetime.combine(day.date(), op) + dt.timedelta(seconds=int(rng.integers(40, 9 * 60)))
            last = dt.datetime.combine(day.date(), dt.time(21, 0)) - dt.timedelta(seconds=int(rng.integers(20, 6 * 60)))
            tx = int(rng.poisson(1650 * size[idx[st]] * P.DOW[day.dayofweek]))
            rows.append((st, day.date(), first.strftime("%H:%M:%S"), last.strftime("%H:%M:%S"), tx))
    return pd.DataFrame(rows, columns=["store_no", "trade_date", "first_sale", "last_sale", "transactions"])


# ---------------------------------------------------------------------------------------------------------------
# Ask C: purchase orders, EDI messages and goods received at the distribution centre

DC_SUPPLIERS = {"Kaimai Spring Ltd": ("W", 7, (3, 8)), "Te Puna Bottling": ("W", 7, (2, 6)),
                "Southern Alps Beverages": ("W", 14, (5, 10)), "Ruahine Artesian": ("W", 14, (4, 9)),
                "Huntaway Petfoods": ("P", 7, (5, 11)), "Manawatu Pet Nutrition": ("P", 14, (4, 9)),
                "Blue Ridge Pet Co": ("P", 14, (8, 15)), "Feline Choice NZ": ("P", 7, (6, 12)),
                "Bakehouse Gluten Free": ("G", 2, (1, 3)), "Rangi Baking": ("G", 3, (1, 4))}
CHANGE_SHARE = 0.36
# cases to a pallet as each supplier builds them, and the cases a line is ordered in
PER_PALLET = {"Kaimai Spring Ltd": 72, "Te Puna Bottling": 80, "Southern Alps Beverages": 64, "Ruahine Artesian": 70,
              "Huntaway Petfoods": 50, "Manawatu Pet Nutrition": 45, "Blue Ridge Pet Co": 40, "Feline Choice NZ": 60,
              "Bakehouse Gluten Free": 120, "Rangi Baking": 110}
LINE_CASES = {"W": (300, 900), "P": (160, 520), "G": (12, 55)}
SPLIT = {"W": 0.36, "P": 0.30, "G": 0.0}     # a cycle's order raised as two orders, one per buying group
HOLD = {"W": 0.0, "P": 0.0, "G": 0.42}       # a bakery holding an order to ship it with the next one
TRUCK = 24                                    # pallets a supplier's truck carries
TOPUP = {"W": 0.0, "P": 0.0, "G": 0.22}       # a bakery's short-dated top-up order, sent the same day on its own van


def purchasing(rng, ln):
    """Purchase orders raised from 1 June 2025 to 30 June 2026 for the lines the distribution centre stocks, the EDI
    messages that placed and changed them, the goods received against them and the dock's appointments. A supplier
    sends a dispatch advice for each order and ships the orders it has ready on one truck where they fit (the two
    orders of a split cycle; a bakery's held order with the next one) and on two trucks the same day where they do
    not; the receiving system books each truck's pallets onto every line it receives from that truck, under every
    dispatch advice the truck carried."""
    po_rows, msg_rows, grn_rows, dock_rows = [], [], [], []
    po_no, grn_no = 4500210, 7700050
    appt = [0]
    start = pd.Timestamp("2025-06-01")
    for s_i, (sup, (cat, every, (lo, hi))) in enumerate(DC_SUPPLIERS.items()):
        arts = ln[ln.supplier == sup].article.tolist()
        day = start + pd.Timedelta(days=int(rng.integers(0, every)))
        held = []
        da = 0
        while day <= P.D1:
            if day.dayofweek >= 5:
                day += pd.Timedelta(days=7 - day.dayofweek)
            lead = int(rng.integers(lo, hi + 1))
            due = day + pd.Timedelta(days=lead)
            received = due + pd.Timedelta(days=int(rng.choice([0, 0, 0, 0, 1, 1, 2, -1])))
            while received.dayofweek == 6:
                received += pd.Timedelta(days=1)
            groups = [arts]
            if len(arts) >= 2 and rng.uniform() < SPLIT[cat]:
                cut = int(rng.integers(1, len(arts)))
                groups = [arts[:cut], arts[cut:]]
            ready = []
            topup = cat == "G" and rng.uniform() < TOPUP[cat]
            if topup:
                groups = groups + [sorted(rng.choice(arts, min(2, len(arts)), replace=False).tolist())]
            for g_i, grp in enumerate(groups):
                sent = dt.datetime.combine(day.date(), dt.time(int(rng.integers(8, 16)), int(rng.integers(0, 60)),
                                                                 int(rng.integers(0, 60))))
                k = max(1, int(rng.integers(max(1, len(grp) // 2), len(grp) + 1)))
                lines = sorted(rng.choice(grp, k, replace=False).tolist())
                if topup and g_i == len(groups) - 1:
                    lines = list(grp)
                qty = {a: int(rng.integers(*LINE_CASES[cat])) for a in lines}
                msg_rows.append((po_no, sup, "ORDERS", sent))
                issued = day
                # the buyer changes some orders before the supplier ships: each change issues the order again
                if rng.uniform() < CHANGE_SHARE and (received - day).days >= 2:
                    n_ch = 1 + int(rng.uniform() < 0.25)
                    when = sorted(rng.integers(1, max(2, (received - day).days), n_ch).tolist())
                    for w in when:
                        t = dt.datetime.combine((day + pd.Timedelta(days=int(w))).date(),
                                                dt.time(int(rng.integers(8, 17)), int(rng.integers(0, 60)),
                                                        int(rng.integers(0, 60))))
                        if t.weekday() >= 5:
                            continue
                        msg_rows.append((po_no, sup, "ORDCHG", t))
                        issued = pd.Timestamp(t.date())
                        a = lines[int(rng.integers(0, len(lines)))]
                        qty[a] = max(1, qty[a] + int(rng.integers(-20, 40)))
                for a in lines:
                    po_rows.append((po_no, sup, issued.date(), a, qty[a], due.date()))
                if rng.uniform() >= 0.015:
                    got = {a: (q if rng.uniform() > 0.06 else max(0, q - int(rng.integers(1, 1 + max(1, q // 6)))))
                           for a, q in qty.items()}
                    got = {a: q for a, q in got.items() if q}
                    if got:
                        ready.append((po_no, got, topup and g_i == len(groups) - 1))
                po_no += 1
            vans = [[(p_no, got, -(-sum(got.values()) // PER_PALLET[sup]))] for p_no, got, t in ready if t]
            ready = [(p_no, got) for p_no, got, t in ready if not t]
            if HOLD[cat] and ready and not held and rng.uniform() < HOLD[cat]:
                held = ready
                ready = []
            else:
                ready = held + ready
                held = []
            # an order too big for one truck goes on two, each receipted on its own note
            parts = []
            for p_no, got in ready:
                if -(-sum(got.values()) // PER_PALLET[sup]) > TRUCK:
                    keys = sorted(got)
                    parts += [(p_no, {a: got[a] for a in keys[0::2]}), (p_no, {a: got[a] for a in keys[1::2]})]
                else:
                    parts.append((p_no, got))
            trucks, load, used = [], [], 0
            for p_no, got in parts:
                pal = -(-sum(got.values()) // PER_PALLET[sup])
                if load and used + pal > TRUCK:
                    trucks.append(load)
                    load, used = [], 0
                load.append((p_no, got, pal))
                used += pal
            if load:
                trucks.append(load)
            trucks += vans
            if trucks:
                for load in trucks:
                    appt[0] += 1
                    t_arr = dt.datetime.combine(received.date(), dt.time(int(rng.integers(5, 15)), int(rng.integers(0, 60)),
                                                                         int(rng.integers(0, 60))))
                    pallets = sum(x[2] for x in load)
                    for p_no, got, _ in load:
                        da += 1
                        ref = "%s-%05d" % ("".join(w[0] for w in sup.split()[:2]).upper(), 1200 + 37 * s_i + da)
                        dock_rows.append(("AP%06d" % (310000 + appt[0]), sup, t_arr, int(rng.integers(1, 9)), ref))
                        for a in sorted(got):
                            grn_rows.append((grn_no, p_no, ref, received.date(), a, got[a], pallets))
                        grn_no += 1
            day += pd.Timedelta(days=every)
    po = pd.DataFrame(po_rows, columns=["po_no", "supplier", "issued", "article", "cases", "due"])
    msg = pd.DataFrame(msg_rows, columns=["po_no", "supplier", "message", "sent"])
    msg["sent"] = pd.to_datetime(msg.sent).dt.strftime("%Y-%m-%d %H:%M:%S")
    grn = pd.DataFrame(grn_rows, columns=["grn_no", "po_no", "delivery_ref", "received", "article", "cases", "pallets"])
    rd = pd.to_datetime(grn.received)
    grn = grn[(rd >= P.BASE_LO) & (rd <= P.D1)]
    dock = pd.DataFrame(dock_rows, columns=["appointment_no", "supplier", "arrived", "door", "delivery_ref"])
    ad = pd.to_datetime(dock.arrived)
    dock = dock[(ad >= P.BASE_LO) & (ad < P.D1 + pd.Timedelta(days=1))].copy()
    dock["arrived"] = pd.to_datetime(dock.arrived).dt.strftime("%Y-%m-%d %H:%M:%S")
    return (po.sort_values(["po_no", "article"]).reset_index(drop=True),
            msg.sort_values(["sent", "po_no"]).reset_index(drop=True),
            grn.sort_values(["received", "grn_no", "article"]).reset_index(drop=True),
            dock.sort_values(["arrived", "appointment_no", "delivery_ref"]).reset_index(drop=True))
