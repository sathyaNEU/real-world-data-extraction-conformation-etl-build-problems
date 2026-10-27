"""The pack-only solver: reads target/ the way an analyst would, builds each panel home's 2025 hours in market time,
runs the programme battery hour by hour, and computes every rung of the ladder and the golden.

    python3 task310/generator/solve.py [target dir]
"""
import os
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import params as P  # noqa: E402

M0 = pd.Timestamp("2025-01-01 00:00")
NH = 8760
DST_END = pd.Timestamp("2025-04-06 02:00")      # market time
DST_START = pd.Timestamp("2025-10-05 02:00")


def battery(gen, load, cap=P.BAT_USABLE_KWH, pmax=P.BAT_POWER_KW, ec=P.BAT_CHARGE_EFF, ed=P.BAT_DISCHARGE_EFF):
    """(homes, hours) solar and general-supply use in kWh per hour; returns the energy each home's battery delivers."""
    n, T = gen.shape
    soc = np.zeros(n)
    out = np.zeros(n)
    sur = gen - load
    for t in range(T):
        s = sur[:, t]
        c = np.minimum(np.minimum(np.clip(s, 0, None), pmax), (cap - soc) / ec)
        soc = soc + c * ec
        d = np.minimum(np.minimum(np.clip(-s, 0, None), pmax), soc * ed)
        soc = soc - d / ed
        out += d
    return out


