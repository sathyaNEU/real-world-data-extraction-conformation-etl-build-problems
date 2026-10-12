"""The records behind the two assistance indicators, drawn from the premises' events.

Ask 1 (residential disconnections for nonpayment completed in January 2026): Kestrel Valley's CIS service orders
(pulled 3 February) and its contractor's job report, Northbank's field activity and crew completions, Pine Harbor's
work orders and its head-end meter events. Ask 2 (residential accounts on a low-income payment plan on 31 January
2026): Kestrel Valley's enrolment file, Northbank's premise flags and account history, Pine Harbor's plan table.

The truth (k1, k2) is counted from the events; the ledger names the rows each device touches, for checks.py.
"""
from collections import defaultdict
from datetime import datetime, time, timedelta

import events as EV
import world as W

D = W.D
TD = timedelta
JAN0, JAN1 = D(2026, 1, 1), D(2026, 1, 31)
ROSTER_REFRESH = D(2025, 12, 1)     # Northbank's last refresh of its premise flags before 31 January
ORDERS_FROM = D(2025, 12, 1)        # Kestrel Valley's January extract: order activity from 1 December
# Kestrel Valley's intake county: the applicant's mailing address. Post-office-box households near the county
# lines give a box in the neighbouring county's post office.
INTAKE_MAIL = {"Ashwell": ("Brennock", 0.15), "Carrow": ("Brennock", 0.13), "Dellmoor": ("Brennock", 0.10),
               "Evanshade": ("Dellmoor", 0.14), "Brennock": ("Carrow", 0.04), "Tillery": ("Lorrance", 0.22)}
CREWS_PHE = "ABCDEFG"


def injan(d):
    return d is not None and JAN0 <= d <= JAN1


def acct_on(p, day):
    for a, s, e in p.accounts:
        if s <= day and (e is None or day <= e):
            return a
    return None


def _t(d, r, h0=8, h1=16):
    return datetime.combine(d, time(int(r.integers(h0, h1)), int(r.integers(0, 60))))


def _batch_utc(d, r):
    """Pine Harbor's head end runs the collections batch at about 7 pm Eastern; in winter that is about midnight
    UTC, so roughly half the commands carry the next day's UTC date."""
    local = datetime.combine(d, time(18, 35)) + TD(seconds=int(r.integers(0, 3000)))
    return local + TD(hours=5)


def build(prem):
    out = dict(kvg_orders=[], northline=[], nng_activity=[], nng_crew=[], phe_wo=[], phe_events=[],
               kvg_lipp=[], nng_roster=[], nng_accounts=[], nng_enrol={}, phe_plans=[], ledger=defaultdict(list),
               k1=defaultdict(int), k2=defaultdict(int))
    seq = defaultdict(int)

    def nxt(key, start):
        seq[key] += 1
        return start + seq[key]

    out["nxt"] = nxt
    for p in prem:
        r = W.rng("ind", p.pid)
        for ev in p.events:
            k = ev["kind"]
            if k == "NP":
                if injan(ev["date"]):
                    out["k1"][p.county] += 1
                {"KVG": _kvg_np, "NNG": _nng_np, "PHE": _phe_np}[p.util](p, ev, r, out, nxt)
            elif k in ("CUST_OFF", "SAFETY_OFF", "SEASONAL_OFF", "SEASONAL_ON"):
                _other_order(p, ev, r, out, nxt)
        _plans(p, r, out, nxt)
        if p.util == "NNG":
            for a, s, e in p.accounts:
                out["nng_accounts"].append(dict(account=a, premise=p.pid, start=s, end=e))
    _kvg_cerr(prem, out, nxt)
    _nng_cancelled(prem, out, nxt)
    _noise_events(prem, out, nxt)
    _plan_noise(prem, out, nxt)
    return out


