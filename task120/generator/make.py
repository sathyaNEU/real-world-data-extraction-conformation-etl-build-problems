"""Build the pack and the goldens, write metadata.json and figures.json, run every check and the independent
verifier, build a second time into a scratch folder and require byte-identical output, then cut target.zip.

    python3 task120/generator/make.py [--once]
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
import asks as A
import checks as C
import core
import docs as D
import golden as GD
import pack as P
import verify as V
import world as WD

TASK = os.path.dirname(HERE)
TARGET = os.path.join(TASK, "target")
GOLDEN = os.path.join(TASK, "golden")
STAMP = 1791860400          # 12 October 2026, 23:00 local

SOURCES = {
    "scada": "Water SCADA historian export: hourly samples of 27 tags, 1 October 2025 to 1 October 2026 (UTC)",
    "tags": "Water SCADA tag list",
    "readme": "Readme of the SCADA historian export",
    "log": "Water operators' daily log, October 2025 to 11 October 2026",
    "tests": "Well pump test records 2021 to 2026 and well data",
    "facilities": "Campus water system facilities summary (revised July 2026)",
    "letter": "State drinking water program's 2026 sanitary survey letter (15 September 2026)",
    "amr": "AMR fixed network month-end register reads, 1 October 2025 to 1 October 2026",
    "meters": "Meter shop's meter inventory (8 October 2026)",
    "cmms": "CMMS water work orders, opened 1 October 2025 to 9 October 2026",
    "space": "Office of Space Management building inventory (30 September 2026)",
    "lsl": "Service line inventory filed 15 October 2024",
    "weather": "Campus weather station daily record, October 2025 to September 2026",
    "irrigation": "Grounds Department irrigation controller programs, 2026 season",
    "ccr": "Borough water authority's 2025 drinking water quality report",
    "index": "Records index of the survey response",
    "guide": "Field guide to the water records",
}


def write_all(target, golden):
    if os.path.isdir(target):
        shutil.rmtree(target)
    os.makedirs(target)
    W = WD.build()
    final = A.meters(W)
    n_samples = P.write_scada(W, target)
    rows = n_samples * len(P.TAGS)
    P.write_log(W, target)
    P.write_tests(target)
    P.write_meters(final, target)
    amr_n, amr_dup = P.write_amr(final, target)
    cmms_n = P.write_cmms(W, final, target)
    P.write_space(target)
    P.write_lsl(final, target)
    P.write_weather(W, target)
    P.write_irrigation(target)
    D.letter_pdf(os.path.join(target, P.FILES["letter"]))
    D.facilities_docx(os.path.join(target, P.FILES["facilities"]))
    D.readme_txt(os.path.join(target, P.FILES["readme"]), P.FILES, n_samples, rows)
    D.guide_txt(os.path.join(target, P.FILES["guide"]), P.FILES)
    D.index_csv(os.path.join(target, P.FILES["index"]), P.FILES)
    D.ccr_pdf(os.path.join(target, P.FILES["ccr"]))
    F = AN.main_figures(W)
    G = AN.ask_figures(W, final)
    GD.write(golden, F, G, W)
    for f in os.listdir(target):
        os.utime(os.path.join(target, f), (STAMP, STAMP))
    info = dict(samples=n_samples, scada_rows=rows, amr_rows=amr_n, amr_dup=amr_dup, cmms_rows=cmms_n)
    return W, final, F, G, info


def rows_of(path):
    if path.endswith(".csv"):
        with open(path, encoding="utf-8") as f:
            return sum(1 for _ in f) - 1
    return None


def metadata():
    files = []
    for k, f in sorted(P.FILES.items(), key=lambda x: x[1]):
        pth = os.path.join(TARGET, f)
        files.append({"path": f, "format": f.rsplit(".", 1)[1], "bytes": os.path.getsize(pth), "rows": rows_of(pth),
                      "source": "Constructed: " + SOURCES[k], "date": "2026-10-12",
                      "license": "CC BY 4.0 (original work, constructed for this task)"})
    big = max((x for x in files if x["rows"]), key=lambda x: x["rows"])
    meta = {
        "task": "task120",
        "title": "The well capacity a university's campus water system must add before June 2027 so that its wells, "
                 "with the largest out of service, would have met the most water the campus used on any day of the "
                 "twelve months to September 2026, with the year's water audit",
        "domain": "Energy Systems & Utilities",
        "subdomain": "generation capacity planning (water source capacity against maximum-day demand)",
        "objective": "Opportunity Sizing & Decision Support",
        "prompt_shape": "other: the call and its three components (the maximum day, the water used on it, the firm "
                        "capacity), the water lost in each of twelve months with the year and its share and a bar per "
                        "month, and the year's water used by four building groups",
        "as_of": "2026-10-12",
        "deliverables": [GD.XLSX, GD.DOCX],
        "distractor_files": [P.FILES[k] for k in P.DISTRACTORS],
        "input_gates": {"files": len(files), "formats": sorted({x["format"] for x in files}),
                        "largest_file": big["path"], "largest_file_rows": big["rows"]},
        "sources": [{"files": "all files under target/",
                     "origin": "constructed for this task by task120/generator/make.py (seeded, deterministic) "
                               "around a fictional university, its campus water system, borough and people; the "
                               "Pennsylvania Department of Environmental Protection is named as the state regulator, "
                               "and every record, reading and figure is invented.",
                     "date": "2026-10-12", "license": "CC BY 4.0 (original work)"}],
        "created": "2026-10-12",
        "generator": "task120/generator/make.py",
        "files": files,
    }
    with open(os.path.join(TASK, "metadata.json"), "w") as f:
        json.dump(meta, f, indent=1)
        f.write("\n")


def g(x):
    return "{:,}".format(int(x))


def figures_json(W, final, F, G, info):
    gold = G["gold"]
    gr = F["grid"]
    out = {
        "call_gpm": F["call"],
        "gap_gpm": "%.2f" % F["gap"],
        "maximum_day": F["gold_day"].strftime("%B %-d, %Y"),
        "maximum_day_iso": F["gold_day"].isoformat(),
        "water_used_on_maximum_day": g(F["gold_use"]),
        "production_on_maximum_day": g(F["gold_P"]),
        "tanks_gave_up_on_maximum_day": g(-F["gold_dS"]),
        "maximum_day_demand_gpm": "{:,.1f}".format(F["gold_use"] / 1440.0),
        "minutes_a_day": 1440,
        "w3_register_max": "{:,}".format(core.W3_REGISTER - 1),
        "annex_building_no": core.ANNEX["no"],
        "firm_capacity_gpm": F["firm"],
        "firm_capacity_gal_per_day": g(F["firm_gal"]),
        "tested_capacity_gpm": {w: core.TESTED[w] for w in core.WELLS},
        "largest_well": core.LARGEST,
        "evaluation_days": len(F["days"]),
        "window": ["October 1, 2025", "September 30, 2026"],
        "default_path": {"day": F["R0"]["day"].strftime("%B %-d, %Y"), "production": g(F["R0"]["figure"]),
                         "gap_gpm": "%.1f" % F["R0"]["gap"], "call": "none"},
        "rungs": {
            "main_zone_tanks_only": {"day": F["R1"]["day"].isoformat(), "figure": g(F["R1"]["figure"]),
                                     "call_gpm": F["R1"]["call"]},
            "utc_days": {"day": F["R2"]["day"].isoformat(), "figure": g(F["R2"]["figure"]),
                         "call_gpm": F["R2"]["call"]},
            "daily_mean_storage": {"day": F["R3"]["day"].isoformat(), "figure": g(F["R3"]["figure"]),
                                   "call_gpm": F["R3"]["call"] or "none"},
        },
        "grid": {"%s/%s" % k: {"day": v["day"].isoformat(), "figure": g(round(v["figure"])),
                               "gap_gpm": "%.1f" % v["gap"], "call": v["call"] or "none"} for k, v in gr.items()},
        "rolling_24h": {"figure": g(F["rolling"]["figure"]), "start_utc": F["rolling"]["start"].isoformat()},
        "golden_day_production_rank": F["gold_prod_rank"],
        "second_largest_use": g(F["second_use"]),
        "water_lost_by_month": [{"month": GD.MONTH_NAMES[k], "used": g(gold["used"][k]),
                                 "delivered": g(gold["metered"][k]), "lost": g(gold["lost"][k])} for k in range(12)],
        "water_lost_year": g(gold["year"]),
        "water_used_year": g(gold["used_year"]),
        "delivered_year": g(sum(gold["metered"])),
        "water_loss_percentage": G["share_r"],
        "groups": {GD.GROUP_NAMES[k]: g(gold["groups"][k]) for k in A.GROUPS},
        "ask_stops": {
            "sub_meters_summed": {"year": g(G["stops"][(True, True, True, True, "used")]["year"]),
                                  "share": "%.1f" % G["stops"][(True, True, True, True, "used")]["share"]},
            "vault_meters_missing": {"year": g(G["stops"][(False, False, True, True, "used")]["year"]),
                                     "share": "%.1f" % G["stops"][(False, False, True, True, "used")]["share"]},
            "both": {"year": g(G["stops"][(True, False, True, True, "used")]["year"]),
                     "share": "%.1f" % G["stops"][(True, False, True, True, "used")]["share"]},
            "partials_dropped": {"year": g(G["stops"][(False, True, False, True, "used")]["year"]),
                                 "share": "%.1f" % G["stops"][(False, True, False, True, "used")]["share"]},
            "production_as_used": {"year": g(G["stops"][(False, True, True, True, "prod")]["year"]),
                                   "share": "%.1f" % G["stops"][(False, True, True, True, "prod")]["share"]},
            "groups_sub_meters_summed": {GD.GROUP_NAMES[k]: g(G["gstops"][(True, True, True, True, "golden")][k])
                                         for k in A.GROUPS},
            "groups_building_47_current": {GD.GROUP_NAMES[k]: g(G["gstops"][(False, True, True, True, "current")][k])
                                           for k in A.GROUPS},
            "groups_annex_dropped": {GD.GROUP_NAMES[k]: g(G["gstops"][(False, True, True, True, "drop")][k])
                                     for k in A.GROUPS},
        },
        "pack": {"scada_rows": info["scada_rows"], "amr_rows": info["amr_rows"], "amr_resent_rows": info["amr_dup"],
                 "cmms_rows": info["cmms_rows"], "meters": len(final), "sub_meters": sum(m["sub"] for m in final),
                 "vault_meters": sum(m["vault"] for m in final)},
    }
    return out


def main():
    W, final, F, G, info = write_all(TARGET, GOLDEN)
    metadata()
    n, cells = C.run(W, final, F, G, TARGET, GOLDEN, TASK, info)
    print("checks: %d assertions green (%d composition cells)" % (n, cells))
    fj = figures_json(W, final, F, G, info)
    with open(os.path.join(HERE, "figures.json"), "w") as fh:
        json.dump(fj, fh, indent=1)
        fh.write("\n")
    v = V.run(TARGET)
    gold = G["gold"]
    assert v["day"] == F["gold_day"] and v["use"] == F["gold_use"] and v["call"] == F["call"], (v["day"], v["use"])
    assert v["firm"] == F["firm"] and v["default_day"] == F["R0"]["day"] and v["default_P"] == F["R0"]["figure"]
    assert v["lost"] == gold["lost"] and v["year"] == gold["year"] and v["share"] == G["share_r"], (v["lost"], v["share"])
    assert v["groups"] == gold["groups"], v["groups"]
    print("verifier: green (call %d gpm, %s used on %s, loss %s%%)" % (v["call"], g(v["use"]), v["day"], v["share"]))
    if "--once" not in sys.argv:
        tmp = tempfile.mkdtemp()
        t2, g2 = os.path.join(tmp, "target"), os.path.join(tmp, "golden")
        write_all(t2, g2)
        for a, b in ((TARGET, t2), (GOLDEN, g2)):
            fa, fb = sorted(os.listdir(a)), sorted(os.listdir(b))
            assert fa == fb
            for x in fa:
                assert filecmp.cmp(os.path.join(a, x), os.path.join(b, x), shallow=False), x
        shutil.rmtree(tmp)
        print("second build: byte-identical (%d pack files, %d goldens)" % (len(os.listdir(TARGET)),
                                                                          len(os.listdir(GOLDEN))))
    zp = os.path.join(TASK, "target.zip")
    with zipfile.ZipFile(zp, "w", zipfile.ZIP_DEFLATED) as z:
        for x in sorted(os.listdir(TARGET)):
            zi = zipfile.ZipInfo(x, date_time=(2026, 10, 12, 23, 0, 0))
            zi.compress_type = zipfile.ZIP_DEFLATED
            with open(os.path.join(TARGET, x), "rb") as fh:
                z.writestr(zi, fh.read())
    print("target.zip cut (%d bytes)" % os.path.getsize(zp))


if __name__ == "__main__":
    main()
