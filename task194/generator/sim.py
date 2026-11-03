"""The clean truth: every flow, pressure, user, account and job, before any file is written."""
import datetime as dt
import numpy as np
import world as W

STEP = dt.timedelta(minutes=15)
N = W.DAYS * 96


def stamps():
    return [W.UTC0 + i * STEP for i in range(N)]


def local(t):
    return t + dt.timedelta(hours=1) if t < W.BST_END else t


def hh_profile(h, weekend):
    """l per household property per hour at local clock hour h (float)."""
    night = W.HH_NU
    morning = np.where(weekend, 22.0, 30.0)
    mpeak = np.where(weekend, 9.0, 7.4)
    v = night + morning * np.exp(-((h - mpeak) / 1.4) ** 2) + 17.0 * np.exp(-((h - 13.0) / 3.0) ** 2) \
        + 25.0 * np.exp(-((h - 19.0) / 2.1) ** 2)
    v = np.where((h >= 1.0) & (h < 5.0), night, v)
    return v


def nhh_profile(h, weekend):
    day = np.where(weekend, 0.0, 38.0)
    v = W.NHH_NU + day * np.exp(-((h - 12.0) / 3.5) ** 2)
    return np.where((h >= 1.0) & (h < 5.0), W.NHH_NU, v)


def large_users(rng):
    """Logged large users: (user_id, name, [(meter_serial, supply_point, area, share)], night m3/h, day m3/h, start)."""
    names = ["Hollin Dairies Ltd", "Vale Crescent Care Home", "St Aidan's RC High School", "Moorend Laundry Services",
             "Calvert Rise Leisure Centre", "Thrushgate Business Park (Unit 4-7)", "Northern Rail Depot - Barrowfold",
             "Netherby Road Health Centre", "OAKSHAW GOLF CLUB", "Stanecroft Brewery Co.", "Crake Bank Garden Centre",
             "Arnvale College, Whinlow Moor Campus", "Gorsey Bank Hotel", "Tollbar Cold Store",
             "R. Pennock & Sons (Abattoir)", "Lidden Common Primary School", "Ravensclough Mill Apartments (bulk)",
             "Ashworth Fold Medical Practice", "Kestle Hill Car Wash", "Upper Sowden Farm Shop"]
    areas = ["D4130", "D4136", "D4142", "D4123", "D4149", "D4155", "D4130", "D4168", "D4174", "D4180", "D4193",
             "D4211", "D3341", "D4230", "D3341", "D4161", "D4224", "D4205", "D4117", "D4142"]
    users = []
    for i, (nm, a) in enumerate(zip(names, areas)):
        night = float(np.round(rng.uniform(0.05, 0.9), 3))
        day = float(np.round(rng.uniform(1.5, 9.0), 3))
        uid = "LU%05d" % (31207 + int(rng.integers(5, 40)) * 23 + i * 61)
        serial = "%02dA%06d" % (int(rng.integers(10, 25)), int(rng.integers(100000, 999999)))
        users.append(dict(uid=uid, name=nm, area=a, night=night, day=day, start=None,
                          meters=[dict(serial=serial, sp="SP%07d" % int(rng.integers(1000000, 9999999)), area=a, share=1.0)]))
    # the college's second supply, a sports hall fed from Ravensclough, on its own meter and supply point
    col = users[11]
    col["meters"][0]["share"] = 0.63
    col["meters"].append(dict(serial="%02dA%06d" % (19, int(rng.integers(100000, 999999))),
                              sp="SP%07d" % int(rng.integers(1000000, 9999999)), area="D4224", share=0.37))
    # the hotel's laundry block sits over the boundary and is fed from Tollbar
    hot = users[12]
    hot["meters"][0]["share"] = 0.71
    hot["meters"].append(dict(serial="%02dA%06d" % (21, int(rng.integers(100000, 999999))),
                              sp="SP%07d" % int(rng.integers(1000000, 9999999)), area="D4230", share=0.29))
    # tenants' check meters behind three bulk supplies, logged on their own accounts at the bulk supply point
    for parent, tenant, frac in ((5, "Kalder Print Finishing Ltd (Unit 6, Thrushgate Business Park)", 0.34),
                                 (9, "Stanecroft Brewery Co. - bottling hall sub-meter", 0.41),
                                 (6, "Barrowfold Rail Maintenance (Network Fleet Services)", 0.27)):
        p = users[parent]
        users.append(dict(uid="LU%05d" % (32000 + int(rng.integers(100, 900))), name=tenant, area=p["area"], night=0, day=0,
                          start=None, sub_of=parent, frac=frac,
                          meters=[dict(serial="%02dA%06d" % (int(rng.integers(10, 25)), int(rng.integers(100000, 999999))),
                                       sp=p["meters"][0]["sp"], area=p["area"], share=1.0, sub=True)]))
    # the new depot at Pellow Bridge: logged from its connection, runs through the night
    users.append(dict(uid="LU%05d" % 33877, name="Pellow Bridge Distribution Centre (Kerrow Logistics)", area="D4187",
                      night=W.NEW_USER[2], day=11.8, start=W.NEW_USER[1],
                      meters=[dict(serial="24A%06d" % int(rng.integers(100000, 999999)),
                                   sp="SP%07d" % int(rng.integers(1000000, 9999999)), area="D4187", share=1.0)]))
    return users


