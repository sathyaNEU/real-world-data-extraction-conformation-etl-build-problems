"""The generator's assertions on the cut pack and the seeded world: the input gates, the call and its ladder with
margins, every semantic fork row (SF1 to SF14), the one-decimal corridor, the whole traces and partner-gateway's root
mix that refutes rung 3, the back-test, the three rules on the clean truth, the shock screen, the separation of the
asks from the call (SEP), the asks against the world's truths, the cracker sheet and the documents' controls.

    python3 checks.py [target_dir]            (run by build.py)"""
import csv
import json
import os
import shutil
import sys
import tempfile

import numpy as np
import pyarrow.parquet as pq

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import analysis as AN   # noqa: E402
import asks as A        # noqa: E402
import ceiling          # noqa: E402
import common as K      # noqa: E402
import world as W       # noqa: E402

GOLD5 = ["journey-search", "places", "seat-map", "partner-gateway", "notifications"]
FOUR = ["journey-search", "places", "seat-map", "notifications"]
H = K.REVIEW_HOURS
FAILS = []


def check(name, ok, detail=""):
    print("%s  %s%s" % ("PASS" if ok else "FAIL", name, (": " + detail) if detail else ""))
    if not ok:
        FAILS.append(name)


def over(fig, bud=None):
    bud = bud or K.BUDGET
    return [s for s in K.SVC if K.r1(fig[s]) > bud[s]]


# ------------------------------------------------------------------ the estimator under each reading
class Variants:
    """The golden's estimator re-run on the parquet under one alternative reading at a time."""

    def __init__(self, target, g):
        self.g = g
        tb = pq.read_table(os.path.join(target, K.FILES["spans"])).to_pydict()
        self.rows = list(zip(tb["trace_id"], tb["span_id"], tb["parent_span_id"], tb["service_name"], tb["span_name"],
                             tb["span_kind"], tb["start_time_unix_nano"], tb["end_time_unix_nano"],
                             tb["http_status_code"]))
        self.N, self.E = g.counts()

    def sli(self, dedupe=True, probes=False, client_internal=False, drop5xx=False, ge=False, drop404=False,
            first_try=False):
        g, N = self.g, self.N
        seen, rows = set(), []
        for tid, sid, pid, svc, name, kind, t0, t1, code in self.rows:
            if dedupe and sid in seen:
                continue
            seen.add(sid)
            if name == "GET /healthz" and not probes:
                continue
            rows.append((tid, sid, pid, g.by_trace[svc], name, kind, (t0 - AN.DEC0_NS) // (3600 * 10 ** 9),
                         (t1 - t0) / 1e6, code))
        root, kroot = {}, {e: np.zeros(H) for e in K.EDGE}
        for r in rows:
            if r[5] == "SPAN_KIND_SERVER" and r[2] == "":
                if r[4] != "GET /healthz":
                    root[r[0]] = (r[3], int(r[6]))
                if r[3] in K.EDGE and 0 <= r[6] < H:
                    kroot[r[3]][int(r[6])] += 1
        tries = {}
        out = {}
        for s in K.SVC:
            if client_internal and s in K.INTERNAL:
                mine = [r for r in rows if r[5] == "SPAN_KIND_CLIENT" and r[4].split(" ")[1] == K.TRACE_NAME[s]]
            else:
                mine = [r for r in rows if r[5] == "SPAN_KIND_SERVER" and r[3] == s and r[4] != "GET /healthz"]
            num = 0.0
            for r in sorted(mine, key=lambda x: x[6]):
                h = int(r[6])
                if not 0 <= h < H:
                    continue
                if first_try:
                    key = (r[0], r[4])
                    tries[key] = tries.get(key, 0) + 1
                    if tries[key] > 1:
                        continue
                if (drop5xx and r[8] >= 500) or (drop404 and r[8] == 404):
                    continue
                rt = root.get(r[0])
                if rt is None:
                    continue
                e, he = rt
                w = N[e][he] / max(kroot[e][he], 1)
                slow = r[7] >= g.thr[s] if ge else r[7] > g.thr[s]
                num += w * slow
            den = N[s].sum() - (self.E[s].sum() if drop5xx else 0)
            out[s] = 100 * num / den
        return out


