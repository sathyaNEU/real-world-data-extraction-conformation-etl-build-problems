"""Build the pack and the goldens, write metadata.json and figures.json, run every check and the independent
verifier, build a second time into a scratch folder and require byte-identical output, then cut target.zip.

    python3 task121/generator/make.py [--once]
"""
import filecmp
import json
import os
import shutil
import sys
import tempfile
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import analysis as AN
import checks as C
import core
import golden as GD
import logic as L
import pack as P
import records as R
import verify as V
import world as WD

TASK = os.path.dirname(HERE)
TARGET = os.path.join(TASK, "target")
GOLDEN = os.path.join(TASK, "golden")
STAMP = 1791874800          # 13 October 2026, 00:00 local


def clearances(W, rows, legacy, station):
    """C1 by construction: no season event's hourly wind within 0.25 degree of a facility's 30-degree edge (either
    bearing formula) or within 0.03 m/s of calm; nudge that hour's records and recompute."""
    tmp = tempfile.mkdtemp()
    for it in range(12):
        P.write_met(station, tmp)
        P.write_maint(R.audits() + [R.OUTAGE], tmp)
        allr = P.write_complaints(W, [dict(r) for r in rows], tmp)
        P.write_ocs(legacy, tmp)
        P.write_boundary(tmp)
        met = AN.read_met(tmp)
        held, _ = AN.read_held(tmp)
        hw = AN.hourly(met, held)
        gold = AN.clean(AN.read_complaints(tmp), AN.read_ocs(tmp), AN.read_boundary(tmp))
        evs = AN.season_events(gold)
        bad = {}
        for e in evs:
            d, h = L.event_hour(e)
            w = hw.get((d, h))
            if w is None:
                continue
            if abs(w[0] - core.CALM_MS) < 0.03:
                bad[(d, h)] = "speed"
                continue
            if w[0] < core.CALM_MS:
                continue
            for f in core.FKEYS:
                for bf in (core.bearing_deg, core.bearing_planar):
                    b = bf(e["lat"], e["lon"], core.FAC[f]["lat"], core.FAC[f]["lon"])
                    if abs(core.angdiff(w[1], b) - core.UPWIND_DEG) < 0.25 or abs(core.angdiff(w[1], b) - 22.5) < 0.25:
                        bad[(d, h)] = "dir"
        if not bad:
            shutil.rmtree(tmp)
            return it
        for (d, h), why in bad.items():
            for rec in station[d]:
                if rec[0] // 60 == h and rec[7] == "V" and rec[1] > 0:
                    if why == "dir":
                        rec[2] = (rec[2] + 0.9) % 360
                    else:
                        rec[1] = rec[1] * 1.12
    raise AssertionError("clearances did not settle: %d hours" % len(bad))


def build_target(target):
    if os.path.isdir(target):
        shutil.rmtree(target)
    os.makedirs(target)
    W = WD.build()
    rows, legacy, c1, c2 = R.complaints(W)
    station, held = R.station_records(W)
    n_it = clearances(W, rows, legacy, station)
    n_met = P.write_met(station, target)
    P.write_maint(held, target)
    allr = P.write_complaints(W, rows, target)
    P.write_ocs(legacy, target)
    P.write_boundary(target)
    P.write_procedure(target)
    P.write_permits(target)
    P.write_totals(target)
    P.write_operators(target)
    P.write_pm25(W, target)
    P.write_airport(target)
    for f in os.listdir(target):
        os.utime(os.path.join(target, f), (STAMP, STAMP))
    return W, rows, legacy, allr, dict(met_rows=n_met, clearance_iterations=n_it)


def metadata(target, info):
    rows_of = lambda p: (sum(1 for _ in open(p, encoding="utf-8")) - 1) if p.endswith(".csv") else None
    files = []
    for k, f in sorted(P.FILES.items(), key=lambda x: x[1]):
        pth = os.path.join(target, f)
        files.append({"path": f, "format": f.rsplit(".", 1)[1], "bytes": os.path.getsize(pth), "rows": rows_of(pth),
                      "source": "Constructed: " + SOURCES[k], "date": "2026-10-12",
                      "license": "CC BY 4.0 (original work, constructed for this task)"})
    big = max((x for x in files if x["rows"]), key=lambda x: x["rows"])
    return {
        "task": "task121",
        "title": "Which permitted odor source around Harlow Falls is behind the 2026 surge in odor complaints, and "
                 "which comes closest, with the complaint record by month and the station's usable and calm hours",
        "domain": "Physical & Environmental Sciences",
        "subdomain": "pollution source attribution (odor complaints against the valley's wind)",
        "objective": "Root-Cause Analysis",
        "prompt_shape": "07: the call and the rival, the five facilities' upwind counts, the complaints by month "
                        "(January to September), the station's usable and calm hours by month (May to September), "
                        "the sixteen-sector chart",
        "as_of": "2026-10-12",
        "deliverables": [GD.DOCX, GD.XLSX, GD.PNG],
        "distractor_files": [P.FILES[k] for k in P.DISTRACTORS],
        "input_gates": {"files": len(files), "formats": sorted({x["format"] for x in files}),
                        "largest_file": big["path"], "largest_file_rows": big["rows"]},
        "sources": [{"files": "all files under target/",
                     "origin": "constructed for this task by task121/generator/make.py (seeded, deterministic) around a "
                               "fictional California air district, town, facilities and people; every record, reading "
                               "and figure is invented.",
                     "date": "2026-10-12", "license": "CC BY 4.0 (original work)"}],
        "files": files,
    }


