"""Readers for the shipped files: everything the analysis computes is read back from the pack, never from the world."""
from __future__ import annotations

import csv
import datetime as dt
import os

import numpy as np

import common as K

T0 = dt.datetime.combine(K.WINDOW_START, dt.time(0)) + dt.timedelta(hours=4)   # midnight local on day 0, in UTC


def path(target, key):
    return os.path.join(target, K.FILES[key])


def rows(target, key):
    with open(path(target, key), newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def date(s):
    return dt.date.fromisoformat(s) if s else None


def qh_index(utc):
    """quarter-hours since midnight local time on the window's first day (in UTC terms)"""
    return int((utc - T0).total_seconds() // 900)


class Pack:
    """the panel and Tollard records joined the way the Schedule defines them"""

    def __init__(self, target, dedupe=True, local_offsets=True, plan_source="history", panel="schedule",
                 holidays=True, by_unit=False):
        self.target = target
        plans = {r["plan_code"]: float(r["download_mbps"]) for r in rows(target, "plans")}
        self.plan_mbps = plans
        reg = rows(target, "nodes")
        self.node_hub = {r["node_id"]: r["hub_code"] for r in reg}
        # address to node, with effective dates
        self.addr_nodes = {}
        for r in rows(target, "addr"):
            self.addr_nodes.setdefault(r["service_address_id"], []).append(
                (date(r["effective_from"]), date(r["effective_to"]), r["node_id"]))
        subs = {}
        for r in rows(target, "subs"):
            subs.setdefault(r["account_number"], []).append(
                (date(r["effective_from"]), date(r["effective_to"]), r["plan_code"]))
        hh = rows(target, "households")
        units = rows(target, "units")
        if by_unit:
            first = {}
            for u in sorted(units, key=lambda r: r["installed_on"]):
                first.setdefault(u["household_id"], u["unit_id"])
            extra = []
            for u in units:
                if u["unit_id"] != first.get(u["household_id"]):
                    base = next(r for r in hh if r["household_id"] == u["household_id"])
                    extra.append(dict(base, household_id=u["unit_id"]))
            hh = hh + extra
        self.households = {}
        for r in hh:
            en, out = date(r["enrolled_on"]), date(r["withdrawn_on"])
            if panel == "schedule":
                # a panel household for the window: enrolled before the window opened and still in the panel
                if en >= K.WINDOW_START or out is not None:
                    continue
            elif panel == "all_with_tests":
                if out is not None and out < K.WINDOW_START:
                    continue
            self.households[r["household_id"]] = dict(account=r["tollard_account"],
                                                      addr="SA-%07d" % int(r["service_address"]),
                                                      enrol_plan=r["plan_at_enrolment"])
        self.hh_list = sorted(self.households)
        self.hh_index = {h: i for i, h in enumerate(self.hh_list)}
        NHp = len(self.hh_list)
        # each household's node, hub and plan on each day of the window
        self.node_day = np.empty((NHp, K.DAYS), dtype=object)
        self.down_day = np.zeros((NHp, K.DAYS))
        self.hub = []
        for i, h in enumerate(self.hh_list):
            H = self.households[h]
            for d in range(K.DAYS):
                day = K.day(d)
                node = None
                for a, b, n in self.addr_nodes[H["addr"]]:
                    if a <= day and (b is None or day <= b):
                        node = n
                self.node_day[i, d] = node
                if plan_source == "history":
                    plan = None
                    for a, b, p in subs[H["account"]]:
                        if a <= day and (b is None or day <= b):
                            plan = p
                else:
                    plan = H["enrol_plan"]
                self.down_day[i, d] = plans[plan]
            hubs = {self.node_hub[n] for n in self.node_day[i]}
            assert len(hubs) == 1, (h, hubs)
            self.hub.append(hubs.pop())
        self.hub = np.array(self.hub)
        # utilisation by node and quarter-hour
        self.util = {}
        for r in rows(target, "util"):
            t = dt.datetime.strptime(r["interval_start_utc"], "%Y-%m-%dT%H:%M:00Z")
            self.util.setdefault(r["node_id"], {})[qh_index(t)] = float(r["ds_util_pct"]) / 100.0
        # the tests: unit to household, local time to UTC, kbit/s to Mbit/s
        unit_hh = {r["unit_id"]: r["household_id"] for r in units}
        if by_unit:
            for u in units:
                if u["unit_id"] in self.hh_index:
                    unit_hh[u["unit_id"]] = u["unit_id"]
        seen = set()
        H, Dd, Q, MB, LOCALH = [], [], [], [], []
        self.n_dupes = 0
        for r in rows(target, "tests"):
            key = (r["unit_id"], r["test_start_local"], r["bytes_received"])
            if key in seen:
                self.n_dupes += 1
                if dedupe:
                    continue
            seen.add(key)
            hid = unit_hh[r["unit_id"]]
            if hid not in self.hh_index:
                continue
            local = dt.datetime.strptime(r["test_start_local"], "%Y-%m-%d %H:%M:%S")
            off = int(r["utc_offset"][:3]) if local_offsets else -4
            utc = local - dt.timedelta(hours=off)
            H.append(self.hh_index[hid])
            Dd.append((local.date() - K.WINDOW_START).days)
            Q.append(qh_index(utc))
            LOCALH.append(local.hour * 4 + local.minute // 15)
            MB.append(int(r["throughput_kbps"]) / 1000.0)
        self.t_hh = np.array(H)
        self.t_day = np.array(Dd)
        self.t_q = np.array(Q)
        self.t_localq = np.array(LOCALH)
        self.t_mbps = np.array(MB)
        wk = np.array([K.day(d).weekday() < 5 and (holidays or K.day(d) not in K.HOLIDAYS) for d in range(K.DAYS)])
        self.weekday = wk
        pk_lo, pk_hi = K.PEAK_FROM * 4, K.PEAK_TO * 4
        self.t_peak = wk[self.t_day] & (self.t_localq >= pk_lo) & (self.t_localq < pk_hi)
        self.t_ratio = self.t_mbps / self.down_day[self.t_hh, self.t_day]
        self.t_below = self.t_ratio < K.STANDARD
        self.t_load = np.array([self.util[self.node_day[h, d]][q] for h, d, q in zip(self.t_hh, self.t_day, self.t_q)])
        # every weekday evening peak quarter-hour of the window, per household: its node's load and its plan
        self.peak_days = np.where(wk)[0]
        qs = []
        for d in self.peak_days:
            base = dt.datetime.combine(K.day(int(d)), dt.time(K.PEAK_FROM))
            for k in range((K.PEAK_TO - K.PEAK_FROM) * 4):
                local = base + dt.timedelta(minutes=15 * k)
                off = K.offset_hours(local) if local_offsets else -4
                qs.append((int(d), qh_index(local - dt.timedelta(hours=off))))
        self.peak_q = qs
        self.q_load = np.array([[self.util[self.node_day[i, d]][q] for d, q in qs] for i in range(NHp)])
        self.q_day = np.array([d for d, q in qs])
