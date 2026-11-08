"""task482 architecture 17: the ask layer's cracker, mirror and full-includer sheets, run on the cut pack.

Each path is a complete handling of the shipped files; each graded ask figure (entered, sat, make-up candidates and
make-up mean, each by region) scores a hit when it sits within half a unit of the asked rounding of figures.json.
The golden path must reproduce figures.json exactly. Prints each path's keep and the pair ceilings (a response on
the call scores 38 + 7 + 55 L, one off it 5 + 7 + 55 L), stamped with the pack's digest. Exit 1 if the golden path
misses, the cracker keeps a figure or the full includer keeps two fifths or more."""
import csv
import hashlib
import json
import os
import re
import subprocess
import sys

import openpyxl

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
TARGET = os.path.join(TASK, "target")
REGIONS = ["Northern", "Central", "Capital", "Southern"]


def digest():
    h = hashlib.sha256()
    for f in sorted(os.listdir(TARGET)):
        h.update(f.encode())
        h.update(open(os.path.join(TARGET, f), "rb").read())
    return h.hexdigest()[:16]


def load():
    schools, names = {}, {}
    with open(os.path.join(TARGET, "member_schools.csv"), newline="") as fh:
        for r in csv.DictReader(fh):
            schools[r["school_code"]] = r["region"]
            names[r["school_name"]] = r["school_code"]
    online = {}
    with open(os.path.join(TARGET, "y10sci_aug2026_sessions.csv"), newline="") as fh:
        for r in csv.DictReader(fh):
            online[r["entry_no"]] = r["school_code"]
    wb = openpyxl.load_workbook(os.path.join(TARGET, "entries_register_aug2026.xlsx"), read_only=True)
    rows = list(wb["Entries"].iter_rows(values_only=True))
    head = [str(h) for h in rows[0]]
    entries = [dict(zip(head, r)) for r in rows[1:] if any(v is not None for v in r)]
    with open(os.path.join(TARGET, "makeup_scripts_keyed.csv"), newline="") as fh:
        scripts = list(csv.DictReader(fh))
    txt = subprocess.run(["pdftotext", "-layout", os.path.join(TARGET, "makeup_roster_aug2026.pdf"), "-"],
                         capture_output=True, text=True, check=True).stdout
    roster = []
    for line in txt.splitlines():
        m = re.search(r"\b(26-\d{5})\b", line)
        if not m:
            continue
        s = re.search(r"\b(C\d{3}-\d{3})\b", line)
        h = re.search(r"\b(C\d{3})\b(?!-)", line)
        roster.append(dict(entry=m.group(1), script=s.group(1) if s else "", home=h.group(1) if h else None))
    return schools, online, entries, scripts, roster


def entered(schools, entries, how):
    seen, exact, out = set(), set(), {r: 0 for r in REGIONS}
    for e in entries:
        if str(e["Status"]).strip() != "E":
            continue
        t = tuple(e.values())
        if t in exact:
            continue
        exact.add(t)
        if how == "nsn":
            key = ("n", e["NSN"]) if e["NSN"] not in (None, "") else ("e", e["Entry no"])
        elif how == "surname_dob":
            key = (e["Surname"], str(e["Date of birth"]))
        else:
            key = (e["First name"], e["Surname"], str(e["Date of birth"]))
        if key in seen:
            continue
        seen.add(key)
        out[schools[e["School code"]]] += 1
    return out


def placed(schools, entries, scripts, roster, how):
    """Each keyed script's region (None when the handling drops it). how: 'keyed' (the school code keyed),
    'roster' (the typed roster's home school; unmatched scripts dropped), 'roster_keyed' (unmatched scripts at the
    code keyed), 'golden' (unmatched scripts through the entry number keyed to the entries register)."""
    home = {x["script"]: x["home"] for x in roster if x["script"]}
    school_of = {}
    for e in entries:
        school_of.setdefault(e["Entry no"], e["School code"])
    out = []
    for s in scripts:
        if how == "keyed":
            out.append(schools[s["school_code"]])
        elif s["script_no"] in home:
            out.append(schools[home[s["script_no"]]])
        elif how == "roster_keyed":
            out.append(schools[s["school_code"]])
        elif how == "golden" and s["entry_no"]:
            out.append(schools[school_of[s["entry_no"]]])
        else:
            out.append(None)
    return out


def blocks(schools, online, entries, scripts, roster, e_how, s_how, pct):
    e = entered(schools, entries, e_how)
    sat = {r: 0 for r in REGIONS}
    for entry, code in online.items():
        sat[schools[code]] += 1
    n = {r: 0 for r in REGIONS}
    mk = {r: [] for r in REGIONS}
    if s_how == "roster_lines":
        for x in roster:
            sat[schools[x["home"]]] += 1
            n[schools[x["home"]]] += 1
        places = placed(schools, entries, scripts, roster, "roster")
    else:
        places = placed(schools, entries, scripts, roster, s_how)
        for reg in places:
            if reg:
                sat[reg] += 1
                n[reg] += 1
    wrong = {s["batch"] for s in scripts if float(s["mark"]) > 50}     # a batch keyed off the 50-mark scale
    for s, reg in zip(scripts, places):
        if not reg:
            continue
        v = float(s["mark"])
        if (pct == "over50" and v > 50) or (pct == "batch" and s["batch"] in wrong):
            v /= 2
        mk[reg].append(v)
    mean = {r: (round(sum(v) / len(v), 1) if v else None) for r, v in mk.items()}
    return e, sat, n, mean


def main():
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    gold = [({r: float(fig[k][r]) for r in REGIONS}, half) for k, half in
            (("entered", 0.5), ("sat", 0.5), ("makeup_candidates", 0.5), ("makeup_mean", 0.05))]
    data = load()
    paths = {"golden": ("full", "golden", "batch"),
             "cracker": ("nsn", "keyed", "batch"),
             "mirror": ("nsn", "keyed", "batch"),
             "full includer": ("full", "roster", "over50"),
             "full includer, unmatched at the code keyed": ("full", "roster_keyed", "over50"),
             "full includer, batch whole": ("full", "roster", "batch")}
    keep = {}
    for name, (e_how, s_how, pct) in paths.items():
        got = blocks(*data, e_how, s_how, pct)
        hits = []
        for (g, half), v in zip(gold, got):
            hits += [v[r] is not None and abs(v[r] - g[r]) <= half + 1e-9 for r in REGIONS]
        keep[name] = sum(hits) / len(hits)
        print("%-44s keep %2d of %d (%.2f)  %s" % (name, sum(hits), len(hits), keep[name],
                                                    " | ".join(str(x) for x in got)))
    on = 38 + 7
    off = 5 + 7
    lfi = max(keep[k] for k in keep if k.startswith("full includer"))
    print("pack %s" % digest())
    print("pair, the full includer on the call and the mirror off it: %.1f" % ((on + 55 * lfi + off + 55 * keep["mirror"]) / 2))
    print("pair, the full includer and the cracker both on the call: %.1f" % ((on + 55 * lfi + on + 55 * keep["cracker"]) / 2))
    print("pair, two full includers on the call: %.1f" % (on + 55 * lfi))
    bad = []
    if keep["golden"] < 1.0:
        bad.append("the golden path does not reproduce figures.json")
    if keep["cracker"] > 0.0:
        bad.append("the cracker keeps an ask figure")
    if lfi >= 0.4:
        bad.append("a full includer keeps two fifths or more")
    for b in bad:
        print("FAIL " + b)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