class Pack:
    def __init__(self, target):
        f = lambda k: os.path.join(target, P.FILES[k])
        self.reg = pd.read_csv(f("register"), dtype=str)
        self.sys = pd.read_excel(f("systems"), dtype={"panel_id": str})
        self.conn = pd.read_csv(f("connections"), dtype={"nmi": str})
        self.pids = list(self.reg.panel_id)
        self.idx = {p: i for i, p in enumerate(self.pids)}
        self.region = np.array([{v: k for k, v in P.REGIONS.items()}[r] for r in self.reg.region])
        n = len(self.pids)
        self.gen = np.zeros((n, NH))
        self.e1 = np.zeros((n, NH))
        self.b1 = np.zeros((n, NH))
        self.e2 = np.zeros((n, NH))
        self._inverters(f("velkora"), f("ondrava"))
        self._meter(f("meter"))
        self.load = self.gen + self.e1 - self.b1
        self._systems()

    def _inverters(self, sv_path, ht_path):
        ref2pid = dict(zip(self.reg.inverter_ref, self.reg.panel_id))
        for r in self.sys.itertuples():
            ref2pid[str(r.inverter_ref)] = r.panel_id
        sv = pd.read_parquet(sv_path)
        loc = pd.to_datetime(sv.period_start)
        off = sv.utc_offset.map({"+10:00": 0, "+11:00": 1}).astype(int)
        mkt = loc - pd.to_timedelta(off, unit="h")
        t = ((mkt - M0) / pd.Timedelta(hours=1)).astype(int).to_numpy()
        rows = sv.site_ref.map(lambda s: self.idx[ref2pid[s]]).to_numpy()
        ok = (t >= 0) & (t < NH)
        np.add.at(self.gen, (rows[ok], t[ok]), sv.energy_wh.to_numpy()[ok] / 1000.0)
        ht = pd.read_csv(ht_path, dtype={"serial": str})
        for serial, g in ht.groupby("serial", sort=False):
            loc_end = pd.to_datetime(g.read_at).to_list()
            cnt = g.total_yield_wh.to_numpy()
            # local hour-end stamps to market: daylight saving until the clocks go back (the first of the repeated
            # 03:00 readings) and again after they go forward
            mkt_end = []
            seen_repeat = False
            for lt in loc_end:
                if lt == pd.Timestamp("2025-04-06 03:00"):
                    m = lt - pd.Timedelta(hours=1) if not seen_repeat else lt
                    seen_repeat = True
                elif lt < pd.Timestamp("2025-04-06 03:00") or lt >= pd.Timestamp("2025-10-05 03:00"):
                    m = lt - pd.Timedelta(hours=1)
                else:
                    m = lt
                mkt_end.append(m)
            e = np.diff(cnt, prepend=np.nan)
            sysrow = self.sys[self.sys.inverter_ref.astype(str) == serial]
            new_inverter = bool(len(sysrow)) and str(sysrow.iloc[0].note).startswith("replacement")
            if new_inverter:
                e[0] = cnt[0]                     # a replacement inverter's counter starts from zero
            else:
                e[0] = 0.0                        # the year's first reading closes a night hour
            pid = ref2pid[serial]
            for m, v in zip(mkt_end, e):
                t = int((m - pd.Timedelta(hours=1) - M0) / pd.Timedelta(hours=1))
                if 0 <= t < NH:
                    self.gen[self.idx[pid], t] += v / 1000.0

    def _meter(self, path):
        m = pd.read_parquet(path)
        nmi2i = {n: self.idx[p] for n, p in zip(self.reg.nmi, self.reg.panel_id)}
        end = pd.to_datetime(m.interval_end)
        t = ((end - pd.Timedelta(minutes=30) - M0) / pd.Timedelta(hours=1)).astype(int).to_numpy() if False else \
            (((end - pd.Timedelta(minutes=30)) - M0) // pd.Timedelta(hours=1)).to_numpy()
        rows = m.nmi.map(nmi2i).to_numpy()
        ok = (t >= 0) & (t < NH)
        np.add.at(self.e1, (rows[ok], t[ok]), m.e1_kwh.to_numpy()[ok])
        np.add.at(self.b1, (rows[ok], t[ok]), m.b1_kwh.to_numpy()[ok])
        np.add.at(self.e2, (rows[ok], t[ok]), np.nan_to_num(m.e2_kwh.to_numpy()[ok]))

    def _systems(self):
        n = len(self.pids)
        self.kwp = np.zeros((n, NH))
        self.ac = np.zeros((n, NH))
        self.orient = np.array([""] * n, dtype=object)
        hours = M0 + pd.to_timedelta(np.arange(NH), unit="h")
        for r in self.sys.itertuples():
            i = self.idx[r.panel_id]
            a = pd.Timestamp(r.valid_from)
            b = pd.Timestamp(r.valid_to) if isinstance(r.valid_to, str) and r.valid_to else pd.Timestamp("2100-01-01")
            mask = (hours >= a) & (hours < b)
            self.kwp[i, mask] = r.array_kwp
            self.ac[i, mask] = r.inverter_ac_kw
            self.orient[i] = r.array_orientation
        lim = dict(zip(self.conn.nmi, self.conn.export_limit_kw))
        self.limit = np.array([lim[n] for n in self.reg.nmi])
        self.limited = self.limit < self.ac.max(axis=1)


def rebuild(pk, stat="median", by_orient=False):
    """The golden family: each limited home's available solar rebuilt hour by hour from its region's unlimited homes'
    output per kWp under the same sky, capped at the home's inverter rating."""
    gen = pk.gen.copy()
    with np.errstate(invalid="ignore", divide="ignore"):
        per = np.where(pk.kwp > 0, pk.gen / pk.kwp, 0.0)
    for i in np.where(pk.limited)[0]:
        sel = (pk.region == pk.region[i]) & (~pk.limited)
        if by_orient:
            s2 = sel & (pk.orient == pk.orient[i])
            if s2.sum() >= 3:
                sel = s2
        ref = np.median(per[sel], axis=0) if stat == "median" else per[sel].mean(axis=0)
        gen[i] = np.minimum(pk.kwp[i] * ref, pk.ac[i])
        gen[i] = np.maximum(gen[i], pk.gen[i])
    return gen


def by_region(pk, v):
    return {r: float(v[pk.region == r].mean()) for r in P.REGION_ORDER}


def order(vals):
    return sorted(P.REGION_ORDER, key=lambda r: -vals[r])


def solve(target):
    pk = Pack(target)
    res = {}
    res["golden"] = by_region(pk, battery(rebuild(pk), pk.load))
    res["recorded"] = by_region(pk, battery(pk.gen, pk.load))
    exp_y = pk.b1.sum(1)
    imp_y = pk.e1.sum(1)
    cap_y = 365 * P.BAT_USABLE_KWH * P.BAT_DISCHARGE_EFF
    res["annual_totals"] = by_region(pk, np.minimum(np.minimum(exp_y * P.BAT_CHARGE_EFF * P.BAT_DISCHARGE_EFF, imp_y), cap_y))
    keep = ~pk.limited
    rec = battery(pk.gen, pk.load)
    res["unlimited_only"] = {r: float(rec[(pk.region == r) & keep].mean()) for r in P.REGION_ORDER}
    return pk, res


if __name__ == "__main__":
    tgt = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "target")
    pk, res = solve(tgt)
    for k, v in res.items():
        print("%-16s" % k, "  ".join("%s %.0f" % (r, v[r]) for r in order(v)))