def lu_hourly(u, t_local_h, weekend, active):
    h = t_local_h
    on = (h >= 6.0) & (h < 20.0) & (~weekend)
    return np.where(active, np.where(on, u["day"], u["night"]), 0.0)


def run(rng):
    ts = stamps()
    loc = [local(t) for t in ts]
    h = np.array([l.hour + l.minute / 60.0 for l in loc])
    wk = np.array([l.weekday() >= 5 for l in loc])
    tarr = np.array(ts, dtype="datetime64[m]")
    users = large_users(rng)
    nights = {}
    truth = {}
    flows = {}
    press = {}
    # each area's own wander between the periods: a step at a random October instant
    wander = {}
    for a in W.AREAS:
        code = a[0]
        if code in ("D4117", "D4123", W.BURST[0], W.NEW_USER[0], W.PRV[0]):
            wander[code] = (0.0, None)
        else:
            d = W.WANDER_LS[code] * 3.6 + float(rng.normal(0.0, 0.004))
            when = W.UTC0 + dt.timedelta(days=int(rng.integers(65, 70)), hours=int(rng.integers(0, 24)))
            wander[code] = (d, when)
    lu_area = {}
    for u in users:
        if u.get("sub_of") is not None:
            continue
        active = np.ones(N, bool) if u["start"] is None else (tarr >= np.datetime64(u["start"], "m"))
        base = lu_hourly(u, h, wk, active)
        for m in u["meters"]:
            q = base * m["share"] * (1.0 + rng.normal(0, 0.04, N))
            q = np.clip(q, 0, None)
            m["q"] = q
            lu_area[m["area"]] = lu_area.get(m["area"], 0) + q
    for u in users:
        if u.get("sub_of") is not None:   # a check meter records part of what its bulk meter already records
            pq = users[u["sub_of"]]["meters"][0]["q"]
            u["meters"][0]["q"] = np.clip(pq * u["frac"] * (1.0 + rng.normal(0, 0.05, N)), 0, None)
    for a in W.AREAS:
        code, name, tags, hh, nhh, km, pl, pn, l0 = a
        dn = rng.normal(0, 0.025, W.DAYS).repeat(96)
        hhq = hh * hh_profile(h, wk) * (1 + dn) / 1000.0
        nhq = nhh * nhh_profile(h, wk) / 1000.0
        luq = lu_area.get(code, np.zeros(N))
        demand = hhq + nhq + luq
        dmax = np.percentile(demand, 99)
        pset = np.full(N, pn)
        if code == W.PRV[0]:
            pset = np.where(tarr >= np.datetime64(W.PRV[1], "m"), W.PRV[3], W.PRV[2])
        p = pset - 6.5 * (demand / dmax) ** 2 + rng.normal(0, 0.12, N)
        leak0 = np.full(N, l0)
        d, when = wander[code]
        if when is not None:
            leak0 = leak0 + np.where(tarr >= np.datetime64(when, "m"), d, 0.0)
        if code == W.BURST[0]:
            leak0 = leak0 + np.where(tarr >= np.datetime64(W.BURST[1], "m"), W.BURST[2], 0.0)
        pref = pset[0] if code != W.PRV[0] else W.PRV[2]
        leak = leak0 * (p / pref) ** W.N1
        q = demand + leak
        flows[code] = q.copy()
        press[code] = p
        truth[code] = dict(hh=hhq, nh=nhq, lu=luq, leak=leak, leak0=leak0, p=p, demand=demand, pref=pref)
    # the open boundary valve: part of Moorend Low's draw comes through Kestle Hill's inlet
    open_ = tarr >= np.datetime64(W.VALVE_OPEN, "m")
    T = np.where(open_, W.TRANSFER_SHARE * flows["D4123"], 0.0)
    flows["D4117"] = flows["D4117"] + T
    flows["D4123"] = flows["D4123"] - T
    truth["transfer"] = T
    return dict(ts=ts, loc=loc, h=h, wk=wk, flows=flows, press=press, truth=truth, users=users, wander=wander)
