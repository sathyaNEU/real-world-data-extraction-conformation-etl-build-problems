"""The ask sheet's cracker and mirror, run on the cut pack (target.zip) against the golden in submission.md.

The cracker landed the call, ran the hygiene battery (UTC read as BST, counter wraps added, a restart's jump
dropped, each counter read as it is named), executed the asking sentences' pins (every paid row summed, each claim
banded by its train's lateness at the destination in the running record on the claim's journey date, matched on the
stated origin and booked departure, a claim it cannot match left out) and read every document. The careful row is
the cracker that also tries an unmatched claim the other way round. The mirror stops on the most attractive wrong
rung: the same-train replay for the call, the same battery for the gates and the band the claims file paid for
Delay Repay. Scored on 38 (call side), 7 (instructions) and 55 (asks), a hit being the golden figure at the asked
rounding. Prints the rows, the pair, the mirror's ask leakage and, for the record, a full includer that handles
every device (the verifier's route)."""
import datetime as dt
import os
import re
import sys
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import verify as V          # the independent loader and replay; no generator module is imported

DAY = dt.date(2026, 10, 13)
LO, HI = dt.date(2026, 9, 7), dt.date(2026, 11, 27)
LINES = {"Crossmoor": "Crossmoor line", "Ambrey": "Ambrey line", "Holm Ferry": "Holm Ferry line"}
BANDS = ["15 to 29", "30 to 59", "60 or more"]


def golden(b4):
    g = {"save": {}, "gates": {}, "repay": {}}
    for nm, v in re.findall(r"^   - ([A-Z][\w' ]+): ([\d,]+)$", b4, re.M):
        g["save"][nm] = int(v.replace(",", ""))
    m = re.search(r"Pick (.+?) \(([\d,]+)\); runner-up (.+?) \(([\d,]+)\); gap ([\d,]+)", b4)
    g["pick"], g["ru"], g["gap"] = m.group(1), m.group(3), int(m.group(5).replace(",", ""))
    for nm, e, l_ in re.findall(r"- ([\w' ]+): entered ([\d,]+); left ([\d,]+)", b4):
        g["gates"][nm] = (int(e.replace(",", "")), int(l_.replace(",", "")))
    for ln, a, b, c in re.findall(r"- ([\w ]+ line): 15 to 29 minutes £([\d,]+); 30 to 59 minutes £([\d,]+); "
                                  r"60 minutes or more £([\d,]+)", b4):
        for band, v in zip(BANDS, (a, b, c)):
            g["repay"][(ln, band)] = int(v.replace(",", ""))
    return g


def gates_battery(pack):
    crs_name = {s["crs"]: s["station"] for s in pack["stations"]}
    by = defaultdict(list)
    for r in pack["gates"]:
        by[r["array"]].append((dt.datetime.strptime(r["reading_utc"], "%Y-%m-%d %H:%M:%S"), r["crs"],
                               int(r["entries"]), int(r["exits"])))
    out = defaultdict(lambda: [0, 0])
    for arr, rows in by.items():
        rows.sort()
        for (t0, c0, e0, x0), (t1, c1, e1, x1) in zip(rows, rows[1:]):
            lt = t1 + dt.timedelta(hours=1)
            if (lt - dt.timedelta(seconds=1)).date() != DAY:
                continue
            de, dx = (e1 - e0) % 65536, (x1 - x0) % 65536
            out[crs_name[c1]][0] += de if de <= 2000 else 0
            out[crs_name[c1]][1] += dx if dx <= 2000 else 0
    return {k: tuple(v) for k, v in out.items()}


def repay_routes(pack, how):
    """how: 'cracker' (every paid row, the band from the record on the stated date, matched on the stated origin and
    time, an unmatched claim dropped), 'careful' (the cracker with the return legs matched the other way round),
    'paid_band' (every row, the band the claims file paid), 'full' (the verifier's route)."""
    LO_, HI_ = LO, HI
    if how == "paid_band":
        crs_line = {s["crs"]: s["lines"] for s in pack["stations"]}
        out = defaultdict(float)
        for r in pack["repay"]:
            jd = dt.date.fromisoformat(r["journey_date"])
            if r["decision"] != "APPROVED" or not (LO_ <= jd <= HI_) or jd.weekday() > 4 \
                    or "RVC" not in (r["origin_crs"], r["destination_crs"]):
                continue
            other = r["destination_crs"] if r["origin_crs"] == "RVC" else r["origin_crs"]
            band = "60 or more" if r["band_paid"] in ("60 to 119", "120 or more") else r["band_paid"]
            out[(LINES[crs_line[other]], band)] += float(r["amount_gbp"])
        return {k: int(round(v)) for k, v in out.items()}
    rp = V.repay(pack, reverse=how in ("careful", "full"), redate=how == "full")
    return {(LINES[k[0]], k[1]): int(round(v)) for k, v in rp.items()}


