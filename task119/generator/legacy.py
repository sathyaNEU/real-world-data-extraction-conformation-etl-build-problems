"""From the generator's internal records to the network's extracts: referral ids, the migrated CCRS rows
(UTC clock, requested level, temporary identities, no admission time), the pilot-ward copies entered on
both systems during the parallel run, the legacy unit feed's bed-episode rows, the level history, the
transfer audit and the identity merges."""
import datetime as dt
from collections import defaultdict

import numpy as np

from common import (CODE, TRUSTS, LETTERS, PARALLEL0, PARALLEL1, lm, day_of, fmt, to_dt, local_to_utc_min, own_unit,
                    rng, DAY, CORE_UNITS)
from people import PILOT_WARDS

GO = lm(dt.date(2024, 4, 2), 0, 0)
OUTCOME = {"admitted": "Admitted", "stood_down": "Stood down", "died": "Died before admission"}


def d_s(d):
    return d.strftime("%Y-%m-%d") if d is not None else ""


def finalize(world, P, stays, refs, death, temp, eps, verified):
    r = rng("legacy")
    out = {}
    person = lambda pid: P.p[pid]["person"]
    vkey = lambda pid: verified.get(person(pid), P.p[pid]["key"])

    # ---------------------------------------------------------------- level semantics on legacy rows
    dv4oc = [ref for ref in refs if "DV4oc" in ref["tags"]]
    dv4oc.sort(key=lambda x: x["rid"])
    for i, ref in enumerate(dv4oc):
        ref["lvl_story"] = "esc" if i % 9 in (0, 2, 4, 6, 8) else "step"
    for ref in refs:
        ref.setdefault("lvl_story", None)
        if ref["legacy"] and ref["lvl_story"] is None and ref["wid"] is None and not ref["tags"]:
            u = r.random()
            if ref["level_dec"] == 2 and u < 0.05:
                ref["lvl_story"] = "deesc"
            elif ref["level_dec"] == 3 and u < 0.035:
                ref["lvl_story"] = "esc"
            elif ref["level_dec"] == 3 and ref["outcome"] == "admitted" and u < 0.06:
                ref["lvl_story"] = "step"
        if "DV4" in ref["tags"]:
            ref["lvl_story"] = "deesc"
    for ref in refs:
        s = ref["lvl_story"]
        if s == "deesc":
            ref["level_first"], ref["level_field"] = 3, 3
        elif s == "esc":
            ref["level_first"], ref["level_field"] = 2, 3
        else:
            ref["level_first"], ref["level_field"] = ref["level_dec"], ref["level_dec"]
    # ---------------------------------------------------------------- pilot-ward copies (parallel run)
    copies = []
    for ref in refs:
        d = day_of(ref["dta"])
        if PARALLEL0 <= d <= PARALLEL1 and ref["ward"] in PILOT_WARDS[ref["letter"]]:
            c = dict(ref)
            c["copy_of"] = ref["rid"]
            c["is_copy"] = True
            lag = int(r.integers(2, 16))
            c["dta"] = ref["dta"] + lag
            c["received"] = ref["received"] + int(r.integers(1, lag + 1))
            c["legacy"] = False
            if c["outcome"] != "admitted":
                c["end"] = ref["end"] + int(r.integers(0, 6))
            copies.append(c)
            ref["has_copy"] = True
    for ref in refs:
        ref.setdefault("is_copy", False)
        ref.setdefault("has_copy", False)
    allrefs = sorted(refs + copies, key=lambda x: (x["received"], x["rid"], x["is_copy"]))
    # ---------------------------------------------------------------- referral ids
    n = 4812337
    seq = defaultdict(int)
    for ref in allrefs:
        if ref["legacy"]:
            n += int(r.integers(1, 4))
            ref["ref_id"] = "CC%07d" % n
        else:
            t = to_dt(ref["received"])
            ym = t.strftime("%y%m")
            seq[ym] += int(r.integers(1, 3))
            ref["ref_id"] = "R%s-%05d" % (ym, seq[ym])
    # ---------------------------------------------------------------- referral log rows
    rows = []
    for ref in allrefs:
        L = ref["letter"]
        key = temp.get(ref["rid"]) if (ref["legacy"] and ref["rid"] in temp) else vkey(ref["pid"])
        if ref["legacy"]:
            conv = local_to_utc_min
            lvl = ref["level_field"]
            oat = "" if ref["outcome"] == "admitted" else fmt(conv(ref["end"]))
        else:
            conv = lambda m: m
            lvl = ref["level_dec"]
            oat = fmt(ref["end"])
        rows.append({"referral_id": ref["ref_id"], "received_at": fmt(conv(ref["received"])),
                     "referring_trust": CODE[L], "referred_from": ref["ward"], "patient_key": key,
                     "dta_at": fmt(conv(ref["dta"])), "level_of_care": lvl, "outcome": OUTCOME[ref["outcome"]],
                     "outcome_at": oat, "admitting_unit": ref["unit"] or "", "_rid": ref["rid"],
                     "_copy": ref["is_copy"]})
    out["referrals"] = rows
    ref_id_of = {ref["rid"]: ref["ref_id"] for ref in allrefs if not ref["is_copy"]}
    copy_id_of = {ref["copy_of"]: ref["ref_id"] for ref in allrefs if ref["is_copy"]}
    out["ref_id_of"] = ref_id_of
    out["copy_id_of"] = copy_id_of
    # ---------------------------------------------------------------- level history (legacy rows only)
    hist = []
    for ref in allrefs:
        if not ref["legacy"]:
            continue
        s = ref["lvl_story"]
        rec, dta = local_to_utc_min(ref["received"]), local_to_utc_min(ref["dta"])
        ev = [(rec, "REQUEST", ref["level_first"])]
        if s == "esc":
            ev.append((rec + max(3, (dta - rec) // 2), "REVISED REQUEST", 3))
        ev.append((dta, "DECISION", ref["level_dec"]))
        if s == "step":
            ev.append((local_to_utc_min(ref["end"]) + int(r.integers(600, 4000)), "LEVEL CHANGE", 2))
        for i, (t, e, lv) in enumerate(ev, start=1):
            hist.append({"referral_id": ref["ref_id"], "entry_no": i, "recorded_at": fmt(t), "entry": e, "level": lv})
    out["level_history"] = hist
    # ---------------------------------------------------------------- unit stays (bed episodes before go-live)
    ref_of_stay = {}
    for ref in refs:
        if ref["stay"] is not None:
            ref_of_stay[ref["stay"]] = ref
    srows = []
    lb = 7340021
    st = 1102544
    order = sorted(range(len(stays)), key=lambda i: (stays[i]["admit"], stays[i]["unit"], stays[i]["pid"]))
    for i in order:
        s = stays[i]
        ref = ref_of_stay.get(i)
        p = P.p[s["pid"]]
        if ref is not None:
            key = temp.get(ref["rid"]) if (ref["legacy"] and ref["rid"] in temp) else vkey(s["pid"])
            rid = ref["ref_id"]
            src = "04" if ref["ward"] == "ED" else "06"
            typ = s["type"]
        else:
            key = p["key"]
            rid = ""
            typ, src = s["type"], s["src"]
            if p["kind"] == "theatre_emerg":
                typ, src = "01", "01"
        legacy = s["admit"] < GO
        seg = s["rows"] if legacy else [(s["admit"], s["discharge"])]
        for j, (a, b) in enumerate(seg):
            if legacy:
                lb += int(r.integers(1, 3))
                sid = "LB%07d" % lb
            else:
                st += int(r.integers(1, 3))
                sid = "ST%07d" % st
            srows.append({"stay_id": sid, "unit_code": s["unit"], "referral_id": rid if j == 0 else "",
                          "patient_key": key, "admitted_at": fmt(a), "discharged_at": fmt(b),
                          "admission_type": typ, "source_location": src, "_stay": i})
    out["stays"] = srows
    # ---------------------------------------------------------------- identity merges
    merges = []
    for rid, tk in sorted(temp.items(), key=lambda kv: kv[1]):
        ref = [x for x in refs if x["rid"] == rid][0]
        merged = day_of(ref["dta"]) + dt.timedelta(days=int(r.integers(1, 22)))
        merges.append({"temporary_key": tk, "verified_key": vkey(ref["pid"]), "merged_on": d_s(merged),
                       "registering_trust": CODE[ref["letter"]]})
    out["merges"] = merges
    # ---------------------------------------------------------------- transfer audit (local clock, verified keys)
    tx = []
    k = 30117
    for ref in sorted(refs, key=lambda x: (x["dta"], x["rid"])):
        if ref["outcome"] != "admitted" or ref["stay"] is None:
            continue
        s = stays[ref["stay"]]
        if own_unit(ref["letter"], day_of(ref["dta"])) == s["unit"]:
            continue
        k += int(r.integers(1, 3))
        dep = s["admit"] + int(r.integers(25, 95))
        arr = dep + int(r.integers(20, 75))
        tx.append({"transfer_ref": "TX%06d" % k, "patient_key": vkey(ref["pid"]),
                   "from_trust": CODE[ref["letter"]], "from_site": TRUSTS[ref["letter"]][2], "to_unit": s["unit"],
                   "decision_at": fmt(ref["dta"]), "bed_confirmed_at": fmt(s["admit"]), "departed_at": fmt(dep),
                   "arrived_at": fmt(arr)})
    out["transfers"] = tx
    # ---------------------------------------------------------------- episodes
    erows = []
    e = 610000000
    for row in sorted(eps, key=lambda x: (x["admission_date"], x["spell"], x["episode_order"])):
        e += int(r.integers(1, 4))
        erows.append({"episode_id": "EP%09d" % e, "spell_id": row["spell"], "patient_key": row["key"],
                      "provider_code": CODE[row["provider"]], "admission_date": d_s(row["admission_date"]),
                      "admission_method": row["admission_method"], "episode_order": row["episode_order"],
                      "episode_start": d_s(row["episode_start"]), "episode_end": d_s(row["episode_end"]),
                      "main_specialty": row["main_specialty"], "discharge_date": d_s(row["discharge_date"]),
                      "discharge_method": row["discharge_method"] or "",
                      "discharge_destination": row["discharge_destination"] or "",
                      "date_of_death": d_s(row["date_of_death"])})
    out["episodes"] = erows
    return out
