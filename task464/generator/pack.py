"""task464 architecture 9: write the pack's data files from the clean truth.

Each clinical system exports in its own layout. System A (Fennbridge, Thistlecombe, Larkspur Road, Pellow Green)
writes UK dates, the product as its prescribers see it and the quantity with its unit word; system B (Cobbet
Street, Marrick House, Wyndhollow) writes ISO dates, its own product strings and the quantity and unit apart, as
JSON lines. The network's searches ran on 1 December 2026 and cover issues from 1 January 2024.

Nothing written here states a rate, an expected count or a ranking of the practices.
"""
import csv, json, os, collections
import numpy as np
import world as W

OUT = os.environ.get("T464_TARGET") or os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "target")

SYS_A = [p["key"] for p in W.PRACTICES if p["system"] == "A"]
SYS_B = [p["key"] for p in W.PRACTICES if p["system"] == "B"]


def uk(t):
    d = W.date_of(t); return "%02d/%02d/%04d" % (d.day, d.month, d.year)


def product_a(r):
    unit = "capsules" if r["form"] == "capsules" else "tablets"
    return "%s %s %s" % (r["drug"], r["strength"], unit)


def product_b(r):
    unit = "caps" if r["form"] == "capsules" else "tabs"
    return "%s %s %s" % (r["drug"].upper().replace(" ERBUMINE", " ERBUMINE"), unit, r["strength"])


def unit_word(r):
    return "capsule" if r["form"] == "capsules" else "tablet"


REFS = {}


def assign_refs(templates):
    """Each system numbers repeats as its prescribers add them: system A from one counter across its practices,
    system B per practice, each step the repeats, acutes and other items written in between."""
    REFS.clear()
    r = np.random.default_rng([46993])
    a = 3184207
    b = {p["code"]: int(r.integers(20000, 60000)) for p in W.PRACTICES if p["system"] == "B"}
    for tp in sorted(templates, key=lambda x: (x["authorised"], x["tid"])):
        p = W.BY_KEY[tp["key"]]
        if p["system"] == "A":
            a += int(r.integers(1, 30))
            REFS[tp["tid"]] = "R%07d" % a
        else:
            b[p["code"]] += int(r.integers(1, 12))
            REFS[tp["tid"]] = "AU-%s-%06d" % (p["code"][-3:], b[p["code"]])


def tref_a(tp):
    return REFS[tp["tid"]]


def tref_b(tp):
    return REFS[tp["tid"]]


def tref(tp):
    return REFS[tp["tid"]]


# Item cancellations other than the 2025 out-of-stock re-sends, as the EPS tracker's item report carries them: an
# item cancelled on the day it was signed and re-signed at once, on ACE inhibitor, ARB and DOAC repeats.
OTHER_CANCEL = [("Prescribing error", 0.36), ("Change to medication treatment regime", 0.22),
                ("Change to presentation", 0.12), ("At the Pharmacist's request", 0.14), ("Other", 0.16)]
OTHER_CANCEL_P = 0.002


def other_cancellations(rows):
    import sim as _S
    r = np.random.default_rng([46994])
    reasons = [x[0] for x in OTHER_CANCEL]; wts = np.array([x[1] for x in OTHER_CANCEL]); wts = wts / wts.sum()
    canc, extra = [], []
    for x in rows:
        if x["slot"] not in ("raas", "doac") or x["acute"] or x["cancelled"] or x["twin"] or x["reissue"]:
            continue
        if r.random() >= OTHER_CANCEL_P:
            continue
        why = reasons[int(r.choice(len(reasons), p=wts))]
        canc.append(dict(token=x["eps"], pid=x["pid"], key=x["key"], t=x["t"], drug=x["drug"], strength=x["strength"],
                         form=x["form"], qty=x["qty"], cancelled_on=x["t"], reason=why))
        extra.append(dict(x, eps=_S.eps_id(r), reissue=True))
    return canc, extra


