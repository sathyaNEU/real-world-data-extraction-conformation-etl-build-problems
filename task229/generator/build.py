"""Build task229's evidence pack into <out>/ (default task229/target). Deterministic: two builds are
byte-identical. Returns the in-memory world for checks.py (the private truth never reaches a file)."""
import datetime as dt
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import world as W
import simulate as S
import asks as A
import docs as DC
import postprocess as PP

TASK = os.path.dirname(HERE)
REPO = os.path.dirname(TASK)
SCRUB = os.path.join(REPO, ".claude", "skills", "reduce-house-fixes", "scripts", "scrub_producer_metadata.py")
ALL_FILES = dict(S.FILES, **A.FILES, **DC.FILES)
MAIN_FILES = ["counts", "locations", "centres", "standard", "programme", "notes"]


def bin_offset(x, unit):
    """Signed distance of x from the centre of its rounding bin."""
    return x - unit * round(x / unit)


def anchor_stock(recs, lines, target, golden):
    """Centre each centre's ask A value in its £1,000 bin by moving one plain face's quantity."""
    by_no = {ln["line_no"]: ln for ln in lines}
    face_count = {}
    for r in recs:
        if r["location_type"] == "PICK":
            face_count[(r["site"], r["line_no"])] = face_count.get((r["site"], r["line_no"]), 0) + 1
    code = {c["name"]: c["code"] for c in W.CENTRES}
    moved = {}
    for name, v in golden.items():
        off = bin_offset(v, 1000)
        if abs(off) <= 250:
            continue
        cands = [r for r in recs if r["site"] == code[name] and r["location_type"] == "PICK" and r["status"] == "AVAILABLE"
                 and r["unit"] == "CS" and not by_no[r["line_no"]]["date_coded"] and by_no[r["line_no"]]["p10"] is None
                 and face_count[(r["site"], r["line_no"])] == 1 and by_no[r["line_no"]]["cost"] >= 30 and r["qty"] >= 20]
        r = cands[len(cands) // 2]
        cost = by_no[r["line_no"]]["cost"]
        k = int(round(-off / cost))
        r["qty"] += k
        r["batches"] = [(b, bb, r["qty"]) for b, bb, _ in r["batches"]]
        moved[name] = (r["location"], k)
    return moved


def anchor_forecast(frows, st, moves, closed26, golden):
    """Centre each centre's ask B figure in its 100-case bin by moving one steady store's forecast."""
    moved_pairs = {(m[0], m[1]) for m in moves}
    dep = {}
    for s in st:
        for regime in ("Ambient", "Chilled", "Frozen"):
            dep.setdefault(s["depots"][regime], []).append((s["store_no"], regime))
    regime_of = {c[0]: c[2] for c in A.CATEGORIES}
    out = {}
    days = [dt.date(2026, 12, 9), dt.date(2026, 12, 10), dt.date(2026, 12, 15), dt.date(2026, 12, 16)]
    for i, (name, v) in enumerate(golden.items()):
        off = bin_offset(v, 100)
        if abs(off) <= 25:
            continue
        off -= ((i * 37) % 41) - 20 + 0.37 * (i % 3)     # land off the exact centre
        cand = sorted(p for p in dep[name] if p not in moved_pairs and p[0] not in closed26)
        store, regime = cand[len(cand) // 3]
        cat = [c[0] for c in A.CATEGORIES if c[2] == regime and c[3] == "CS"][0]
        delta = -off / len(days)
        for r in frows:
            if r[0] == store and r[2] == cat and r[3] in days:
                r[4] = round(r[4] + delta, 2)
        out[name] = (store, cat, round(-off, 2))
    return out


def scrub(path, producer, stamp):
    tmp = tempfile.mkdtemp()
    p2 = os.path.join(tmp, os.path.basename(path))
    shutil.copy(path, p2)
    subprocess.run([sys.executable, SCRUB, tmp, "--apply", "--producer", producer, "--stamp", stamp,
                    "--floor", "2022-01-01", "--ceiling", "2026-12-07"], check=True, stdout=subprocess.DEVNULL)
    shutil.copy(p2, path)
    shutil.rmtree(tmp)


def build(out, quiet=False):
    if os.path.exists(out):
        shutil.rmtree(out)
    os.makedirs(out)
    p = lambda k: os.path.join(out, ALL_FILES[k])
    sim = S.simulate()
    lines = A.catalogue()
    asg = A.assign(sim, lines)
    count_rows = S.write_main(out, sim, asg, lines)
    locs = S.write_locations(out, sim, asg, lines)
    S.write_centres(out)
    recs = A.stock(sim, asg, lines, locs)
    A.write_stock(out, recs)
    A.write_line_master(out, lines)
    A.write_costs(out, lines)
    st = A.stores()
    moves = A.rezoning(st)
    closed26 = A.boxing_closed(st)
    A.write_stores(out, st)
    A.write_servicing(out, st, moves)
    A.write_calendar(out, st, closed26)
    A.write_categories(out)
    frows = A.forecast(st)
    A.write_forecast(out, frows)
    # centre every graded ask figure in its rounding bin (one quiet quantity per centre)
    anchors_a = anchor_stock(recs, lines, out, A.ask_a(out))
    if anchors_a:
        A.write_stock(out, recs)
    anchors_b = anchor_forecast(frows, st, moves, closed26, A.ask_b(out))
    if anchors_b:
        A.write_forecast(out, frows)
    A.write_labour(out)
    A.write_goodsin(out)
    DC.standard_pdf(p("standard"))
    DC.programme_docx(p("programme"))
    DC.notes_txt(p("notes"), ALL_FILES, {"counts": len(count_rows)})
    PP.normalize_zip(p("linemaster"), modified="2026-12-04T08:31:12Z", company="Thornacre Stores Ltd")
    PP.normalize_zip(p("labour"), modified="2026-11-27T17:05:48Z", company="Corderoy Logistics")
    PP.normalize_zip(p("programme"), when=(2026, 5, 15, 16, 41, 0), modified="2026-05-15T15:41:00Z")
    PP.normalize_pdf(p("standard"))
    scrub(p("standard"), "Thornacre Supply Chain", "2026-08-27")
    scrub(p("programme"), "Arthur Mason", "2026-05-15")
    scrub(p("linemaster"), "Thornacre Merchandising", "2026-12-04")
    scrub(p("labour"), "Corderoy Peak Planning", "2026-11-27")
    ts = dt.datetime(2026, 12, 7, 7, 20).timestamp()
    for f in os.listdir(out):
        os.utime(os.path.join(out, f), (ts, ts))
    if not quiet:
        print("built", out, len(os.listdir(out)), "files;", len(count_rows), "count rows; anchors", anchors_a, anchors_b)
    return dict(sim=sim, lines=lines, assign=asg, count_rows=count_rows, locs=locs, recs=recs, stores=st, moves=moves,
                closed26=closed26, frows=frows, anchors_a=anchors_a, anchors_b=anchors_b)


if __name__ == "__main__":
    build(sys.argv[1] if len(sys.argv) > 1 else os.path.join(TASK, "target"))
