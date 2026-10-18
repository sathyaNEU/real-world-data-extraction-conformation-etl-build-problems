"""Build task268: the evidence pack into <task>/target, the goldens into <task>/golden, metadata.json and
generator/figures.json, then the checks and the independent verifier, then a second full build into a scratch folder
inside the task (removed after) compared byte for byte, then target.zip cut from the final build.

    python3 task268/generator/build.py              everything
    python3 task268/generator/build.py --out DIR    the pack only, into DIR
    python3 task268/generator/build.py --golden     the pack and the goldens, no checks"""
import os
for _v in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "1")
import argparse      # noqa: E402
import calendar      # noqa: E402
import datetime as dt  # noqa: E402
import hashlib       # noqa: E402
import shutil        # noqa: E402
import sys           # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import askworld as AW      # noqa: E402
import common as K         # noqa: E402
import docs as D           # noqa: E402
import postprocess as PP   # noqa: E402
import records as R        # noqa: E402
import world as W          # noqa: E402

TASK = os.path.dirname(HERE)
EXPORT = dt.datetime(2026, 11, 6, 15, 12)               # the science office's pack, UK time (GMT)
MTIME = calendar.timegm(EXPORT.timetuple())
GEAR_TRIAL = [["Haddock 30 cm and over", "1,846.2", "1,712.9", "-7%"], ["Haddock under 30 cm", "212.4", "113.8", "-46%"],
              ["Whiting", "934.7", "618.0", "-34%"], ["Cod", "288.3", "276.5", "-4%"], ["Saithe", "141.0", "139.2", "-1%"]]


def world(seed=W.SEED):
    T = W.build(seed)
    T["licences"] = AW.licences(T)
    T["notes"] = AW.sales_notes(T)
    T["ledger"], T["ledger_info"] = AW.ledger(T, T["notes"], T["licences"])
    return T


def build(out, seed=W.SEED):
    if os.path.exists(out):
        shutil.rmtree(out)
    os.makedirs(out)
    p = lambda k: os.path.join(out, K.FILES[k])
    T = world(seed)
    n = {}
    n["grid"] = R.write_grid(p("grid"), T)
    n["paper"] = R.write_paper(p("paper"), T)
    n["elog"] = R.write_elog(p("elog"), T)
    n["survey"] = R.write_survey(p("survey"), T)
    n["factors"] = R.write_factors(p("factors"))
    n["members"] = R.write_members(p("members"), T, T["licences"])
    n["notes"] = R._csv(p("notes"), ["note_no", "buyer_reg", "buyer", "issued", "port", "landing_date", "vessel_pln", "line",
                                     "species", "presentation", "grade", "boxes", "weight_kg", "price_per_kg", "value_gbp"],
                        AW.note_rows(T["notes"]))
    n["ledger"] = R._csv(p("ledger"), ["entry_no", "effective", "posted", "pool", "licence", "type", "tonnes", "reference"],
                         T["ledger"])
    n["temperature"] = R.write_temperature(p("temperature"), T)
    grounds = []
    for g in K.GROUND_NAMES:
        cs = [c for c in T["cells"] if c["ground"] == g]
        grounds.append((g, K.GROUND_CODE[g], len(cs), sum(c["area"] for c in cs)))
    D.write_plan(p("plan"), grounds)
    st = {s["id"]: s for s in T["stations"]}
    replaced = sorted((s["replaces"], s["id"]) for s in T["stations"] if s.get("replaces"))
    missed = sorted(T["missed"])[0][0]
    charter = sorted(T["vessels"], key=lambda v: v["name"])[3]["name"]
    D.MANUAL_HISTORY[:] = []
    for y in (2019, 2020, 2021, 2022):
        ds = sorted(t["date"] for t in T["tows"] if t["year"] == y)
        note = {2019: "first survey", 2020: "station %s not fished (weather)" % missed, 2021: "",
                2022: "net torn at %s" % " and ".join(r[0] for r in replaced)}[y]
        D.MANUAL_HISTORY.append((str(y), ds[0].strftime("%d %b"), ds[-1].strftime("%d %b"), len(ds), note))
    D.write_manual(p("manual"), replaced, missed, charter)
    D.write_rules(p("rules"))
    D.write_gear_trial(p("gear_trial"), GEAR_TRIAL)
    from pypdf import PdfReader
    for k in ("plan", "manual", "rules", "gear_trial"):
        n[k + "_pages"] = len(PdfReader(p(k)).pages)
    D.write_contents(p("contents"), contents(n))
    PP.COMPANY = K.ORG_LTD
    PP.normalize_ooxml(p("members"), "Membership office", K.PEOPLE["science"], "2019-02-04T09:12:40Z",
                       "2026-10-29T14:31:02Z", excel=True)
    PP.normalize_pdf(p("plan"), b"D:20260325101208+00'00'", b"D:20260325101208+00'00'")
    PP.normalize_pdf(p("manual"), b"D:20230904142231+01'00'", b"D:20230904153716+01'00'")
    PP.normalize_pdf(p("rules"), b"D:20260112091544+00'00'", b"D:20260112093310+00'00'")
    PP.normalize_pdf(p("gear_trial"), b"D:20251218113005+00'00'", b"D:20251218114420+00'00'")
    for f in sorted(os.listdir(out)):
        os.utime(os.path.join(out, f), (MTIME, MTIME))
    T["n"] = n
    return T


