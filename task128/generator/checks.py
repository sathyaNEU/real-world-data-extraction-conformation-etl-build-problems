"""In-generator assertion regime. Every graded figure, every rung, every rival-killer and every
input gate is asserted here, loudly, so a later parameter tweak fails the build at the tweak.
"""
import os
import statistics

from params import ESTATES, COLO, CLOUD, DENSE
import ladder as G
import windows as WIN


class Checks:
    def __init__(self):
        self.n = 0

    def ok(self, label, cond, detail=""):
        self.n += 1
        if not cond:
            raise AssertionError(f"[{self.n}] {label}: {detail}")


def _corr(xs, ys):
    n = len(xs)
    mx, my = sum(xs) / n, sum(ys) / n
    cov = sum((a - mx) * (b - my) for a, b in zip(xs, ys)) / n
    sx, sy = statistics.pstdev(xs), statistics.pstdev(ys)
    return cov / (sx * sy) if sx and sy else 0.0


def run(W, out, info, meta):
    C = Checks()
    target = os.path.join(out, "target")
    golden = os.path.join(out, "golden")
    files = sorted(os.listdir(target))
    fmts = sorted({os.path.splitext(f)[1].lower() for f in files})

    # ---- input gates
    C.ok("gate.files", len(files) >= 10, f"{len(files)} input files")
    C.ok("gate.formats", len(fmts) >= 3, f"{len(fmts)} formats: {fmts}")
    C.ok("gate.large", info["spine"] >= 25000, f"spine {info['spine']} rows")
    C.ok("gate.distractors", len(meta["distractor_files"]) >= 2, str(meta["distractor_files"]))
    for d in meta["distractor_files"]:
        C.ok("gate.distractor_present", d in files, d)
    for dv in DEL_FILES():
        C.ok("gate.deliverable", os.path.exists(os.path.join(golden, dv)), dv)
    # no file name or text in the pack names a distractor
    for f in files:
        C.ok("gate.noword_name", "distractor" not in f.lower(), f)
    for f in files:
        ext = os.path.splitext(f)[1].lower()
        if ext in (".csv", ".md", ".txt", ".json", ".jsonl", ".yaml", ".eml"):
            txt = open(os.path.join(target, f), encoding="utf-8", errors="ignore").read().lower()
            C.ok("gate.noword_text", "distractor" not in txt, f)

    # ---- the ladder
    r = W["rungs"]
    tot = {k: r[k][1] for k in ("R0", "R1", "R2", "R3", "R4")}
    ans = tot["R4"]
    C.ok("ladder.R0_above", tot["R0"] > ans, f"R0 {tot['R0']} vs {ans}")
    C.ok("ladder.R1_above", tot["R1"] > ans, f"R1 {tot['R1']} vs {ans}")
    C.ok("ladder.R2_below", tot["R2"] < ans, f"R2 {tot['R2']}")
    C.ok("ladder.R3_below", tot["R3"] < ans, f"R3 {tot['R3']}")
    C.ok("ladder.R4_feasible_max", ans > tot["R2"] and ans > tot["R3"], "R4 top feasible")
    C.ok("ladder.R4_over_R3", ans / tot["R3"] >= 1.20, f"ratio {ans/tot['R3']:.3f}")
    # nearest wrong cell at least 8 per cent from the answer
    nearest = min(abs(ans - tot[k]) / ans for k in ("R0", "R1", "R2", "R3"))
    C.ok("sep.nearest_8pct", nearest >= 0.08, f"nearest {nearest:.3f}")
    # colocated signature (1,1) is unique to the answer
    sig = (W["answer_split"]["payments"], W["answer_split"]["checkout"])
    C.ok("sep.answer_sig", sig == (1, 1), str(sig))
    for k in ("R0", "R1", "R2", "R3"):
        s = r[k][0]
        C.ok(f"sep.{k}_sig", (s["payments"], s["checkout"]) != (1, 1),
             f"{s['payments']}/{s['checkout']}")
    # colocated discriminator dominance
    colo_r4 = sum(W["rungs"]["r4c"][e][1] for e in COLO)
    colo_r3 = sum(W["rungs"]["r3c"][e][1] for e in COLO)
    C.ok("disc.colo_edge", colo_r4 / colo_r3 >= 1.2, f"{colo_r4}/{colo_r3}")

    # ---- mid-bin
    for e in ESTATES:
        r_ = W["figs"][e] % 10
        d = abs(r_ - 5) if r_ else 0
        C.ok(f"bin.{e}", d >= 3, f"fig {W['figs'][e]} dist {d} from the x5 edge")
    dt_ = abs(ans % 10 - 5) if ans % 10 else 0
    C.ok("bin.total", dt_ >= 3, f"total {ans} dist {dt_}")

    # ---- decorrelation and lens-swap
    wh, _ = WIN.nov_drains()
    for e in COLO:
        hs = W["hosts"][e]
        # richness on the packages the stop rung tickets (the estate's dense role packages)
        dense = {pk for _, pk, _ in DENSE[e]}
        xs = [sum(h.pkg_count(p) for p in dense) for h in hs]
        ys = [h.whole() for h in hs]
        C.ok(f"decorr.{e}", abs(_corr(xs, ys)) < 0.25, f"corr {_corr(xs, ys):.3f}")
        r4d = set(G.golden_drained(W, e, wh[e]))
        # r3 drained hosts (densest package first)
        agg = {}
        for h in hs:
            cnt = {}
            for pkg, cve in h.findings:
                cnt[pkg] = cnt.get(pkg, 0) + 1
            for pkg, c in cnt.items():
                agg.setdefault(pkg, []).append((h.hid, c))
        rate = {p: sum(c for _, c in rows) / len(rows) for p, rows in agg.items()}
        used, r3d = 0, set()
        for pkg in sorted(agg, key=lambda p: (-rate[p], p)):
            if used >= wh[e]:
                break
            for hid, c in sorted(agg[pkg], key=lambda x: (-x[1], x[0])):
                if used >= wh[e]:
                    break
                r3d.add(hid); used += 1
        ov = len(r3d & r4d) / len(r4d)
        C.ok(f"lens.{e}", ov < 0.15, f"overlap {ov:.3f}")

    # ---- Nov drains
    C.ok("drain.payments", wh["payments"] == 96, str(wh))
    C.ok("drain.checkout", wh["checkout"] == 120, str(wh))

    # ---- close-out back-test
    co = W["co_rivals"]
    C.ok("closeout.truth_cells", len(W["co_truth"]) == 12, str(len(W["co_truth"])))
    for name, d in co.items():
        C.ok(f"closeout.{name}.cells", d["cell_misses"] >= 3, str(d))
        C.ok(f"closeout.{name}.pct", d["pct_off"] >= 4.0, str(d))

    # ---- every shipped file registered in the provenance record, every extract in the dictionary
    tdir = os.path.join(out, "target")
    prov = open(os.path.join(tdir, "extract_provenance_2026-10-23.md"), encoding="utf-8").read()
    dic = open(os.path.join(tdir, "warehouse_data_dictionary.md"), encoding="utf-8").read()
    shipped = sorted(os.listdir(tdir))
    C.ok("reg.provenance", all(f in prov for f in shipped if not f.startswith("extract_provenance")),
         "provenance lists every file")
    C.ok("reg.dictionary", all(f in dic for f in shipped
                               if f.endswith((".csv", ".jsonl", ".parquet", ".xlsx", ".json"))),
         "dictionary covers every extract")

    # ---- strict cutline under the answer: the last ticket in and the first below are unique
    n_cl = 300 - sum(W["rungs"]["r4c"][e][0] for e in COLO)
    cv = [x[0] for x in G._cloud_sorted(W["scorev"])]
    C.ok("cut.strict", cv[n_cl - 2] > cv[n_cl - 1] > cv[n_cl] > cv[n_cl + 1],
         f"{cv[n_cl-2]}/{cv[n_cl-1]}/{cv[n_cl]}/{cv[n_cl+1]}")

    # ---- the rebuild identity the decisive rung reads, and the colocated ticket's legality
    import datetime as _d
    latest = {}
    for rq in W["requests"]:
        for hid in rq["hosts"][:rq["accepted"]]:
            latest[hid] = max(latest.get(hid, rq["date"]), rq["date"])
    bad_bind = bad_fix = future = 0
    for e in COLO:
        for h in W["hosts"][e]:
            if h.in_service > _d.date(2026, 10, 22):
                future += 1
            if h.hid in latest and latest[h.hid] != h.in_service:
                bad_bind += 1
            if h.hid not in latest and h.in_service >= _d.date(2026, 5, 1):
                bad_bind += 1
            for pkg, cve in h.findings:
                if W["reg"].by_id[cve].published <= h.in_service:
                    bad_fix += 1
    C.ok("rebuild.bind", bad_bind == 0, f"{bad_bind} hosts disagree with their latest accepted window")
    C.ok("rebuild.identity", bad_fix == 0, f"{bad_fix} findings whose fix predates in_service")
    C.ok("rebuild.no_future", future == 0, f"{future} in_service dates after 22 October")
    for e in COLO:
        drained = G.golden_drained(W, e, wh[e])
        pkg, cov = G.colo_ticket_package(W["hosts"], drained, e, W["reg"])
        C.ok(f"ticket.{e}", pkg is not None and cov == len(drained), f"{pkg} covers {cov}/{len(drained)}")
        ranked = sorted(W["hosts"][e], key=lambda h: (-h.whole(), h.hid))
        b = wh[e]
        C.ok(f"host_rank_edge.{e}", ranked[b - 1].whole() >= ranked[b].whole(),
             f"{ranked[b-1].whole()} vs {ranked[b].whole()}")

    # ---- acknowledgements back-test
    C.ok("acks.count", len(W["requests"]) >= 400, str(len(W["requests"])))
    for name, miss in W["req_rivals"].items():
        C.ok(f"acks.{name}", miss >= 20, f"{name} misses {miss}")

    # ---- ask answers present and well-formed
    for e in ESTATES:
        a = W["ans_A"][e]
        C.ok(f"askA.{e}", a["median_days"] > 0 and a["tickets_missed"] >= 0, str(a))
    for e in CLOUD:
        b = W["ans_B"][e]
        C.ok(f"askB.{e}", b["in_service"] > 0 and 0 <= b["unscanned_14d"] <= b["in_service"], str(b))

    # ---- metadata coherence
    C.ok("meta.inputs", meta["input_files"] == files, "metadata lists the shipped inputs")
    C.ok("meta.total", meta["answer"]["total_exposures"] == ans, "metadata total matches")
    return C.n


def DEL_FILES():
    import golden as GOLD
    return [GOLD.CUT, GOLD.DECK]
