"""Cut the bundle, compute the goldens from it, write figures.json, then check and verify."""
import datetime as dt
import os
import shutil
import sys
import time

import deliver as DL
import docs
import figures as FG
import golden as G
import metadata as MD
import pack as PK
import postprocess as PP
import sim
import world as W

EXPORT_STAMP = dt.datetime(2027, 3, 5, 17, 40, 0)


def golden_factors(target):
    """The development factors, read back from the close-out register's own shipped bytes.

    For each cost centre, what a quarter's count at its own close and at each close after it grew to by the
    time the quarter stopped moving, pooled over the quarters that have finished moving. Nothing is fitted:
    each factor is a ratio of two sums the register prints.
    """
    import golden as G
    return G.development_factors(G._read(target, PK.FILES["closeout"]))


def cut(target):
    if os.path.isdir(target):
        shutil.rmtree(target)
    os.makedirs(target)
    rows, expected, expected_net, inscope = sim.episodes(W.UNITS)
    sim.statistical_discharges(rows, W.UNITS)
    design = sim.design_ratios(W.UNITS, expected, expected_net, inscope)
    sim.assign_complications(rows, expected, design, W.UNITS)
    observed = sim.settle_additive(rows, expected, design, W.UNITS)
    allsep = {}
    for r in rows:
        allsep[(r["unit"], r["q"])] = allsep.get((r["unit"], r["q"]), 0) + 1
    plans = {x[0]: x[7] for x in W.UNITS if x[7] is not None}

    # the comparison frequency the record itself carries, and each unit's avoidable count per separation
    num, den = {}, {}
    for r in rows:
        if not r["in_scope"]:
            continue
        st = (W.DRG_BAND[r["drg"]], r["age"])
        den[st] = den.get(st, 0) + 1
        num[st] = num.get(st, 0) + (1 if r["hac"] else 0)
    rate = {st: num[st] / den[st] for st in den}
    per_sep, expected_per_sep = {}, {}
    for x in W.UNITS:
        code = x[0]
        if code not in plans:
            continue
        qs = [q for q in sim.quarters_for(x) if (code, q) in expected]
        if not qs:
            continue
        e = sum(expected[(code, q)] for q in qs)
        n = sum(allsep[(code, q)] for q in qs)
        if not e or not n:
            continue                                  # a unit outside the indicator carries no excess
        o = sum(observed[(code, q)] for q in qs)
        en = 0.0
        for r in rows:
            if r["unit"] == code and r["in_scope"]:
                en += rate[(W.DRG_BAND[r["drg"]], r["age"])]
        per_sep[code] = (o - en) / n                  # charter 4.3 per separation
        expected_per_sep[code] = e / n                # specification 3.4 per separation
    detail = sim.complications(rows, W.UNITS)
    # only the complications coded by the pull date stay in the record, and the two most recent quarters
    # are short by their own patients' mix of reporting groups
    observed, ultimate, vintage = sim.apply_coding_lag(rows, W.UNITS)
    detail = [d for d in detail if rows[d["row"]]["hac"]]
    PK.write_close_out(target, vintage)
    factors = golden_factors(target)
    # each unit's avoidable complications per separation, on the counts developed to what the quarters'
    # patients had, which is the figure the charter asks for and the one that is graded
    by_unit = {}
    for r in rows:
        if not r["in_scope"]:
            continue
        cell = by_unit.setdefault(r["unit"], {"obs": 0.0, "dev": 0.0})
        if r["hac"]:
            cell["obs"] += 1
            cell["dev"] += factors.get((r["unit"], W.IMMATURE[r["q"]]), 1.0) \
                if r["q"] in W.IMMATURE else 1.0
    dev_per_sep = {}
    for x in W.UNITS:
        code = x[0]
        if code not in plans or code not in by_unit:
            continue
        qs = [q for q in sim.quarters_for(x) if (code, q) in expected]
        e = sum(expected[(code, q)] for q in qs)
        n = sum(allsep[(code, q)] for q in qs)
        if not e or not n:
            continue
        dev_per_sep[code] = (by_unit[code]["dev"] - e) / n
    elig = [c for c in dev_per_sep if c in {x[0] for x in W.UNITS if x[10] == "eligible"}]
    ranked = sorted(elig, key=lambda c: -dev_per_sep[c] * plans[c])
    plans = sim.centre_plans(plans, dev_per_sep, ranked, ranked[0], expected_per_sep)
    assert sorted(elig, key=lambda c: -dev_per_sep[c] * plans[c])[:2] == ranked[:2], \
        "centring the planned volumes moved the two graded units"
    replays = sim.add_replays(rows, W.UNITS)
    allrows = PK.write_extract(target, rows, replays)
    PK.write_detail(target, rows, detail)
    PK.write_series(target, expected, observed, inscope)
    PK.write_summary(target, rows)
    PK.write_plan(target, plans)
    PK.write_units(target)
    PK.write_sites(target)
    PK.write_bands(target)
    PK.write_strata(target)
    PK.write_catlist(target)
    PK.write_placements(target)
    PK.write_dashboard(target, expected, observed, inscope, rows)
    PK.write_distractors(target)
    PK.write_dictionary(target)
    docs.charter(target)
    docs.specification(target)
    docs.thread(target)
    PK.write_manifest(target)
    PP.normalize_pdf(os.path.join(target, "improvement_partnership_charter_v3.pdf"),
                     b"D:20240617093000+11'00'", b"D:20240617093000+11'00'")
    PP.normalize_pdf(os.path.join(target, "hac_indicator_specification_v4.pdf"),
                     b"D:20240624141500+11'00'", b"D:20240624141500+11'00'")
    PP.normalize_ooxml(os.path.join(target, PK.FILES["dashboard"]), "Joseph Hunter", "Joseph Hunter",
                       "2027-03-05T06:12:00Z", "2027-03-05T06:40:00Z",
                       title="Inpatient quality indicators, quarter ended 31 December 2026", excel=True)
    stamp = time.mktime(EXPORT_STAMP.timetuple())
    for name in sorted(os.listdir(target)):
        os.utime(os.path.join(target, name), (stamp, stamp))
    return dict(rows=rows, allrows=allrows, expected=expected, expected_net=expected_net,
                observed=observed, inscope=inscope, allsep=allsep, detail=detail, replays=replays,
                design=design, plans=plans, net_rate=rate, per_sep=per_sep,
                expected_per_sep=expected_per_sep)