def line_distance(x):
    return abs((x * 10) % 1 - 0.5) / 10


def main(target):
    g = AN.Golden(target)
    m = g.main()
    sli = {s: m[s]["sli"] for s in K.SVC}

    # ---------------------------------------------------------- input gates
    files = [K.FILES[k] for k in K.FILES]
    check("every pack file present", all(os.path.exists(os.path.join(target, f)) for f in files),
          "%d files" % len(files))
    fmts = {os.path.splitext(f)[1] for f in files}
    check("three or more formats", len(fmts) >= 3, ", ".join(sorted(fmts)))
    n_spans = pq.ParquetFile(os.path.join(target, K.FILES["spans"])).metadata.num_rows
    check("a file of 25,000 rows or more", n_spans >= 25000, "%d span rows" % n_spans)
    check("two or more distractors", len(K.DISTRACTORS) >= 2, ", ".join(K.FILES[d] for d in K.DISTRACTORS))

    # ---------------------------------------------------------- the call and its ladder
    golden = over(sli)
    check("the call: five services breach", golden == GOLD5, ", ".join(golden))
    for s in K.SVC:
        print("      %-16s SLI %.4f (%.1f) budget %.1f | service-hour %.3f hour-of-day %.3f day %.3f kept %.3f"
              % (s, sli[s], K.r1(sli[s]), K.BUDGET[s], m[s]["by_service_hour"], m[s]["by_hour_of_day"],
                 m[s]["by_day"], m[s]["unweighted"]))
    rung = {k: over({s: m[s][k] for s in K.SVC}) for k in ("by_service_hour", "by_hour_of_day", "by_day", "unweighted")}
    check("R3 (each service post-stratified by its own hourly count) files four", rung["by_service_hour"] == FOUR,
          ", ".join(rung["by_service_hour"]))
    check("R2 (hour-of-day pooling) files four", rung["by_hour_of_day"] == FOUR, ", ".join(rung["by_hour_of_day"]))
    check("R1 (day weighting) files notifications alone", rung["by_day"] == ["notifications"], ", ".join(rung["by_day"]))
    check("R0 (the kept share) files notifications alone", rung["unweighted"] == ["notifications"],
          ", ".join(rung["unweighted"]))
    gr = min(sli[s] / K.BUDGET[s] if s in GOLD5 else K.BUDGET[s] / sli[s] for s in K.SVC)
    check("golden margin: every SLI at least a quarter from its budget", gr >= 1.25, "smallest ratio %.3f" % gr)
    pgm = (K.BUDGET["partner-gateway"] - m["partner-gateway"]["by_service_hour"]) / K.BUDGET["partner-gateway"]
    check("rung 3 margin: partner-gateway a fifth under its budget", pgm >= 0.2, "%.3f" % pgm)
    m0 = min((K.BUDGET[s] - m[s]["unweighted"]) / K.BUDGET[s] for s in ("journey-search", "places", "seat-map",
                                                                      "partner-gateway"))
    check("rung 0 margin: the busy services 15 per cent under", m0 >= 0.15, "%.3f" % m0)

    # ---------------------------------------------------------- semantic fork rows
    v = Variants(target, g)
    slo = text_of(os.path.join(target, K.FILES["slo"]))
    check("SF1 the kept spans are not the requests (2.2)", "whether or not the tracing store kept a span for it" in slo
          and rung["unweighted"] != GOLD5)
    for sf, label, kw in (("SF2", "caller's client span for an internal service", dict(client_internal=True)),
                          ("SF3", "kept probes counted", dict(probes=True)),
                          ("SF4", "re-sent rows twice", dict(dedupe=False)),
                          ("SF9", "5xx dropped from both sides", dict(drop5xx=True)),
                          ("SF12", "at or over the threshold", dict(ge=True)),
                          ("SF13", "404 responses dropped", dict(drop404=True)),
                          ("SF14", "first tries only", dict(first_try=True))):
        alt = v.sli(**kw)
        check("%s %s: same call" % (sf, label), over(alt) == GOLD5,
              "partner-gateway %.3f, journey-search %.3f" % (alt["partner-gateway"], alt["journey-search"]))
    import asks as AS
    dec_off = {AS.lisbon_offset(AS.Y0.replace(month=12) + __import__("datetime").timedelta(hours=h)) for h in range(H)}
    check("SF5 December in Lisbon time is UTC", dec_off == {0})
    check("SF6 a child's own hour: same figure to one decimal",
          all(K.r1(m[s]["own_hour"]) == K.r1(sli[s]) for s in K.SVC))
    n_orph = sum(m[s]["orphans"] for s in K.SVC)
    check("SF7 spans whose trace began before December: either handling identical",
          all(K.r1(m[s]["orphans_dropped"]) == K.r1(sli[s]) for s in K.SVC), "%d such spans" % n_orph)
    check("SF8 the unrounded SLI against the budget: the same five",
          [s for s in K.SVC if sli[s] > K.BUDGET[s]] == GOLD5)
    check("SF10 the weighted kept count as the denominator: same figure to one decimal",
          all(K.r1(m[s]["hajek"]) == K.r1(sli[s]) for s in K.SVC))
    check("SF11 weights calibrated hour by hour: same figure to one decimal",
          all(K.r1(m[s]["calibrated"]) == K.r1(sli[s]) for s in K.SVC))
    corridor = {s: [sli[s], m[s]["hajek"], m[s]["calibrated"], m[s]["own_hour"], m[s]["orphans_dropped"]]
                for s in K.SVC}
    worst = min(line_distance(x) for s in K.SVC for x in corridor[s])
    check("corridor: every standing estimator 0.008 or more from a rounding line", worst >= 0.008, "%.4f" % worst)

    # ---------------------------------------------------------- the whole traces, the root mix, the back-test
    ids = {r[1]: r for r in v.rows}
    internal = [r for r in v.rows if r[5] == "SPAN_KIND_SERVER" and g.by_trace[r[3]] in K.INTERNAL
                and r[4] != "GET /healthz"]
    whole = 0
    for r in internal:
        c = ids.get(r[2])
        if c is not None and c[5] == "SPAN_KIND_CLIENT":
            rt = ids.get(c[2])
            if rt is not None and rt[5] == "SPAN_KIND_SERVER" and rt[2] == "":
                whole += 1
    check("whole traces: every internal server span has its client span and its root in the export",
          whole == len(internal) - n_orph, "%d of %d" % (whole, len(internal)))
    mix_k, mix_w = m["partner-gateway"]["root_mix_kept"], m["partner-gateway"]["root_mix_weighted"]
    check("partner-gateway's kept spans are a third each by edge service, its requests mostly journey-search's",
          mix_k.get("journey-search", 0) < 0.4 and mix_w.get("journey-search", 0) > 0.75,
          "kept %s, weighted %s" % ({k: round(x, 3) for k, x in mix_k.items()},
                                    {k: round(x, 3) for k, x in mix_w.items()}))
    kept5 = {}
    for tid, sid, pid, svc, name, kind, t0, t1, code in v.rows:
        if kind == "SPAN_KIND_SERVER" and name != "GET /healthz":
            s = g.by_trace[svc]
            a, b = kept5.get(s, (0, 0))
            kept5[s] = (a + (code >= 500), b + 1)
    gap5 = max(abs(100 * kept5[s][0] / kept5[s][1] - m[s]["lb_5xx_share"]) for s in K.SVC)
    check("back-test: the kept 5xx share ties the balancer's 5xx counts for every service", gap5 < 0.15,
          "largest gap %.3f points" % gap5)

    # ---------------------------------------------------------- three rules on the clean truth
    w = W.World(K.SEED)
    sp = w.sp
    srv = sp["kind"] == "SERVER"
    inwin = (sp["t0"] >= 0) & (sp["t0"] < H * 3600)
    N = {s: w.N[s][W.DEC0:W.DEC0 + H].astype(float) for s in K.SVC}
    r3 = {}
    for s in K.SVC:
        sel = srv & inwin & (sp["svc"] == s)
        hh = (sp["t0"][sel] // 3600).astype(int)
        kh = np.bincount(hh, minlength=H).astype(float)
        sh = np.bincount(hh, weights=(sp["ms"][sel] > K.THRESHOLD[s]).astype(float), minlength=H)
        r3[s] = 100 * (np.where(kh > 0, N[s] / np.maximum(kh, 1), 0) * sh).sum() / N[s].sum()
    check("analyst test on the clean truth: post-stratifying each service by its own hour files four",
          over(r3) == FOUR, "partner-gateway %.3f" % r3["partner-gateway"])
    cheap = [k for k in ("by_service_hour", "by_hour_of_day", "by_day", "unweighted") if rung[k] == GOLD5]
    check("cheap routes reaching the call: none", not cheap, ", ".join(cheap) or "0 of 4")
    truth_set = [s for s in K.SVC if w.true_sli(s) > K.BUDGET[s]]
    check("the world's own truth breaches the same five", truth_set == GOLD5, ", ".join(truth_set))

    # ---------------------------------------------------------- the shock screen
    stats = {"December requests": {s: m[s]["requests"] for s in K.SVC},
             "kept spans": {s: m[s]["kept"] for s in K.SVC},
             "5xx share": {s: m[s]["lb_5xx_share"] for s in K.SVC},
             "threshold": dict(K.THRESHOLD), "budget": dict(K.BUDGET)}
    for label, st in stats.items():
        order = sorted(K.SVC, key=lambda s: st[s])
        pos = sorted(order.index(s) for s in GOLD5)
        contiguous = pos == list(range(pos[0], pos[0] + 5))
        ties = len(set(st.values())) < len(K.SVC)
        check("shock: the five are not an interval on %s" % label, not contiguous or ties,
              "positions %s" % pos)

    # ---------------------------------------------------------- SEP: the call never reads an ask file
    tmp = tempfile.mkdtemp()
    try:
        for k in ("spans", "lb_h2", "catalogue", "slo"):
            shutil.copy(os.path.join(target, K.FILES[k]), tmp)
        m2 = AN.Golden(tmp).main()
        check("SEP the call computes from the trace export, the balancer's counts, the catalogue and the standard alone",
              all(abs(m2[s]["sli"] - sli[s]) < 1e-12 for s in K.SVC))
    finally:
        shutil.rmtree(tmp)
    full = AN.Golden(target).run()
    for dk in K.DISTRACTORS:
        tmp = tempfile.mkdtemp()
        try:
            for f in os.listdir(target):
                if f != K.FILES[dk]:
                    shutil.copy(os.path.join(target, f), tmp)
            part = AN.Golden(tmp).run()
            same = part["over"] == full["over"] and part["deploys"] == full["deploys"] and \
                part["costs"] == full["costs"] and part["incidents"] == full["incidents"] and \
                all(part["main"][s]["sli"] == full["main"][s]["sli"] for s in K.SVC)
            check("distractor %s deleted: the call and every ask unchanged" % K.FILES[dk], same)
        finally:
            shutil.rmtree(tmp)
    cols = pq.ParquetFile(os.path.join(target, K.FILES["spans"])).schema.names
    check("SEP the trace export carries no version, deployment, cost or incident field",
          not any(c for c in cols if any(x in c for x in ("version", "deploy", "cost", "incident"))), ", ".join(cols))

    # ---------------------------------------------------------- the asks against the world's truths
    _, _, dtruth = A.deployments()
    _, _, _, btruth, _ = A.billing()
    _, _, _, _, itruth = A.incidents()
    gd, gc, gi = g.deploys(), g.costs(), g.incidents()
    check("ask A releases and rollbacks match the world", gd == dtruth)
    check("ask B costs match the world to the cent", all(gc[s] == [round(x, 2) for x in btruth[s]] for s in K.SVC))
    check("ask C minutes match the world", all(abs(a - b) < 1e-6 for s in K.SVC for a, b in zip(gi[s], itruth[s])))
    near = [(s, i) for s in K.SVC for i in (0, 1) if abs(gc[s][i] % 1 - 0.5) < 0.01 or abs(gi[s][i] % 1 - 0.5) < 0.01]
    check("no euro or minute figure on a half-unit line", not near, str(near))
    rows, L, on, off = ceiling.measure(target)
    check("cracker sheet: every path misses", all(k < 20 for _, _, k in rows),
          "; ".join("%s %d" % (lab.split(":")[0], k) for lab, _, k in rows))
    check("pair ceiling at or under 60", (on + off) / 2 <= 60, "%.1f" % ((on + off) / 2))

    # ---------------------------------------------------------- documents
    names = [f.lower() for f in os.listdir(target)]
    notes_words = ("readme", "dictionary", "notes", "manifest", "glossary", "schema", "codebook", "field_guide")
    from openpyxl import load_workbook
    sheets = []
    for f in os.listdir(target):
        if f.endswith(".xlsx"):
            sheets += [x.lower() for x in load_workbook(os.path.join(target, f), read_only=True).sheetnames]
    check("no readme, dictionary, notes or manifest file or sheet under target/",
          not any(w_ in n_ for n_ in names + sheets for w_ in notes_words), ", ".join(sorted(sheets)))
    check("PR-SLO-3 control: the filed request sentence reads back", "through its load balancer target group" in slo)
    # realism sweep: no id column is an arithmetic sequence
    import re as _re
    idcols = {}
    for row in csv.DictReader(open(os.path.join(target, K.FILES["incidents"]))):
        idcols.setdefault("incident_id", []).append(row["incident_id"])
    for row in csv.DictReader(open(os.path.join(target, K.FILES["resources"]))):
        idcols.setdefault("resource_id", []).append(row["resource_id"])
    for x in json.load(open(os.path.join(target, K.FILES["deploys"])))["deployments"]:
        idcols.setdefault("deployment_id", []).append(x["deployment_id"])
    flat = []
    for col, vals in idcols.items():
        nums = sorted({int(_re.sub(r"\D", "", v) or 0, 16 if col == "resource_id" else 10) for v in vals})
        steps = {b_ - a_ for a_, b_ in zip(nums, nums[1:])}
        if len(steps) <= 1:
            flat.append(col)
    check("realism: no id column is an arithmetic sequence", not flat, ", ".join(flat) or "%d id columns" % len(idcols))
    import collections as _c
    from openpyxl import load_workbook as _lw
    rv = [r_[4] for r_ in _lw(os.path.join(target, K.FILES["feedback"]), read_only=True).active.iter_rows(min_row=2,
                                                                                                          values_only=True)]
    top = max((v_ for k_, v_ in _c.Counter(x for x in rv if x and len(x) > 12).items()), default=0)
    check("realism: no review text longer than a few words recurs more than ten times", top <= 10, "most %d" % top)
    tb_h = pq.read_table(os.path.join(target, K.FILES["spans"]), columns=["service_name", "host_name"]).to_pydict()
    hosts = {}
    for svc_, h_ in zip(tb_h["service_name"], tb_h["host_name"]):
        hosts.setdefault(svc_, set()).add(h_)
    counts = sorted(len(x) for x in hosts.values())
    check("realism: services do not share one pod count", len(set(counts)) > 3, "distinct pods per service %s" % counts)
    check("PR-SLO-3 files the release unit", "the code of one commit" in slo)
    check("PR-SLO-3 counts a service's minutes while an incident named it", "named it at the time" in slo.replace("\n", " "))
    dashes = []
    for f in files:
        p = os.path.join(target, f)
        if f.endswith((".md", ".csv", ".json")):
            if "—" in open(p, encoding="utf-8").read():
                dashes.append(f)
        elif f.endswith(".docx"):
            if "—" in text_of(p):
                dashes.append(f)
    check("no em dash in a shipped text", not dashes, ", ".join(dashes))

    print()
    print("%s  %d failures" % ("PASS" if not FAILS else "FAIL", len(FAILS)))
    return 1 if FAILS else 0


def text_of(path):
    import docx
    d = docx.Document(path)
    parts = [p.text for p in d.paragraphs]
    for t in d.tables:
        for row in t.rows:
            parts.append(" | ".join(c.text for c in row.cells))
    return "\n".join(parts)


if __name__ == "__main__":
    tgt = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "target")
    sys.exit(main(tgt))
