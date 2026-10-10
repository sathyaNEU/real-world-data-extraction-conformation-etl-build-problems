"""The regional data service's theatre extract: one row per theatre case for the patients in the referral record or
the unit feed. Every unit stay that came from theatre has its case, the patient leaving recovery before the bed was
assigned, except the elective centre beds Stennock's unit assigned at its morning bed meeting from the platform's
go-live, whose patients were still in theatre when the bed was assigned. Background cases add the ward surgery of
referred patients."""
import datetime as dt
from collections import defaultdict

from common import CODE, TRUSTS, lm, day_of, fmt, rng, own_unit, DST_WINDOWS
import plan

EC_SITE = "Stennock Treatment Centre"
ELECTIVE_CC = ["H33.4", "G27.1", "J02.1", "L19.4", "M02.3", "H10.1", "G28.1", "J56.1", "H06.9", "M34.1"]
EMERGENCY_CC = ["T30.1", "H07.9", "H33.5", "G35.2", "L18.6", "J72.1"]
WARD = ["H01.1", "J18.3", "W46.1", "W19.1", "T20.1", "S57.1", "Q07.4", "H59.2", "T24.4", "W38.1", "H20.1", "T85.2"]
CC_DEST = "Critical care unit"


def p_min(s):
    return lm(dt.datetime.strptime(s, "%Y-%m-%d %H:%M"))


def clear(t):
    for a, b in DST_WINDOWS:
        if a - 5 <= t <= b + 5:
            return b + 10
    return t


def case_times(r, left, not_before=None, urgency="Elective"):
    rec = int(r.integers(25, 95))
    op = int(r.integers(70, 320)) if urgency in ("Elective", "Expedited") else int(r.integers(45, 200))
    out_th = left - rec
    into = out_th - op
    if not_before is not None and into < not_before + 10:
        span = left - (not_before + 10)
        rec = max(10, span // 3)
        out_th = left - rec
        into = not_before + 10
        assert into < out_th, ("theatre case squeeze", fmt(left))
    return into, out_th


def build_theatre(world, P, stays, refs, out):
    r = rng("theatre")
    first = {}
    key_of = {}
    for row in out["stays"]:
        i = row["_stay"]
        a = p_min(row["admitted_at"])
        if i not in first or a < first[i]:
            first[i] = a
            key_of[i] = row["patient_key"]
    src_of = {row["_stay"]: row["source_location"] for row in out["stays"] if row["referral_id"] or True}
    ref_of_stay = {x["stay"]: x for x in refs if x.get("stay") is not None}
    forced = defaultdict(list)
    for u, U in world.units.items():
        for f in U.forced:
            forced[u].append(f["t"])
    cases = []
    for i, s in enumerate(stays):
        if i not in first or src_of.get(i) not in ("01", "02"):
            continue
        p = P.p[s["pid"]]
        ref = ref_of_stay.get(i)
        t0 = first[i]
        unit_trust = s["unit"].split("-")[0]
        prov, site, urg = unit_trust, None, "Elective"
        not_before = None
        if p.get("booked_arrive") is not None:
            w = world.waits_by_id[p["booked_wid"]]
            arrive = p["booked_arrive"]
            hi = min(plan.EC_TRANSIT[1], arrive - w["dta"] - plan.HOLD_CLEAR)
            assert hi >= plan.EC_TRANSIT[0], ("held bed transit", w["wid"])
            left = arrive - int(r.integers(plan.EC_TRANSIT[0], hi + 1))
            site = EC_SITE
            not_before = s["admit"] - 60
            kind = "held"
        elif ref is not None and own_unit(ref["letter"], day_of(ref["dta"])) != s["unit"]:
            prov = CODE[ref["letter"]]
            site = TRUSTS[ref["letter"]][2]
            dep = out["tx_dep"][i]
            left = dep - int(r.integers(5, 21))
            if ref["ward"] == "REC":
                left = max(left, ref["dta"] + 2)
            kind = "transfer"
        elif p.get("ec"):
            site = EC_SITE
            left = t0 - int(r.integers(8, 36))
            if ref is not None:
                left = max(left, ref["dta"] + 2)
            kind = "local"
        else:
            if p["kind"] == "theatre_emerg":
                urg = str(r.choice(["Immediate", "Urgent", "Urgent"]))
            left = t0 - int(r.integers(3, 21))
            nb = [x for x in forced[s["unit"]] if x < t0 and t0 - x < 2880]
            not_before = max(nb) if nb else None
            kind = "local"
        if site is None:
            site = [v[2] for v in TRUSTS.values() if v[0] == prov][0]
        assert left <= t0 - 2 or kind in ("held", "transfer"), ("left recovery after the bed", i, kind)
        into, out_th = case_times(r, left, not_before, urg)
        proc = str(r.choice(ELECTIVE_CC if urg in ("Elective", "Expedited") else EMERGENCY_CC))
        cases.append({"key": key_of[i], "prov": prov, "site": site, "urg": urg, "proc": proc, "into": into,
                      "out": out_th, "left": left, "dest": CC_DEST, "kind": kind, "stay": i})
    # ward surgery for referred patients (texture): around the referral, at the referring trust's hospital
    rb = rng("theatre_bg")
    for ref in refs:
        if ref.get("stay") is not None and src_of.get(ref["stay"]) in ("01", "02"):
            continue
        if ref["ward"] in ("REC", "SDU") or rb.random() > 0.09:
            continue
        d = day_of(ref["dta"]) + dt.timedelta(days=int(rb.integers(-3, 6)))
        urg = str(rb.choice(["Urgent", "Expedited", "Elective", "Urgent"]))
        into = clear(lm(d, 8, 30) + int(rb.integers(0, 11 * 60)))
        op = int(rb.integers(35, 150))
        rec = int(rb.integers(25, 80))
        cases.append({"key": P.p[ref["pid"]]["key"], "prov": CODE[ref["letter"]], "site": TRUSTS[ref["letter"]][2],
                      "urg": urg, "proc": str(rb.choice(WARD)), "into": into, "out": into + op,
                      "left": clear(into + op + rec), "dest": "Ward", "kind": "bg", "stay": None})
    cases.sort(key=lambda c: (c["into"], c["prov"], c["key"]))
    rows = []
    n = 40211077
    for c in cases:
        n += int(r.integers(1, 4))
        rows.append({"case_id": "TC%09d" % n, "patient_key": c["key"], "provider_code": c["prov"],
                     "site_name": c["site"], "case_date": fmt(c["into"])[:10], "urgency": c["urg"],
                     "procedure_code": c["proc"], "into_theatre_at": fmt(c["into"]),
                     "out_of_theatre_at": fmt(c["out"]), "left_recovery_at": fmt(c["left"]),
                     "recovery_destination": c["dest"], "_kind": c["kind"], "_stay": c["stay"]})
    return rows