# ---------------------------------------------------------------- the asks, read from the pack
CENSUS = pd.Timestamp("2026-09-30")
SOLAR_BY = pd.Timestamp("2025-09-30")
STYPES = {"STREET": "ST", "ROAD": "RD", "AVENUE": "AVE", "CRESCENT": "CRES", "PLACE": "PL", "DRIVE": "DR",
          "COURT": "CT", "PARADE": "PDE", "CLOSE": "CL"}


def norm_addr(a):
    a = str(a).upper().replace(",", " ").split()
    if a and a[0] == "UNIT":
        a = [a[1] + "/" + a[2]] + a[3:]
    if a and a[-1] in STYPES:
        a[-1] = STYPES[a[-1]]
    return " ".join(a)


def ask_eligible(target, mode="golden"):
    """Eligible homes per region on the census date. Modes: golden; der_only (no Booster claims); nmi_only (claims
    matched on the NMI they carry, no chain, no address); no_normalise (addresses as written); active_row (solar dated
    from the active register row); nmi_min (solar dated from the NMI's own earliest row, no chain)."""
    f = lambda k: os.path.join(target, P.FILES[k])
    der = pd.read_csv(f("der"), dtype={"nmi": str, "postcode": str})
    sd = pd.read_csv(f("standing"), dtype={"nmi": str, "postcode": str, "previous_nmi": str})
    bc = pd.read_excel(f("booster"), dtype={"nmi": str, "postcode": str})
    der["commissioned"] = pd.to_datetime(der.commissioned)
    pv_all = der[der.der_type == "PV"]
    pv = pv_all[(pv_all.status == "Active") & (pv_all.customer_class == "RES") & (pv_all.commissioned <= CENSUS)]
    bess = der[(der.der_type == "BESS") & (der.status == "Active") & (der.commissioned <= CENSUS)]
    cand = pv.drop_duplicates("nmi")
    cand = cand[~cand.nmi.isin(set(bess.nmi))]
    # when solar was first connected at the premises: the earliest PV row on the NMI and on every NMI it replaced
    first = pv_all.groupby("nmi").commissioned.min().to_dict()
    prev = dict(zip(sd.nmi, sd.previous_nmi.fillna("")))
    def start(n, chain=True):
        best = first.get(n)
        p = prev.get(n, "") if chain else ""
        while p:
            if p in first:
                best = min(best, first[p]) if best is not None else first[p]
            p = prev.get(p, "")
        return best
    if mode == "active_row":
        cand = cand[cand.commissioned <= SOLAR_BY]
    elif mode == "nmi_min":
        cand = cand[cand.nmi.map(lambda n: start(n, False)) <= SOLAR_BY]
    else:
        cand = cand[cand.nmi.map(start) <= SOLAR_BY]
    if mode == "der_only":
        return cand.groupby("network_region").size().to_dict()
    paid = bc[bc.status == "Paid"].copy()
    paid["nmi"] = paid.nmi.fillna("")
    excl = set(paid.nmi[paid.nmi != ""])
    if mode != "nmi_only":
        chain = dict(zip(sd.previous_nmi.fillna(""), sd.nmi))
        excl = {chain.get(n, n) for n in excl}
        act = sd[sd.nmi_status == "Active"]
        nn = paid[paid.nmi == ""]
        if mode == "no_normalise":
            key = dict(zip(act.address.str.upper() + "|" + act.suburb + "|" + act.postcode, act.nmi))
            look = [str(a).upper() + "|" + str(sb).upper() + "|" + pc for a, sb, pc in zip(nn.premises_address, nn.suburb, nn.postcode)]
        else:
            key = dict(zip(act.address + "|" + act.suburb + "|" + act.postcode, act.nmi))
            look = [norm_addr(a) + "|" + str(sb).upper() + "|" + pc for a, sb, pc in zip(nn.premises_address, nn.suburb, nn.postcode)]
        for k in look:
            n = key.get(k)
            if n:
                excl.add(n)
    cand = cand[~cand.nmi.isin(excl)]
    return cand.groupby("network_region").size().to_dict()


