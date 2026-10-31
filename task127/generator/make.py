"""Build the pack and the goldens, write metadata.json and figures.json, run every check and the independent
verifier, build a second time into a scratch folder and require byte-identical output, then cut target.zip.

    python3 task127/generator/make.py [--once] [--target DIR]
"""
import datetime as dt
import filecmp
import json
import os
import shutil
import sys
import tempfile
import zipfile
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import analysis as AN
import core
import golden as GD
import pack as P
import records as RC

TASK = os.path.dirname(HERE)
TARGET = os.path.join(TASK, "target")
GOLDEN = os.path.join(TASK, "golden")
STAMP = 1791561000          # 9 October 2026, 16:30 BST, when System Flow assembled the pack


def bin_ok(k, S, c):
    """The part-filled hospital's bed-days sit mid-bin, and rounding the value to two or three places first gives
    the same whole number."""
    x = Fraction(k * S, c)
    frac = x - int(x)
    r = lambda v: int(v + Fraction(1, 2))
    v2 = Fraction(round(S / c, 2)).limit_denominator(100) * k
    v3 = Fraction(round(S / c, 3)).limit_denominator(1000) * k
    return Fraction(1, 5) <= frac <= Fraction(4, 5) and r(x) == r(v2) == r(v3)


def clearance(R):
    """C1 by construction: bring equipment deliveries forward a day at the part-filled hospital until its bed-days
    sit mid-bin under every rounding of the value."""
    caps, save = {s: 0 for s in core.SITES}, {s: 0 for s in core.SITES}
    for sp in R["spells"]:
        if (sp["pathway"] == 1 and sp["p1"] == "New" and core.in_winter(sp["ready"]) and sp["home"] != "Severnside"):
            caps[sp["site"]] += 1
            save[sp["site"]] += max(0, (sp["dis_t"].date() - max(sp["ready"], sp["equip"] or sp["ready"])).days)
    val = {s: Fraction(save[s], caps[s]) for s in core.SITES}
    order, pk = AN.allocate(val, caps)
    part = [s for s in core.SITES if 0 < pk[s] < caps[s]]
    assert len(part) == 1, pk
    p = part[0]
    for n in range(0, 8):
        if bin_ok(pk[p], save[p] + n, caps[p]):
            if n:
                RC.nudge(R, p, n)
            return p, n
    raise AssertionError("no clearance found")


def build_target(target):
    if os.path.isdir(target):
        shutil.rmtree(target)
    os.makedirs(target)
    R = RC.build()
    part, n = clearance(R)
    subs = RC.submissions(R["spells"])
    ws = RC.ward_stays(R["spells"])
    eq = RC.equipment(R)
    refs = RC.referrals(R)
    inv = RC.spot_invoices(refs)
    c = {}
    c["spells"] = P.write_spells(R, subs, target)
    c["wards"] = P.write_wards(ws, target)
    P.write_wardref(target)
    P.write_practices(target)
    c["ices"] = P.write_ices(eq, target)
    c["brokerage"] = P.write_brokerage(refs, target)
    c["spot"] = P.write_spot(inv, target)
    P.write_postcodes(target)
    P.write_weekly(R["spells"], target)
    P.write_census(ws + RC.ward_stays(R["lates"]), target)
    P.write_reablement(target)
    P.write_docs(target, c)
    for f in os.listdir(target):
        os.utime(os.path.join(target, f), (STAMP, STAMP))
    return R, dict(counts=c, clearance=(part, n), refs=refs, eq=eq, subs=subs, ws=ws, inv=inv)


SOURCES = {
    "spells": "ICB data warehouse: acute discharges of patients aged 65 and over, Dec 2024 to Sep 2026",
    "wards": "ICB data warehouse: ward stays of the same spells",
    "wardref": "The two trusts' ward reference",
    "practices": "GP practice list (Marchshire and Severnside ICBs)",
    "ices": "Integrated community equipment service: order lines, Dec 2024 to Sep 2026",
    "brokerage": "County council brokerage: referrals for home care, Dec 2024 to Sep 2026",
    "spot": "County council finance: spot-care invoice lines, 2025-26",
    "postcodes": "County council postcode lookup",
    "guidance": "ICB allocation note SF-2026-14, Winter Discharge Fund 2026/27",
    "weekly": "National discharge collection as submitted by the two trusts (weekly, by trust)",
    "census": "Daily general and acute bed census by site",
    "reablement": "Reablement 91-day outcomes by district and quarter",
}


def metadata(target):
    def rows_of(p):
        return (sum(1 for _ in open(p, encoding="utf-8")) - 1) if p.endswith(".csv") else None
    files = []
    for k, f in sorted(P.FILES.items(), key=lambda x: x[1]):
        pth = os.path.join(target, f)
        files.append({"path": f, "format": f.rsplit(".", 1)[1], "bytes": os.path.getsize(pth), "rows": rows_of(pth),
                      "source": "Constructed: " + SOURCES[k], "date": "2026-10-12",
                      "license": "CC BY 4.0 (original work, constructed for this task)"})
    big = max((x for x in files if x["rows"]), key=lambda x: x["rows"])
    return {
        "task": "task127",
        "title": "Winter discharge-to-assess package split, 2026-27",
        "domain": "Healthcare Delivery & Health Economics",
        "subdomain": "patient flow, beds and workforce optimisation (discharge-to-assess packages)",
        "objective": "Opportunity Sizing & Decision Support",
        "prompt_shape": "05: an allocation of a fixed number of packages across hospitals with the bed-days they free, "
                        "referral starts by district and month, and delayed bed-days by hospital and month on a chart",
        "as_of": "2026-10-12",
        "deliverables": [GD.XLSX, GD.SVG],
        "distractor_files": [P.FILES[k] for k in P.DISTRACTORS],
        "input_gates": {"files": len(files), "formats": sorted({x["format"] for x in files}),
                        "largest_file": big["path"], "largest_file_rows": big["rows"]},
        "sources": [{"files": "all files under target/",
                     "origin": "constructed for this task by task127/generator/make.py (seeded, deterministic) around a "
                               "fictional English county, its integrated care board, two acute trusts, county council "
                               "and people; every record and figure is invented.",
                     "date": "2026-10-12", "license": "CC BY 4.0 (original work)"}],
        "files": files,
    }