SOURCES = {
    "complaints": "Complaint system export of 2 October 2026 (odor complaints, January to October 2026)",
    "fields": "Field reference of the complaint system export",
    "ocs": "Retired complaint system (OCS): open complaints at 31 December 2025",
    "met": "Harlow Falls station 5-minute meteorological records, January to September 2026 (PST)",
    "readme": "Readme of the Harlow Falls station export",
    "maint": "Harlow Falls station maintenance log, 2026",
    "procedure": "Compliance Procedure CP-14 rev. 4, odor complaint response",
    "permits": "District odor source list (30 September 2026)",
    "boundary": "District boundary",
    "totals": "District odor complaint totals 2019 to 2025",
    "operators": "Odor sources' monthly operating reports, January to September 2026",
    "pm25": "Harlow Falls station hourly PM2.5, January to September 2026 (PST)",
    "airport": "Kestrel County Airport hourly observations, 2026 (UTC)",
}


def figures(F, n_checks, cr, kept, hits):
    g = lambda x: "{:,}".format(int(x))
    name = {k: core.FAC[k]["name"] for k in core.FKEYS}
    short = {k: core.FAC[k]["short"] for k in core.FKEYS}
    out = {
        "call": "The district should take %s to the hearing board: its odor is behind the 2026 surge in odor complaints, "
                "and %s comes closest." % (name[F["call"]], short[F["rival"]]),
        "call_facility": name[F["call"]], "rival_facility": name[F["rival"]],
        "n_events": g(F["n_events"]), "calm_events": g(F["calm_events"]), "nowind_events": g(F["nowind_events"]),
        "upwind": {short[f]: g(F["O"][f]) for f in core.FKEYS},
        "expected": {short[f]: "%.1f" % F["E"][f] for f in core.FKEYS},
        "beyond": {short[f]: "%.1f" % F["excess"][f] for f in core.FKEYS},
        "times": {short[f]: "%.1f" % F["ratio"][f] for f in core.FKEYS},
        "all_hours_ratio": {short[f]: "%.2f" % (F["all"][0][f] / F["all"][1][f]) for f in core.FKEYS},
        "months": {m: g(v) for m, v in zip(GD.MONTHS, F["months"])},
        "months_total": g(sum(F["months"])),
        "usable": {m: g(v) for m, v in zip(GD.MONTHS[4:], F["usable"])},
        "calm": {m: g(v) for m, v in zip(GD.MONTHS[4:], F["calm"])},
        "usable_total": g(sum(F["usable"])), "calm_total": g(sum(F["calm"])),
        "sectors": dict(zip(AN.SECTORS, [g(x) for x in F["sectors"]])),
        "directional_events": g(sum(F["sectors"])),
        "carried_over": g(F["carried"]), "months_season": "5",
        "checks": n_checks, "cracker_kept": kept, "strong_battery_hits": hits,
    }
    return out


def main():
    once = "--once" in sys.argv
    W, rows, legacy, allr, info = build_target(TARGET)
    F = AN.main(TARGET)
    GD.write(GOLDEN, F)
    meta = metadata(TARGET, info)
    json.dump(meta, open(os.path.join(TASK, "metadata.json"), "w"), indent=1)
    n, cells, gold, cr, kept, hits = C.run(F, TARGET, meta)
    print("checks: %d assertions green (fork grid %d cells)" % (n, len(cells)))
    v = V.run(TARGET)
    short = {core.FAC[k]["name"]: k for k in core.FKEYS}
    assert v["n"] == F["n_events"] and short[v["call"]] == F["call"] and short[v["rival"]] == F["rival"]
    assert all(v["O"][core.FAC[k]["name"]] == F["O"][k] for k in core.FKEYS)
    assert all(abs(v["E"][core.FAC[k]["name"]] - F["E"][k]) < 1e-6 for k in core.FKEYS)
    assert v["months"] == F["months"] and v["usable"] == F["usable"] and v["calm"] == F["calm"]
    print("verifier: green (%s; %d events; months %s)" % (v["call"], v["n"], v["months"]))
    fig = figures(F, n, cr, kept, hits)
    json.dump(fig, open(os.path.join(HERE, "figures.json"), "w"), indent=1, ensure_ascii=False)
    if not once:
        tmp = tempfile.mkdtemp()
        t2, g2 = os.path.join(tmp, "target"), os.path.join(tmp, "golden")
        build_target(t2)
        F2 = AN.main(t2)
        GD.write(g2, F2)
        for a, b in ((TARGET, t2), (GOLDEN, g2)):
            names = sorted(os.listdir(a))
            assert names == sorted(os.listdir(b))
            for f in names:
                assert filecmp.cmp(os.path.join(a, f), os.path.join(b, f), shallow=False), "rebuild differs: %s" % f
        shutil.rmtree(tmp)
        print("second build: byte-identical (%d pack files, %d goldens)" % (len(os.listdir(TARGET)), len(os.listdir(GOLDEN))))
    zp = os.path.join(TASK, "target.zip")
    with zipfile.ZipFile(zp, "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(os.listdir(TARGET)):
            zi = zipfile.ZipInfo("target/" + f, date_time=(2026, 10, 12, 18, 0, 0))
            zi.compress_type = zipfile.ZIP_DEFLATED
            z.writestr(zi, open(os.path.join(TARGET, f), "rb").read())
    print("target.zip cut (%d bytes)" % os.path.getsize(zp))


if __name__ == "__main__":
    main()
