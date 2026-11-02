"""Build task277: the planning folder into <task>/target, the goldens into <task>/golden, metadata.json and
generator/figures.json; then the checks, the independent verifier, a second build compared byte for byte, and
target.zip from the final build.

    python3 task277/generator/build.py              everything
    python3 task277/generator/build.py --out DIR    the pack only, into DIR
"""
import argparse
import datetime as dt
import hashlib
import json
import os
import shutil
import subprocess
import sys
import time
import warnings
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
warnings.filterwarnings("ignore")

import docs as D      # noqa: E402
import golden as G    # noqa: E402
import pack as K      # noqa: E402
import params as P    # noqa: E402
import world as W     # noqa: E402

TASK = os.path.dirname(HERE)
STAMP = time.mktime(dt.datetime(2027, 1, 4, 9, 41).timetuple())


def closeout_table(w, pack_info):
    h = G.history(w)
    o = w["orders"]
    late = o["dispatch_min"] > 23 * 60
    o = o.assign(month=[d.month for d in o["day"]], late=late)
    disp = o.groupby("month")["late"].mean()
    import pandas as pd
    counts = pd.read_csv(os.path.join(pack_info["out"], K.FILES["counts"]))
    counts["month"] = pd.to_datetime(counts["count_date"]).dt.month
    inv = counts.assign(ok=counts["system_qty"] == counts["counted_qty"]).groupby("month")["ok"].mean()
    reg = w["register"]
    rec = pd.Series([d.month for d in reg["received"] if d.year == 2026]).value_counts()
    names = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
             "November", "December"]
    rows = []
    for m in range(1, 13):
        rows.append([names[m - 1], "{:,}".format(int(h.loc[m, "lines"])), "%.2f%%" % h.loc[m, "accuracy"],
                     "%.1f%%" % (100 * (1 - disp[m])), "%.2f%%" % (100 * inv[m]), str(int(rec.get(m, 0)))])
    rise = 100.0 * (h.loc[12, "lines"] / h.loc[11, "lines"] - 1)
    ppl = w["people"]
    inducted = int(((ppl["first"] >= dt.date(2026, 11, 1)) & (ppl["first"] <= dt.date(2026, 12, 31))).sum())
    late_dec = int(o[(o["month"] == 12) & o["late"]].shape[0])
    words = {0: "No", 1: "One", 2: "Two", 3: "Three", 4: "Four", 5: "Five", 6: "Six", 7: "Seven", 8: "Eight", 9: "Nine"}
    notes = ["December volume ran %d per cent above November, with %s agency pickers inducted in November and December; pick "
             "accuracy was %.2f per cent. %s retail orders left the site after 23:00 in December." % (
                 int(round(rise)), words.get(inducted, str(inducted)).lower(), h.loc[12, "accuracy"], words.get(late_dec, str(late_dec))),
             "Cycle counts covered the fast-moving faces in the retail aisles; differences were corrected the same day."]
    return rows, notes


def write_pack(out, w):
    if os.path.exists(out):
        shutil.rmtree(out)
    os.makedirs(out)
    info = K.write_all(out, w)
    info["out"] = out
    D.write_schedule(os.path.join(out, K.FILES["sla"]))
    D.write_pcn(os.path.join(out, K.FILES["pcn"]))
    rows, notes = closeout_table(w, info)
    D.write_closeout(os.path.join(out, K.FILES["closeout"]), rows, notes)
    for f in os.listdir(out):
        os.utime(os.path.join(out, f), (STAMP, STAMP))
    return info


def figures(w):
    h = G.history(w)
    f = G.forecast(w)
    out = {"forecast": {}, "history": {int(m): round(float(h.loc[m, "accuracy"]), 2) for m in h.index}}
    for m in (2, 3):
        x = f[m]
        out["forecast"][m] = dict(plan=int(x["plan"]), plan_T=int(x["plan_T"]), plan_W=int(x["plan_W"]),
                                  fail=float(x["fail"]), fail_r=G.nearest(x["fail"], 10),
                                  accuracy=float(x["accuracy"]), acc_r=round(float(x["accuracy"]) + 1e-12, 1),
                                  holds=bool(x["holds"]))
    pk = G.picked(w)
    out["hep_table"] = {s: dict(lines=int((pk["struct"] == s).sum()), fails=int(pk.loc[pk["struct"] == s, "fail"].sum()),
                                rate=float(pk.loc[pk["struct"] == s, "fail"].mean())) for s in ("whole", "loose", "mixed")}
    out["claims"] = G.claims_units(w)
    out["rungs"] = {k: {m: round(float(v[m]["accuracy"]), 3) for m in (2, 3)} for k, v in G.rungs(w).items()}
    return out


