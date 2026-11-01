"""Build task125's pack, goldens, figures.json, submission.md and metadata.json twice, require byte-identical output,
cut target.zip, then run the checks and the verifier.

    python3 task125/generator/build.py
"""
import datetime as dt
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import docs as D    # noqa: E402
import pack as PK   # noqa: E402
import sim as S     # noqa: E402
import world as W   # noqa: E402

STAMP = (2027, 1, 6, 9, 20, 0)
SOURCES = {
    "rms": "a municipal police service's records management system occurrence export (versions)",
    "crosswalk": "a records management system's 2023 offence code crosswalk",
    "segments": "a city's street centreline segment file",
    "register": "a police paid-duty office's booking register",
    "cad": "a police communications centre's computer-aided dispatch export",
    "roster": "a patrol division's tour roster",
    "wards": "a city's ward profiles from the 2021 census",
    "lights": "a city's streetlight service requests",
    "protocol": "a crime analysis unit's hot spot designation protocol",
    "directive": "a police service's directive on patrol workload and response measures",
    "request": "the Superintendent, Patrol Operations' email",
}


def world():
    r = W.rng()
    segs = W.streets(r)
    base, inc_g, inc_l, role = W.base_rates(r, segs)
    ev = W.calendars(r)
    crimes = W.crimes(r, segs, base, inc_g, inc_l, ev)
    nonp = W.nonpatrol_rates(r, segs, base)
    twp = W.township(r)
    bdg = S.badges(r)
    rost = S.roster(r, bdg)
    events = S.cad(r, segs, twp, base, nonp)
    bks = S.bookings(r, segs, ev, bdg)
    settle_edges(segs, rost, events, bks)
    return {"r": r, "segs": segs, "base": base, "inc_g": inc_g, "inc_l": inc_l, "role": role, "ev": ev,
            "crimes": crimes, "nonp": nonp, "twp": twp, "badges": bdg, "roster": rost, "events": events,
            "bookings": bks}


def _own_date_tour(t):
    h = t.hour + t.minute / 60.0
    return t.date(), ("D" if 7 <= h < 19 else "N")


def _quarter_hours(segs, rost, events, naive=False):
    out = {}
    for ev in events:
        if ev["area"] != "city" or ev["source"] == "OFFICER":
            continue
        q = (ev["received"].month - 1) // 3 + 1
        for u in ev["units"]:
            key = (_own_date_tour if naive else S.tour_of)(u["dispatched"])
            n = len(rost.get(key + (u["unit"],), [0]))
            k = (ev["ward"], q)
            el = u["cleared"].astimezone(dt.timezone.utc) - u["dispatched"].astimezone(dt.timezone.utc)
            out[k] = out.get(k, 0.0) + el.total_seconds() / 3600.0 * n
    return out


def _duty_hours(bks):
    out = {}
    for b in bks:
        if b["date"].year != 2026:
            continue
        for ln in b["lines"]:
            if ln["status"] == "WORKED":
                out[b["ward"]] = out.get(b["ward"], 0.0) + ln["hours"]
    return out


def _later(t, seconds):
    """An aware time moved on by elapsed seconds (never by wall-clock arithmetic across a clock change)."""
    return (t.astimezone(dt.timezone.utc) + dt.timedelta(seconds=seconds)).astimezone(t.tzinfo)


