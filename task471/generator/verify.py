"""The independent verifier: reads only the shipped pack (target/) and the golden files, recomputes the survey
population, the six counties and the retest figures by its own code, and compares them with the golden workbook and
submission.md. It imports nothing from the generator.

    python3 task471/generator/verify.py
"""
import csv
import datetime as dt
import os
import re
import sys

import openpyxl

LINE, STD, NO3 = 250, 10.0, 4.427
TOKENS = set("N S E W NORTH SOUTH EAST WEST RD ROAD LN LANE DR DRIVE TRL TRAIL HWY HIGHWAY CT COURT AVE AVENUE ST "
             "STREET".split())


def find(target, pattern):
    hits = [f for f in os.listdir(target) if re.search(pattern, f)]
    assert len(hits) == 1, (pattern, hits)
    return os.path.join(target, hits[0])


def rows(path):
    with open(path, encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def akey(num, text):
    words = [w for w in re.split(r"[\s.,]+", str(text).upper()) if w and w not in TOKENS]
    return "%d|%s" % (int(num), " ".join(words))


def akey_line(text):
    head, _, rest = str(text).strip().partition(" ")
    return akey(head, rest)


def digits(v):
    d = "".join(ch for ch in str(v) if ch.isdigit())
    return d if len(d) == 9 else None


def day(v):
    if isinstance(v, (dt.date, dt.datetime)):
        return v.strftime("%Y-%m-%d")
    v = str(v)
    return v[:4] + "-" + v[4:6] + "-" + v[6:8] if v.isdigit() else v[:10]


def compute(target):
    codes = rows(find(target, r"county_codes"))
    by_name = {r["PERMIT_DB_COUNTY"]: r["COUNTY_CODE"] for r in codes}
    by_sheet = {r["ASSESSOR_SHEET"]: r["COUNTY_CODE"] for r in codes}
    names = {r["COUNTY_CODE"]: r["COUNTY"] for r in codes}
    P = {k: {} for k in names}
    for r in rows(find(target, r"permits_extract")):
        if r["WELL_USE"] == "DOMESTIC" and r["WELL_STATUS"] == "ACTIVE" and "1986-01-01" <= r["DATE_DRILLED"] <= "2025-08-31":
            P[by_name[r["COUNTY"]]][r["PERMIT_NO"]] = (digits(r["PARCEL_NO"]) if r["PARCEL_NO"] else None,
                                                       akey_line(r["SITE_ADDRESS"]))
    wb = openpyxl.load_workbook(find(target, r"parcels"), read_only=True)
    Q = {k: {} for k in names}          # parcel digits -> (address key, private?)
    for ws in wb.worksheets:
        if ws.title not in by_sheet:
            continue
        k = by_sheet[ws.title]
        it = ws.iter_rows(values_only=True)
        h = list(next(it))
        for v in it:
            if v[0] is None:
                continue
            d = dict(zip(h, v))
            if "PIN" in d:
                pid, ak, code = d["PIN"], akey(d["HOUSE_NO"], d["STREET"]), d["WATER_SOURCE"]
            elif "PARCEL_ID" in d:
                pid, ak, code = d["PARCEL_ID"], akey_line(d["SITUS_ADDRESS"]), d["WATER"]
            else:
                pid, ak, code = d["Parcel Number"], akey_line(d["Property Address"]), d["Water Service"]
            Q[k][digits(pid)] = (ak, str(code).strip() in ("W", "WELL", "2") if code is not None else False)
    out = {}
    for k in names:
        addr_to_pid = {ak: pid for pid, (ak, _p) in Q[k].items()}
        on_q = {}
        for no, (pid, ak) in P[k].items():
            pid = pid if pid else addr_to_pid.get(ak)
            on_q[no] = bool(pid and Q[k].get(pid, (None, False))[1])
        priv = {pid for pid, (_a, p) in Q[k].items() if p}
        q_on_p = set()
        for no, (pid, ak) in P[k].items():
            pid = pid if pid else addr_to_pid.get(ak)
            if pid in priv:
                q_on_p.add(pid)
        both = sum(on_q.values())
        out[k] = dict(name=names[k], NP=len(P[k]), NQ=len(priv), union=len(P[k]) + len(priv) - both, on_q=on_q,
                      q_on_p=q_on_p, wells={}, nP=0, nQ=0)
    for r in rows(find(target, r"draw_manifest")):
        if r["OUTCOME"] not in ("TESTED", "TESTED_EARLIER"):
            continue
        o = out[r["COUNTY_CODE"]]
        w = o["wells"].setdefault(r["KIT_ID"], dict(p=False, q=False, addr=None))
        if r["FRAME"] == "PERMIT":
            o["nP"] += 1
            w["p"] = True
            w["q"] = w["q"] or o["on_q"][r["FRAME_RECORD"]]
            w["addr"] = P[r["COUNTY_CODE"]][r["FRAME_RECORD"]][1]
        else:
            o["nQ"] += 1
            pid = digits(r["FRAME_RECORD"])
            w["q"] = True
            w["p"] = w["p"] or pid in o["q_on_p"]
            w["addr"] = w["addr"] or Q[r["COUNTY_CODE"]][pid][0]
    res = {}
    for r in rows(find(target, r"Halvorsen")):
        if r["RESULT_STATUS"] == "FINAL":
            v = r["NO3N_MG_L"]
            res[r["KIT_ID"]] = (r["COLLECTED"], 0.0 if v.startswith("<") else float(v))
    wb = openpyxl.load_workbook(find(target, r"Cedarline"), read_only=True)
    it = wb["Results"].iter_rows(values_only=True)
    h = list(next(it))
    best = {}
    for v in it:
        d = dict(zip(h, v))
        if d["Analyte"] == "Nitrate as N" and (d["Client Kit"] not in best or day(d["Report Date"]) > best[d["Client Kit"]][0]):
            best[d["Client Kit"]] = (day(d["Report Date"]), day(d["Date Sampled"]),
                                     0.0 if d["Qualifier"] == "U" else float(d["Result"]))
    for kit, (_r, c, n) in best.items():
        res[kit] = (c, n)
    ver = {}
    for r in rows(find(target, r"Kinsale")):
        if r["PARAMETER"] == "NITRATE" and int(r["VERSION"]) >= ver.get(r["CLIENTID"], 0):
            ver[r["CLIENTID"]] = int(r["VERSION"])
            res[r["CLIENTID"]] = (day(r["SAMPLED"]), 0.0 if r["FLAG"] == "<" else float(r["VALUE"]) / NO3)
    for k, o in out.items():
        fP, fQ = o["nP"] / o["NP"], o["nQ"] / o["NQ"]
        est = 0.0
        for kit, w in o["wells"].items():
            if res[kit][1] > STD:
                est += 1.0 / (1 - (1 - (fP if w["p"] else 0)) * (1 - (fQ if w["q"] else 0)))
        o["estimate"], o["qualifies"] = est, est >= LINE
    # retests: each request to its well (first kit, or ship-to address in the request's county), counted where tested
    kit_county = {kit: k for k, o in out.items() for kit in o["wells"]}
    addr_kit = {(k, w["addr"]): kit for k, o in out.items() for kit, w in o["wells"].items()}
    first = {kit: res[kit][1] for kit in kit_county}
    for o in out.values():
        o["retested"], o["still"] = 0, 0
    done = set()
    for r in rows(find(target, r"retest_kit_requests")):
        kit = r["ORIGINAL_KIT"] or addr_kit.get((r["COUNTY_CODE"], akey_line(r["SHIP_TO_ADDRESS"])))
        if not kit or kit not in kit_county or kit in done or r["RETEST_KIT"] not in res:
            continue
        coll, n = res[r["RETEST_KIT"]]
        if coll > "2026-06-30" or first[kit] <= STD:
            continue
        done.add(kit)
        o = out[kit_county[kit]]
        o["retested"] += 1
        o["still"] += 1 if n > STD else 0
    return out


def main(target, gdir, sub=None):
    out = compute(target)
    ok = True
    wb = openpyxl.load_workbook(os.path.join(gdir, "nitrate_assistance_counties_2027.xlsx"), read_only=True)
    golden = {r[0]: r for r in wb["Counties 2027"].iter_rows(min_row=5, values_only=True) if r[0]}
    for k, o in sorted(out.items()):
        g = golden[k]
        want = (o["union"], "Yes" if o["qualifies"] else "No", o["retested"], o["still"])
        if tuple(g[2:6]) != want:
            ok = False
            print("VERIFY MISMATCH %s: golden %s, recomputed %s" % (k, g[2:6], want))
    sub = sub or os.path.join(os.path.dirname(gdir), "submission.md")
    text = open(sub, encoding="utf-8").read()
    for k, o in out.items():
        line = "   - %s: %s; %s; %d; %d" % (o["name"], "{:,}".format(o["union"]), "yes" if o["qualifies"] else "no",
                                           o["retested"], o["still"])
        if line not in text:
            ok = False
            print("VERIFY MISMATCH submission.md: %s" % line)
    q = sorted(o["name"] for o in out.values() if o["qualifies"])
    print("verify: %d counties qualify (%s); %s" % (len(q), ", ".join(q), "golden and submission agree" if ok
                                                      else "MISMATCHES"))
    return ok


if __name__ == "__main__":
    here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.exit(0 if main(os.path.join(here, "target"), os.path.join(here, "golden")) else 1)
