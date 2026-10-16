"""The carriers' records of Corvane's matters: one carrier claim per matter under each entity's occurrence policies,
opened when the carrier first heard of it (a precautionary notice, or the weekly claims report), carrying the
reference Corvane gave it then, and valued on the carrier's own reserves."""
from __future__ import annotations

import datetime as dt

import common as K


def _on_line(inc):
    return any(d.line != "CONTRACT" for c in inc.claims for d in c.defendants) or inc.route == "NOTICE"


def expiring_era(inc):
    """The matter falls under the entity's expiring carrier's occurrence policies: its incident is on or after the
    date the entity moved to that carrier (earlier incidents stay with the former carrier)."""
    return inc.date >= K.ENTITIES[inc.entity]["carrier_from"]


def mark_clinician_reported(incidents, V=K.VALUATION):
    """Suits a clinician sent straight to the carrier: the policy asks the insured to forward a summons at once, and
    the carrier opens its file from the clinician's copy, which carries no Corvane reference. One open suit at each
    entity and about two in five of the closed ones, each the only incident its entity has on its date of care."""
    import claims as C
    rng = K.claims_stream("clinician-reported")
    dates = {}
    for inc in incidents:
        dates.setdefault((inc.entity, inc.date), []).append(inc)
    open_by, closed = {}, []
    for inc in incidents:
        inc.clinician_reported = False
        if inc.route != "DIRECT" or inc.notice is not None or len(inc.claims) != 1 or len(dates[(inc.entity,
                                                                                                    inc.date)]) > 1:
            continue
        c = inc.claims[0]
        if c.matter_type != "Suit" or c.prior is not None or c.report is None or c.report > V:
            continue
        if not any(d.line != "CONTRACT" for d in c.defendants) or not expiring_era(inc):
            continue
        if C._open_at(c, V):
            open_by.setdefault(inc.entity, []).append(inc)
        else:
            closed.append(inc)
    for e in K.ENTITY_ORDER:
        cands = sorted(open_by.get(e, []), key=lambda i: i.incident_no)
        if cands:
            cands[int(rng.integers(0, len(cands)))].clinician_reported = True
    for car in ("QM", "SC"):
        pool = sorted((i for i in closed if K.ENTITIES[i.entity]["carrier"] == car), key=lambda i: i.incident_no)
        picked = [i for i in pool if rng.random() < 0.4]
        rest = [i for i in pool if i not in picked]
        while len(picked) < 2 and rest:
            picked.append(rest.pop(int(rng.integers(0, len(rest)))))
        for inc in picked:
            inc.clinician_reported = True


def records(incidents, notice_only, Vr, key):
    """Every carrier claim open or closed on the carrier's books at valuation date Vr."""
    rng = K.claims_stream("carrier-reserves")
    factors = {}
    out = []
    for inc in incidents + notice_only:
        f = float(rng.uniform(0.8, 1.6))
        if not _on_line(inc) or not expiring_era(inc):
            continue
        factors[inc.incident_no] = f
        reports = [c.report for c in inc.claims if c.report is not None]
        created = min([inc.notice] * (inc.notice is not None) + reports) if (inc.notice or reports) else None
        if created is None or created > Vr:
            continue
        known = [c for c in inc.claims if c.report is not None and c.report <= Vr and c.made <= Vr]
        if getattr(inc, "clinician_reported", False):
            ref = ""
        else:
            ref = inc.notice_no if inc.notice is not None else inc.claims[0].claim_no
        if not known:
            ctype = "Incident"
            status = "Open" if (Vr - inc.notice).days < 540 else "Closed"
            paid_i = paid_e = res_i = 0.0
            res_e = 2500.0 if status == "Open" and (inc.incident_no[-1] in "13579") else 0.0
        else:
            ctype = "Suit" if any(c.matter_type == "Suit" for c in known) else "Claim"
            vals = [c.vals[key] for c in known]
            if any(v["status"] == "OPEN" for v in vals):
                status = "Open"
            elif any(v["status"] == "REOPENED" for v in vals):
                status = "Reopened"
            else:
                status = "Closed"
            on = lambda c: sum(d.share for d in c.defendants if d.line != "CONTRACT")
            paid_i = sum(c.vals[key]["paid_ind"] * on(c) for c in known)
            paid_e = sum(c.vals[key]["paid_def"] * on(c) for c in known)
            ri = sum(c.vals[key]["res_ind"] * on(c) for c in known)
            re_ = sum(c.vals[key]["res_def"] * on(c) for c in known)
            res_i = float(int(ri * f / 5000 + 0.5) * 5000) if status != "Closed" else 0.0
            res_e = float(int(re_ * f / 1000 + 0.5) * 1000) if status != "Closed" else 0.0
        out.append(dict(incident_no=inc.incident_no, entity=inc.entity, created=created, ref=ref,
                        date_of_loss=inc.date, ctype=ctype, status=status, paid_ind=round(paid_i, 2),
                        paid_exp=round(paid_e, 2), res_ind=res_i, res_exp=res_e,
                        policy=K.policy_number(inc.entity, inc.date), period=K.policy_period(inc.entity, inc.date)))
    out.sort(key=lambda r: (r["created"], r["incident_no"]))
    return out


def number(recs_sep):
    """Carrier claim numbers, given in the order the carrier opened its files (the same number on every run)."""
    seq = {}
    nums = {}
    for r in recs_sep:
        car = K.ENTITIES[r["entity"]]["carrier"]
        y = r["created"].year
        seq[(car, y)] = seq.get((car, y), 0) + (7 if car == "QM" else 3) + (len(nums) * 13) % 11
        n = seq[(car, y)]
        nums[r["incident_no"]] = ("Q%02d-%05d" % (y % 100, 1200 + n * 3)) if car == "QM" else ("PL%02d%05d" % (y % 100, 40000 + n * 7))
    return nums