def figures_json(fig, path):
    flat = {
        "feb_failing_lines": fig["forecast"][2]["fail_r"], "mar_failing_lines": fig["forecast"][3]["fail_r"],
        "feb_accuracy": "%.1f" % fig["forecast"][2]["acc_r"], "mar_accuracy": "%.1f" % fig["forecast"][3]["acc_r"],
        "feb_plan_lines": fig["forecast"][2]["plan"], "mar_plan_lines": fig["forecast"][3]["plan"],
        "target": "99.80",
        "hep_whole_pct": "%.3f" % (100 * fig["hep_table"]["whole"]["rate"]),
        "hep_loose_pct": "%.3f" % (100 * fig["hep_table"]["loose"]["rate"]),
        "hep_mixed_pct": "%.3f" % (100 * fig["hep_table"]["mixed"]["rate"]),
        "lines_whole": fig["hep_table"]["whole"]["lines"], "lines_loose": fig["hep_table"]["loose"]["lines"],
        "lines_mixed": fig["hep_table"]["mixed"]["lines"], "fails_whole": fig["hep_table"]["whole"]["fails"],
        "fails_loose": fig["hep_table"]["loose"]["fails"], "fails_mixed": fig["hep_table"]["mixed"]["fails"],
        "history": {str(k): "%.2f" % v for k, v in fig["history"].items()},
        "claims": {"%s_Q%d" % k: v for k, v in fig["claims"].items()},
        "claims_year": {g: sum(fig["claims"][(g, q)] for q in (1, 2, 3, 4)) for g in G.GROUP_ORDER},
        "rungs": {k: {str(m): "%.2f" % v[m] for m in (2, 3)} for k, v in fig["rungs"].items()},
        "rungs_fail": {},
    }
    json.dump(flat, open(path, "w"), indent=1, sort_keys=True)
    open(path, "a").write("\n")


def digest(folder):
    h = hashlib.sha256()
    for f in sorted(os.listdir(folder)):
        h.update(f.encode())
        h.update(open(os.path.join(folder, f), "rb").read())
    return h.hexdigest()


def zip_target(folder, path):
    if os.path.exists(path):
        os.remove(path)
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(os.listdir(folder)):
            zi = zipfile.ZipInfo("target/" + f, date_time=(2027, 1, 4, 9, 41, 0))
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, open(os.path.join(folder, f), "rb").read())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out")
    ap.add_argument("--fast", action="store_true")
    args = ap.parse_args()
    t0 = time.time()
    w = W.build()
    if args.out:
        write_pack(args.out, w)
        print("pack", args.out, digest(args.out))
        return
    target = os.path.join(TASK, "target")
    write_pack(target, w)
    fig = figures(w)
    figures_json(fig, os.path.join(HERE, "figures.json"))
    gold = os.path.join(TASK, "golden")
    os.makedirs(gold, exist_ok=True)
    import deliver as DL
    DL.workbook(os.path.join(gold, "venlo_accuracy_forecast_feb_mar_2027.xlsx"), fig)
    DL.chart(os.path.join(gold, "siersma_pick_accuracy_q1_2027.png"), fig)
    import metadata as M
    M.write(os.path.join(TASK, "metadata.json"), target)
    print("built in %.0fs" % (time.time() - t0), digest(target))
    if args.fast:
        return
    for script in ("checks.py", "verify.py"):
        r = subprocess.run([sys.executable, os.path.join(HERE, script)], capture_output=True, text=True)
        print(r.stdout[-3000:])
        if r.returncode:
            print(r.stderr[-3000:])
            sys.exit("%s failed" % script)
    scratch = os.path.join(TASK, ".rebuild")
    r = subprocess.run([sys.executable, os.path.abspath(__file__), "--out", scratch], capture_output=True, text=True)
    second = r.stdout.strip().split()[-1] if r.stdout.strip() else ""
    first = digest(target)
    shutil.rmtree(scratch, ignore_errors=True)
    print("rebuild", "IDENTICAL" if first == second else "DIFFERENT", first[:16], second[:16])
    if first != second:
        sys.exit("rebuild differs")
    zip_target(target, os.path.join(TASK, "target.zip"))
    print("target.zip", hashlib.sha256(open(os.path.join(TASK, "target.zip"), "rb").read()).hexdigest()[:16])


if __name__ == "__main__":
    main()
