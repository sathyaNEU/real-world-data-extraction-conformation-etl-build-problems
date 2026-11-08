"""task268's golden, computed from the shipped pack alone: each service's December 2026 latency SLI (the kept server
spans weighted hour by hour by the load balancer's request counts), its verdict against its budget, and the asks
(releases and rollbacks, customer-facing incident minutes by half, cost by half). The ladder's rungs are computed
beside the golden for the checks."""
import csv
import datetime as dt
import json
import os

import numpy as np
import pyarrow.parquet as pq
from openpyxl import load_workbook

import common as K

DEC0_NS = int((dt.datetime(2026, 12, 1) - dt.datetime(1970, 1, 1)).total_seconds()) * 10 ** 9
H = K.REVIEW_HOURS


def catalogue(target):
    wb = load_workbook(os.path.join(target, K.FILES["catalogue"]), read_only=True)
    ws = wb["Services"]
    rows = list(ws.iter_rows(values_only=True))
    head = rows[0]
    out = [dict(zip(head, r)) for r in rows[1:] if r[0]]
    return out


class Golden:
    def __init__(self, target):
        self.t = target
        self.cat = catalogue(target)
        self.by_trace = {c["Tracing service name"]: c["Service"] for c in self.cat}
        self.by_tg2 = {c["Load balancer target group (from 1 Jul 2026)"]: c["Service"] for c in self.cat}
        slo = self.slo_table()
        self.thr = {s: slo[s][0] for s in slo}
        self.bud = {s: slo[s][1] for s in slo}

    def slo_table(self):
        from docx import Document
        d = Document(os.path.join(self.t, K.FILES["slo"]))
        tab = d.tables[0]
        out = {}
        for row in tab.rows[1:]:
            c = [x.text for x in row.cells]
            out[c[0]] = (float(c[2].replace(",", "")), float(c[3].rstrip("%")))
        return out

    # ------------------------------------------------------------ the main call
    def spans(self):
        """The kept server spans that started in December, re-sent rows and health probes removed, each with the
        service and start hour of the request that began its trace (None where that span is not in the export)."""
        tb = pq.read_table(os.path.join(self.t, K.FILES["spans"]),
                           columns=["trace_id", "span_id", "parent_span_id", "service_name", "span_name", "span_kind",
                                    "start_time_unix_nano", "end_time_unix_nano"]).to_pydict()
        seen = set()
        rows = []
        for tid, sid, pid, svc, name, kind, t0, t1 in zip(tb["trace_id"], tb["span_id"], tb["parent_span_id"],
                                                          tb["service_name"], tb["span_name"], tb["span_kind"],
                                                          tb["start_time_unix_nano"], tb["end_time_unix_nano"]):
            if sid in seen or name == "GET /healthz":
                continue
            seen.add(sid)
            rows.append((tid, sid, pid, self.by_trace[svc], kind, (t0 - DEC0_NS) // (3600 * 10 ** 9),
                         (t1 - t0) / 1e6))
        root = {}
        for tid, sid, pid, svc, kind, h, ms in rows:
            if kind == "SPAN_KIND_SERVER" and pid == "":
                root[tid] = (svc, int(h))
        self.n_client = sum(1 for x in rows if x[4] == "SPAN_KIND_CLIENT")
        self.ids = {x[1] for x in rows}
        self.parent_of = {x[1]: x[2] for x in rows}
        out = []
        for tid, sid, pid, svc, kind, h, ms in rows:
            if kind != "SPAN_KIND_SERVER" or not 0 <= h < H:
                continue
            out.append((svc, int(h), ms, root.get(tid), pid))
        return out

    def counts(self):
        N = {s: np.zeros(H, dtype=np.int64) for s in K.SVC}
        E = {s: np.zeros(H, dtype=np.int64) for s in K.SVC}
        with open(os.path.join(self.t, K.FILES["lb_h2"])) as fh:
            for row in csv.DictReader(fh):
                t = dt.datetime.strptime(row["TimePeriodStart"], "%Y-%m-%dT%H:%M:%SZ")
                if t < dt.datetime(2026, 12, 1):
                    continue
                h = int((t - dt.datetime(2026, 12, 1)).total_seconds() // 3600)
                s = self.by_tg2[row["TargetGroupName"]]
                N[s][h] = int(row["RequestCount"])
                E[s][h] = int(row["HTTPCode_Target_5XX_Count"])
        return N, E

    def main(self):
        sp = self.spans()
        N, E = self.counts()
        hod, day = np.arange(H) % 24, np.arange(H) // 24
        # each edge service's kept share of its requests, hour by hour: its kept root spans over the balancer's count
        Kroot = {e: np.zeros(H, dtype=np.int64) for e in K.EDGE}
        for svc, h, ms, rt, pid in sp:
            if pid == "":
                Kroot[svc][h] += 1
        for e in K.EDGE:
            assert not ((Kroot[e] == 0) & (N[e] > 0)).any(), e
        out = {}
        for s in K.SVC:
            mine = [x for x in sp if x[0] == s]
            h_own = np.array([x[1] for x in mine], dtype=np.int64)
            slow = np.array([x[2] > self.thr[s] for x in mine], dtype=float)
            Kh = np.bincount(h_own, minlength=H).astype(float)
            Sh = np.bincount(h_own, weights=slow, minlength=H)
            w_root, w_ownh, orphan = [], [], []
            for svc, h, ms, rt, pid in mine:
                if rt is None:                         # the request that began the trace is not in the export
                    orphan.append(True)
                    w_root.append(N[s][h] / max(Kh[h], 1))
                    w_ownh.append(N[s][h] / max(Kh[h], 1))
                else:
                    e, he = rt
                    orphan.append(False)
                    w_root.append(N[e][he] / Kroot[e][he])
                    w_ownh.append(N[e][h] / max(Kroot[e][h], 1))
            w_root, w_ownh, orphan = np.array(w_root), np.array(w_ownh), np.array(orphan, dtype=bool)
            Ns = float(N[s].sum())
            sli = 100 * (w_root * slow).sum() / Ns
            num_h = np.bincount(h_own, weights=w_root * slow, minlength=H)
            den_h = np.bincount(h_own, weights=w_root, minlength=H)

            def strat(g):
                Ng, Kg, Sg = np.bincount(g, N[s].astype(float)), np.bincount(g, Kh), np.bincount(g, Sh)
                return 100 * (np.where(Kg > 0, Ng / np.maximum(Kg, 1), 0) * Sg).sum() / Ns
            w_drop = np.where(orphan, 0.0, w_root)
            out[s] = {"sli": sli, "sli1": K.r1(sli), "budget": self.bud[s], "threshold": self.thr[s],
                      "over": K.r1(sli) > self.bud[s], "requests": int(Ns), "kept": int(Kh.sum()),
                      "kept_slow": int(Sh.sum()), "orphans": int(orphan.sum()),
                      "weighted_requests": float(w_root.sum()),
                      "hajek": 100 * (w_root * slow).sum() / w_root.sum(),
                      "calibrated": 100 * np.where(den_h > 0, N[s] * num_h / np.maximum(den_h, 1e-12), 0).sum() / Ns,
                      "own_hour": 100 * (w_ownh * slow).sum() / Ns,
                      "orphans_dropped": 100 * (w_drop * slow).sum() / Ns,
                      "unweighted": 100 * Sh.sum() / Kh.sum(), "by_day": strat(day), "by_hour_of_day": strat(hod),
                      "by_service_hour": strat(np.arange(H)),
                      "lb_5xx_share": 100 * E[s].sum() / Ns}
            # the root mix of the service's kept spans against the mix its weights give
            mix_k, mix_w = {}, {}
            for (svc, h, ms, rt, pid), wv in zip(mine, w_root):
                key = rt[0] if rt else None
                mix_k[key] = mix_k.get(key, 0) + 1
                mix_w[key] = mix_w.get(key, 0.0) + wv
            out[s]["root_mix_kept"] = {k: v / len(mine) for k, v in mix_k.items()}
            out[s]["root_mix_weighted"] = {k: v / w_root.sum() for k, v in mix_w.items()}
        return out

    # ------------------------------------------------------------ ask A: releases and rollbacks
    def deploys(self):
        """Production's changes in order: the pipeline's successful production deploys up to the cluster's build on 14
        April, then prd-lis-2's rollout history, every change whoever made it; images are named by commit hash, which
        the pipeline's records map to versions. A release is an image reaching production for the first time, a
        rollback a change to an image first released before the running one."""
        d = json.load(open(os.path.join(self.t, K.FILES["deploys"])))["deployments"]
        hist = list(csv.DictReader(open(os.path.join(self.t, K.FILES["rollouts"]))))
        start = {}
        for h in hist:
            if h["revision"] == "1":
                start[h["deployment"]] = dt.datetime.strptime(h["changed_at_utc"], "%Y-%m-%d %H:%M:%S")
        seq = {}
        for x in d:
            if x["environment"] != "production" or x["outcome"] != "succeeded":
                continue
            t = dt.datetime.strptime(x["started_at"], "%Y-%m-%dT%H:%M:%SZ")
            if t < start[x["service"]]:
                seq.setdefault(x["service"], []).append((t, x["commit"][:7]))
        for h in hist:
            sha = h["image"].rsplit(":", 1)[1]
            t = dt.datetime.strptime(h["changed_at_utc"], "%Y-%m-%d %H:%M:%S")
            seq.setdefault(h["deployment"], []).append((t, sha if h["revision"] != "1" else None))
        out = {}
        for name, ev in seq.items():
            ev.sort(key=lambda e: e[0])
            first, running, rel, roll = {}, None, 0, 0
            for t, sha in ev:
                if sha is None:                      # the cutover revision: the image already running, no change
                    continue
                if sha not in first:
                    first[sha] = t
                    rel += 1
                elif running is not None and sha != running and first[sha] < first[running]:
                    roll += 1
                running = sha
            out[self.by_trace[name]] = {"releases": rel, "rollbacks": roll}
        return out

    # ------------------------------------------------------------ ask B: cost by half
    def costs(self):
        rate = {}
        with open(os.path.join(self.t, K.FILES["invoices"])) as fh:
            for row in csv.DictReader(fh):
                rate[row["invoice_id"]] = float(row["usd_eur_rate"])
        res = {}
        with open(os.path.join(self.t, K.FILES["resources"])) as fh:
            for row in csv.DictReader(fh):
                res[row["resource_id"]] = row
        succ = {row["replaces"]: rid for rid, row in res.items() if row["replaces"]}
        tag_svc = {c["Cost tag (service=)"]: c["Service"] for c in self.cat}

        def service_of(rid, tags):
            for part in tags.split(";"):
                if part.startswith("service="):
                    return tag_svc[part.split("=", 1)[1]]
            seen = rid
            while seen in succ:                       # a replaced resource ran for its replacement's service
                seen = succ[seen]
                for part in res[seen]["tags_now"].split(";"):
                    if part.startswith("service="):
                        return tag_svc[part.split("=", 1)[1]]
            return None
        out = {s: [0.0, 0.0] for s in K.SVC}
        with open(os.path.join(self.t, K.FILES["billing"])) as fh:
            for row in csv.DictReader(fh):
                if row["line_type"] == "tax":
                    continue
                s = service_of(row["resource_id"], row["resource_tags"])
                if s is None:
                    continue
                eur = float(row["cost"]) * (rate[row["invoice_id"]] if row["currency"] == "USD" else 1.0)
                half = 0 if row["usage_date"] < "2026-07-01" else 1
                out[s][half] += eur
        return {s: [round(v[0], 2), round(v[1], 2)] for s, v in out.items()}

    # ------------------------------------------------------------ ask C: customer-facing incident minutes by half
    def incidents(self):
        import asks as A
        st = json.load(open(os.path.join(self.t, K.FILES["status"])))

        def utc(local):
            t = dt.datetime.strptime(local, "%Y-%m-%d %H:%M")
            for off in (1, 0):
                u = t - dt.timedelta(hours=off)
                if A.lisbon_offset(u) == off:
                    return u
            return t
        posts = [{"components": set(p["components"]), "created": utc(p["created_at"])} for p in st["incidents"]]
        ops = {}
        for c in st["component_status_changes"]:
            if c["status"] == "operational":
                ops.setdefault(c["component"], []).append(utc(c["at"]))
        for v in ops.values():
            v.sort()
        named = {}
        for row in csv.DictReader(open(os.path.join(self.t, K.FILES["timeline"]))):
            if row["event"] == "service added":
                named[(row["incident_id"], row["detail"])] = dt.datetime.strptime(row["at_utc"], "%Y-%m-%d %H:%M:%S")
        comp = {c["Service"]: c["Status page component"] for c in self.cat}
        iv = {s: [] for s in K.SVC}
        for row in csv.DictReader(open(os.path.join(self.t, K.FILES["incidents"]))):
            decl = dt.datetime.strptime(row["declared_at_utc"], "%Y-%m-%d %H:%M:%S")
            names = row["services"].split(";")
            # the post for this incident: on a component of a service it named, opened in the minutes after it was
            # declared
            match = [p for p in posts if p["components"] & {comp[self.by_trace[x]] for x in names}
                     and dt.timedelta(0) <= p["created"] - decl.replace(second=0) <= dt.timedelta(minutes=15)]
            if not match:
                continue
            assert len(match) == 1
            p = match[0]
            end = max(min(t for t in ops[c] if t > p["created"]) for c in p["components"])
            for x in names:
                a_ = max(decl, named[(row["incident_id"], x)])
                if a_ < end:
                    iv[self.by_trace[x]].append((a_, end))
        h1_end = dt.datetime(2026, 6, 30, 23, 0)            # 1 July 00:00 Lisbon
        res = {}
        for s, lst in iv.items():
            merged = []
            for a_, b_ in sorted(lst):
                if merged and a_ <= merged[-1][1]:
                    merged[-1][1] = max(merged[-1][1], b_)
                else:
                    merged.append([a_, b_])
            m = [0.0, 0.0]
            for a_, b_ in merged:
                for i, (lo, hi) in enumerate(((dt.datetime(2026, 1, 1), h1_end), (h1_end, dt.datetime(2027, 1, 1)))):
                    lo_, hi_ = max(a_, lo), min(b_, hi)
                    if hi_ > lo_:
                        m[i] += (hi_ - lo_).total_seconds() / 60
            res[s] = m
        return res

    def run(self):
        main = self.main()
        over = [s for s in K.SVC if main[s]["over"]]
        return {"main": main, "over": over, "deploys": self.deploys(), "costs": self.costs(),
                "incidents": self.incidents()}