def ask_pilot(target, mode="golden"):
    """The pilot batteries' energy delivered in each quarter of 2025, MWh. Modes: golden; rows (every row summed);
    daily (re-sent rows dropped, daily rows summed); counters (re-sent rows dropped, each battery's counter read at
    the quarter ends, every battery summed); pairs_once (as counters, every two-battery home counted once)."""
    f = lambda k: os.path.join(target, P.FILES[k])
    t = pd.read_parquet(f("telemetry"))
    reg = pd.read_excel(f("pilot_sites"), dtype=str).fillna("")
    t["date"] = pd.to_datetime(t.date)
    q = t.date.dt.quarter
    if mode == "rows":
        return [round(t.discharged_wh[q == i].sum() / 1e6, 4) for i in (1, 2, 3, 4)]
    t = t.drop_duplicates(["battery_serial", "date"]).sort_values(["battery_serial", "date"], kind="mergesort")
    if mode == "daily":
        q = t.date.dt.quarter
        return [round(t.discharged_wh[q == i].sum() / 1e6, 4) for i in (1, 2, 3, 4)]
    qend = [pd.Timestamp("2025-03-31"), pd.Timestamp("2025-06-30"), pd.Timestamp("2025-09-30"),
            pd.Timestamp("2025-12-31")]
    new_units = set(reg.battery_serial[reg.note == "replacement unit"])
    per = {}
    for s_, g in t.groupby("battery_serial", sort=True):
        first = g.iloc[0]
        prev = 0.0 if s_ in new_units else float(first.lifetime_discharged_wh - first.discharged_wh)
        out = [0.0, 0.0, 0.0, 0.0]
        for i, qe in enumerate(qend):
            upto = g[g.date <= qe]
            if len(upto) == 0:
                continue
            c = float(upto.lifetime_discharged_wh.iloc[-1])
            out[i] = c - prev
            prev = c
        per[s_] = out
    # homes with two batteries in service together (a replacement unit follows the battery it replaced)
    live = reg[reg.note != "replacement unit"]
    once = set()
    for site, g in live.groupby("site_id"):
        if len(g) < 2:
            continue
        u1, u2 = list(g.battery_serial)[:2]
        if mode == "pairs_once":
            once.add(u2)
            continue
        if mode == "golden":
            a1 = t[t.battery_serial == u1].set_index("date").discharged_wh
            a2 = t[t.battery_serial == u2].set_index("date").discharged_wh
            common = a1.index.intersection(a2.index)
            if len(common) and (a1[common] == a2[common]).all():
                once.add(u2)                      # one battery meter reported on both units' rows
    tot = [0.0, 0.0, 0.0, 0.0]
    for s_, v in per.items():
        if s_ in once:
            continue
        tot = [x + y for x, y in zip(tot, v)]
    return [round(x / 1e6, 4) for x in tot]