# ------------------------------------------------------------------ Ask 1, Kestrel Valley
def _kvg_np(p, ev, r, out, nxt):
    acct = ev["account"]
    created = ev["due"] - TD(int(r.integers(3, 9)))
    for status, d in ev["attempts"]:
        if status == "UNABLE":
            out["kvg_orders"].append(dict(order=nxt("kvo", 26100000), account=acct, premise=p.pid, otype="OFF",
                                          reason="NP", status="UNAB", created=_t(created, r), done=_t(d, r),
                                          crew="KV-W%02d" % int(r.integers(1, 15))))
            created = d
    comp = ev["date"]
    if EV.CONTRACTOR_FROM <= comp <= EV.CONTRACTOR_TO:
        keyed = comp + TD(int(r.integers(4, 31)))
        crew = "NUS-%d" % int(r.integers(1, 5))
        out["northline"].append(dict(job="NL-2601-%04d" % nxt("nl", 3000), date=comp, account=acct, premise=p.pid,
                                     address=p.street, town=p.town, tech=crew, done=_t(comp, r)))
        if keyed <= W.KVG_ORDERS_PULL:
            out["kvg_orders"].append(dict(order=nxt("kvo", 26100000), account=acct, premise=p.pid, otype="OFF",
                                          reason="NP", status="COMP", created=_t(keyed, r), done=out["northline"][-1]["done"],
                                          crew=crew))
            out["ledger"]["kvg_contractor_keyed"].append(p.pid)
        else:
            out["ledger"]["kvg_contractor_late"].append(p.pid)
    elif comp <= W.KVG_ORDERS_PULL:
        out["kvg_orders"].append(dict(order=nxt("kvo", 26100000), account=acct, premise=p.pid, otype="OFF",
                                      reason="NP", status="COMP", created=_t(created, r), done=_t(comp, r),
                                      crew="KV-W%02d" % int(r.integers(1, 15))))
    if ev["recon"] and ev["recon"] <= W.KVG_ORDERS_PULL:
        out["kvg_orders"].append(dict(order=nxt("kvo", 26100000), account=acct, premise=p.pid, otype="ON",
                                      reason="RCN", status="COMP", created=_t(ev["recon"], r, 7, 9),
                                      done=_t(ev["recon"], r, 10, 18), crew="KV-W%02d" % int(r.integers(1, 15))))


def _kvg_cerr(prem, out, nxt):
    """Orders completed in error: a crew closed a nonpayment order in the field system against the wrong account
    and the office reversed it; the order keeps its completion stamp."""
    kvg = [p for p in prem if p.util == "KVG" and not any(e["kind"] == "NP" for e in p.events)]
    r = W.rng("cerr")
    for k in r.choice(len(kvg), 5, replace=False):
        p = kvg[int(k)]
        d = EV.bday_on_or_after(D(2026, 1, 5) + TD(int(r.integers(0, 24))))
        if EV.PAUSE_FROM <= d <= EV.PAUSE_TO:
            d = EV.bday_on_or_after(D(2026, 1, 6) + TD(int(r.integers(0, 9))))
        out["kvg_orders"].append(dict(order=nxt("kvo", 26100000), account=acct_on(p, d), premise=p.pid, otype="OFF",
                                      reason="NP", status="CERR", created=_t(d - TD(4), r), done=_t(d, r),
                                      crew="KV-W%02d" % int(r.integers(1, 15))))
        out["ledger"]["kvg_cerr"].append(p.pid)


# ------------------------------------------------------------------ Ask 1, Northbank
def _nng_np(p, ev, r, out, nxt):
    for status, d in ev["attempts"]:
        if status == "UNABLE":
            a = nxt("nna", 5100000)
            crew = "NB%02d" % int(r.integers(1, 9))
            out["nng_activity"].append(dict(act=a, premise=p.pid, code="DNP", sched=d, route=p.route, crew=crew,
                                            result="U"))
            out["nng_crew"].append(dict(act=a, done=_t(d, r), crew=crew, note="NO ACCESS"))
    a = nxt("nna", 5100000)
    crew = "NB%02d" % int(r.integers(1, 9))
    out["nng_activity"].append(dict(act=a, premise=p.pid, code="DNP", sched=ev["sched"], route=p.route, crew=crew,
                                    result="C"))
    out["nng_crew"].append(dict(act=a, done=_t(ev["date"], r), crew=crew, note=""))
    if ev["date"] != ev["sched"]:
        out["ledger"]["nng_carried"].append((p.pid, ev["sched"], ev["date"]))
    if ev["recon"]:
        a = nxt("nna", 5100000)
        crew = "NB%02d" % int(r.integers(1, 9))
        out["nng_activity"].append(dict(act=a, premise=p.pid, code="RNP", sched=ev["recon"], route=p.route, crew=crew,
                                        result="C"))
        out["nng_crew"].append(dict(act=a, done=_t(ev["recon"], r), crew=crew, note=""))


