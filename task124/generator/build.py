"""Build task124: the evidence pack into <task>/target, the goldens into <task>/golden, metadata.json and
generator/figures.json, then the checks and the independent verifier, then a second full build into a scratch folder
inside the task (removed after) compared byte for byte.

    python3 task124/generator/build.py              everything
    python3 task124/generator/build.py --out DIR    the pack only, into DIR"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import os
import shutil
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import asks as A           # noqa: E402
import common as K         # noqa: E402
import docs as D           # noqa: E402
import postprocess as PP   # noqa: E402
import records as R        # noqa: E402
import world as W          # noqa: E402

TASK = os.path.dirname(HERE)
EXPORT_STAMP = dt.datetime(2027, 1, 8, 21, 40, tzinfo=dt.timezone.utc)   # 4:40 pm Eastern, the extract's hand-off

EXTRACT_LOG_COLS = ["file", "system_of_record", "extracted_or_issued_on", "data_rows", "prepared_by", "scope"]


def simulate():
    segs, lines, sweeps, ev, projects = W.build()
    moved = A.redraw(segs, lines)
    lines, st, co = A.completions(lines)
    ag = A.agreements(lines, moved)
    return dict(segs=segs, lines=lines, sweeps=sweeps, ev=ev, projects=projects, moved=moved, st=st, co=co, ag=ag)


def progress_tables(inv, ver, comp):
    """The progress report's figures, from the rows the pack ships."""
    import pandas as pd
    v = ver[ver.source == "WMS"].copy()
    v["d"] = pd.to_datetime(v.verified_date)
    v = v[v.d.dt.year == 2026]
    verified_q = {q: int(v[v.d.dt.quarter == q].sl_id.nunique()) for q in (1, 2, 3, 4)}
    c = comp.copy()
    utc = pd.to_datetime(c.completed_utc, utc=True)
    c["local"] = utc.dt.tz_convert("America/New_York").dt.date
    c = c.drop_duplicates("site_id")
    replaced_q = {q: int(sum(1 for d in c.local if K.quarter_of(d) == q and d.year == 2026)) for q in (1, 2, 3, 4)}
    rep = inv[inv.replaced_on != ""]
    by_year = rep.replaced_on.str[:4].astype(int).value_counts().sort_index()
    return dict(verified_q=verified_q, verified_year=int(v.sl_id.nunique()), replaced_q=replaced_q,
                replaced_year=int(sum(replaced_q.values())),
                replaced_by_year={int(y): int(n) for y, n in by_year.items()},
                inventory={k: int((inv.sl_class == k).sum()) for k in ("LEAD", "GRR", "NON-LEAD",
                                                                          "LEAD STATUS UNKNOWN")})


