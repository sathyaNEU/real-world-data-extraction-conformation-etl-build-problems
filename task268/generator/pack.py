"""Write task268's evidence pack: the tracing store's December span export, the load balancer's two 2026 request
exports, the deployment log, the cloud billing lines, invoices and resource inventory, the incident export and the
status page history; docs.py writes the standard, the catalogue, the readme and the two context files."""
import csv
import datetime as dt
import json
import os

import numpy as np
import pyarrow as pa
import pyarrow.parquet as pq

import asks as A
import common as K
import world as W

EPOCH = dt.datetime(1970, 1, 1)
DEC0_UTC = dt.datetime(2026, 12, 1)


def _ns(t):
    return int((t - EPOCH).total_seconds()) * 10 ** 9


def _hex(r, n):
    return "".join("%02x" % b for b in r.integers(0, 256, n // 2, dtype=np.uint8))


# the operations each edge service's own spans carry (name, share), and the internal operations by caller
EDGE_OPS = {
    "journey-search": [("GET /v2/journeys/search", 0.86), ("GET /v2/journeys/{id}", 0.14)],
    "places": [("GET /places/autocomplete", 0.93), ("GET /places/{id}", 0.07)],
    "seat-map": [("GET /seatmaps/{tripId}", 1.0)],
    "booking": [("POST /bookings", 1.0)],
    "accounts": [("POST /auth/token", 0.58), ("GET /me", 0.42)],
    "tickets": [("GET /tickets/{ref}/pdf", 0.64), ("GET /tickets/{ref}", 0.36)],
}
INT_OPS = {("fares", "quote"): ("POST", "/fares/quote"),
           ("partner-gateway", "availability"): ("POST", "/operators/{code}/availability"),
           ("partner-gateway", "seats"): ("GET", "/operators/{code}/seats/{tripId}"),
           ("partner-gateway", "reserve"): ("POST", "/operators/{code}/reservations"),
           ("payments", "authorise"): ("POST", "/payments/authorise"),
           ("notifications", "email"): ("POST", "/messages/email")}


class PodPool:
    """Each service's pods through December: as many as its hourly load needs between its autoscaling bounds, named
    for the replica set of the deployment revision running (a new one at every revision in the rollout history)."""

    def __init__(self, w):
        self.r = np.random.default_rng(K.SEED + 414)
        _, hist, _ = A.deployments()
        self.revs = {}
        for s in K.SVC:
            hs = sorted(h["changed_at"] for h in hist if h["deployment"] == K.TRACE_NAME[s])
            before = [t for t in hs if t < DEC0_UTC]
            during = [t for t in hs if DEC0_UTC <= t]
            starts = before[-1:] + during
            self.revs[s] = [((t - DEC0_UTC).total_seconds(), _hex(self.r, 10)[:10]) for t in starts]
        self.n = {}
        for s in K.SVC:
            lo, hi, per = K.AUTOSCALE[s]
            N = w.N[s][W.DEC0:W.DEC0 + K.REVIEW_HOURS]
            self.n[s] = np.clip(np.ceil(N / per), lo, hi).astype(int)
        self.suffix = {}

    def pick(self, svc, t0):
        rs = [h for t, h in self.revs[svc] if t <= t0][-1]
        k = int(self.n[svc][min(max(int(t0 // 3600), 0), K.REVIEW_HOURS - 1)])
        i = int(self.r.integers(0, k))
        key = (svc, rs, i)
        if key not in self.suffix:
            self.suffix[key] = "".join(self.r.choice(list("bcdfghjklmnpqrstvwxz2456789"), 5))
        return "%s-%s-%s" % (K.TRACE_NAME[svc], rs, self.suffix[key])

    def peak(self, svc):
        return int(self.n[svc].max())


def span_table(w):
    """The kept spans that started in December (UTC), the load balancer's kept health probes and the exporter's
    re-sent batches, in export order."""
    r = np.random.default_rng(K.SEED + 404)
    sp = w.sp
    keep = (sp["t0"] >= 0) & (sp["t0"] < K.REVIEW_HOURS * 3600)
    idx = np.nonzero(keep)[0]
    pool = PodPool(w)
    tr_hex = {}
    sid_hex = {}

    def tid_of(t):
        if t not in tr_hex:
            tr_hex[t] = _hex(r, 32)
        return tr_hex[t]

    def sid_of(i):
        if i not in sid_hex:
            sid_hex[i] = _hex(r, 16)
        return sid_hex[i]

    cols = {k: [] for k in ("trace_id", "span_id", "parent_span_id", "service_name", "span_name", "span_kind",
                             "start_time_unix_nano", "end_time_unix_nano", "status_code", "http_status_code",
                             "host_name")}
    base_ns = _ns(DEC0_UTC)
    pod_of = {}
    for i in idx:
        svc, op, kind, t0, ms, code = (str(sp["svc"][i]), str(sp["op"][i]), str(sp["kind"][i]), float(sp["t0"][i]),
                                       float(sp["ms"][i]), int(sp["code"][i]))
        tr = int(sp["trace"][i])
        if kind == "SERVER" and op == "own":
            names, shares = zip(*EDGE_OPS[svc])
            name = names[int(r.choice(len(names), p=shares))]
            if code == 200 and name.startswith("GET") and ms < K.THRESHOLD[svc] / 3 and r.random() < 0.004:
                code = 404
        elif kind == "SERVER":
            meth, path = INT_OPS[(svc, op)]
            name = meth + " " + path
        else:
            callee, cop = op.split(":")
            meth, path = INT_OPS[(callee, cop)]
            name = "%s %s %s" % (meth, K.TRACE_NAME[callee], path)
        # a trace's spans in one service come from one pod
        pk = (tr, svc)
        if pk not in pod_of:
            pod_of[pk] = pool.pick(svc, t0)
        par = int(sp["parent"][i])
        cols["trace_id"].append(tid_of(tr))
        cols["span_id"].append(sid_of(int(sp["sid"][i])))
        cols["parent_span_id"].append("" if par < 0 else sid_of(par))
        cols["service_name"].append(K.TRACE_NAME[svc])
        cols["span_name"].append(name)
        cols["span_kind"].append("SPAN_KIND_" + kind)
        s0 = base_ns + int(round(t0 * 1e9))
        cols["start_time_unix_nano"].append(s0)
        cols["end_time_unix_nano"].append(s0 + max(1000, int(round(ms * 1e6))))
        cols["status_code"].append("STATUS_CODE_ERROR" if code >= 500 else "STATUS_CODE_UNSET")
        cols["http_status_code"].append(code)
        cols["host_name"].append(pod_of[pk])
    # the load balancer probes /healthz on every pod every 15 seconds; the store keeps about one probe in 720
    for svc in K.SVC:
        for h in range(K.REVIEW_HOURS):
            for _ in range(int(r.poisson(2))):
                t0 = h * 3600 + float(r.uniform(0, 3599))
                s0 = base_ns + int(round(t0 * 1e9))
                cols["trace_id"].append(_hex(r, 32))
                cols["span_id"].append(_hex(r, 16))
                cols["parent_span_id"].append("")
                cols["service_name"].append(K.TRACE_NAME[svc])
                cols["span_name"].append("GET /healthz")
                cols["span_kind"].append("SPAN_KIND_SERVER")
                cols["start_time_unix_nano"].append(s0)
                cols["end_time_unix_nano"].append(s0 + int(r.uniform(0.6, 3.2) * 1e6))
                cols["status_code"].append("STATUS_CODE_UNSET")
                cols["http_status_code"].append(200)
                cols["host_name"].append(pool.pick(svc, t0))
    n = len(cols["span_id"])
    order = np.argsort(np.array(cols["start_time_unix_nano"]), kind="stable")
    # the exporter re-sends about one batch in three hundred: those rows appear twice, identical
    dup = r.random(n) < 0.003
    out_idx = []
    for i in order:
        out_idx.append(i)
        if dup[i]:
            out_idx.append(i)
    return {k: [v[i] for i in out_idx] for k, v in cols.items()}


def write_spans(path, w):
    c = span_table(w)
    table = pa.table({
        "trace_id": pa.array(c["trace_id"], pa.string()),
        "span_id": pa.array(c["span_id"], pa.string()),
        "parent_span_id": pa.array(c["parent_span_id"], pa.string()),
        "service_name": pa.array(c["service_name"], pa.string()),
        "span_name": pa.array(c["span_name"], pa.string()),
        "span_kind": pa.array(c["span_kind"], pa.string()),
        "start_time_unix_nano": pa.array(c["start_time_unix_nano"], pa.int64()),
        "end_time_unix_nano": pa.array(c["end_time_unix_nano"], pa.int64()),
        "status_code": pa.array(c["status_code"], pa.string()),
        "http_status_code": pa.array(c["http_status_code"], pa.int32()),
        "host_name": pa.array(c["host_name"], pa.string()),
    })
    pq.write_table(table, path, compression="zstd", row_group_size=131072, use_dictionary=True,
                   store_schema=False, write_statistics=True)
    _drop_created_by(path)
    return table.num_rows


def write_lb(out, w):
    """H1: the old billing tool's export (hour, target group, requests, processed GB); H2: the FinOps metrics export
    from 1 July (ISO hours, target group names after the July rename, request and 5xx counts, bytes and LCUs)."""
    r = np.random.default_rng(K.SEED + 505)
    p1 = os.path.join(out, K.FILES["lb_h1"])
    p2 = os.path.join(out, K.FILES["lb_h2"])
    size_kb = {"journey-search": 14.2, "fares": 3.1, "places": 1.4, "seat-map": 22.5, "booking": 6.8, "payments": 2.9,
               "tickets": 61.0, "accounts": 2.2, "partner-gateway": 9.4, "notifications": 4.0}
    h1, h2 = [], []
    for hidx in range(W.HOURS_YEAR):
        t = dt.datetime(2026, 1, 1) + dt.timedelta(hours=hidx)
        for svc in K.SVC:
            n = int(w.N[svc][hidx])
            gb = n * size_kb[svc] * r.uniform(0.9, 1.1) / 1024 / 1024
            if t < dt.datetime(2026, 7, 1):
                h1.append([t.strftime("%Y-%m-%d %H:%M"), K.TG_H1[svc], n, "%.3f" % gb])
            else:
                lcu = max(n / 25.0 / 3600 * 1.0, gb / 1.0) * 1.0
                h2.append([t.strftime("%Y-%m-%dT%H:%M:%SZ"), K.TG_H2[svc], n, int(w.E[svc][hidx]),
                           int(round(gb * 1024 ** 3)), "%.4f" % lcu])
    with open(p1, "w", newline="") as fh:
        wr = csv.writer(fh, lineterminator="\r\n")
        wr.writerow(["hour_utc", "target_group", "requests", "processed_gb"])
        wr.writerows(h1)
    with open(p2, "w", newline="") as fh:
        wr = csv.writer(fh, lineterminator="\n")
        wr.writerow(["TimePeriodStart", "TargetGroupName", "RequestCount", "HTTPCode_Target_5XX_Count", "ProcessedBytes",
                     "ConsumedLCUs"])
        wr.writerows(h2)
    return len(h1), len(h2)


def _iso(t):
    return t.strftime("%Y-%m-%dT%H:%M:%SZ")


def write_asks(out):
    rows, hist, dtruth = A.deployments()
    with open(os.path.join(out, K.FILES["deploys"]), "w") as fh:
        json.dump({"exported_at": "2027-01-04T08:12:44Z", "source": "Rotalinha delivery pipeline",
                   "deployments": [{"deployment_id": x["deployment_id"], "service": x["service"],
                                    "environment": x["environment"], "version": x["version"], "commit": x["commit"],
                                    "started_at": _iso(x["started_at"]), "finished_at": _iso(x["finished_at"]),
                                    "outcome": x["outcome"], "triggered_by": x["triggered_by"]} for x in rows]},
                  fh, indent=1)
        fh.write("\n")
    with open(os.path.join(out, K.FILES["rollouts"]), "w", newline="") as fh:
        wr = csv.writer(fh, lineterminator="\n")
        wr.writerow(["deployment", "revision", "image", "changed_at_utc", "changed_by"])
        for x in hist:
            wr.writerow([x["deployment"], x["revision"], x["image"], x["changed_at"].strftime("%Y-%m-%d %H:%M:%S"),
                         x["changed_by"]])
    lines, invoices, resources, btruth, rate = A.billing()
    with open(os.path.join(out, K.FILES["billing"]), "w", newline="") as fh:
        wr = csv.writer(fh, lineterminator="\n")
        wr.writerow(["usage_date", "invoice_id", "resource_id", "resource_tags", "product", "line_type", "currency",
                     "cost", "description"])
        for x in lines:
            wr.writerow([x["usage_date"].isoformat(), x["invoice_id"], x["resource_id"], x["resource_tags"],
                         x["product"], x["line_type"], x["currency"], "%.2f" % x["cost"], x["description"]])
    with open(os.path.join(out, K.FILES["invoices"]), "w", newline="") as fh:
        wr = csv.writer(fh, lineterminator="\n")
        wr.writerow(["invoice_id", "billing_period", "issued_on", "invoice_currency", "usd_eur_rate"])
        for x in invoices:
            wr.writerow([x["invoice_id"], x["billing_period"], x["issued_on"].isoformat(), x["currency"],
                         "%.4f" % x["usd_eur_rate"]])
    with open(os.path.join(out, K.FILES["resources"]), "w", newline="") as fh:
        wr = csv.writer(fh, lineterminator="\n")
        wr.writerow(["resource_id", "kind", "created", "deleted", "replaces", "tags_now"])
        for x in resources:
            wr.writerow([x["resource_id"], x["kind"], x["created"].isoformat(),
                         x["deleted"].isoformat() if x["deleted"] else "", x["replaces"], x["tags"]])
    inc, posts, changes, timeline, itruth = A.incidents()
    with open(os.path.join(out, K.FILES["timeline"]), "w", newline="") as fh:
        wr = csv.writer(fh, lineterminator="\n")
        wr.writerow(["incident_id", "at_utc", "event", "detail"])
        for iid, at, ev, det in timeline:
            wr.writerow([iid, at.strftime("%Y-%m-%d %H:%M:%S"), ev, det])
    with open(os.path.join(out, K.FILES["incidents"]), "w", newline="") as fh:
        wr = csv.writer(fh, lineterminator="\n")
        wr.writerow(["incident_id", "declared_at_utc", "resolved_at_utc", "severity", "services", "title",
                     "commander"])
        for x in inc:
            wr.writerow([x["incident_id"], x["declared_at"].strftime("%Y-%m-%d %H:%M:%S"),
                         x["resolved_at"].strftime("%Y-%m-%d %H:%M:%S"), x["severity"], x["services"], x["title"],
                         x["commander"]])
    with open(os.path.join(out, K.FILES["status"]), "w") as fh:
        json.dump({"page": "status.rotalinha.pt", "timezone": "Europe/Lisbon",
                   "incidents": [{"id": p["post_id"], "name": p["name"], "components": p["components"],
                                  "created_at": p["created_local"].strftime("%Y-%m-%d %H:%M"),
                                  "resolved_at": p["resolved_local"].strftime("%Y-%m-%d %H:%M")} for p in posts],
                   "component_status_changes": [{"component": c["component"], "status": c["status"],
                                                 "at": c["at_local"].strftime("%Y-%m-%d %H:%M")} for c in changes]},
                  fh, indent=1)
        fh.write("\n")
    return {"deploys": dtruth, "billing": btruth, "incidents": itruth, "rate": rate}


def write_pack(out, w=None):
    import docs as D
    w = w or W.World()
    n = {"spans": write_spans(os.path.join(out, K.FILES["spans"]), w)}
    n["lb_h1"], n["lb_h2"] = write_lb(out, w)
    truths = write_asks(out)
    D.write_docs(out, w)
    return w, n, truths


# ------------------------------------------------------------------ parquet footer without a writer name
def _varint(b, i):
    v = s = 0
    while True:
        c = b[i]; i += 1
        v |= (c & 0x7F) << s; s += 7
        if not c & 0x80:
            return v, i


def _skip(b, i, t):
    """Skip one compact-protocol thrift value of type t starting at b[i]."""
    if t in (1, 2):
        return i
    if t == 3:
        return i + 1
    if t in (4, 5, 6):
        return _varint(b, i)[1]
    if t == 7:
        return i + 8
    if t == 8:
        n, i = _varint(b, i)
        return i + n
    if t in (9, 10):
        h = b[i]; i += 1
        n, et = h >> 4, h & 0x0F
        if n == 15:
            n, i = _varint(b, i)
        for _ in range(n):
            i = i + 1 if et in (1, 2) else _skip(b, i, et)
        return i
    if t == 11:
        n, i = _varint(b, i)
        if n:
            kv = b[i]; i += 1
            for _ in range(n):
                i = _skip(b, i, kv >> 4)
                i = _skip(b, i, kv & 0x0F)
        return i
    if t == 12:
        while True:
            h = b[i]; i += 1
            if h == 0:
                return i
            if not h >> 4:
                i = _varint(b, i)[1]
            i = _skip(b, i, h & 0x0F)
    raise ValueError("thrift type %d" % t)


def _drop_created_by(path):
    """The span export carries no writer name: FileMetaData field 6 (created_by) is left out of the footer,
    as the format allows, and the next field's header is re-based on the field before it."""
    raw = open(path, "rb").read()
    assert raw[-4:] == b"PAR1"
    n = int.from_bytes(raw[-8:-4], "little")
    meta, body = raw[-8 - n:-8], raw[:-8 - n]
    out, i, last, prev, dropped = bytearray(), 0, 0, 0, False
    while meta[i]:
        h, j = meta[i], i + 1
        if h >> 4:
            fid = last + (h >> 4)
        else:
            z, j = _varint(meta, j)
            fid = (z >> 1) ^ -(z & 1)
        t = h & 0x0F
        end = _skip(meta, j, t)
        if fid == 6:
            dropped = True
        else:
            out += bytes([((fid - prev) << 4) | t]) if 0 < fid - prev <= 15 else bytes([t]) + _zz(fid)
            out += meta[j:end]
            prev = fid
        last, i = fid, end
    out += meta[i:]
    assert dropped, "no created_by in the footer"
    open(path, "wb").write(body + bytes(out) + len(out).to_bytes(4, "little") + b"PAR1")


def _zz(v):
    z, o = (v << 1) ^ (v >> 63), bytearray()
    while True:
        if z < 0x80:
            o.append(z)
            return bytes(o)
        o.append((z & 0x7F) | 0x80); z >>= 7