def contents(n):
    F = K.FILES
    pg = lambda k: "%d pages" % n[k + "_pages"] if n[k + "_pages"] != 1 else "1 page"
    rw = lambda k: "{:,} rows".format(n[k])
    return [
        ["File", "What it holds", "Kept by", "As at", "Size"],
        [F["plan"], "Haddock stock recovery plan, adopted 24 March 2026", "Management committee", "2026-03-24", pg("plan")],
        [F["grid"], "Annex A to the plan: the grid cells of the six grounds", "Science office", "2026-03-24", rw("grid")],
        [F["paper"], "Members' paper tow sheets 2019 to 2022, keyed in", "Science office", "2023-02-17", rw("paper")],
        [F["elog"], "Members' e-logbook hauls, January 2023 to October 2026", "E-logbook app export", "2026-11-02", rw("elog")],
        [F["survey"], "Autumn gear and bycatch survey tows, 2019 to 2026", "Science office", "2026-10-30", rw("survey")],
        [F["manual"], "Autumn survey field manual, revision 3", "Science office", "2023-09-04", pg("manual")],
        [F["members"], "Member vessels, their registrations and licences", "Membership office", "2026-10-29",
         "%d vessels" % n["members"]],
        [F["factors"], "Live-weight conversion factors used by the landings system", "Landings system", "2026-11-02",
         rw("factors")],
        [F["notes"], "Buyers' sales notes issued 1 January to 2 November 2026", "Landings system export", "2026-11-02",
         rw("notes")],
        [F["ledger"], "Haddock quota ledger 2026", "Quota office", "2026-11-03", rw("ledger")],
        [F["rules"], "Quota management rules 2026: haddock", "Management committee", "2026-01-12", pg("rules")],
        [F["temperature"], "Sea temperatures from members' net sensors, by rectangle and month", "Science office",
         "2026-11-02", rw("temperature")],
        [F["gear_trial"], "Square-mesh panel trial, autumn 2025: note to members", "Science office", "2025-12-18",
         pg("gear_trial")],
    ]


def tree_digest(d):
    h = hashlib.sha256()
    for f in sorted(os.listdir(d)):
        h.update(f.encode())
        h.update(open(os.path.join(d, f), "rb").read())
    return h.hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out")
    ap.add_argument("--golden", action="store_true")
    ap.add_argument("--seed", type=int, default=W.SEED)
    a = ap.parse_args()
    if a.out:
        T = build(a.out, a.seed)
        print("pack:", T["n"])
        return
    target = os.path.join(TASK, "target")
    T = build(target)
    print("pack:", T["n"])
    import deliver
    deliver.write(target, os.path.join(TASK, "golden"), T)
    if a.golden:
        return
    import checks
    checks.run(target, T)
    r = os.system("python3 %s %s" % (os.path.join(HERE, "verify.py"), target))
    assert r == 0, "verify failed"
    scratch = os.path.join(TASK, ".rebuild")
    build(scratch)
    same = tree_digest(scratch) == tree_digest(target)
    shutil.rmtree(scratch)
    assert same, "second build differs"
    print("rebuild byte-identical")
    zp = os.path.join(TASK, "target.zip")
    if os.path.exists(zp):
        os.remove(zp)
    import zipfile
    with zipfile.ZipFile(zp, "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(os.listdir(target)):
            zi = zipfile.ZipInfo("target/" + f, date_time=EXPORT.timetuple()[:6])
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, open(os.path.join(target, f), "rb").read())
    print("target.zip cut")


if __name__ == "__main__":
    main()
