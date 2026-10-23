"""Build task273: the evidence pack into <task>/target, the goldens into <task>/golden, metadata.json and
generator/figures.json, then the checks and the independent verifier, then a second build into a scratch folder inside
the task (removed after) compared byte for byte, then target.zip cut from the final build.

    python3 task273/generator/build.py              everything
    python3 task273/generator/build.py --out DIR    the pack only, into DIR
    python3 task273/generator/build.py --golden     the pack and the goldens, no checks"""
import os
for _v in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "1")
import argparse      # noqa: E402
import calendar      # noqa: E402
import csv           # noqa: E402
import datetime as dt  # noqa: E402
import hashlib       # noqa: E402
import json          # noqa: E402
import shutil        # noqa: E402
import sys           # noqa: E402
import warnings      # noqa: E402

warnings.filterwarnings("ignore")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import common as K         # noqa: E402
import docs as DC          # noqa: E402
import events as EV        # noqa: E402
import fleet as FL         # noqa: E402
import records as R        # noqa: E402
import roads as RD         # noqa: E402
import world as W          # noqa: E402

TASK = os.path.dirname(HERE)
MTIME = calendar.timegm(K.ASSEMBLED.timetuple())

CONTENTS = [
    ("rule", "Stonereach Valley Regional Transportation Commission: Commercial Fleet Safety Programme, coverage rule "
             "(adopted 14 October 2026)."),
    ("crashes", "State crash records system, regional extract for Stonereach County, crashes of 2021 to 2025: one row "
                "a crash (extract of 30 September 2026)."),
    ("units", "The same extract: one row a unit on each crash report (vehicles, parked vehicles, pedestrians, "
              "pedalcyclists)."),
    ("persons", "The same extract: one row a person, for crashes with an injury recorded."),
    ("dictionary", "The extract's data dictionary, with the codes of both report forms."),
    ("deaths", "State road fatality register: deaths within 30 days of a crash in Stonereach County, 2021 to 2025."),
    ("inventory", "Linear referencing system: road inventory of Stonereach County (31 December 2025), with the legacy "
                  "route numbers."),
    ("tmr", "Department of Transportation: Travel Monitoring Report 2025, Stonereach Valley region."),
    ("stations", "Department of Transportation: continuous count stations in the region, 2025."),
    ("atr", "Department of Transportation: hourly volumes at the continuous count stations, 2025."),
    ("costs", "Department of Transportation: crash unit costs for safety analysis, 2025."),
    ("operators", "The Commission's licensed operators, with the names officers write on crash reports, and the fleet "
                  "returns of the operators that file them."),
    ("platforms", "Quarterly reports of the ride-hail and delivery platforms to the Commission, 2021 to 2025."),
    ("registrations", "Department of Motor Vehicles: registrations in force in Stonereach County, 2021 to 2025."),
    ("weather", "Daily weather at Kelderwick Regional Airport, 2021 to 2025."),
    ("workzones", "Department of Transportation: work zone log, Stonereach County, 2021 to 2025."),
]


def tmr_tables(segs, atr_head, atr_rows, sts):
    vmt = {fu: {y: round(W.vmt(y, fu) / 1e6, 1) for y in K.YEARS} for fu in W.VMT_SHARE}
    daily = {}
    for fu in W.VMT_SHARE:
        cl = sum(s["e"] - s["b"] for s in segs if (s["fc"], s["ur"]) == fu)
        daily[fu] = (cl, W.vmt(2025, fu) / 365.0 / 1000.0)
    gnum = {i + 1: g for i, g in enumerate(K.GROUPS)}
    st_rows = []
    grp = {}
    for st in sts:
        st_rows.append([st["id"], st["route"], "%.2f" % st["mp"], str(st["fc"]), "Urban" if st["ur"] == "U" else
                        "Rural", str(K.GROUPS.index(st["group"]) + 1)])
        grp[st["id"]] = st["group"]
    month = {g: [0.0] * 12 for g in K.GROUPS}
    mdays = {g: [0] * 12 for g in K.GROUPS}
    by = {}
    for r in atr_rows:
        key = (r[0], r[1])
        v = sum(int(x) for x in r[3:] if x != "")
        by[key] = by.get(key, 0) + v
    for (sid, day), v in by.items():
        g = grp[sid]
        m = int(day[5:7]) - 1
        month[g][m] += v
        mdays[g][m] += 1
    monthly = {}
    for g in K.GROUPS:
        avg = [month[g][m] / mdays[g][m] for m in range(12)]
        ann = sum(month[g]) / sum(mdays[g])
        monthly[g] = [a / ann for a in avg]
    share = {u: FL.use_miles(u, 2025) if u == "PV" else W.SHARE[u][2025] * W.VMT_TOTAL[2025] for u in
             ["PV"] + list(W.SHARE)}
    tot = sum(share.values())
    classes = [("Motorcycles", share["MC"] / tot),
               ("Passenger cars", 0.47 * (share["PV"] + share["RH"] + share["AD"] + share["TX"] + share["LM"]) / tot),
               ("Light trucks (pickups, SUVs, vans)", (0.53 * (share["PV"] + share["RH"] + share["AD"] + share["TX"]
                                                               + share["LM"]) + share["GV"] * 0.8 + share["EM"] * 0.7
                                                       + share["OC"] * 0.2 + share["PT"] * 0.6 + share["AS"] * 0.55
                                                       + share["PD"] * 0.8) / tot),
               ("Buses", (share["TB"] + share["SB"] + share["PT"] * 0.4 + share["AS"] * 0.45) / tot),
               ("Single-unit trucks", (share["OC"] * 0.5 + share["PD"] * 0.2 + share["GV"] * 0.2 + share["EM"] * 0.3)
                / tot),
               ("Combination trucks", share["OC"] * 0.3 / tot)]
    s = sum(c[1] for c in classes)
    classes = [(c, v / s) for c, v in classes]
    return vmt, daily, st_rows, monthly, classes


