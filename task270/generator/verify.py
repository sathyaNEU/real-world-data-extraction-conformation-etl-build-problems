"""The independent verifier: reads only the shipped bundle (target/ and figures.json) and recomputes the call, the
regional shares and every ask figure with its own code (csv and openpyxl readers, plain dictionaries, its own
day-first date parsing), then compares with figures.json."""
import csv
import datetime as dt
import json
import os
import statistics as stx
import sys

import openpyxl

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import common as K    # noqa: E402


def half_up(x, n=0):
    from decimal import Decimal, ROUND_HALF_UP
    return float(Decimal(repr(float(x))).quantize(Decimal(1).scaleb(-n), rounding=ROUND_HALF_UP))


def rows(path):
    with open(path, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def d(s):
    return dt.datetime.strptime(s, "%d/%m/%Y").date()


def run(task):
    T = os.path.join(task, "target")
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    out = []

    def ok(label, a, b):
        out.append((label, a == b, "%s | %s" % (a, b)))

    names = {"SOLSTICE N40": "R448A", "OPTEON XP40": "R449A"}
    norm = lambda g: names.get(g.strip().upper(), g.strip().upper().replace("-", ""))   # noqa: E731
    region = {v: k for k, v in K.REGION_NAME.items()}
    stores = {int(r["store_no"]): region[r["region"]] for r in rows(os.path.join(T, K.FILES["stores"]))}
    wb = openpyxl.load_workbook(os.path.join(T, K.FILES["register"]), read_only=True)
    packs = {}
    for r in list(wb["Packs"].iter_rows(values_only=True))[1:]:
        code, _, _, gas, charge, since, dec, _ = r
        if norm(gas) not in {"R404A", "R448A", "R449A", "R407F"} or dec or d(since) > dt.date(2026, 1, 1):
            continue
        packs[code] = dict(region=stores[int(code[:3])], charge=float(charge), gas=norm(gas))
    eq = {}
    for r in list(wb["Cabinets and cold rooms"].iter_rows(values_only=True))[1:]:
        eq[r[0]] = int(r[1])
    jobs = rows(os.path.join(T, K.FILES["jobs"]))
    net = {c: 0.0 for c in packs}
    ratios, deps, last = {}, {}, {}
    for j in jobs:
        code = "%03d/%s" % (int(j["store"]), j["asset"])
        if code not in packs or j["job_type"] not in ("ROUTINE", "BREAKDOWN"):
            continue
        ch, rc = float(j["charged_kg"]), float(j["recovered_kg"])
        day = d(j["job_date"])
        if day.year == 2026:
            net[code] += ch - rc
        if ch > 0 and j["receiver_departure_pct"]:
            deps.setdefault(code, []).append(float(j["receiver_departure_pct"]))
        if ch - rc > 0.5 and j["receiver_arrival_pct"] and float(j["receiver_arrival_pct"]) > 1 and \
                float(j["receiver_departure_pct"]) < 99:
            ratios.setdefault(code, []).append((float(j["receiver_departure_pct"]) - float(j["receiver_arrival_pct"]))
                                               / (ch - rc))
        if code not in last or day >= last[code][0]:
            last[code] = (day, norm(j["refrigerant"]))
    tags = {r["bureau_tag"]: r["pack_code"] for r in rows(os.path.join(T, K.FILES["tags"]))}
    lev = {}
    with open(os.path.join(T, K.FILES["levels"]), encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r["date"] in ("2025-12-31", "2026-12-31") and r["receiver_level_pct"]:
                lev[(tags.get(r["bureau_tag"]), r["date"])] = float(r["receiver_level_pct"])
    loss = {}
    for c in packs:
        k, full = stx.median(ratios[c]), stx.median(deps[c])
        short = lambda day: max(0.0, (full - lev[(c, day)]) / k)   # noqa: E731
        loss[c] = net[c] + short("2026-12-31") - short("2025-12-31")
    share = {}
    for g in K.REGIONS:
        cs = [c for c in packs if packs[c]["region"] == g]
        share[g] = 100 * sum(loss[c] for c in cs) / sum(packs[c]["charge"] for c in cs)
        ok("share %s" % g, int(half_up(share[g])), fig["components"]["loss_share_pct"][g])
    top = sorted(share, key=lambda g: -share[g])
    ok("call", top[0], fig["call"]["region"])
    ok("runner-up", top[1], fig["call"]["runner_up"])
    ok("gap", int(half_up(share[top[0]] - share[top[1]])), fig["call"]["gap_points"])
    # asks: CO2e of the full charge at the refrigerant Kelbray charged, all packs and R404A
    for g in K.REGIONS:
        cs = [c for c in packs if packs[c]["region"] == g]
        gas = {c: last[c][1] if c in last else packs[c]["gas"] for c in cs}
        tot = sum(packs[c]["charge"] * K.GWP[gas[c]] for c in cs) / 1000
        r4 = sum(packs[c]["charge"] * K.GWP[gas[c]] for c in cs if gas[c] == "R404A") / 1000
        ok("full charge CO2e %s" % g, int(half_up(tot)), fig["asks"]["charge_co2e_t"][g])
        ok("R404A CO2e %s" % g, int(half_up(r4)), fig["asks"]["r404a_co2e_t"][g])
    used = {}
    for r in rows(os.path.join(T, K.FILES["cylinders"])):
        used[r["job_no"]] = used.get(r["job_no"], 0.0) + float(r["gross_before_kg"]) - float(r["gross_after_kg"])
    seen, kg = set(), {g: 0.0 for g in K.REGIONS}
    for j in jobs:
        if j["asset"] in eq and d(j["job_date"]).year == 2026 and j["job_no"] not in seen:
            seen.add(j["job_no"])
            kg[stores[int(j["store"])]] += used.get(j["job_no"], 0.0)
    for g in K.REGIONS:
        ok("cabinets and cold rooms %s" % g, half_up(kg[g], 1), fig["asks"]["equipment_kg"][g])
    bad = [o for o in out if not o[1]]
    for label, good, detail in out:
        print("%s  verify %s  [%s]" % ("PASS" if good else "FAIL", label, detail))
    print("verify: %d figures, %d differ" % (len(out), len(bad)))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(run(sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(HERE)))