def _nng_cancelled(prem, out, nxt):
    """Nonpayment disconnections scheduled and then cancelled before a crew was sent (the customer paid or
    arranged a plan): an activity row with no crew completion."""
    r = W.rng("nng-cancel")
    nng = [p for p in prem if p.util == "NNG" and not any(e["kind"] == "NP" for e in p.events)]
    for k in r.choice(len(nng), 31, replace=False):
        p = nng[int(k)]
        d = EV.bday_on_or_after(D(2025, 12, 1) + TD(int(r.integers(0, 88))))
        if EV.PAUSE_FROM <= d <= EV.PAUSE_TO or acct_on(p, d) is None:
            continue
        out["nng_activity"].append(dict(act=nxt("nna", 5100000), premise=p.pid, code="DNP", sched=d, route=p.route,
                                        crew="", result="X"))


# ------------------------------------------------------------------ Ask 1, Pine Harbor
def _phe_np(p, ev, r, out, nxt):
    acct, comp = ev["account"], ev["date"]
    crew = lambda: "PH-%s" % CREWS_PHE[int(r.integers(0, len(CREWS_PHE)))]
    if p.ami:
        ref = "SR%s%05d" % (comp.strftime("%y%m"), nxt("sr", 0) % 100000)
        if r.random() < 0.06:
            # the valve did not close on the evening batch before; a field crew shut the service off
            prev = comp - TD(1)
            while prev.weekday() >= 5:
                prev -= TD(1)
            out["phe_events"].append(dict(meter=p.meter_new, utc=_batch_utc(prev, r), code="VALVE_CLOSE_FAILED",
                                          source="HES", ref=ref, reason="NP"))
            out["phe_wo"].append(dict(wo=nxt("pwo", 640000), account=acct, premise=p.pid, wtype="Collections Shutoff",
                                      status="Completed", sched=comp, done=_t(comp, r), crew=crew()))
            out["ledger"]["phe_field_after_failed"].append(p.pid)
        else:
            out["phe_events"].append(dict(meter=p.meter_new, utc=_batch_utc(comp, r), code="VALVE_CLOSE", source="HES",
                                          ref=ref, reason="NP"))
            out["ledger"]["phe_remote_np"].append((p.pid, comp))
        if ev["recon"]:
            out["phe_events"].append(dict(meter=p.meter_new, utc=_t(ev["recon"], r, 13, 22) + TD(hours=5),
                                          code="VALVE_OPEN", source="HES",
                                          ref="SR%s%05d" % (ev["recon"].strftime("%y%m"), nxt("sr", 0) % 100000),
                                          reason="RC"))
    else:
        for status, d in ev["attempts"]:
            if status == "UNABLE":
                out["phe_wo"].append(dict(wo=nxt("pwo", 640000), account=acct, premise=p.pid,
                                          wtype="Collections Shutoff", status="Unable to Complete", sched=d,
                                          done=_t(d, r), crew=crew()))
        out["phe_wo"].append(dict(wo=nxt("pwo", 640000), account=acct, premise=p.pid, wtype="Collections Shutoff",
                                  status="Completed", sched=ev["sched"], done=_t(comp, r), crew=crew()))
        if ev["recon"]:
            out["phe_wo"].append(dict(wo=nxt("pwo", 640000), account=acct, premise=p.pid, wtype="Collections Restore",
                                      status="Completed", sched=ev["recon"], done=_t(ev["recon"], r), crew=crew()))