def settle_edges(segs, rost, events, bks):
    """Keep every ask figure clear of its rounding edge. An officer-hours cell sits at least a quarter of an hour from
    a half hour, so no reading of the clocks moves it across; each nudge lets one unit clear nine minutes later,
    inside its tour. A paid-duty total at a half hour moves by a quarter hour (the register's own record)."""
    for _ in range(400):
        moved = False
        for k, v in sorted(_quarter_hours(segs, rost, events).items()):
            if abs((v % 1) - 0.5) < 0.25:
                for e in events:
                    if not (e["area"] == "city" and e["ward"] == k[0] and e["source"] != "OFFICER" and
                            (e["received"].month - 1) // 3 + 1 == k[1] and e["units"]):
                        continue
                    u = e["units"][0]
                    if _later(u["cleared"], 540) < S.tour_end(u["dispatched"]) - dt.timedelta(minutes=2) and \
                            not u.get("nudged"):
                        u["cleared"] = _later(u["cleared"], 540)
                        u["nudged"] = True
                        break
                moved = True
        gold = _quarter_hours(segs, rost, events)
        for k, v in sorted(_quarter_hours(segs, rost, events, naive=True).items()):
            if abs(v - gold[k]) < 1.0:
                for e in events:
                    if not (e["area"] == "city" and e["ward"] == k[0] and e["source"] != "OFFICER" and
                            (e["received"].month - 1) // 3 + 1 == k[1]):
                        continue
                    for u in e["units"]:
                        if u.get("nudged") or u["dispatched"].hour >= 7:
                            continue
                        c_true = len(rost[S.tour_of(u["dispatched"]) + (u["unit"],)])
                        c_own = len(rost[_own_date_tour(u["dispatched"]) + (u["unit"],)])
                        sign = 1 if v >= gold[k] else -1
                        if (c_own - c_true) * sign <= 0:
                            continue
                        if _later(u["cleared"], 1500) < S.tour_end(u["dispatched"]) - dt.timedelta(minutes=2):
                            u["cleared"] = _later(u["cleared"], 1500)
                            u["nudged"] = True
                            break
                    else:
                        continue
                    break
                moved = True
        for w, v in sorted(_duty_hours(bks).items()):
            if abs((v % 1) - 0.5) < 0.012:
                b = next(b for b in bks if b["date"].year == 2026 and b["ward"] == w and
                         any(ln["status"] == "WORKED" for ln in b["lines"]) and not b["overnight"])
                ln = next(ln for ln in b["lines"] if ln["status"] == "WORKED")
                ln["a_end"] += 15
                ln["hours"] += 0.25
                moved = True
        if not moved:
            return
    raise SystemExit("settle_edges did not converge")


def build_pack(out):
    os.makedirs(out, exist_ok=True)
    f = lambda k: os.path.join(out, PK.FILES[k])
    w = world()
    r = w["r"]
    occ, rows = PK.occurrences(r, w["segs"], w["crimes"], w["nonp"])
    n = {"rms": PK.write_rms(rows, f("rms"))}
    PK.write_crosswalk(f("crosswalk"))
    PK.write_segments(w["segs"], f("segments"))
    PK.write_register(w["bookings"], f("register"), dt.datetime(2027, 1, 6, 7, 2, 11), dt.datetime(2027, 1, 6, 7, 9, 48))
    n["cad"] = PK.write_cad(r, w["events"], f("cad"))
    PK.write_roster(w["roster"], f("roster"))
    PK.write_wards(f("wards"))
    n["lights"] = PK.write_lights(r, w["segs"], f("lights"))
    D.protocol(f("protocol"))
    D.directive(f("directive"))
    D.request(f("request"))
    t = dt.datetime(*STAMP).timestamp()
    for k in PK.FILES:
        os.utime(f(k), (t, t))
    w["occ"] = occ
    return n, w


def metadata(n):
    return {"task": "task125", "architecture": 4, "as_of": "2027-01-06",
            "files": {PK.FILES[k]: {"source": SOURCES[k], "date": "2027-01-06", "license": "synthetic, CC0",
                                    "role": "distractor" if k in PK.DISTRACTORS else "evidence"} for k in PK.FILES},
            "distractors": [PK.FILES[k] for k in PK.DISTRACTORS],
            "largest_file": {"name": PK.FILES["rms"], "rows": n["rms"]},
            "cad_rows": n["cad"],
            "deliverables": ["hot_spot_patrols_2027.pptx", "patrol_figures_2026.csv"]}


def digest(folder):
    h = {}
    for root, _d, files in os.walk(folder):
        for fn in sorted(files):
            p = os.path.join(root, fn)
            h[os.path.relpath(p, folder)] = hashlib.sha256(open(p, "rb").read()).hexdigest()
    return h


def one_build(base):
    import golden as GD
    target, golden = os.path.join(base, "target"), os.path.join(base, "golden")
    n, w = build_pack(target)
    fig = GD.write_all(target, golden, base)
    json.dump(fig, open(os.path.join(base, "figures.json"), "w"), indent=1, sort_keys=True)
    json.dump(metadata(n), open(os.path.join(base, "metadata.json"), "w"), indent=1, sort_keys=True)
    return digest(base), fig


def cut_zip(target, path):
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        for fn in sorted(os.listdir(target)):
            zi = zipfile.ZipInfo(fn, date_time=STAMP)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, open(os.path.join(target, fn), "rb").read())


def main():
    a, b = tempfile.mkdtemp(), tempfile.mkdtemp()
    ha, fig = one_build(a)
    hb, _ = one_build(b)
    same = ha == hb
    print("two builds byte-identical:", same, "(%d files)" % len(ha))
    if not same:
        for k in sorted(set(ha) | set(hb)):
            if ha.get(k) != hb.get(k):
                print("  differs:", k)
        sys.exit(1)
    for sub in ("target", "golden"):
        dst = os.path.join(TASK, sub)
        if os.path.isdir(dst):
            shutil.rmtree(dst)
        shutil.copytree(os.path.join(a, sub), dst)
    shutil.copy(os.path.join(a, "figures.json"), os.path.join(HERE, "figures.json"))
    shutil.copy(os.path.join(a, "metadata.json"), os.path.join(TASK, "metadata.json"))
    shutil.copy(os.path.join(a, "submission.md"), os.path.join(TASK, "submission.md"))
    shutil.rmtree(a)
    shutil.rmtree(b)
    zp = os.path.join(TASK, "target.zip")
    cut_zip(os.path.join(TASK, "target"), zp)
    print("target.zip sha256", hashlib.sha256(open(zp, "rb").read()).hexdigest())
    print("designated", fig["designated"])
    for script in ("checks.py", "verify.py"):
        p = os.path.join(HERE, script)
        if os.path.exists(p):
            rc = subprocess.call([sys.executable, p])
            print(script, "exit", rc)
            if rc:
                sys.exit(rc)


if __name__ == "__main__":
    main()