def fmt(x):
    return "{:,}".format(int(x))


def figures(F, n_checks):
    M = F["M"]
    name = {s: core.HOSPITALS[s]["name"] for s in core.SITES}
    short = {s: core.HOSPITALS[s]["short"] for s in core.SITES}
    whole = lambda x: int(x + Fraction(1, 2))
    order = M["order"]
    out = {
        "call": "Give Royal Marchford Hospital %s packages, Wendlebury Hospital %s, Holmford Infirmary %s, Cleeve Park "
                "Hospital %s and Ashby Vale Hospital none; they free %s occupied bed-days."
                % (fmt(M["packages"]["RMC01"]), fmt(M["packages"]["RMC02"]), fmt(M["packages"]["RSM03"]),
                   fmt(M["packages"]["RSM02"]), fmt(whole(M["total"]))),
        "packages": {name[s]: fmt(M["packages"][s]) for s in order},
        "bed_days": {name[s]: fmt(whole(M["bed"][s])) for s in order},
        "bed_days_total": fmt(whole(M["total"])),
        "packages_total": fmt(sum(M["packages"].values())),
        "no_packages": [name[s] for s in M["none"]],
        "covered": {name[s]: fmt(M["caps"][s]) for s in order},
        "covered_total": fmt(sum(M["caps"].values())),
        "nights_per_package": {name[s]: "%.2f" % float(M["val"][s]) for s in order},
        "nights_saved_total": {name[s]: fmt(M["save"][s]) for s in order},
        "rung_R1_nights": {name[s]: "%.2f" % float(M["rungs"]["R1"][s]) for s in order},
        "rung_R1_packages": {name[s]: fmt(M["alloc"]["R1"][s]) for s in order},
        "rung_R1_bed_days": fmt(whole(sum(M["rung_bed"]["R1"].values()))),
        "ask_a": {name[s]: {core.MONTH_LABEL[m]: fmt(F["A"][(s, m)]) for m in core.ASK_MONTHS}
                  for s in sorted(core.SITES, key=lambda s: -sum(F["A"][(s, m)] for m in core.ASK_MONTHS))},
        "ask_a_patients": {name[s]: {core.MONTH_LABEL[m]: fmt(F["AP"][(s, m)]) for m in core.ASK_MONTHS}
                           for s in sorted(core.SITES, key=lambda s: -sum(F["A"][(s, m)] for m in core.ASK_MONTHS))},
        "ask_a_total": fmt(F["A_total"]),
        "ask_b": {dist: {core.MONTH_LABEL[m]: fmt(F["B"][(dist, m)]) for m in core.ASK_MONTHS}
                  for dist in core.DISTRICTS},
        "covered_with_equipment": fmt(F["X"]["with_equipment"]),
        "left_on_delivery_day": {name[s]: fmt(F["X"]["left_on_delivery"][s]) for s in order},
        "spot_closed_winter": fmt(F["X"]["spot_winter"]),
        "checks": n_checks,
    }
    return out


def zip_target(target, path):
    with zipfile.ZipFile(path, "w") as z:
        for f in sorted(os.listdir(target)):
            zi = zipfile.ZipInfo(f, date_time=(2026, 10, 9, 16, 30, 0))
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, open(os.path.join(target, f), "rb").read())


def main():
    once = "--once" in sys.argv
    target = TARGET
    if "--target" in sys.argv:
        target = sys.argv[sys.argv.index("--target") + 1]
    R, info = build_target(target)
    F = AN.main(target)
    golden_dir = GOLDEN if target == TARGET else os.path.join(os.path.dirname(target), "golden")
    GD.write(golden_dir, F)
    meta = metadata(target)
    import checks as C
    n = C.run(F, target, meta, R, info, golden_dir)
    print("checks: %d assertions green" % n)
    import verify as V
    v = V.run(target)
    V.agree(v, F)
    print("verifier: green")
    if target == TARGET:
        json.dump(meta, open(os.path.join(TASK, "metadata.json"), "w"), indent=1)
        json.dump(figures(F, n), open(os.path.join(HERE, "figures.json"), "w"), indent=1, ensure_ascii=False)
    if not once:
        tmp = tempfile.mkdtemp()
        t2 = os.path.join(tmp, "target")
        build_target(t2)
        F2 = AN.main(t2)
        GD.write(os.path.join(tmp, "golden"), F2)
        for f in sorted(os.listdir(target)):
            assert filecmp.cmp(os.path.join(target, f), os.path.join(t2, f), shallow=False), "not byte-identical: " + f
        for f in sorted(os.listdir(golden_dir)):
            assert filecmp.cmp(os.path.join(golden_dir, f), os.path.join(tmp, "golden", f), shallow=False), \
                "golden not byte-identical: " + f
        shutil.rmtree(tmp)
        print("rebuild: byte-identical (%d files, %d goldens)" % (len(os.listdir(target)), len(os.listdir(golden_dir))))
    if target == TARGET:
        zip_target(target, os.path.join(TASK, "target.zip"))
        print("target.zip written")


if __name__ == "__main__":
    main()
