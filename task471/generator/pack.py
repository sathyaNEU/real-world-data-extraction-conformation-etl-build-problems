"""The pack's data files, in the layouts the register, the audit and the hub write them."""
import csv
import datetime as dt
import io

import numpy as np

import sim as S
import world as W

FILES = {
    "register": "population_register_extract_20260101.txt",
    "events": "population_register_events_extract.csv",
    "sample": "register_coverage_audit_2026_sample.csv",
    "visits": "register_coverage_audit_2026_visits.csv",
    "sample_events": "register_coverage_audit_2026_histories.csv",
    "messages": "deregistration_messages_2025.csv",
    "acks": "hub_acknowledgements_2025.csv",
    "nonres": "non_resident_records_extract.csv",
    "regulation": "municipal_fund_regulation_2027_article_14.pdf",
    "report": "register_coverage_audit_2026_report.pdf",
    "layouts": "population_register_record_layouts.pdf",
    "spec": "adjusted_population_delivery_specification_2027.docx",
    "codes": "municipality_codes_2026.xlsx",
    "countries": "country_codes.csv",
    "pilot": "register_coverage_pilot_2024.xlsx",
    "levy": "waste_levy_households_20260101.csv",
}
DISTRACTORS = ("pilot", "levy")

REGISTER_COLS = ["PERSON_KEY", "MUN_CODE", "ADDRESS_ID", "ADDRESS_SINCE", "SEX", "BIRTH_DATE", "BIRTH_COUNTRY",
                 "NATIONALITY", "MARITAL_STATUS"]
EVENT_COLS = ["PERSON_KEY", "SEQ", "EVENT", "EVENT_DATE", "MUN_CODE", "COUNTRY", "FROM_MUN_CODE", "ANNULS_SEQ"]
SAMPLE_COLS = ["AUDIT_NO", "PERSON_KEY", "MUN_CODE", "SEX", "BIRTH_DATE", "BIRTH_COUNTRY", "NATIONALITY",
               "ADDRESS_SINCE"]
VISIT_COLS = ["AUDIT_NO", "VISIT", "VISIT_DATE", "MODE", "RESULT"]
MESSAGE_COLS = ["MESSAGE_ID", "SENT_AT", "SENDER_MUN", "PERSON_KEY", "MESSAGE_TYPE", "EVENT_DATE", "COUNTRY"]
ACK_COLS = ["MESSAGE_ID", "RECEIVED_AT", "RESULT", "REASON"]
NONRES_COLS = ["PERSON_KEY", "LAST_MUN_CODE", "DEPARTURE_DATE", "COUNTRY", "STATUS", "STATUS_DATE", "SEX", "BIRTH_DATE"]
COUNTRY_COLS = ["CODE", "COUNTRY"]
LEVY_COLS = ["MUN_CODE", "MUNICIPALITY", "HOUSEHOLDS_BILLED", "EXEMPT", "BILLING_DATE"]


def rng(seed, *parts):
    return np.random.default_rng([seed, *parts])


def everything(seed=W.SEED, counts=None):
    """the whole world: register, audit, histories with their annulments, addresses, 2025 traffic"""
    reg, sample = S.register(seed, counts or W.COUNT)
    msgs, nonres = S.traffic(seed, reg)
    out, acks = S.acknowledge(seed, msgs, nonres)
    visits = S.fieldwork(seed, sample)
    addresses(seed, reg, sample)
    annul(seed, reg, sample)
    moves(seed, reg, sample)
    return dict(reg=reg, sample=sample, msgs=out, acks=acks, nonres=nonres, visits=visits)


SIZES = (1, 2, 3, 4, 5, 6)
SIZE_P = (0.38, 0.30, 0.14, 0.11, 0.05, 0.02)


def _prefix(code, r):
    return W.FORMER[int(r.integers(0, 2))][1] if code == W.MERGED[1] else code


def addresses(seed, reg, sample):
    """households at addresses; an address keeps the code of the municipality that issued it (Ravenmeer's were issued
    by its two former municipalities)"""
    for code in W.CODES:
        r = rng(seed, 90, int(code))
        people = list(reg[code])
        order = r.permutation(len(people))
        i, used = 0, set()
        while i < len(order):
            size = int(r.choice(SIZES, p=SIZE_P))
            while True:
                aid = _prefix(code, r) + "20" + "%010d" % int(r.integers(10 ** 9, 10 ** 10 - 1))
                if aid not in used:
                    used.add(aid)
                    break
            for j in order[i:i + size]:
                people[j]["address"] = aid
            i += size
    r = rng(seed, 91)
    for p in sample:
        if "address" not in p:
            p["address"] = p["mun"] + "20" + "%010d" % int(r.integers(10 ** 9, 10 ** 10 - 1))


