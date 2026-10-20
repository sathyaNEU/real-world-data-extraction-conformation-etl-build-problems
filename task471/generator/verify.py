"""The independent verifier: reads only the shipped pack (target/) and the golden files, rebuilds each person's current
stay and earlier departure from the event histories, the audit's shares, each municipality's adjusted resident
population and qualification, and the two 2025 counts, by its own code, and compares them with the golden CSV and
submission.md. It imports nothing from the generator.

    python3 task471/generator/verify.py
"""
import csv
import datetime as dt
import os
import re
import sys
from zoneinfo import ZoneInfo

REF = dt.date(2026, 1, 1)
LINE = 5000
MERGED = {"0731": "1987", "0744": "1987"}
LOCAL = ZoneInfo("Europe/Brussels")


def find(target, pattern):
    hits = [f for f in os.listdir(target) if re.search(pattern, f)]
    assert len(hits) == 1, (pattern, hits)
    return os.path.join(target, hits[0])


def rows(path, delimiter=","):
    with open(path, encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh, delimiter=delimiter))


def ymd(s):
    s = s.replace("-", "")
    return dt.date(int(s[:4]), int(s[4:6]) or 7, int(s[6:8]) or 1)


def careers(events):
    """person -> (stay in completed years since the latest IMM, or None; 1 if an EMI came before that IMM)"""
    by = {}
    for e in events:
        by.setdefault(e["PERSON_KEY"], []).append(e)
    out = {}
    for k, evs in by.items():
        void = {e["ANNULS_SEQ"] for e in evs if e["EVENT"] == "ANN"}
        live = [(ymd(e["EVENT_DATE"]), int(e["SEQ"]), e["EVENT"]) for e in evs if e["EVENT"] != "ANN" and e["SEQ"] not in void]
        imm = max((d for d, _, ev in live if ev == "IMM"), default=None)
        if imm is None:
            out[k] = (None, 0)
            continue
        years = REF.year - imm.year - ((REF.month, REF.day) < (imm.month, imm.day))
        out[k] = (years, int(any(ev == "EMI" and d < imm for d, _, ev in live)))
    return out


def cell(c):
    stay, left = c
    if stay is None:
        return ("never", 0)
    return (0 if stay == 0 else 1 if stay <= 4 else 2 if stay <= 9 else 3, left)