def _other_order(p, ev, r, out, nxt):
    d = ev["date"]
    acct = acct_on(p, d)
    k = ev["kind"]
    if acct is None:
        return
    if p.util == "KVG":
        reason = {"CUST_OFF": "CUST", "SAFETY_OFF": "SAFE", "SEASONAL_OFF": "SEAS", "SEASONAL_ON": "SEAS"}[k]
        if ORDERS_FROM <= d <= W.KVG_ORDERS_PULL:
            out["kvg_orders"].append(dict(order=nxt("kvo", 26100000), account=acct, premise=p.pid,
                                          otype="ON" if k == "SEASONAL_ON" else "OFF", reason=reason, status="COMP",
                                          created=_t(d - TD(int(r.integers(0, 6))), r), done=_t(d, r),
                                          crew="KV-W%02d" % int(r.integers(1, 15))))
            if ev.get("recon") and ev["recon"] > d and ev["recon"] <= W.KVG_ORDERS_PULL:
                out["kvg_orders"].append(dict(order=nxt("kvo", 26100000), account=acct, premise=p.pid, otype="ON",
                                              reason=reason, status="COMP", created=_t(d, r),
                                              done=_t(ev["recon"], r), crew="KV-W%02d" % int(r.integers(1, 15))))
    elif p.util == "NNG":
        code = {"CUST_OFF": "TOF", "SAFETY_OFF": "LKC", "SEASONAL_OFF": "TOF", "SEASONAL_ON": "TON"}[k]
        if D(2025, 12, 1) <= d <= D(2026, 2, 28):
            a = nxt("nna", 5100000)
            crew = "NB%02d" % int(r.integers(1, 9))
            out["nng_activity"].append(dict(act=a, premise=p.pid, code=code, sched=d, route=p.route, crew=crew,
                                            result="C"))
            out["nng_crew"].append(dict(act=a, done=_t(d, r), crew=crew,
                                        note="LEAK REPAIRED, RELIT" if k == "SAFETY_OFF" else ""))
    else:
        if not (D(2025, 12, 1) <= d <= D(2026, 2, 28)):
            return
        if p.ami:
            if k == "SAFETY_OFF":
                t = datetime.combine(d, time(0, 0)) + TD(seconds=int(r.integers(0, 86400))) + TD(hours=5)
                out["phe_events"].append(dict(meter=p.meter_new, utc=t - TD(minutes=2), code="HIGH_FLOW_ALARM",
                                              source="METER", ref="", reason=""))
                out["phe_events"].append(dict(meter=p.meter_new, utc=t, code="VALVE_CLOSE", source="METER", ref="",
                                              reason="SF"))
            else:
                out["phe_events"].append(dict(meter=p.meter_new, utc=_batch_utc(d, r), code="VALVE_CLOSE",
                                              source="HES", ref="SR%s%05d" % (d.strftime("%y%m"),
                                                                             nxt("sr", 0) % 100000), reason="SR"))
            if ev.get("recon") and ev["recon"] > d:
                out["phe_events"].append(dict(meter=p.meter_new, utc=_t(ev["recon"], r, 9, 17) + TD(hours=5),
                                              code="VALVE_OPEN", source="HES",
                                              ref="SR%s%05d" % (ev["recon"].strftime("%y%m"), nxt("sr", 0) % 100000),
                                              reason="RS"))
        else:
            wtype = "Customer Shutoff" if k == "CUST_OFF" else "Leak Investigation"
            out["phe_wo"].append(dict(wo=nxt("pwo", 640000), account=acct, premise=p.pid, wtype=wtype,
                                      status="Completed", sched=d, done=_t(d, r), crew="PH-%s" % CREWS_PHE[
                                          int(r.integers(0, len(CREWS_PHE)))]))
            if ev.get("recon") and ev["recon"] > d:
                out["phe_wo"].append(dict(wo=nxt("pwo", 640000), account=acct, premise=p.pid,
                                          wtype="Customer Turn-On", status="Completed", sched=ev["recon"],
                                          done=_t(ev["recon"], r), crew="PH-%s" % CREWS_PHE[
                                              int(r.integers(0, len(CREWS_PHE)))]))


