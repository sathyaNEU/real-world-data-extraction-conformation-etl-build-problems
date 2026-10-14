"""The three supporting tables, each with the readings a careful analyst might take (the stops of its ladder).

A  the 2026 disclosure cycle by department: faculty who owed a 2026 disclosure (an appointment on 31 December 2026,
   by the department of the primary appointment that day) and how many of them had not submitted it by 11:59 p.m.
   Eastern on 15 January 2027 (no submission at or before 2027-01-16 04:59:59 UTC). A faculty member is a person:
   one whose employee number changed in 2026 holds the appointment under the new number and filed under the number
   the disclosure system knew, the two tied by the NPI they share.
B  the register's 2025 remuneration by nature, to the faculty who held an appointment at any time in 2025: records
   tied to a faculty member through the covered-recipient profile, payments to the faculty member personally.
C  2026 remuneration disclosed from companies that do not report to Open Payments, by relationship type: the
   current version's items whose company has no Open Payments identifier and appears under no name in the register
   (a typed name or a listed company resolved through the register's present and earlier names)."""
import datetime as dt
from collections import defaultdict

import conform as C

DEADLINE_UTC = dt.datetime(2027, 1, 16, 4, 59, 59)
TYPES_2026 = ["Consulting or advisory board", "Speaking or teaching", "Expert testimony", "Other paid services"]
NATURE_LABEL = ["Consulting fees", "Services other than consulting, including speaking outside continuing education",
                "Honoraria", "Faculty or speaker, accredited or certified continuing education",
                "Faculty or speaker, unaccredited continuing education"]


def ask_a(data, time_rule="first", clock="utc", dept_rule="mapped", owed_rule="dec31", link="npi"):
    """{dept: [owed, not submitted by the deadline]}"""
    fac = C.faculty(data)
    day = dt.date(2026, 12, 31) if owed_rule == "dec31" else dt.date(2027, 1, 20)
    person = (lambda e: fac[e]["npi"]) if link == "npi" else (lambda e: e)
    owed = {}
    for e, f in fac.items():
        if C.holds(f, day):
            owed.setdefault(person(e), e)
    did = {d["disclosure_id"]: d for d in data["disc"] if int(d["disclosure_year"]) == 2026}
    first = {}
    for ev in data["history"]:
        if ev["disclosure_id"] in did and ev["event"] == "Submitted":
            t = dt.datetime.strptime(ev["event_time_utc"], "%Y-%m-%dT%H:%M:%SZ")
            p = person(did[ev["disclosure_id"]]["emp_id"])
            first[p] = min(first.get(p, t), t)
    last = {}
    for d in did.values():
        v = d["last_submitted_utc"]
        last[person(d["emp_id"])] = v if isinstance(v, dt.datetime) else dt.datetime.strptime(v, "%Y-%m-%d %H:%M:%S")
    when = first if time_rule == "first" else last
    out = defaultdict(lambda: [0, 0])
    for p in sorted(owed):
        f = fac[owed[p]]
        if dept_rule == "mapped":
            dept = C.dept_on(data, f, day)
        else:
            prim = sorted(t for t in f["terms"] if t[4] and t[0] <= day)
            dept = prim[-1][2]
        t = when.get(p)
        late = t is None or (t > DEADLINE_UTC if clock == "utc" else t.date() > dt.date(2027, 1, 15))
        out[dept][0] += 1
        out[dept][1] += int(late)
    return {k: tuple(v) for k, v in sorted(out.items())}


def ask_b(data, attribution="profile", personal=True, scope="held2025"):
    """{nature index: dollars}"""
    fac = C.faculty(data)
    att = C.attribute(data, attribution)
    out = defaultdict(float)
    for r in data["register"]:
        if r["Program_Year"] != "2025" or r["Nature_of_Payment_or_Transfer_of_Value"] not in C.REMUN:
            continue
        e = att.get(r["Record_ID"])
        if not e:
            continue
        if personal and r["Third_Party_Payment_Recipient_Indicator"] != "No Third Party Payment":
            continue
        if scope == "held2025" and not any(s <= dt.date(2025, 12, 31) and t >= dt.date(2025, 1, 1)
                                           for s, t, *_ in fac[e]["terms"]):
            continue
        out[C.REMUN.index(r["Nature_of_Payment_or_Transfer_of_Value"])] += float(r["Total_Amount_of_Payment_USDollars"])
    return {k: out.get(k, 0.0) for k in range(5)}


def ask_c(data, typed="resolve", version="latest", listed="resolve"):
    """{relationship type: dollars}"""
    ent = {e["entity_id"]: e for e in data["entities"]}
    present = {e["entity_name"].strip().lower(): e["open_payments_id"] for e in data["entities"] if e["open_payments_id"]}
    n2op = C.name_to_op(data) if typed == "resolve" else (present if typed == "present" else {})
    cur = {x["disclosure_id"]: x for x in data["disc"]}
    first = defaultdict(lambda: 99)
    for it in data["items"]:
        first[it["disclosure_id"]] = min(first[it["disclosure_id"]], it["version"])
    out = defaultdict(float)
    for it in data["items"]:
        x = cur[it["disclosure_id"]]
        if int(x["disclosure_year"]) != 2026 or it["relationship_type"] not in C.REMUN_TYPES:
            continue
        if version == "latest" and it["version"] != x["current_version"]:
            continue
        if version == "first" and it["version"] != first[it["disclosure_id"]]:
            continue
        if it["entity_id"]:
            op = ent[it["entity_id"]]["open_payments_id"]
            if not op and listed == "resolve":
                op = C.name_to_op(data).get(it["entity_name"].strip().lower())
        else:
            op = n2op.get(it["entity_name"].strip().lower())
        if not op:
            out[it["relationship_type"]] += float(it["amount_usd"] or 0)
    return {t: out.get(t, 0.0) for t in TYPES_2026}


def stops(data):
    """Each ask's golden and the readings that land elsewhere."""
    return {
        "A": {"golden": ask_a(data), "employee numbers joined as they stand": ask_a(data, link="emp"),
              "latest submission time": ask_a(data, time_rule="last"),
              "UTC date against 15 January": ask_a(data, clock="date"),
              "roster's department code": ask_a(data, dept_rule="raw"),
              "everyone on the roster at the pull": ask_a(data, owed_rule="pull")},
        "B": {"golden": ask_b(data), "the office's matched employee number": ask_b(data, attribution="matcher"),
              "records carrying an NPI only": ask_b(data, attribution="npi"),
              "payments to the university kept": ask_b(data, personal=False),
              "every record in the extract": ask_b(data, scope="all")},
        "C": {"golden": ask_c(data), "the list's blank identifier trusted": ask_c(data, listed="list"),
              "typed names against the list's present names": ask_c(data, typed="present"),
              "every typed name": ask_c(data, typed="list"), "the first version": ask_c(data, version="first"),
              "every version": ask_c(data, version="sum")},
    }