def main(target, gdir, quiet=False):
    ok = True

    def check(cond, msg):
        nonlocal ok
        if not cond:
            ok = False
            print("VERIFY FAIL:", msg)

    reg = rows(find(target, r"^population_register_extract_\d+\.txt$"), delimiter="|")
    trailer = [r for r in reg if r["PERSON_KEY"] == "TRAILER"]
    reg = [r for r in reg if r["PERSON_KEY"] != "TRAILER"]
    check(int(trailer[0]["MUN_CODE"]) == len(reg), "the trailer's count")
    events = rows(find(target, r"^population_register_events_extract\.csv$"))
    car = careers(events)
    sample = rows(find(target, r"audit_2026_sample\.csv$"))
    scar = careers(rows(find(target, r"audit_2026_histories\.csv$")))
    final = {}
    for v in rows(find(target, r"audit_2026_visits\.csv$")):
        if v["AUDIT_NO"] not in final or int(v["VISIT"]) > int(final[v["AUDIT_NO"]][0]):
            final[v["AUDIT_NO"]] = (v["VISIT"], v["RESULT"])
    n, x = {}, {}
    for r in sample:
        c = cell(scar.get(r["PERSON_KEY"], (None, 0)))
        n[c] = n.get(c, 0) + 1
        x[c] = x.get(c, 0) + int(final[r["AUDIT_NO"]][1] in ("20", "30", "40"))
    rate = {c: x[c] / n[c] for c in n}
    absent = sum(x.values())
    count, expect = {}, {}
    for r in reg:
        m = r["MUN_CODE"]
        count[m] = count.get(m, 0) + 1
        expect[m] = expect.get(m, 0.0) + rate[cell(car.get(r["PERSON_KEY"], (None, 0)))]
    adjusted = {m: count[m] - expect[m] for m in count}
    qual = {m: round(adjusted[m]) < LINE for m in count}
    # the two 2025 counts
    msgs = rows(find(target, r"^deregistration_messages_2025\.csv$"))
    res = {a["MESSAGE_ID"]: a["RESULT"] for a in rows(find(target, r"^hub_acknowledgements_2025\.csv$"))}
    void = set()
    by = {}
    for e in events:
        by.setdefault(e["PERSON_KEY"], {})[e["SEQ"]] = e
    for k, evs in by.items():
        for e in evs.values():
            if e["EVENT"] == "ANN":
                a = evs[e["ANNULS_SEQ"]]
                void.add((k, a["EVENT"], ymd(a["EVENT_DATE"])))
    ended = {r["PERSON_KEY"]: r["DEPARTURE_DATE"] for r in rows(find(target, r"^non_resident_records_extract\.csv$"))}
    dep = {m: 0 for m in count}
    dth = {m: 0 for m in count}
    for mm in msgs:
        sent = dt.datetime.strptime(mm["SENT_AT"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=dt.timezone.utc)
        if sent.astimezone(LOCAL).year != 2025 or not mm["EVENT_DATE"].startswith("2025") or res[mm["MESSAGE_ID"]] != "ACCEPTED":
            continue
        m = MERGED.get(mm["SENDER_MUN"], mm["SENDER_MUN"])
        if (mm["PERSON_KEY"], mm["MESSAGE_TYPE"], ymd(mm["EVENT_DATE"])) in void:
            continue
        if mm["MESSAGE_TYPE"] == "EMI":
            dep[m] += 1
        elif mm["MESSAGE_TYPE"] == "OVL" and not (mm["PERSON_KEY"] in ended and ended[mm["PERSON_KEY"]] <= mm["EVENT_DATE"]):
            dth[m] += 1
    # against the golden CSV
    gold = rows(os.path.join(gdir, "adjusted_population_supplement_2027.csv"))
    check(len(gold) == 24 == len(count), "24 municipalities")
    names = {}
    for g in gold:
        m = g["MUNICIPALITY_CODE"][2:]
        names[m] = g["MUNICIPALITY"]
        check(int(g["REGISTERED_20260101"]) == count[m], "%s registered" % m)
        check(int(g["ADJUSTED_POPULATION"]) == round(adjusted[m]), "%s adjusted %s against %.1f" % (
            m, g["ADJUSTED_POPULATION"], adjusted[m]))
        check(int(g["NOT_RESIDENT_ESTIMATE"]) == count[m] - round(adjusted[m]), "%s estimate" % m)
        check((g["QUALIFIES"] == "Y") == qual[m], "%s qualifies" % m)
        check(int(g["DEPARTURES_ABROAD_2025"]) == dep[m], "%s departures %s against %d" % (m, g["DEPARTURES_ABROAD_2025"], dep[m]))
        check(int(g["DEATHS_2025"]) == dth[m], "%s deaths %s against %d" % (m, g["DEATHS_2025"], dth[m]))
    # against submission.md
    sub = open(os.path.join(os.path.dirname(gdir), "submission.md"), encoding="utf-8").read()
    rec = sub.split("## 1. Final Recommendation")[1].split("## 2.")[0]
    called = sorted(names[m] for m in count if qual[m])
    check(all(nm in rec.split("**")[1] for nm in called) and "Nine of the 24" in rec, "the recommendation names the nine")
    check("**%s of %s**" % ("{:,}".format(absent), "{:,}".format(len(sample))) in sub, "the audit's count")
    for m in count:
        line = re.search(r"^   - %s \(GM%s\): (qualifies|does not qualify), ([\d,]+) departures abroad, ([\d,]+) deaths$" % (
            re.escape(names[m]), m), sub, re.M)
        check(line is not None and (line.group(1) == "qualifies") == qual[m] and int(line.group(2).replace(",", "")) ==
              dep[m] and int(line.group(3).replace(",", "")) == dth[m], "submission line for %s" % names[m])
    if not quiet:
        print("verify: %s; %d qualify (%s); %d of %d sampled not living there" % (
            "PASS" if ok else "FAIL", len(called), ", ".join(called), absent, len(sample)))
    return ok


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    task = os.path.dirname(here)
    sys.exit(0 if main(os.path.join(task, "target"), os.path.join(task, "golden")) else 1)