def annul(seed, reg, sample):
    """register corrections: a settlement entered twice and a departure entered in error, each annulled"""
    r = rng(seed, 95)
    for p in [q for code in W.CODES for q in reg[code]] + [q for q in sample if q["mun"] not in W.CODES]:
        p.setdefault("annulled", [])
        if p["stay"] is None:
            continue
        u = r.random()
        imm = [e for e in p["events"] if e[0] == "IMM"][-1]
        if u < 0.005:
            p["annulled"].append(("IMM", imm[1], imm[2], imm[3], ""))
        elif u < 0.008 and imm[1] < dt.date(2024, 10, 1):   # the 2025 departures entered in error are sim.traffic's
            when = S._rand_date(r, imm[1] + dt.timedelta(days=60), min(W.REF, dt.date(2025, 1, 1)) - dt.timedelta(days=30))
            p["annulled"].append(("EMI", when, imm[2], "5012", ""))


def moves(seed, reg, sample):
    """a departure abroad leaves from the municipality the person lived in: where the history has the person living
    elsewhere until then, the move into the municipality is recorded between the two (no stay or departure moves)"""
    r = rng(seed, 96)
    for p in [q for code in W.CODES for q in reg[code]] + list(sample):
        here, prev, add = None, None, []
        for e in sorted(p["events"], key=lambda e: e[1]):
            if e[0] in ("GEB", "IMM", "VER"):
                here, prev = e[2], e[1]
            elif e[0] == "EMI":
                if here and e[2] != here and (e[1] - prev).days > 60:
                    when = S._rand_date(r, prev + dt.timedelta(days=30), e[1] - dt.timedelta(days=30))
                    add.append(("VER", when, e[2], "", here))
                here = None
        if add:
            p["events"] = sorted(p["events"] + add, key=lambda e: e[1])


def event_rows(people):
    out = []
    for p in people:
        evs = sorted([(e, False) for e in p["events"]] + [(e, True) for e in p.get("annulled", [])],
                     key=lambda x: (x[0][1], x[1]))
        seq = 0
        later = []
        for e, bad in evs:
            seq += 1
            code, when, mun, country, frm = e
            out.append(dict(PERSON_KEY=p["key"], SEQ=seq, EVENT=code, EVENT_DATE=S.ymd(when), MUN_CODE=mun or "",
                            COUNTRY=country, FROM_MUN_CODE=frm, ANNULS_SEQ=""))
            if bad:
                later.append((seq, code, when))
        for s_, code, when in later:
            seq += 1
            on = p.get("ann_dates", {}).get((code, when), when + dt.timedelta(days=9))
            out.append(dict(PERSON_KEY=p["key"], SEQ=seq, EVENT="ANN", EVENT_DATE=S.ymd(on),
                            MUN_CODE=out[-1]["MUN_CODE"], COUNTRY="", FROM_MUN_CODE="", ANNULS_SEQ=s_))
    return out


def birth_text(p):
    b = S.ymd(p["birth"])
    return b[:4] + "0000" if p.get("partial") == "Y" else b[:6] + "00" if p.get("partial") == "M" else b


def register_rows(x):
    rows = []
    for code in sorted(W.CODES):
        for p in x["reg"][code]:
            rows.append(dict(PERSON_KEY=p["key"], MUN_CODE=code, ADDRESS_ID=p["address"], ADDRESS_SINCE=S.ymd(p["since"]),
                             SEX=p["sex"], BIRTH_DATE=birth_text(p), BIRTH_COUNTRY=p["bcountry"],
                             NATIONALITY=p["nat"], MARITAL_STATUS=p["marital"]))
    rows.sort(key=lambda d: (d["MUN_CODE"], d["ADDRESS_ID"], d["PERSON_KEY"]))
    return rows


def sample_rows(x):
    rows = [dict(AUDIT_NO=p["audit_no"], PERSON_KEY=p["key"], MUN_CODE=p["mun"], SEX=p["sex"], BIRTH_DATE=birth_text(p),
                 BIRTH_COUNTRY=p["bcountry"], NATIONALITY=p["nat"], ADDRESS_SINCE=S.ymd(p["since"]))
            for p in x["sample"]]
    rows.sort(key=lambda d: d["AUDIT_NO"])
    return rows


def visit_rows(x):
    return [dict(AUDIT_NO=v["audit"], VISIT=v["visit"], VISIT_DATE=v["date"].isoformat(), MODE=v["mode"],
                 RESULT=v["result"]) for v in sorted(x["visits"], key=lambda v: (v["audit"], v["visit"]))]