def build(out, quiet=False, world=None):
    if os.path.exists(out):
        shutil.rmtree(out)
    os.makedirs(out)
    p = lambda f: os.path.join(out, f)
    w = world or simulate()
    lines, ev, st, co, ag = w["lines"], w["ev"], w["st"], w["co"], w["ag"]
    counts = {}
    inv = R.inventory(lines, ev)
    counts[K.INVENTORY] = R.write_csv(p(K.INVENTORY), R.INV_COLS, list(inv.itertuples(index=False)))
    ver = R.verifications(ev, lines)
    counts[K.VERIFICATIONS] = R.write_csv(p(K.VERIFICATIONS), R.VER_COLS, list(ver.itertuples(index=False)),
                                          crlf=True)
    counts[K.CROSSWALK] = R.write_csv(p(K.CROSSWALK), ["legacy_premise_no", "sl_id", "match_method", "migrated_on"],
                                      R.crosswalk(lines))
    counts[K.CODES] = R.write_csv(p(K.CODES), ["result_code", "recorded_on", "material", "inventory_class"], R.codes())
    comp = R.completions(st, co, ev, lines)
    counts[K.COMPLETIONS] = R.write_csv(p(K.COMPLETIONS), R.COMP_COLS, list(comp.itertuples(index=False)), crlf=True)
    counts[K.CONTRACTS] = R.write_csv(p(K.CONTRACTS), R.CONTRACT_COLS, R.contracts())
    counts[K.AGREEMENTS] = R.write_csv(p(K.AGREEMENTS), R.AG_COLS, R.agreements(ag))
    counts[K.TAP_SAMPLES] = R.write_csv(p(K.TAP_SAMPLES), R.TAP_COLS, R.tap_samples(lines))
    counts[K.METER_EXCHANGES] = R.write_csv(p(K.METER_EXCHANGES), R.METER_COLS, R.meter_exchanges(lines), crlf=True)
    contractor_of = {c[0]: c[1] for c in K.CONTRACTS_2026}
    D.write_change_orders(p(K.CHANGE_ORDERS), co, contractor_of)
    counts[K.CHANGE_ORDERS] = len(co)
    D.write_unit_costs(p(K.UNIT_COSTS))
    counts[K.UNIT_COSTS] = len(K.PLAN_ORDER)
    D.write_plan(p(K.PLAN))
    D.write_capital(p(K.CAPITAL))
    D.write_progress(p(K.PROGRESS), progress_tables(inv, ver, comp))
    D.write_notes(p(K.NOTES), counts)
    log = [
        (K.INVENTORY, "GIS service line inventory layer", "2027-01-08", counts[K.INVENTORY], "GIS and Asset Records",
         "every service line, all fourteen zones"),
        (K.VERIFICATIONS, "Work management system (customer system service orders migrated 13 March 2023)",
         "2027-01-08", counts[K.VERIFICATIONS], "GIS and Asset Records", "service line material verifications, "
         "4 January 2021 to 18 December 2026"),
        (K.CROSSWALK, "Customer system to GIS migration", "2023-03-13", counts[K.CROSSWALK], "GIS and Asset Records",
         "premises in service at the cut-over"),
        (K.CODES, "Work management system code tables", "2027-01-08", counts[K.CODES], "GIS and Asset Records",
         "service line result codes, all recording routes"),
        (K.COMPLETIONS, "Work management system, contract management module", "2027-01-08", counts[K.COMPLETIONS],
         "LSLR programme office", "full replacement completions under the 2026 contracts"),
        (K.CONTRACTS, "Purchasing contract register", "2027-01-08", counts[K.CONTRACTS], "Purchasing",
         "the 2026 lead service line replacement contracts"),
        (K.CHANGE_ORDERS, "Engineering change order log", "2027-01-07", counts[K.CHANGE_ORDERS], "Engineering",
         "approved change orders, 2026 contracts"),
        (K.AGREEMENTS, "Right-of-entry agreement system", "2027-01-08", counts[K.AGREEMENTS],
         "LSLR programme office", "agreement forms on lines open in the plan, 2022 to 2027"),
        (K.PLAN, "Engineering", "2026-10-20", "", "Engineering", "lead service line replacement plan, revision 2"),
        (K.CAPITAL, "Finance", "2026-12-14", "", "Finance", "capital improvement plan 2027 to 2037, board draft"),
        (K.UNIT_COSTS, "Engineering", "2026-11-02", counts[K.UNIT_COSTS], "Engineering",
         "2027 unit costs by zone"),
        (K.PROGRESS, "LSLR programme office", "2027-01-06", "", "LSLR programme office", "2026 progress report"),
        (K.NOTES, "GIS and Asset Records", "2027-01-08", "", "GIS and Asset Records", "field notes for this extract"),
        (K.TAP_SAMPLES, "Laboratory information system", "2027-01-08", counts[K.TAP_SAMPLES], "Water Quality",
         "lead and copper compliance samples, tier 1 sites, 2025 and 2026"),
        (K.METER_EXCHANGES, "Meter shop rollout tracker", "2027-01-08", counts[K.METER_EXCHANGES], "Customer Service",
         "automated meter exchanges, April 2023 to December 2025"),
    ]
    R.write_csv(p(K.EXTRACT_LOG), EXTRACT_LOG_COLS, log)
    PP.normalize_ooxml(p(K.UNIT_COSTS), K.PEOPLE["engineer"], K.PEOPLE["engineer"], "2026-10-27T14:12:08Z",
                       "2026-11-02T20:31:44Z", excel=True)
    PP.normalize_ooxml(p(K.CHANGE_ORDERS), K.PEOPLE["engineer"], K.PEOPLE["engineer"], "2026-03-30T13:05:51Z",
                       "2027-01-07T19:48:20Z", excel=True)
    PP.normalize_ooxml(p(K.CAPITAL), K.PEOPLE["finance"], K.PEOPLE["finance"], "2026-11-18T15:22:00Z",
                       "2026-12-14T21:06:00Z", title="Capital Improvement Plan 2027 to 2037")
    PP.normalize_pdf(p(K.PLAN), b"D:20261020101522-04'00'", b"D:20261020143005-04'00'")
    PP.normalize_pdf(p(K.PROGRESS), b"D:20270106091410-05'00'", b"D:20270106112852-05'00'")
    stamp = EXPORT_STAMP.timestamp()
    for f in os.listdir(out):
        os.utime(os.path.join(out, f), (stamp, stamp))
    w["counts"] = counts
    w["inv"], w["ver"], w["comp"] = inv, ver, comp
    if not quiet:
        print("built %s: %d files; %s" % (out, len(os.listdir(out)),
                                          ", ".join("%s %d" % kv for kv in counts.items())))
    return w