def build(out, seed=K.SEED, keep=False):
    if os.path.exists(out):
        shutil.rmtree(out)
    os.makedirs(out)
    p = lambda k: os.path.join(out, K.FILES[k])
    w = EV.world(seed)
    wr = R.Writer(w, seed)
    n = {}
    for key, fn in (("crashes", wr.crash_rows), ("units", wr.unit_rows), ("persons", wr.person_rows),
                    ("deaths", wr.fatality_rows), ("weather", wr.weather_rows), ("workzones", wr.workzone_rows)):
        head, rows = fn()
        R.write_csv(p(key), head, rows)
        n[key] = len(rows)
    segs = w["segs"]
    sts = RD.stations(segs, seed)
    head, rows = R.station_rows(sts, segs)
    R.write_csv(p("stations"), head, rows)
    n["stations"] = len(rows)
    ahead, arows = R.atr_rows(segs, sts, seed)
    R.write_csv(p("atr"), ahead, arows)
    n["atr"] = len(arows)
    legacy = sorted({(RD.old_route_id(s["route"]), s["route"]) for s in segs})
    DC.write_inventory(p("inventory"), segs, legacy)
    n["inventory"] = len(segs)
    vmt, daily, st_rows, monthly, classes = tmr_tables(segs, ahead, arows, sts)
    DC.write_tmr(p("tmr"), vmt, daily, st_rows, monthly, classes)
    DC.write_costs(p("costs"))
    DC.write_rule(p("rule"))
    DC.write_dictionary(p("dictionary"))
    ops, _ = FL.operators(seed)
    fr = FL.fleet_returns(seed)
    DC.write_operators(p("operators"), ops, fr)
    n["operators"] = len(ops)
    ph, prow = FL.platform_quarters(seed)
    R.write_csv(p("platforms"), ph, prow)
    n["platforms"] = len(prow)
    DC.write_registrations(p("registrations"), FL.registrations(seed))
    DC.write_contents(p("contents"), [(K.FILES[k], d) for k, d in CONTENTS])
    return dict(w=w if keep else None, counts=n)


PDF_DATES = {"rule": ("D:20261014093000-07'00'", "D:20261014093000-07'00'"),
             "dictionary": ("D:20261002141500-07'00'", "D:20261002141500-07'00'"),
             "tmr": ("D:20260818101000-07'00'", "D:20260818101000-07'00'"),
             "costs": ("D:20250306113000-08'00'", "D:20250306113000-08'00'")}
OOXML = {
    "inventory": ("Transportation Data Office", "Transportation Data Office", "2023-02-06T17:20:00Z",
                  "2026-01-12T22:41:00Z", "Road inventory, Stonereach County", True),
    "operators": ("Licensing", "Amanda Barrera", "2019-05-14T16:02:00Z", "2026-10-28T23:15:00Z",
                  "Operator register", True),
    "registrations": ("DMV Research and Statistics", "DMV Research and Statistics", "2026-02-03T18:30:00Z",
                      "2026-02-03T18:30:00Z", "Registrations in force", True),
}


def finish(out):
    """The containers as their writers save them, then every file's modified time set to the pack's assembly."""
    import postprocess as PP
    for k, (c, m) in PDF_DATES.items():
        PP.normalize_pdf(os.path.join(out, K.FILES[k]), c.encode(), m.encode())
    PP.COMPANY = K.COMPANY
    for k, (cr, lb, c, m, title, excel) in OOXML.items():
        PP.normalize_ooxml(os.path.join(out, K.FILES[k]), cr, lb, c, m, title=title, excel=excel)
    for f in os.listdir(out):
        os.utime(os.path.join(out, f), (MTIME, MTIME))