def summer_time(day):
    """the country's summer time (UTC+2) for a batch sent shortly after midnight on `day`: the last Sunday of March to
    the last Sunday of October; otherwise UTC+1"""
    def last_sunday(month):
        d = dt.date(day.year, month, 31)
        return d - dt.timedelta(days=(d.weekday() + 1) % 7)
    return last_sunday(3) < day <= last_sunday(10)


def _stamp(r, registered):
    """the night batch after the registration day: 00:05 to 00:59 the next day in the country's time, written in UTC"""
    batch = registered + dt.timedelta(days=1)
    local = dt.datetime(batch.year, batch.month, batch.day, 0, int(r.integers(5, 60)), int(r.integers(0, 60)))
    utc = local - dt.timedelta(hours=2 if summer_time(batch) else 1)
    return utc.strftime("%Y-%m-%dT%H:%M:%SZ")


def message_rows(x, seed=W.SEED):
    r = rng(seed, 100)
    msgs = sorted(x["msgs"], key=lambda m: (m["sent"], m["sender"], m["key"], m["kind"], m["date"]))
    rows, acks = [], []
    by_id = {}
    for i, m in enumerate(msgs):
        mid = "%s-25-%06d" % (m["sender"], 100000 + i * 7 + int(r.integers(0, 7)))
        sent = _stamp(r, m["sent"])
        by_id[id(m)] = (mid, sent)
        sender = m["sender"]
        rows.append(dict(MESSAGE_ID=mid, SENT_AT=sent, SENDER_MUN=sender, PERSON_KEY=m["key"], MESSAGE_TYPE=m["kind"],
                         EVENT_DATE=m["date"].isoformat(), COUNTRY=m["country"]))
    for m, res, reason in x["acks"]:
        mid, sent = by_id[id(m)]
        t = dt.datetime.strptime(sent, "%Y-%m-%dT%H:%M:%SZ") + dt.timedelta(seconds=int(r.integers(4, 900)))
        acks.append(dict(MESSAGE_ID=mid, RECEIVED_AT=t.strftime("%Y-%m-%dT%H:%M:%SZ"), RESULT=res, REASON=reason))
    acks.sort(key=lambda a: (a["RECEIVED_AT"], a["MESSAGE_ID"]))
    return rows, acks


def nonres_rows(x):
    rows = [dict(PERSON_KEY=n["key"], LAST_MUN_CODE=n["last"], DEPARTURE_DATE=n["dep"].isoformat(), COUNTRY=n["country"],
                 STATUS=n["status"], STATUS_DATE=n["sdate"].isoformat(), SEX=n["sex"], BIRTH_DATE=S.ymd(n["birth"]))
            for n in x["nonres"]]
    rows.sort(key=lambda d: (d["LAST_MUN_CODE"], d["DEPARTURE_DATE"], d["PERSON_KEY"]))
    return rows


def country_rows():
    rows = [dict(CODE="0000", COUNTRY="Unknown"), dict(CODE=W.HOME[0], COUNTRY="(this country)")]
    rows += [dict(CODE=c, COUNTRY=n) for c, n, _ in W.COUNTRIES]
    return sorted(rows, key=lambda d: d["CODE"])


def levy_rows(x, seed=W.SEED):
    """households billed for the 2026 waste levy: the municipalities' own billing, not the register"""
    r = rng(seed, 110)
    rows = []
    for code in sorted(W.CODES):
        n_addr = len({p["address"] for p in x["reg"][code]})
        billed = int(round(n_addr * float(r.uniform(0.95, 1.03))))
        rows.append(dict(MUN_CODE=code, MUNICIPALITY=W.NAME[code], HOUSEHOLDS_BILLED=billed,
                         EXEMPT=int(round(billed * float(r.uniform(0.01, 0.04)))), BILLING_DATE="2026-01-01"))
    return rows


def write_csv(path, cols, rows, crlf=False, delimiter=","):
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=cols, lineterminator="\r\n" if crlf else "\n", delimiter=delimiter)
    w.writeheader()
    for row in rows:
        w.writerow(row)
    with open(path, "w", encoding="utf-8", newline="") as fh:
        fh.write(buf.getvalue())
    return len(rows)


def write_register(path, rows):
    """the register's extract format: pipe-delimited, a header line and a trailer with the record count"""
    n = write_csv(path, REGISTER_COLS, rows, crlf=True, delimiter="|")
    with open(path, "a", encoding="utf-8", newline="") as fh:
        fh.write("TRAILER|%d|%s\r\n" % (n, S.ymd(W.EXTRACT_DATE)))
    return n