def zip_pack(target, path):
    """target.zip from the cut bundle: the files at the archive's root under their own names, sorted, one
    fixed timestamp, deflated, so a solver who unzips it gets the pack and not a folder, and so the archive
    is a function of the bundle's bytes and nothing else."""
    import hashlib
    import zipfile
    names = sorted(os.listdir(target))
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        for name in names:
            info = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            with open(os.path.join(target, name), "rb") as fh:
                z.writestr(info, fh.read())
    # what a consumer unzips is the pack: the same names at the root, byte for byte
    with zipfile.ZipFile(path) as z:
        entries = z.namelist()
        assert entries == names, "zip entries are not the pack's files: %s" % (set(entries) ^ set(names))
        assert not any("/" in n or "\\" in n for n in entries), "a zip entry carries a directory"
        for name in entries:
            on_disk = open(os.path.join(target, name), "rb").read()
            assert hashlib.sha256(z.read(name)).hexdigest() == hashlib.sha256(on_disk).hexdigest(), \
                "zip entry %s differs from the file on disk" % name
    return path


if __name__ == "__main__":
    task = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    gendir = os.path.dirname(os.path.abspath(__file__))
    tgt = sys.argv[1] if len(sys.argv) > 1 else os.path.join(task, "target")
    state = cut(tgt)
    g = G.compute(tgt)
    gold = os.path.join(task, "golden")
    os.makedirs(gold, exist_ok=True)
    chart_png = os.path.join(gendir, "_chart.png")
    DL.chart(chart_png, g)
    DL.workbook(os.path.join(gold, "embed_placement_2027q4.xlsx"), g)
    DL.brief(os.path.join(gold, "embed_placement_brief.pdf"), g, chart_png)
    PP.normalize_ooxml(os.path.join(gold, "embed_placement_2027q4.xlsx"), "Maureen Watts",
                       "Maureen Watts", "2027-03-17T23:15:00Z", "2027-03-18T04:05:00Z",
                       title="Cycle IP-09 placement", excel=True)
    PP.normalize_pdf(os.path.join(gold, "embed_placement_brief.pdf"),
                     b"D:20270318151000+11'00'", b"D:20270318151000+11'00'")
    MD.write(task, g)
    FG.write(gendir, g)
    import checks as CK
    import verify as VF
    n = CK.run(tgt, g, state)
    k = VF.run(tgt, os.path.join(gendir, "figures.json"))
    print("generator assertions", n, "independent checks", k)
    if CK.GAPS:
        print()
        for line in CK.GAPS:
            print("DESIGN GATE RED: %s" % line)
        print()
    print("call    : %s %s, %.1f avoidable complications on %d planned separations"
          % (g["answer"]["unit"], g["answer"]["name"], g["answer"]["avoidable"], g["answer"]["plan"]))
    print("closest : %s %s, %.1f; lead %.2f complications, %.2fx, %.2f standard errors (SE gap %.2f)"
          % (g["runner"]["unit"], g["runner"]["name"], g["runner"]["avoidable"], g["gap"], g["margin"],
             g["se_lead"], g["se_gap"]))
    print("rungs   : 0 %s %.1f published, 3 %s %.1f per 1,000, 4 %s %.1f; answer %d of %d published"
          % (g["rung0"]["unit"], g["rung0"]["published_excess"], g["rung3"]["unit"],
             g["rung3"]["per_1000"], g["rung4"]["unit"], g["rung4"]["avoidable"],
             g["published_rank"], len(g["eligible"])))
    print("forcing : band drift %.3f to %.3f (factor %.2f); surgical share %.3f to %.3f, %d carrying none"
          % (g["facts"]["drift_low"], g["facts"]["drift_high"], g["facts"]["drift_spread"],
             g["facts"]["surgical_low"], g["facts"]["surgical_high"], g["facts"]["surgical_none"]))
    print("demo    : %s published %.1f to %.1f (x%.1f), internal %.1f to %.1f (spread %.2f)"
          % (g["demo"]["unit"], g["demo"]["published_low"], g["demo"]["published_high"],
             g["demo"]["published_multiple"], g["demo"]["internal_low"], g["demo"]["internal_high"],
             g["demo"]["internal_spread"]))
    moved = [k for k, v in g["convergence"].items() if v["first"] != g["answer"]["unit"]]
    print("converge: %d readings of charter 4.3, %d naming another unit" % (len(g["convergence"]), len(moved)))
    if tgt == os.path.join(task, "target"):
        zip_pack(tgt, os.path.join(task, "target.zip"))
        print("zip     : %s" % os.path.join(task, "target.zip"))
    if CK.GAPS:
        sys.exit(1)