def write(w):
    os.makedirs(OUT, exist_ok=True)
    stats = {}
    tps = w.templates
    assign_refs(tps)
    # ------------------------------------------------------------ issues
    rows = [r for r in w.issues if W.EXTRACT_FROM <= r["t"] <= W.ASOF]
    rows.sort(key=lambda r: (r["t"], W.BY_KEY[r["key"]]["code"], r["pid"], r["slot"], r["eps"]))
    other_canc, resent = other_cancellations(rows)
    rows += resent
    rows.sort(key=lambda r: (r["t"], W.BY_KEY[r["key"]]["code"], r["pid"], r["slot"], r["eps"]))
    pa = os.path.join(OUT, "repeat_issues_system_a_2024-01_to_2026-11.csv")
    na = nb = 0
    with open(pa, "w", newline="", encoding="utf-8") as fa, \
            open(os.path.join(OUT, "repeat_issues_system_b_2024-01_to_2026-11.jsonl"), "w", encoding="utf-8") as fb:
        wa = csv.writer(fa, lineterminator="\r\n")
        wa.writerow(["Practice Code", "Patient Ref", "Issue Date", "Drug", "Quantity", "Course", "Repeat Ref",
                     "EPS Prescription ID"])
        for r in rows:
            p = W.BY_KEY[r["key"]]
            if p["system"] == "A":
                wa.writerow([p["code"], r["pid"], uk(r["t"]), product_a(r), "%d %s" % (r["qty"], unit_word(r)),
                             "Acute" if r["acute"] else "Repeat", "" if r["tid"] is None else tref_a(tps[r["tid"]]),
                             r["eps"]])
                na += 1
            else:
                fb.write(json.dumps({"org": p["code"], "patient_pseudo": r["pid"], "issued": W.iso(r["t"]),
                                     "product": product_b(r), "qty": r["qty"], "qty_unit": unit_word(r),
                                     "course": "acute" if r["acute"] else "repeat",
                                     "authorisation": None if r["tid"] is None else tref_b(tps[r["tid"]]),
                                     "eps_id": r["eps"]}, separators=(",", ":")) + "\n")
                nb += 1
    stats["issues_a"] = na; stats["issues_b"] = nb
    # ------------------------------------------------------------ repeat authorisations
    # a repeat is in the search when it was active at any point from 1 January 2024
    successor = {}
    by_pid_slot = collections.defaultdict(list)
    for tp in tps:
        by_pid_slot[(tp["pid"], tp["slot"])].append(tp)
    keep = []
    for tp in tps:
        if tp["authorised"] > W.ASOF:
            continue
        end = tp["ended"]
        if end is not None and end < W.EXTRACT_FROM:
            continue
        if tp["authorised"] < W.EXTRACT_FROM and tp["made"] == 0:
            continue
        keep.append(tp)
    keep.sort(key=lambda tp: (W.BY_KEY[tp["key"]]["code"], tp["pid"], tp["authorised"], tp["slot"]))
    mi_filed = {(e["pid"], e["t"]): e["filed"] for e in w.events if e["code"] == "22298006"}
    fa = open(os.path.join(OUT, "repeat_authorisations_system_a.csv"), "w", newline="", encoding="utf-8")
    fbb = open(os.path.join(OUT, "repeat_authorisations_system_b.csv"), "w", newline="", encoding="utf-8")
    wa = csv.writer(fa, lineterminator="\r\n"); wb = csv.writer(fbb, lineterminator="\n")
    wa.writerow(["Practice Code", "Patient Ref", "Repeat Ref", "Drug", "Dosage", "Quantity",
                 "Authorised Issues", "Authorised Date", "End Date", "Status"])
    wb.writerow(["org", "patient_pseudo", "authorisation", "product", "directions", "qty_per_issue",
                 "issues_authorised", "start_date", "end_date"])
    nta = ntb = 0
    for tp in keep:
        p = W.BY_KEY[tp["key"]]
        end = tp["ended"] if (tp["ended"] is not None and tp["ended"] <= W.ASOF) else None
        # a repeat left running when a patient stops one medicine, or when a review is not done, stays active on the
        # list until a clinician adds a new repeat of that medicine, which ends it
        if tp["end_reason"] in ("stopped", "review not done", "course complete"):
            end = None
        # a repeat the hospital changed is ended when the practice files the discharge summary, not before
        if tp["end_reason"] == "changed in hospital" and end is not None and \
                mi_filed.get((tp["pid"], tp["ended"]), W.ASOF + 2) > W.ASOF + 1:
            end = None
        if end is None:
            later = [x for x in by_pid_slot[(tp["pid"], tp["slot"])] if x["authorised"] > tp["authorised"]
                     and x["authorised"] <= W.ASOF]
            end = min(x["authorised"] for x in later) if later else None
        if p["system"] == "A":
            wa.writerow([p["code"], tp["pid"], tref_a(tp), product_a(tp), tp["directions"],
                         "%d %s" % (tp["qty"], unit_word(tp)), tp["M"], uk(tp["authorised"]),
                         "" if end is None else uk(end), "Active" if end is None else "Inactive"])
            nta += 1
        else:
            wb.writerow([p["code"], tp["pid"], tref_b(tp), product_b(tp), tp["directions"], tp["qty"],
                         tp["M"], W.iso(tp["authorised"]), "" if end is None else W.iso(end)])
            ntb += 1
    fa.close(); fbb.close()
    stats["templates_a"] = nta; stats["templates_b"] = ntb
    # ------------------------------------------------------------ register
    pids = set(r["pid"] for r in rows)
    with open(os.path.join(OUT, "patient_register_2026-12-01.csv"), "w", newline="", encoding="utf-8") as fh:
        wr = csv.writer(fh, lineterminator="\n")
        wr.writerow(["patient_ref", "practice_code", "year_of_birth", "sex", "registered", "deregistered",
                     "deregistration_reason"])
        reg_rows = []
        for pid in sorted(pids):
            P = w.patients[pid]
            for k, a, b, why in P["episodes"]:
                if b is not None and b < W.EXTRACT_FROM:
                    continue
                if a > W.ASOF:
                    continue
                bb = b if (b is not None and b <= W.ASOF) else None
                reason = ""
                if bb is not None:
                    reason = {"death": "Death", "left": "Left practice area", "transferred": "Registered at another practice"}[why]
                reg_rows.append([W.BY_KEY[k]["code"], pid, P["yob"], P["sex"], W.iso(a), "" if bb is None else W.iso(bb), reason])
        reg_rows.sort(key=lambda r: (r[0], r[1], r[4]))
        for r in reg_rows:
            wr.writerow([r[1], r[0], r[2], r[3], r[4], r[5], r[6]])
    stats["register"] = len(reg_rows)
    # ------------------------------------------------------------ cancellations (the EPS tracker's item report)
    canc = [c for c in w.cancellations if W.EXTRACT_FROM <= c["t"] <= W.ASOF] + other_canc
    canc.sort(key=lambda c: (c["cancelled_on"], c["token"], c["drug"], c["strength"]))
    with open(os.path.join(OUT, "eps_item_cancellations_2024-2026.csv"), "w", newline="", encoding="utf-8") as fh:
        wr = csv.writer(fh, lineterminator="\n")
        wr.writerow(["prescription_id", "ods_code", "patient_ref", "signed_date", "item", "quantity",
                     "cancelled_date", "cancellation_reason"])
        for c in canc:
            r = dict(drug=c["drug"], strength=c["strength"], form=c["form"])
            wr.writerow([c["token"], W.BY_KEY[c["key"]]["code"], c["pid"], W.iso(c["t"]), product_a(r), c["qty"],
                         W.iso(c["cancelled_on"]), c["reason"]])
    stats["cancellations"] = len(canc)
    return stats
