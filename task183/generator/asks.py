"""The two asks, computed from the shipped outage export, step file, connectivity model, device list and customer
extract (data frames read back from target/), with every designed wrong stop beside the golden reading.

Golden reading (the reliability reporting standard): an interruption is sustained for a customer when that
customer's own restoration comes more than five minutes after the outage began; a customer is restored at the
step whose restoring device is the nearest one above it; the reliability year and its days are local prevailing
time; legacy OMS times are local and ADMS times are UTC; major event days by the 2.5 beta method on the five prior
reliability years' daily SAIDI; customers served are the connectivity model's metered points on the last day."""
import datetime as dt
import math

import numpy as np
import pandas as pd

import world as W

RY = (dt.date(2025, 10, 1), dt.date(2026, 9, 30))
PRIOR = [(dt.date(y - 1, 10, 1), dt.date(y, 9, 30)) for y in range(2021, 2026)]


def parse(ts, system, convert=True):
    t = dt.datetime.strptime(ts, "%Y-%m-%d %H:%M:%S")
    if system == "OMS":
        return t.replace(tzinfo=W.LOCAL)
    if not convert:          # the wrong path: a UTC stamp read as local time
        return t.replace(tzinfo=W.LOCAL)
    return t.replace(tzinfo=W.UTC).astimezone(W.LOCAL)


class Net:
    def __init__(self, devices_doc, conn):
        self.parent = {d["device_id"]: d["parent_device_id"] for d in devices_doc["devices"]}
        self.children = {}
        for d, p in self.parent.items():
            if p is not None:
                self.children.setdefault(p, []).append(d)
        self.rows = {}
        for m, dev, f, a, b in zip(conn["meter_id"], conn["device_id"], conn["feeder_id"], conn["eff_from"],
                                   conn["eff_to"]):
            b = None if (b is None or (isinstance(b, float) and math.isnan(b)) or pd.isna(b)) else b
            self.rows.setdefault(dev, []).append((m, f, a, b))
        self._desc, self._chain = {}, {}

    def desc(self, d):
        if d not in self._desc:
            out, st = [], [d]
            while st:
                x = st.pop()
                out.append(x)
                st.extend(self.children.get(x, []))
            self._desc[d] = out
        return self._desc[d]

    def chain(self, d):
        if d not in self._chain:
            out, x = [], d
            while x is not None:
                out.append(x)
                x = self.parent[x]
            self._chain[d] = out
        return self._chain[d]

    def meters(self, d, day):
        out = []
        for dev in self.desc(d):
            for m, f, a, b in self.rows.get(dev, []):
                if a <= day and (b is None or day < b):
                    out.append((m, dev, f))
        return out

    def served(self, day):
        n = {}
        seen = set()
        for dev, rows in self.rows.items():
            for m, f, a, b in rows:
                if a <= day and (b is None or day < b) and m not in seen:
                    seen.add(m)
                    n[f] = n.get(f, 0) + 1
        return n


def interruptions(net, oms, steps, convert=True):
    """One row per outage and interrupted meter: outage_id, meter, feeder at the outage, start (local), own minutes,
    outage minutes (restore_ts less start_ts on the export row), the export row's feeder list."""
    st_by = {}
    for r in steps.itertuples(index=False):
        st_by.setdefault(r.outage_id, []).append((int(r.step_no), r.restoring_device_id, r.step_restore_ts,
                                                  r.source_system))
    out = []
    for oid, g in oms.groupby("outage_id", sort=False):
        r0 = g.iloc[0]
        start = parse(r0["start_ts"], r0["source_system"], convert)
        out_min = (parse(r0["restore_ts"], r0["source_system"], convert) - start).total_seconds() / 60
        sts = sorted(st_by[oid])
        steps_l = [(rd, parse(ts, sy, convert)) for _, rd, ts, sy in sts]
        depth = {rd: len(net.chain(rd)) for rd, _ in steps_l}
        day = start.date()
        for m, dev, f in net.meters(r0["device_id"], day):
            ch = net.chain(dev)
            best = None
            for i, (rd, t) in enumerate(steps_l):
                if rd in ch and (best is None or depth[rd] > depth[steps_l[best][0]] or
                                 (depth[rd] == depth[steps_l[best][0]] and t > steps_l[best][1])):
                    best = i
            own = (steps_l[best][1] - start).total_seconds() / 60
            out.append((oid, m, f, start, day, own, out_min, len(steps_l)))
    return pd.DataFrame(out, columns=["outage_id", "meter_id", "feeder_id", "start", "day", "own_min", "outage_min",
                                      "n_steps"])


def served_on(net, day):
    return net.served(day)


def daily_saidi(intr, net, periods, sustained="own"):
    col = "own_min" if sustained == "own" else "outage_min"
    s = intr[intr[col] > 5.0]
    cm = s.groupby("day")["own_min" if sustained == "own" else "outage_min"].sum()
    out = {}
    for lo, hi in periods:
        base = sum(net.served(hi).values())
        d = lo
        while d <= hi:
            out[d] = float(cm.get(d, 0.0)) / base
            d += dt.timedelta(days=1)
    return out


def t_med(daily, ddof=1):
    v = np.array([x for x in daily.values() if x > 0])
    lv = np.log(v)
    return float(math.exp(lv.mean() + 2.5 * lv.std(ddof=ddof)))


