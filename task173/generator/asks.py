"""The two checks on the 2026 deadline fortnight, from the shipped files alone: the outsourcer's billable hours by
day and the invoiced hours the ACD does not support by invoice week; the English-queue customers answered after more
than three minutes by day and the share answered within three minutes by week. Each figure is computed the way the
records support (truth) and along the routes a careful analyst takes on the way (the cracker sheet reads these)."""
from __future__ import annotations

import csv
import datetime as dt
import os
import re

import common as K

UTC_FMT = "%Y-%m-%dT%H:%M:%SZ"


def _p(s):
    return dt.datetime.strptime(s, UTC_FMT)


def fortnight_days():
    f0, f1 = K.fortnight(K.SEASON_CRM)
    return [f0 + dt.timedelta(k) for k in range(14)]


def weeks():
    f0, _ = K.fortnight(K.SEASON_CRM)
    return [f0, f0 + dt.timedelta(7)]


# ------------------------------------------------------------------------------------------------- loading
def read_csv(target, name):
    with open(os.path.join(target, name), encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def read_xlsx(target, name, sheet):
    import openpyxl
    wb = openpyxl.load_workbook(os.path.join(target, name), read_only=True, data_only=True)
    rows = [list(r) for r in wb[sheet].iter_rows(values_only=True)]
    wb.close()
    head = rows[0]
    return [dict(zip(head, r)) for r in rows[1:] if any(v is not None for v in r)]


def pdf_text(path):
    import logging
    logging.getLogger("pypdf").setLevel(logging.ERROR)
    from pypdf import PdfReader
    return "\n".join(p.extract_text() or "" for p in PdfReader(path).pages)


def invoices(target):
    """Each invoice in the pack: number, service week, the invoice it replaces, and its lines (agent ID, hours)."""
    txt = pdf_text(os.path.join(target, "hcs_invoices_2026_deadline_period.pdf"))
    out = []
    for block in re.split(r"(?=Hillsborough Contact Services Ltd\.\nContact centre services)", txt):
        m = re.search(r"INVOICE (HCS-\d\d-\d{4})", block)
        if not m:
            continue
        wk = re.search(r"Service week\s+(\d{1,2} \w+ \d{4}) to", block)
        rep = re.search(r"replaces invoice (HCS-\d\d-\d{4})", block)
        lines = [(a, float(h)) for a, h in re.findall(r"(HCS-\d{4})\s+([\d.]+)\s+38\.50", block)]
        out.append(dict(no=m.group(1), week=dt.datetime.strptime(wk.group(1), "%d %B %Y").date(),
                        replaces=rep.group(1) if rep else None, lines=lines))
    return out


def current_invoices(target):
    inv = invoices(target)
    replaced = {i["replaces"] for i in inv if i["replaces"]}
    return {i["week"]: i for i in inv if i["no"] not in replaced}


# ------------------------------------------------------------------------------------------------- Ask A
BILLABLE = ("Available", "On Contact", "After-Contact Work")


def login_agents(target):
    """Every login of the outsourcer's agents, mapped to the HCS agent ID: the onboarding list's own logins, and
    any other agent login whose email is an onboarded agent's."""
    ob = read_xlsx(target, "hcs_agent_onboarding_2026.xlsx", "Agents")
    users = read_csv(target, "acd_users_2026-10-29.csv")
    by_email = {r["Email"].lower(): r["HCS Agent ID"] for r in ob}
    out = {r["ACD Login"]: r["HCS Agent ID"] for r in ob}
    for u in users:
        if u["Role"] == "Agent" and u["Email"].lower() in by_email:
            out.setdefault(u["Login"], by_email[u["Email"].lower()])
    return out


def state_intervals(target):
    rows = read_csv(target, "acd_agent_state_detail_hcs_2026.csv")
    out = []
    for r in rows:
        if r["State"] in BILLABLE:
            out.append((r["Agent Login"], r["Session ID"], K.eastern(_p(r["Start (UTC)"])), K.eastern(_p(r["End (UTC)"]))))
    return out


def _union(iv):
    iv = sorted(iv)
    out = []
    for a, b in iv:
        if out and a <= out[-1][1]:
            if b > out[-1][1]:
                out[-1][1] = b
        else:
            out.append([a, b])
    return out


def _split_days(a, b):
    """Hours of [a, b) on each Eastern date."""
    out = {}
    while a < b:
        nxt = dt.datetime.combine(a.date() + dt.timedelta(1), dt.time(0))
        c = min(b, nxt)
        out[a.date()] = out.get(a.date(), 0.0) + (c - a).total_seconds() / 3600
        a = c
    return out


def billable_by_agent(target, union=True):
    """Each HCS agent's billable time as intervals of Eastern clock time: the union over every login and session
    (union=False keeps every row, as a plain sum would)."""
    la = login_agents(target)
    by = {}
    for login, sid, a, b in state_intervals(target):
        ag = la.get(login)
        if ag is None:
            continue
        by.setdefault(ag, []).append((a, b))
    if union:
        return {ag: [tuple(x) for x in _union(iv)] for ag, iv in by.items()}
    return by


def ask_a(target):
    days = fortnight_days()
    by = billable_by_agent(target, union=True)
    daily = {d: 0.0 for d in days}
    weekly = {}
    for ag, iv in by.items():
        for a, b in iv:
            for d, h in _split_days(a, b).items():
                if d in daily:
                    daily[d] += h
                wk = K.monday(d)
                weekly[(ag, wk)] = weekly.get((ag, wk), 0.0) + h
    cur = current_invoices(target)
    unsup = {}
    for wk in weeks():
        inv = cur[wk]
        unsup[wk] = sum(max(0.0, h - weekly.get((ag, wk), 0.0)) for ag, h in inv["lines"])
    return dict(daily=daily, unsupported=unsup, invoices={wk: cur[wk]["no"] for wk in weeks()})


def ask_a_routes(target):
    """The routes a careful analyst takes on the way to Ask A, each a complete pipeline."""
    days = fortnight_days()
    rows = state_intervals(target)
    out = {}

    # the Duration column summed by the Eastern date of each row's start
    r0_ = {d: 0.0 for d in days}
    for r in read_csv(target, "acd_agent_state_detail_hcs_2026.csv"):
        if r["State"] in BILLABLE:
            d = K.eastern(_p(r["Start (UTC)"])).date()
            if d in r0_:
                r0_[d] += int(r["Duration (s)"]) / 3600
    out["Duration column by row start date"] = r0_
    # plain sum of every billable row, by the Eastern date each state started
    r1 = {d: 0.0 for d in days}
    for login, sid, a, b in rows:
        if a.date() in r1:
            r1[a.date()] += (b - a).total_seconds() / 3600
    out["sum of billable rows by start date"] = r1
    # plain sum split at midnight
    r2 = {d: 0.0 for d in days}
    for login, sid, a, b in rows:
        for d, h in _split_days(a, b).items():
            if d in r2:
                r2[d] += h
    out["sum of billable rows split at midnight"] = r2
    # the union per login and session (sessions overlapping left as they are)
    by = {}
    for login, sid, a, b in rows:
        by.setdefault((login, sid), []).append((a, b))
    r3 = {d: 0.0 for d in days}
    for k, iv in by.items():
        for a, b in _union(iv):
            for d, h in _split_days(a, b).items():
                if d in r3:
                    r3[d] += h
    out["union per session"] = r3
    # sessions that timed out dropped whole
    timed = set()
    for r in read_csv(target, "acd_agent_state_detail_hcs_2026.csv"):
        if r["State"] == "Logged Out" and r["Reason Code"] == "Session timeout":
            timed.add((r["Agent Login"], r["Session ID"]))
    r4 = {d: 0.0 for d in days}
    for login, sid, a, b in rows:
        if (login, sid) in timed:
            continue
        for d, h in _split_days(a, b).items():
            if d in r4:
                r4[d] += h
    out["timed-out sessions dropped"] = r4
    # Atlantic dates
    r5 = {d: 0.0 for d in days}
    for login, sid, a, b in rows:
        for d, h in _split_days(a + dt.timedelta(hours=1), b + dt.timedelta(hours=1)).items():
            if d in r5:
                r5[d] += h
    out["Atlantic dates, union"] = r5
    return out


def ask_a_week_routes(target):
    """Routes to the invoiced hours not supported, per invoice week."""
    la_full = login_agents(target)
    ob = read_xlsx(target, "hcs_agent_onboarding_2026.xlsx", "Agents")
    la_ob = {r["ACD Login"]: r["HCS Agent ID"] for r in ob}
    rows = state_intervals(target)
    inv_all = invoices(target)
    cur = current_invoices(target)
    orig = {i["week"]: i for i in inv_all if not i["replaces"]}

    def weekly(la, union):
        by = {}
        for login, sid, a, b in rows:
            ag = la.get(login)
            if ag is not None:
                by.setdefault(ag, []).append((a, b))
        out = {}
        for ag, iv in by.items():
            for a, b in (_union(iv) if union else iv):
                for d, h in _split_days(a, b).items():
                    out[(ag, K.monday(d))] = out.get((ag, K.monday(d)), 0.0) + h
        return out

    def unsup(wkly, invs, clip=True):
        res = {}
        for wk in weeks():
            lines = invs[wk]["lines"]
            if clip:
                res[wk] = sum(max(0.0, h - wkly.get((ag, wk), 0.0)) for ag, h in lines)
            else:
                res[wk] = sum(h for _, h in lines) - sum(wkly.get((ag, wk), 0.0) for ag, _ in lines)
        return res
    out = {}
    dur = {}
    for r in read_csv(target, "acd_agent_state_detail_hcs_2026.csv"):
        ag = la_full.get(r["Agent Login"])
        if r["State"] in BILLABLE and ag is not None:
            wk = K.monday(K.eastern(_p(r["Start (UTC)"])).date())
            dur[(ag, wk)] = dur.get((ag, wk), 0.0) + int(r["Duration (s)"]) / 3600
    out["Duration column, every login"] = unsup(dur, cur)
    out["summed rows, every login"] = unsup(weekly(la_full, False), cur)
    out["summed rows, onboarding logins only"] = unsup(weekly(la_ob, False), cur)
    out["union, onboarding logins only"] = unsup(weekly(la_ob, True), cur)
    out["union, every login, first week-3 invoice"] = unsup(weekly(la_full, True), orig)
    out["union, every login, totals not agent by agent"] = unsup(weekly(la_full, True), cur, clip=False)
    out["summed rows, totals not agent by agent"] = unsup(weekly(la_full, False), cur, clip=False)
    return out


# ------------------------------------------------------------------------------------------------- Ask B
def ask_b_rows(target):
    rows = read_csv(target, "acd_contact_detail_en_2026_deadline.csv")
    crm = {}
    with open(os.path.join(target, "crm_expert_interactions_2026.csv"), encoding="utf-8", newline="") as fh:
        rd = csv.reader(fh)
        head = next(rd)
        i_id, i_st = head.index("Interaction ID"), head.index("Started (UTC)")
        for r in rd:
            crm[r[i_id]] = r[i_st]
    return rows, crm


def _b_figures(waits):
    """waits: list of (Eastern date joined, wait seconds) for answered customers. Each day's average wait in
    seconds and each week's share answered within three minutes, in per cent."""
    days = fortnight_days()
    tot = {d: 0.0 for d in days}
    cnt = {d: 0 for d in days}
    long_ = {d: 0 for d in days}
    wk_n, wk_ok = {w: 0 for w in weeks()}, {w: 0 for w in weeks()}
    for d, w in waits:
        if d not in tot:
            continue
        tot[d] += w
        cnt[d] += 1
        long_[d] += w > 180
        wk = K.monday(d)
        wk_n[wk] += 1
        wk_ok[wk] += w <= 180
    daily = {d: tot[d] / cnt[d] for d in days}
    share = {w: 100.0 * wk_ok[w] / wk_n[w] for w in weeks()}
    return dict(daily=daily, share=share, answered=wk_n, per_day=cnt, over3=long_)


def ask_b(target, rows=None, crm=None):
    if rows is None:
        rows, crm = ask_b_rows(target)
    by = {}
    for r in rows:
        by.setdefault(r["Session ID"], []).append(r)
    waits = []
    for sid, rs in by.items():
        joined = min(_p(r["Queued (UTC)"]) for r in rs)
        conv = [r for r in rs if r["CRM Interaction"]]
        if not conv:
            continue
        start = _p(crm[conv[0]["CRM Interaction"]])
        waits.append((K.eastern(joined).date(), (start - joined).total_seconds()))
    return _b_figures(waits)


def ask_b_routes(target, rows=None, crm=None):
    if rows is None:
        rows, crm = ask_b_rows(target)
    out = {}
    ans = [r for r in rows if r["Result"] == "Answered"]
    # per answered row, the ACD's own times
    out["each answered row, queued to answered"] = _b_figures(
        [(K.eastern(_p(r["Queued (UTC)"])).date(), (_p(r["Answered (UTC)"]) - _p(r["Queued (UTC)"])).total_seconds())
         for r in ans])
    # per contact: earliest queued on the contact, its answered row
    byc = {}
    for r in rows:
        byc.setdefault(r["Contact ID"], []).append(r)
    w = []
    for cid, rs in byc.items():
        a = [r for r in rs if r["Result"] == "Answered"]
        if not a:
            continue
        q = min(_p(r["Queued (UTC)"]) for r in rs)
        w.append((K.eastern(q).date(), (_p(a[0]["Answered (UTC)"]) - q).total_seconds()))
    out["per contact, first queued to answered"] = _b_figures(w)
    # per session: first queued to the first answered row
    bys = {}
    for r in rows:
        bys.setdefault(r["Session ID"], []).append(r)
    w1, w2, w3 = [], [], []
    for sid, rs in bys.items():
        q = min(_p(r["Queued (UTC)"]) for r in rs)
        a = sorted((r for r in rs if r["Result"] == "Answered"), key=lambda r: r["Answered (UTC)"])
        if not a:
            continue
        w1.append((K.eastern(q).date(), (_p(a[0]["Answered (UTC)"]) - q).total_seconds()))
        conv = [r for r in a if r["CRM Interaction"]]
        if conv:
            w2.append((K.eastern(q).date(), (_p(conv[0]["Answered (UTC)"]) - q).total_seconds()))
            # the CRM's start against the answered row's own queued time
            q_own = _p(conv[0]["Queued (UTC)"])
            w3.append((K.eastern(q_own).date(), (_p(crm[conv[0]["CRM Interaction"]]) - q_own).total_seconds()))
    out["per session, first queued to first answered"] = _b_figures(w1)
    out["per session, first queued to the answered row that reached the CRM"] = _b_figures(w2)
    out["answered row's own queued time to the CRM start"] = _b_figures(w3)
    return out
