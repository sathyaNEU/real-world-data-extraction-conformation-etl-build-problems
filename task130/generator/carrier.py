"""The carriers' records of Corvane's matters: one carrier claim per matter under each entity's occurrence policies,
opened when the carrier first heard of it (a precautionary notice, or the weekly claims report), carrying the
reference Corvane gave it then, and valued on the carrier's own reserves."""
from __future__ import annotations

import datetime as dt

import common as K


def _on_line(inc):
    return any(d.line != "CONTRACT" for c in inc.claims for d in c.defendants) or inc.route in ("NOTICE", "GL")


def records(incidents, notice_only, Vr, key, gl=()):
    """Every carrier claim open or closed on the carrier's books at valuation date Vr: the clinician matters, the
    precautionary notices that never became claims, and the claims against an entity alone (general liability)."""
    rng = K.claims_stream("carrier-reserves")
    factors = {}
    out = []
    for inc in incidents + notice_only + list(gl):
        f = float(rng.uniform(0.8, 1.6))
        if not _on_line(inc):
            continue
        factors[inc.incident_no] = f
        reports = [c.report for c in inc.claims if c.report is not None]
        created = min([inc.notice] * (inc.notice is not None) + reports) if (inc.notice or reports) else None
        if created is None or created > Vr:
            continue
        known = [c for c in inc.claims if c.report is not None and c.report <= Vr and c.made <= Vr]
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
            on = (lambda c: 1.0) if inc.route == "GL" else \
                (lambda c: sum(d.share for d in c.defendants if d.line != "CONTRACT"))
            paid_i = sum(c.vals[key]["paid_ind"] * on(c) for c in known)
            paid_e = sum(c.vals[key]["paid_def"] * on(c) for c in known)
            ri = sum(c.vals[key]["res_ind"] * on(c) for c in known)
            re_ = sum(c.vals[key]["res_def"] * on(c) for c in known)
            res_i = float(int(ri * f / 5000 + 0.5) * 5000) if status != "Closed" else 0.0
            res_e = float(int(re_ * f / 1000 + 0.5) * 1000) if status != "Closed" else 0.0
        claim_rptd = min(c.report for c in known) if known else None
        out.append(dict(incident_no=inc.incident_no, entity=inc.entity, created=created, ref=ref,
                        claim_rptd=claim_rptd, route=inc.route,
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