def ask_figures(intr, net, med_days, served=None, sustained="own", feeder_col="feeder_id"):
    """SAIFI, SAIDI (major event days out) and the four-or-more count (major event days in) for the asked year."""
    served = served or net.served(RY[1])
    a = intr[(intr["day"] >= RY[0]) & (intr["day"] <= RY[1])]
    col = "own_min" if sustained == "own" else "outage_min"
    sus = a[a[col] > 5.0]
    nm = sus[~sus["day"].isin(med_days)]
    ci = nm.groupby(feeder_col).size()
    cmi = nm.groupby(feeder_col)["own_min"].sum()
    saifi = {f: ci.get(f, 0) / served[f] for f in W.FEEDERS}
    saidi = {f: float(cmi.get(f, 0.0)) / served[f] for f in W.FEEDERS}
    return saifi, saidi, sus


def cemi4(sus, net, by="current"):
    per = sus.groupby("meter_id")["outage_id"].nunique()
    if by == "current":
        cur = {}
        for dev, rows in net.rows.items():
            for m, f, a, b in rows:
                if a <= RY[1] and (b is None or RY[1] < b):
                    cur[m] = f
        out = {f: 0 for f in W.FEEDERS}
        for m, n in per.items():
            if n >= 4 and m in cur:
                out[cur[m]] += 1
        return out
    # by the feeder each interruption happened on: a meter's count split across the feeders it was on
    per_f = sus.groupby(["meter_id", "feeder_id"])["outage_id"].nunique()
    out = {f: 0 for f in W.FEEDERS}
    for (m, f), n in per_f.items():
        if n >= 4:
            out[f] += 1
    return out


def golden(oms, steps, conn, devices_doc, convert=True, ddof=1):
    net = Net(devices_doc, conn)
    intr = interruptions(net, oms, steps, convert)
    prior = daily_saidi(intr, net, PRIOR)
    T = t_med(prior, ddof)
    cur = daily_saidi(intr, net, [RY])
    meds = sorted(d for d, v in cur.items() if v > T)
    saifi, saidi, sus = ask_figures(intr, net, set(meds))
    c4 = cemi4(sus, net)
    return dict(net=net, intr=intr, T=T, prior=prior, cur=cur, meds=meds, saifi=saifi, saidi=saidi, cemi4=c4,
                served=net.served(RY[1]))


def column_sums(oms, served, med_days, convert=True):
    """The export's own columns summed per feeder row: customers_out and cust_minutes on rows whose outage lasted
    more than five minutes, outages beginning on major event days left out."""
    ci = {f: 0.0 for f in W.FEEDERS}
    cm = {f: 0.0 for f in W.FEEDERS}
    for r in oms.itertuples(index=False):
        st = parse(r.start_ts, r.source_system, convert)
        en = parse(r.restore_ts, r.source_system, convert)
        day = st.date()
        if not (RY[0] <= day <= RY[1]) or day in med_days:
            continue
        if (en - st).total_seconds() / 60 <= 5:
            continue
        ci[r.feeder_id] += r.customers_out
        cm[r.feeder_id] += r.cust_minutes
    return {f: ci[f] / served[f] for f in W.FEEDERS}, {f: cm[f] / served[f] for f in W.FEEDERS}


def cis_served(cis):
    return cis.groupby("feeder_label").size().to_dict()


def stops(g, oms, steps, conn, devices_doc, cis):
    """Every designed wrong stop of the two asks, each as {feeder: figure}."""
    net, intr, meds = g["net"], g["intr"], set(g["meds"])
    out = {}
    served = g["served"]
    out["A1 cracker: export columns summed, connectivity customers"] = column_sums(oms, served, meds)
    out["A1 natural: export columns summed, customer-system labels"] = column_sums(oms, cis_served(cis), meds)
    u = golden(oms, steps, conn, devices_doc, convert=False)
    out["A1 clock: each customer's restoration, ADMS times read as local"] = (u["saifi"], u["saidi"])
    sf, sd, _ = ask_figures(intr, net, meds, sustained="outage")
    out["A1 outage duration: every customer of an outage over five minutes"] = (sf, sd)
    sf, sd, _ = ask_figures(intr, net, meds, served=cis_served(cis))
    out["A1 labels: each customer's restoration, customer-system labels"] = (sf, sd)
    a = intr[(intr["day"] >= RY[0]) & (intr["day"] <= RY[1])]
    sus_out = a[a["outage_min"] > 5.0]
    out["A2 cracker: distinct outages, outage duration"] = cemi4(sus_out, net)
    sus = a[a["own_min"] > 5.0]
    out["A2 row feeder: each customer's restoration, the outage's feeder"] = cemi4(sus, net, by="row")
    # rows counted: a point counted once for each step row of an outage it was behind
    rows = a.loc[a.index.repeat(a["n_steps"])]
    per = rows.groupby("meter_id").size()
    cur = {}
    for dev, rr in net.rows.items():
        for m, f, x, y in rr:
            if x <= RY[1] and (y is None or RY[1] < y):
                cur[m] = f
    c = {f: 0 for f in W.FEEDERS}
    for m, n in per.items():
        if n >= 4 and m in cur:
            c[cur[m]] += 1
    out["A2 rows: one interruption per step row"] = c
    out["A2 clock: ADMS times read as local"] = u["cemi4"]
    return out