def finish_golden(golden):
    import postprocess as PP
    PP.COMPANY = K.COMPANY
    PP.normalize_ooxml(os.path.join(golden, K.DELIVERABLES[0]), K.REQUESTER, K.REQUESTER, "2026-11-18T16:42:00Z",
                       "2026-11-24T22:05:00Z", title="Commercial Fleet Safety Programme: coverage 2027", excel=True)
    PP.normalize_ooxml(os.path.join(golden, K.DELIVERABLES[1]), K.REQUESTER, K.REQUESTER, "2026-11-20T15:10:00Z",
                       "2026-11-25T19:48:00Z", title="Commercial Fleet Safety Programme: coverage 2027", excel=False)
    for f in os.listdir(golden):
        os.utime(os.path.join(golden, f), (MTIME, MTIME))


def metadata(fig, counts):
    src = ("constructed by the task generator (seeded); %s, its cities, agencies, operators, platforms, crashes and "
           "people are fictional; the crash report fields follow the Model Minimum Uniform Crash Criteria and the "
           "traffic counts the Federal Highway Administration's Traffic Monitoring Guide" % K.REGION)
    return {
        "task": "task273",
        "title": "%s: the commercial vehicle uses the Commercial Fleet Safety Programme covers from 1 July 2027"
                 % K.COMMISSION,
        "domain": "General Statistics & Data Science (missing data, censoring and measurement error)",
        "objective": "Descriptive & Distribution Analysis",
        "distractor_files": ["target/" + K.FILES[k] for k in K.DISTRACTORS],
        "deliverables": list(K.DELIVERABLES),
        "provenance": {name: {"source": src, "date": "2026-10-22", "licence": "CC0 1.0 (constructed for this task)"}
                       for name in sorted(K.FILES.values())},
        "rows": {K.FILES[k]: v for k, v in sorted(counts.items())},
        "answer": "%d uses covered: %s" % (fig["call"]["count"], ", ".join(fig["call"]["covered"])),
    }


def main_build(target, golden, seed=K.SEED):
    import deliver as DV
    b = build(target, seed, keep=True)
    finish(target)
    if os.path.exists(golden):
        shutil.rmtree(golden)
    fig, res = DV.write(target, golden)
    finish_golden(golden)
    DV.write_figures(os.path.join(HERE, "figures.json"), fig)
    with open(os.path.join(TASK, "metadata.json"), "w") as f:
        json.dump(metadata(fig, b["counts"]), f, indent=1, sort_keys=True)
        f.write("\n")
    return b, fig, res


def digest(folder):
    return {f: hashlib.sha256(open(os.path.join(folder, f), "rb").read()).hexdigest() for f in sorted(os.listdir(folder))}


def cut_zip(target, path):
    import zipfile
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(os.listdir(target)):
            zi = zipfile.ZipInfo(f, date_time=K.ASSEMBLED.timetuple()[:6])
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, open(os.path.join(target, f), "rb").read())


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--out")
    ap.add_argument("--golden", action="store_true")
    ap.add_argument("--seed", type=int, default=K.SEED)
    a = ap.parse_args()
    if a.out:
        b = build(a.out, a.seed)
        finish(a.out)
        print(b["counts"])
        sys.exit(0)
    target, golden = os.path.join(TASK, "target"), os.path.join(TASK, "golden")
    b, fig, res = main_build(target, golden, a.seed)
    print("pack:", b["counts"])
    print("call:", fig["call"])
    if a.golden:
        sys.exit(0)
    import checks
    import verify
    rc = checks.run(TASK, b, fig, res)
    rv = verify.run(TASK)
    scratch = os.path.join(TASK, "_rebuild_check")
    build(os.path.join(scratch, "target"), a.seed)
    finish(os.path.join(scratch, "target"))
    import deliver as DV
    DV.write(os.path.join(scratch, "target"), os.path.join(scratch, "golden"))
    finish_golden(os.path.join(scratch, "golden"))
    d1, d2 = digest(target), digest(os.path.join(scratch, "target"))
    g1, g2 = digest(golden), digest(os.path.join(scratch, "golden"))
    same = d1 == d2 and g1 == g2
    for f in sorted(set(d1) | set(g1)):
        if d1.get(f, g1.get(f)) != d2.get(f, g2.get(f)):
            print("  differs on rebuild:", f)
    shutil.rmtree(scratch)
    print("second build byte-identical:", same)
    cut_zip(target, os.path.join(TASK, "target.zip"))
    print("target.zip:", hashlib.md5(open(os.path.join(TASK, "target.zip"), "rb").read()).hexdigest())
    sys.exit(0 if (rc == 0 and rv == 0 and same) else 1)
