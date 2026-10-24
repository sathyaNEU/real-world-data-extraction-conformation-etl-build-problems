"""The records behind the call, written from the latent world the way each system holds them: the panel's
households, units and evening download tests (local time with the offset, kbit/s, a buffered batch now and then
received twice), Tollard's plan catalogue, subscription history, node register, address-to-node table and node
utilisation filing (UTC)."""
from __future__ import annotations

import csv
import datetime as dt

import numpy as np

import common as K
import world as W

D = K.DAYS


def write_csv(path, head, rows):
    with open(path, "w", newline="", encoding="utf-8") as f:
        wr = csv.writer(f, lineterminator="\r\n")
        wr.writerow(head)
        wr.writerows(rows)


def iso(d):
    return d.isoformat() if d else ""


class Records:
    def __init__(self, seed=K.SEED, P=None):
        self.seed = seed
        self.w = w = W.World(seed, P)
        rng = self.rng = np.random.default_rng(seed * 7919 + 17)
        NH, NN = w.NH, len(w.nodes)

        # ---------------------------------------------------------------- the plant: every Tollard node in the hubs
        self.node_id = [None] * NN
        reg = []                                   # node_id, hub, class, capacity, from, to, parent
        self.splits = []                           # (parent, child ids, date) of panel nodes split before the window
        for a, (hub, _) in enumerate(K.HUBS):
            mine = [j for j in range(NN) if w.node_hub[j] == a]
            total = len(mine) + int(rng.integers(44, 58))
            nums = rng.permutation(np.arange(1, total + 1))
            for k, j in enumerate(mine):
                self.node_id[j] = "%s-%03d" % (hub, nums[k])
            for k in range(len(mine), total):
                cls = str(rng.choice(["D30-24", "D30-32", "D31"], p=[0.22, 0.48, 0.30]))
                built = dt.date(int(rng.integers(2009, 2024)), int(rng.integers(1, 13)), int(rng.integers(1, 28)))
                reg.append(["%s-%03d" % (hub, nums[k]), hub, cls, K.NODE_CLASSES[cls][1], built, None, ""])
            nxt = total + 1
            for j in mine:
                nd = w.nodes[j]
                built = dt.date(int(rng.integers(2009, 2024)), int(rng.integers(1, 13)), int(rng.integers(1, 28)))
                parent = ""
                if rng.uniform() < 0.12:              # carved out of an older node by a split before the window
                    split_on = dt.date(int(rng.integers(2023, 2027)), int(rng.integers(1, 13)), 1)
                    if split_on >= dt.date(2026, 8, 1):
                        split_on = dt.date(2026, int(rng.integers(2, 8)), 1)
                    parent = "%s-%03d" % (hub, nxt)
                    nxt += 1
                    pcls = nd["cls"] if nd["cls"] != "D31" else "D30-32"
                    reg.append([parent, hub, pcls, K.NODE_CLASSES[pcls][1], built, split_on - dt.timedelta(days=1), ""])
                    sib = "%s-%03d" % (hub, nxt)
                    nxt += 1
                    reg.append([sib, hub, nd["cls"], int(nd["cap"]), split_on, None, parent])
                    self.splits.append((parent, (self.node_id[j], sib), split_on))
                    built = split_on
                reg.append([self.node_id[j], hub, nd["cls"], int(nd["cap"]), built, None, parent])
        reg.sort(key=lambda r: (r[0][:2], int(r[0][3:])))
        self.register = reg
        self.split_child = {c: (p, on) for p, cs, on in self.splits for c in cs}

        # ---------------------------------------------------------------- service address ids, drawn as needed
        self._addr_pool = list(rng.permutation(np.arange(10000, 99000)))

        # ---------------------------------------------------------------- households, accounts and units
        hid = rng.permutation(np.arange(10100, 39900))
        self.hh_id = ["OVH-%05d" % x for x in hid[:NH]]
        acct = rng.permutation(np.arange(10 ** 7, 10 ** 8))[:NH + 200]
        self.account = ["8317-%04d-%04d" % (a // 10 ** 4, a % 10 ** 4) for a in acct[:NH]]
        self.addr = [int(self._addr_pool.pop()) for _ in range(NH)]
        self.addr_node = {a: self.node_id[w.hh_node[h]] for h, a in enumerate(self.addr)}
        self.enrolled = [K.WINDOW_START - dt.timedelta(days=int(rng.integers(30, 820))) for _ in range(NH)]
        units = rng.permutation(np.arange(201000, 239000))
        self.unit_rows = []                        # unit_id, household, model, installed, removed, reason
        self.unit_of = {}                          # unit id -> household index
        self.gap = {}                              # household -> (first day without a unit, first day of the new one)
        ui = 0
        swap = set(rng.choice(NH, 34, replace=False).tolist())
        for h in range(NH):
            model = "Whitebox 8.2" if self.enrolled[h] < dt.date(2025, 6, 1) else "Whitebox 9"
            u1 = "WB%06d" % units[ui]
            ui += 1
            self.unit_of[u1] = h
            if h in swap:
                x = int(rng.integers(3, D - 8))
                g = int(rng.integers(1, 5))
                u2 = "WB%06d" % units[ui]
                ui += 1
                self.unit_of[u2] = h
                self.gap[h] = (x, x + g)
                self.unit_rows.append([u1, self.hh_id[h], model, self.enrolled[h], K.day(x - 1), "Unit fault"])
                self.unit_rows.append([u2, self.hh_id[h], "Whitebox 9", K.day(x + g), None, ""])
            else:
                self.unit_rows.append([u1, self.hh_id[h], model, self.enrolled[h], None, ""])
        self.unit_by_hh = {}
        for u, h in self.unit_of.items():
            self.unit_by_hh.setdefault(h, []).append(u)
        # households that moved during the window: they left the panel, so they are not panel households for it
        lrng = np.random.default_rng(seed * 7919 + 61 + 1000 * K.REC_SEED)
        self.leavers = {}
        for h in lrng.choice([x for x in range(NH) if x not in self.gap], 3, replace=False):
            self.leavers[int(h)] = int(lrng.integers(20, D - 10))          # the first day without its unit
        for h, d0 in self.leavers.items():
            for row in self.unit_rows:
                if row[1] == self.hh_id[h] and row[4] is None:
                    row[4] = K.day(d0 - 1)
                    row[5] = "Household moved"
        self._late(rng, units[ui:ui + 40], hid[NH:NH + 40], acct[NH:NH + 40])
        self._withdrawn(rng, units[ui + 40:ui + 140], hid[NH + 40:NH + 140], acct[NH + 40:NH + 140])

    # ---------------------------------------------------------------------------------------------- late joiners
    def _late(self, rng, units, hid, acct):
        """24 households enrolled after the window opened: not panel households for the window, their tests in the
        extract from the day their unit went in"""
        w = self.w
        n = 24
        self.late = []
        nodes = rng.choice(len(w.nodes), n, replace=False)
        for k in range(n):
            j = int(nodes[k])
            names = {"D31": ["E100", "P300", "M600", "G1000"], "D30-32": ["E100", "P300", "M600"],
                     "D30-24": ["E100", "P300"]}[w.nodes[j]["cls"]]
            plan = str(rng.choice(names))
            on = int(rng.integers(4, 40))
            a = int(self._addr_pool.pop())
            self.addr_node[a] = self.node_id[j]
            self.late.append(dict(hh="OVH-%05d" % hid[k], acct="8317-%04d-%04d" % (acct[k] // 10 ** 4,
                                                                                   acct[k] % 10 ** 4),
                                  node=j, plan=plan, start=on, addr=a, unit="WB%06d" % units[k],
                                  inten=float(rng.choice([0.35, 0.8, 1.4])), over=float(rng.normal(1.0, 0.012))))

    def _withdrawn(self, rng, units, hid, acct):
        """households that left the panel before the window: in the panel's files, with no test in the extract"""
        self.withdrawn = []
        hubs_nodes = [r[0] for r in self.register if r[5] is None]
        for k in range(61):
            node = str(rng.choice(hubs_nodes))
            a = int(self._addr_pool.pop())
            self.addr_node[a] = node
            en = K.WINDOW_START - dt.timedelta(days=int(rng.integers(400, 900)))
            out = en + dt.timedelta(days=int(rng.integers(60, 380)))
            if out >= K.WINDOW_START:
                out = K.WINDOW_START - dt.timedelta(days=int(rng.integers(10, 90)))
            self.withdrawn.append(dict(hh="OVH-%05d" % hid[k], acct="8317-%04d-%04d" % (acct[k] // 10 ** 4,
                                                                                         acct[k] % 10 ** 4),
                                       addr=a, unit="WB%06d" % units[k], enrolled=en, left=out,
                                       plan=str(rng.choice(["E100", "P300", "M600"]))))

    # ---------------------------------------------------------------------------------------------- the tests
    def _late_tests(self):
        """the late joiners' own line use and tests, on the same nights and nodes as the panel"""
        w, P = self.w, self.w.P
        rng = np.random.default_rng(self.seed * 7919 + 29)
        sh = (W.S0 + np.arange(W.NS)) / 12.0
        sprof = W.profile(sh + 1 / 24, P["PROF"])
        out = []
        for L in self.late:
            j = L["node"]
            hub = w.node_hub[j]
            dd = w.night[:, None] * w.town[hub][:, None] * sprof[None, :]
            pa = np.clip(L["inten"] * P["BASE"] * dd ** P["GAM"], 0.01, 0.92)
            busy = np.zeros((D, W.NS), bool)
            busy[:, 0] = rng.uniform(size=D) < pa[:, 0]
            for s in range(1, W.NS):
                p = pa[:, s]
                stay = np.where(busy[:, s - 1], P["RHO"] + (1 - P["RHO"]) * p, P["RHO"] + (1 - P["RHO"]) * (1 - p))
                busy[:, s] = np.where(rng.uniform(size=D) < stay, busy[:, s - 1], ~busy[:, s - 1])
            rate = K.PLAN_DOWN[L["plan"]] * W.OVER[L["plan"]] * L["over"]
            for d in range(L["start"], D):
                for r in range(K.EXTRACT_TO - K.EXTRACT_FROM):
                    m0 = int(rng.integers(0, 45))
                    for k in range(4):
                        slot = r * 12 + (m0 + 5 * k) // 5
                        if not busy[d, slot]:
                            m = m0 + 5 * k
                            q = (K.EXTRACT_FROM - K.FILING_FROM + r) * 4 + m // 15
                            mbps = min(rate, W.avail(w.node_cap[j], w.U[j, d, q])) * rng.lognormal(0, P.get("TN", 0.035))
                            out.append((L["unit"], d, r, m, int(rng.integers(0, 60)), mbps))
                            break
        return out

    def test_rows(self):
        w = self.w
        rng = np.random.default_rng(self.seed * 7919 + 31)
        h, d, r, m, q, mbps = w.tests()
        sec = w.sec[h, d, r]
        rows = []
        for i in range(len(h)):
            hh = int(h[i])
            dd = int(d[i])
            units = self.unit_by_hh[hh]
            if hh in self.leavers and dd >= self.leavers[hh]:
                continue
            if hh in self.gap:
                x, y = self.gap[hh]
                if x <= dd < y:
                    continue
                u = units[0] if dd < x else units[1]
            else:
                u = units[0]
            rows.append((u, dd, int(r[i]), int(m[i]), int(sec[i]), float(mbps[i])))
        rows.extend(self._late_tests())
        servers = ("ndt-kel-01.ovcc.net", "ndt-kel-02.ovcc.net")
        out = []
        for u, dd, rr, mm, ss, mb in rows:
            local = dt.datetime.combine(K.day(dd), dt.time(K.EXTRACT_FROM + rr, mm, ss))
            off = K.offset_hours(local)
            kbps = int(round(mb * 1000))
            dur = 10000 + int(rng.integers(2, 48))
            out.append([u, local.strftime("%Y-%m-%d %H:%M:%S"), "%+03d:00" % off, servers[int(rng.integers(0, 2))],
                        8, dur, int(round(kbps * dur / 8.0)), kbps, local - dt.timedelta(hours=off)])
        # buffered batches received twice: one evening of a unit after its link to the collector came back
        by_unit = {}
        for i, row in enumerate(out):
            by_unit.setdefault(row[0], []).append(i)
        dup_units = rng.choice(sorted(by_unit), 14, replace=False)
        extra = []
        self.duplicated = []
        for u in dup_units:
            idx = by_unit[u]
            day0 = out[idx[int(rng.integers(0, len(idx)))]][1][:10]
            same = [i for i in idx if out[i][1][:10] == day0]
            extra.extend(list(out[i]) for i in same)
            self.duplicated.append((str(u), day0, len(same)))
        out.extend(extra)
        out.sort(key=lambda row: (row[8], row[0]))
        return (["unit_id", "test_start_local", "utc_offset", "target_server", "threads", "duration_ms",
                 "bytes_received", "throughput_kbps"], [row[:8] for row in out])

    # ---------------------------------------------------------------------------------------------- the panel
    def plan_history(self):
        """each account's plans: the plan in force from the account's connection, a migration off the withdrawn
        tiers on 1 April 2025, and the window's own changes"""
        w = self.w
        rng = np.random.default_rng(self.seed * 7919 + 37)
        hist = {}
        legacy = {"P300": "P250", "M600": "M500"}
        for h in range(w.NH):
            start = self.enrolled[h] - dt.timedelta(days=int(rng.integers(20, 1500)))
            p0 = str(w.plan_day[h, 0])
            rows = []
            if start < dt.date(2025, 4, 1) and p0 in legacy and rng.uniform() < 0.55:
                rows.append([legacy[p0], start, dt.date(2025, 3, 31)])
                rows.append([p0, dt.date(2025, 4, 1), None])
            elif rng.uniform() < 0.18:
                lower = {"P300": "E100", "M600": "P300", "G1000": "M600", "E100": "P300"}[p0]
                cut = self.enrolled[h] + dt.timedelta(days=int(rng.integers(-300, 20)))
                cut = min(cut, K.WINDOW_START - dt.timedelta(days=9))
                cut = max(cut, start + dt.timedelta(days=30))
                rows.append([lower, start, cut - dt.timedelta(days=1)])
                rows.append([p0, cut, None])
            else:
                rows.append([p0, start, None])
            for hh, a, b, on in w.changes:
                if hh == h:
                    rows[-1][2] = K.day(on) - dt.timedelta(days=1)
                    rows.append([b, K.day(on), None])
            hist[self.account[h]] = rows
        for L in self.late:
            st = K.day(L["start"]) - dt.timedelta(days=int(rng.integers(10, 900)))
            hist[L["acct"]] = [[L["plan"], st, None]]
        for X in self.withdrawn:
            st = X["enrolled"] - dt.timedelta(days=int(rng.integers(10, 400)))
            hist[X["acct"]] = [[X["plan"], st, None]]
        return hist

    def plan_on(self, rows, day):
        for p, a, b in rows:
            if a <= day and (b is None or day <= b):
                return p
        return rows[0][0]

    def household_rows(self):
        hist = self.plan_history()
        rows = []
        for h in range(self.w.NH):
            left = iso(K.day(self.leavers[h] - 1)) if h in self.leavers else ""
            rows.append([self.hh_id[h], self.account[h], str(self.addr[h]), iso(self.enrolled[h]), left,
                         self.plan_on(hist[self.account[h]], self.enrolled[h])])
        for L in self.late:
            en = K.day(L["start"])
            rows.append([L["hh"], L["acct"], str(L["addr"]), iso(en), "", L["plan"]])
        for X in self.withdrawn:
            rows.append([X["hh"], X["acct"], str(X["addr"]), iso(X["enrolled"]), iso(X["left"]),
                         self.plan_on(hist[X["acct"]], X["enrolled"])])
        rows.sort(key=lambda r: r[0])
        return (["household_id", "tollard_account", "service_address", "enrolled_on", "withdrawn_on",
                 "plan_at_enrolment"], rows)

    def unit_table(self):
        rows = [[u, hh, mdl, iso(a), iso(b), why] for u, hh, mdl, a, b, why in self.unit_rows]
        for L in self.late:
            rows.append([L["unit"], L["hh"], "Whitebox 9", iso(K.day(L["start"])), "", ""])
        for X in self.withdrawn:
            rows.append([X["unit"], X["hh"], "Whitebox 8.2", iso(X["enrolled"]), iso(X["left"]), "Household left panel"])
        rows.sort(key=lambda r: r[0])
        return (["unit_id", "household_id", "unit_model", "installed_on", "removed_on", "removal_reason"], rows)

    def subscription_rows(self):
        hist = self.plan_history()
        rows = []
        for a in sorted(hist):
            for p, f, t in hist[a]:
                rows.append([a, p, iso(f), iso(t)])
        return (["account_number", "plan_code", "effective_from", "effective_to"], rows)

    # ---------------------------------------------------------------------------------------------- Tollard
    def plan_rows(self):
        rows = [[c, n, dn, up, "%.2f" % pr, "2025-04-01", "", av] for c, n, dn, up, pr, av in (
            ("E100", "Essential 100", 100, 10, 49.99, "all nodes"),
            ("P300", "Plus 300", 300, 20, 64.99, "all nodes"),
            ("M600", "Max 600", 600, 35, 79.99, "32-channel and DOCSIS 3.1 nodes"),
            ("G1000", "Gig 1000", 1000, 35, 94.99, "DOCSIS 3.1 nodes"))]
        rows[0][5] = "2022-06-01"
        rows.append(["P250", "Plus 250", 250, 20, "59.99", "2021-03-01", "2025-03-31", "all nodes"])
        rows.append(["M500", "Max 500", 500, 25, "74.99", "2022-06-01", "2025-03-31", "32-channel and DOCSIS 3.1 nodes"])
        return (["plan_code", "plan_name", "download_mbps", "upload_mbps", "monthly_price_usd", "launched_on",
                 "withdrawn_on", "available_on"], rows)

    def register_rows(self):
        return (["node_id", "hub_code", "node_class", "ds_capacity_mbps", "in_service_from", "in_service_to",
                 "split_from"], [[r[0], r[1], r[2], r[3], iso(r[4]), iso(r[5]), r[6]] for r in self.register])

    def address_rows(self):
        """Tollard's node for each service address the Commission lists (the panel's), with effective dates"""
        rows = []
        built = {r[0]: r[4] for r in self.register}
        for a, node in self.addr_node.items():
            sid = "SA-%07d" % a
            if node in self.split_child:
                parent, on = self.split_child[node]
                rows.append([sid, parent, iso(max(built[parent], dt.date(2019, 1, 1))), iso(on - dt.timedelta(days=1))])
                rows.append([sid, node, iso(on), ""])
            else:
                rows.append([sid, node, iso(max(built[node], dt.date(2019, 1, 1))), ""])
        rows.sort(key=lambda r: (r[0], r[2]))
        return (["service_address_id", "node_id", "effective_from", "effective_to"], rows)

    def util_rows(self):
        w = self.w
        rows = []
        for j in range(len(w.nodes)):
            nid = self.node_id[j]
            for d in range(D):
                base = dt.datetime.combine(K.day(d), dt.time(K.FILING_FROM))
                for q in range(W.NQ):
                    t = K.to_utc(base + dt.timedelta(minutes=15 * q))
                    rows.append([nid, t.strftime("%Y-%m-%dT%H:%M:00Z"), "%.1f" % (100 * w.U[j, d, q])])
        rows.sort(key=lambda r: (r[1], r[0]))
        return (["node_id", "interval_start_utc", "ds_util_pct"], rows)

    # ---------------------------------------------------------------------------------------------- distractors
    def complaint_rows(self):
        """the Commission's complaints about the Franchisee, July to mid-November"""
        rng = np.random.default_rng(self.seed * 7919 + 53)
        w = self.w
        cats = ["Speed or reliability", "Outage", "Billing", "Installation or repair", "Customer service"]
        rows = []
        start = dt.date(2026, 7, 1)
        n = 0
        for d in range((dt.date(2026, 11, 20) - start).days + 1):
            day = start + dt.timedelta(days=d)
            for a, hub in enumerate(K.HUB):
                lam = 0.32 + (0.10 if day.weekday() < 5 else 0.03)
                for _ in range(rng.poisson(lam)):
                    n += 1
                    cat = rng.choice(cats, p=[0.30, 0.16, 0.27, 0.15, 0.12])
                    status = "Open" if (dt.date(2026, 11, 20) - day).days < 12 and rng.uniform() < 0.6 else \
                        str(rng.choice(["Closed", "Closed", "Closed", "Referred to franchisee"]))
                    rows.append(["C26-%05d" % (1200 + n), day.isoformat(),
                                 str(rng.choice(["Phone", "Web form", "Email", "Letter"], p=[0.45, 0.38, 0.14, 0.03])),
                                 hub, str(cat), status])
        return (["complaint_id", "received_on", "channel", "hub_code", "category", "status"], rows)

    def latency_rows(self):
        """each unit's daily round-trip summary, 5 pm to midnight"""
        rng = np.random.default_rng(self.seed * 7919 + 59)
        w = self.w
        rows = []
        base = rng.uniform(9.0, 17.0, w.NH)
        for h in range(w.NH):
            j = w.hh_node[h]
            for d in range(D):
                if h in self.gap and self.gap[h][0] <= d < self.gap[h][1]:
                    continue
                if h in self.leavers and d >= self.leavers[h]:
                    continue
                u = w.U[j, d, 4:32]
                busy = w.busy[h, d].mean()
                med = base[h] + 4.0 * u.mean() ** 3 + rng.normal(0, 0.6)
                p95 = med + 6.0 + 55.0 * busy * rng.uniform(0.6, 1.4) + 30.0 * max(0.0, u.max() - 0.8)
                loss = max(0.0, rng.normal(0.02 + 0.3 * max(0.0, u.max() - 0.85), 0.01))
                unit = self.unit_by_hh[h][0] if (h not in self.gap or d < self.gap[h][0]) else self.unit_by_hh[h][1]
                rows.append([unit, K.day(d).isoformat(), "%.1f" % med, "%.1f" % p95, "%.2f" % loss, 25200])
        rows.sort(key=lambda r: (r[1], r[0]))
        return (["unit_id", "date", "rtt_median_ms", "rtt_p95_ms", "loss_pct", "probes"], rows)