def _suburb_region(target):
    f = lambda k: os.path.join(target, P.FILES[k])
    der = pd.read_csv(f("der"), dtype={"nmi": str, "postcode": str}, usecols=["nmi", "network_region"])
    sd = pd.read_csv(f("standing"), dtype={"nmi": str, "postcode": str}, usecols=["nmi", "suburb", "postcode"])
    m = sd.merge(der.drop_duplicates("nmi"), on="nmi")
    sub = m.drop_duplicates(["suburb", "postcode"]).set_index(["suburb", "postcode"]).network_region.to_dict()
    pc = m.groupby("postcode").network_region.agg(lambda x: x.value_counts().index[0]).to_dict()
    return sub, pc


def ask_installs(target, mode="golden"):
    """2025 battery installations per region by installers accredited through 2027. Modes: golden; rows (module rows
    counted); no_amendments; current_numbers_only (only the new accreditation numbers recognised); by_postcode (region
    from the postcode's main region); careful (every certificate an installation once amendments are applied);
    dedup_first (certificates sharing modules collapsed to the first lodged before the amendments);
    neighbour_merge (certificates collapsed on installer, date, suburb and model)."""
    f = lambda k: os.path.join(target, P.FILES[k])
    c = pd.read_csv(f("certificates"), dtype=str)
    am = pd.read_csv(f("amendments"), dtype=str).sort_values(["amended_on", "certificate_no"], kind="mergesort")
    ac = pd.read_csv(f("accreditation"), dtype=str)
    if mode == "rows":
        jobs = c.copy()
    else:
        mods = c.groupby("certificate_no").module_serial.apply(set).to_dict()
        jobs = c.drop_duplicates("certificate_no").copy()
        jobs.index = list(jobs.certificate_no)

        def collapse(js, keep):
            # certificates sharing a module are one installation
            parent = {k: k for k in js.index}
            def root(k):
                while parent[k] != k:
                    parent[k] = parent[parent[k]]
                    k = parent[k]
                return k
            owner = {}
            for k in js.index:
                for m in mods[k]:
                    if m in owner:
                        parent[root(k)] = root(owner[m])
                    else:
                        owner[m] = k
            grp = pd.Series([root(k) for k in js.index], index=js.index)
            js = js.assign(_g=grp, _l=js.lodged)
            js = js.sort_values(["_g", "_l", "certificate_no"], kind="mergesort")
            js = js.groupby("_g").tail(1) if keep == "last" else js.groupby("_g").head(1)
            return js.drop(columns=["_g", "_l"])
        if mode == "dedup_first":
            jobs = collapse(jobs, "first")
        if mode != "no_amendments":
            for r in am.itertuples():
                if r.amendment == "withdrawn":
                    jobs = jobs[jobs.certificate_no != r.certificate_no]
                elif r.amendment == "installer corrected":
                    jobs.loc[jobs.certificate_no == r.certificate_no, "installer_accreditation"] = r.new_value
        if mode == "neighbour_merge":
            jobs = jobs.drop_duplicates(["installer_accreditation", "installed", "suburb", "battery_model"])
        elif mode not in ("careful", "dedup_first"):
            jobs = collapse(jobs, "last")
    ok = ac[(ac.status == "Current") & (pd.to_datetime(ac.expires) >= pd.Timestamp("2027-12-31"))]
    good = set(ok.accreditation_no)
    if mode != "current_numbers_only":
        good |= set(ok.previous_no.dropna())
    jobs = jobs[jobs.installer_accreditation.isin(good)]
    sub, pc = _suburb_region(target)
    if mode == "by_postcode":
        reg = jobs.postcode.map(pc)
    else:
        reg = [sub[(s_.upper(), p)] for s_, p in zip(jobs.suburb, jobs.postcode)]
    jobs = jobs.assign(region=list(reg))
    return jobs.groupby("region").size().to_dict()