def score(name, g, call, gates, repay):
    """call: dict with pick, saves, ru, gap. Returns (total, ask points, rows)."""
    rows = []
    main = 0.0
    main += 12 * (call["pick"] == g["pick"])
    main += 8 * (call["saves"].get(g["pick"]) == g["save"][g["pick"]])
    main += 4 * (call["ru"] == g["ru"])
    main += 4 * (call["saves"].get(g["ru"]) == g["save"][g["ru"]])
    main += 4 * (call["gap"] == g["gap"])
    others = [c for c in g["save"] if c not in (g["pick"], g["ru"])]
    main += sum(1.5 * (call["saves"].get(c) == g["save"][c]) for c in others)
    per = 55.0 / (2 * len(g["gates"]) + len(g["repay"]))
    ask = 0.0
    for st, (e, l_) in g["gates"].items():
        got = gates.get(st, (None, None))
        for lab, want, have in (("entered", e, got[0]), ("left", l_, got[1])):
            hit = want == have
            ask += per * hit
            rows.append(("gates %s %s" % (st, lab), want, have, hit))
    for k, want in g["repay"].items():
        have = repay.get(k)
        hit = want == have
        ask += per * hit
        rows.append(("Delay Repay %s %s" % k, want, have, hit))
    return main + 7 + ask, main, ask, rows


def main(zp=None):
    zp = zp or os.path.join(TASK, "target.zip")
    pack = V.load(zp)
    g = golden(V.block4(os.path.join(TASK, "submission.md")))
    full_sv, _ = V.savings(pack, follow_units=True)
    same_sv, _ = V.savings(pack, follow_units=False)

    def call_from(sv):
        r = {c: int(round(v / 100.0) * 100) for c, v in sv.items()}
        o = sorted(sv, key=lambda c: -sv[c])
        return {"pick": o[0], "ru": o[1], "saves": r, "gap": int(round((sv[o[0]] - sv[o[1]]) / 100.0) * 100)}

    bat = gates_battery(pack)
    full_gates = V.gates(pack)
    full_gates = {k: (v["entered"], v["left"]) for k, v in full_gates.items()}
    C, cm, ca, crow = score("cracker", g, call_from(full_sv), bat, repay_routes(pack, "cracker"))
    S, sm, sa, srow = score("mirror", g, call_from(same_sv), bat, repay_routes(pack, "paid_band"))
    F, fm, fa, frow = score("full includer", g, call_from(full_sv), full_gates, repay_routes(pack, "full"))
    K_, km, ka, krow = score("careful", g, call_from(full_sv), bat, repay_routes(pack, "careful"))
    print("%-34s %8s %8s %8s %8s" % ("ask figure", "golden", "cracker", "mirror", "full"))
    for (lab, want, ch, chit), (_, _, sh, shit), (_, _, fh, fhit) in zip(crow, srow, frow):
        print("%-34s %8s %8s %8s %8s   cracker %s, mirror %s" % (lab, want, ch, sh, fh, "hit" if chit else "miss",
                                                                  "hit" if shit else "miss"))
    print("cracker: call side %.1f, asks %.1f of 55, total %.1f" % (cm, ca, C))
    print("mirror: call side %.1f, asks %.1f of 55, total %.1f (call %s)" % (sm, sa, S, call_from(same_sv)["pick"]))
    print("careful (cracker plus the return legs reversed): asks %.1f of 55, total %.1f" % (ka, K_))
    print("full includer: call side %.1f, asks %.1f of 55, total %.1f" % (fm, fa, F))
    print("pair ceiling (cracker and mirror): %.1f" % ((C + S) / 2))
    print("mirror leakage: %.1f per cent of ask weight" % (100 * sa / 55))
    print("two fifths each: %.1f; full includer with the mirror: %.1f" %
          (((cm + 7 + 22) + (sm + 7 + 22)) / 2, (F + S) / 2))
    print("cracker misses every ask figure: %s" % (not any(r[3] for r in crow)))
    return 0 if (C + S) / 2 <= 60 and 100 * sa / 55 < 50 and not any(r[3] for r in crow) else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else None))