def digest(folder):
    return {f: hashlib.sha256(open(os.path.join(folder, f), "rb").read()).hexdigest()
            for f in sorted(os.listdir(folder))}


def everything(root, quiet=False):
    import deliver as DL
    import metadata as MD
    world = build(os.path.join(root, "target"), quiet=quiet)
    if os.path.exists(os.path.join(root, "golden")):
        shutil.rmtree(os.path.join(root, "golden"))
    DL.main(os.path.join(root, "target"), os.path.join(root, "golden"),
            os.path.join(root, "generator", "figures.json"), world=world)
    MD.write(os.path.join(root, "target"), os.path.join(root, "metadata.json"))
    return world


def main():
    import checks as CK
    import verify as V
    world = everything(TASK)
    CK.run(os.path.join(TASK, "target"), os.path.join(TASK, "golden"), world=world,
           meta_path=os.path.join(TASK, "metadata.json"))
    V.main(os.path.join(TASK, "target"), os.path.join(TASK, "golden"))
    tmp = tempfile.mkdtemp(dir=TASK, suffix=".tmp")
    try:
        os.makedirs(os.path.join(tmp, "generator"))
        everything(tmp, quiet=True)
        same_t = digest(os.path.join(TASK, "target")) == digest(os.path.join(tmp, "target"))
        same_g = digest(os.path.join(TASK, "golden")) == digest(os.path.join(tmp, "golden"))
        same = {}
        for f in ("metadata.json", os.path.join("generator", "figures.json")):
            same[f] = open(os.path.join(TASK, f), "rb").read() == open(os.path.join(tmp, f), "rb").read()
        if not (same_t and same_g and all(same.values())):
            raise SystemExit("second build differs: target %s, golden %s, %s" % (same_t, same_g, same))
    finally:
        shutil.rmtree(tmp)
    allh = hashlib.sha256("".join(v for _, v in sorted(digest(os.path.join(TASK, "target")).items())).encode() +
                          "".join(v for _, v in sorted(digest(os.path.join(TASK, "golden")).items())).encode())
    print("two builds byte-identical: %d target files, %d golden files, metadata.json and figures.json (sha256 %s)" % (
        len(os.listdir(os.path.join(TASK, "target"))), len(os.listdir(os.path.join(TASK, "golden"))),
        allh.hexdigest()[:16]))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", help="build the pack only, into this folder")
    a = ap.parse_args()
    if a.out:
        build(a.out)
    else:
        main()