def _noise_events(prem, out, nxt):
    """The head end's other traffic: battery, tamper and communication alarms on the AMI meters."""
    r = W.rng("hes-noise")
    ami = [p for p in prem if p.ami]
    for k in range(len(ami) // 2):
        p = ami[int(r.integers(0, len(ami)))]
        d = D(2025, 12, 1) + TD(int(r.integers(0, 90)))
        if acct_on(p, d) is None:
            continue
        t = datetime.combine(d, time(0, 0)) + TD(seconds=int(r.integers(0, 86400)))
        code = ["LOW_BATTERY", "COMM_LOSS", "TAMPER_ALERT", "LOW_BATTERY", "COMM_LOSS", "TIME_SYNC"][int(r.integers(0, 6))]
        out["phe_events"].append(dict(meter=p.meter_new, utc=t, code=code, source="METER" if code != "TIME_SYNC"
                                      else "HES", ref="", reason=""))
        if code == "COMM_LOSS":
            out["phe_events"].append(dict(meter=p.meter_new, utc=t + TD(hours=int(r.integers(2, 40))),
                                          code="COMM_RESTORED", source="HES", ref="", reason=""))


# ------------------------------------------------------------------ Ask 2
def _plans(p, r, out, nxt):
    carried = set()
    lipp = sorted([ev for ev in p.events if ev["kind"] == "LIPP"], key=lambda e: (e["date"], e["account"]))
    for ev in lipp:
        a, start, end = ev["account"], ev["date"], ev["end"]
        if a in carried or start > D(2026, 3, 31):
            continue
        active = start <= JAN1 and (end is None or end >= JAN1)
        if p.util == "KVG":
            mail, rate = INTAKE_MAIL.get(p.county, (None, 0.0))
            county = mail if (mail and r.random() < rate) else p.county
            if county != p.county:
                out["ledger"]["kvg_intake_county"].append((p.pid, active))
            retro = r.random() < 0.15
            applied = start - TD(int(r.integers(0, 6)))
            approved = start + TD(int(r.integers(3, 26))) if retro else start - TD(int(r.integers(0, 4)))
            if approved < applied:
                approved = applied
            if approved > W.BILL_PULL:
                continue
            out["kvg_lipp"].append(dict(enr="KLP-%06d" % nxt("klp", 100000), account=a, county=county,
                                        applied=applied, approved=approved, effective=start, end=end,
                                        end_reason="ACCOUNT FINALED" if end and end <= W.BILL_PULL else ""))
            if retro and approved > JAN1 and start <= JAN1:
                out["ledger"]["kvg_approved_after"].append(p.pid)
            if active:
                out["k2"][p.county] += 1
        elif p.util == "NNG":
            # the account's own enrollment record: HHAP ends with the account
            out["nng_enrol"][a] = (start, end)
            if start <= JAN1 and (end is None or end >= ROSTER_REFRESH):
                out["nng_roster"].append(dict(premise=p.pid, since=start, account=a))
                if end is not None and end < JAN1:
                    out["ledger"]["nng_stale_flag"].append(p.pid)
            if active:
                out["k2"][p.county] += 1
        else:
            if p.ami and end == p.install and start <= p.install:
                # converted in October: the plan carried to the new account number, the old row left open
                new = [x for x, s, e in p.accounts if s == p.install + TD(1)][0]
                new_end = [e for x, s, e in p.accounts if x == new][0]
                carried.add(new)
                out["phe_plans"].append(dict(plan="PP%07d" % nxt("pp", 2000000), account=a, ptype="LIPP", start=start,
                                             end=None, status="ACTIVE", created=start))
                out["phe_plans"].append(dict(plan="PP%07d" % nxt("pp", 2000000), account=new, ptype="LIPP",
                                             start=p.install + TD(1), end=new_end,
                                             status="ACTIVE" if new_end is None else "ENDED",
                                             created=p.install + TD(int(r.integers(2, 9)))))
                out["ledger"]["phe_converted_open"].append(p.pid)
                if new_end is None or new_end >= JAN1:
                    out["k2"][p.county] += 1
            else:
                out["phe_plans"].append(dict(plan="PP%07d" % nxt("pp", 2000000), account=a, ptype="LIPP", start=start,
                                             end=end, status="ACTIVE" if end is None else "ENDED", created=start))
                if active:
                    out["k2"][p.county] += 1
    # Northbank's roster keeps one flag per premise: the latest enrolment
    if p.util == "NNG":
        rows = [x for x in out["nng_roster"] if x["premise"] == p.pid]
        if len(rows) > 1:
            keep = max(rows, key=lambda x: x["since"])
            out["nng_roster"] = [x for x in out["nng_roster"] if x["premise"] != p.pid or x is keep]


def _plan_noise(prem, out, nxt):
    """Pine Harbor's plan table also holds budget billing and deferred payment arrangements."""
    r = W.rng("plan-noise")
    phe = [p for p in prem if p.util == "PHE"]
    for k in range(int(len(phe) * 0.11)):
        p = phe[int(r.integers(0, len(phe)))]
        a, s, e = p.accounts[int(r.integers(0, len(p.accounts)))]
        start = max(s, D(2024, 3, 1)) + TD(int(r.integers(0, 500)))
        if (e is not None and start > e) or start > D(2026, 3, 31):
            continue
        kind = "BUDGET" if r.random() < 0.7 else "DPA"
        end = e if kind == "BUDGET" else min([x for x in (e, start + TD(int(r.integers(90, 365)))) if x is not None])
        out["phe_plans"].append(dict(plan="PP%07d" % nxt("pp", 2000000), account=a, ptype=kind, start=start,
                                     end=end if end and end <= W.BILL_PULL else None,
                                     status="ACTIVE" if not end or end > W.BILL_PULL else "ENDED", created=start))
