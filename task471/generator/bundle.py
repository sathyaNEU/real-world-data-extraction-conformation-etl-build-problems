"""Everything computed from the shipped files only (target/): each person's features as the register extract and the
event histories give them, the audit's final results, every method's adjusted resident populations, and the two
population-account asks. golden.py, checks.py and ceiling.py read the pack through this module."""
import csv
import datetime as dt
import os
import re

import methods as M

REF = dt.date(2026, 1, 1)
HOME = "6030"
MERGED, FORMER = "1987", ("0731", "0744")


def _find(target, pattern):
    hits = [f for f in os.listdir(target) if re.search(pattern, f)]
    assert len(hits) == 1, (pattern, hits)
    return os.path.join(target, hits[0])


def _rows(path, delimiter=","):
    with open(path, encoding="utf-8", newline="") as fh:
        return [r for r in csv.DictReader(fh, delimiter=delimiter)]


def _date(s):
    s = s.replace("-", "")
    return dt.date(int(s[:4]), int(s[4:6]) or 7, int(s[6:8]) or 1)


def completed_years(start, ref=REF):
    return max(0, ref.year - start.year - ((ref.month, ref.day) < (start.month, start.day)))


def histories(rows, annulments=True):
    """person -> list of (event, date) with annulled events removed (when asked)"""
    by = {}
    for r in rows:
        by.setdefault(r["PERSON_KEY"], []).append(r)
    out = {}
    for k, evs in by.items():
        dead = {e["ANNULS_SEQ"] for e in evs if e["EVENT"] == "ANN"} if annulments else set()
        out[k] = sorted(((e["EVENT"], _date(e["EVENT_DATE"]), int(e["SEQ"])) for e in evs
                         if e["EVENT"] != "ANN" and e["SEQ"] not in dead), key=lambda x: (x[1], x[2]))
    return out


def features(rec, hist):
    imms = [d for e, d, _ in hist if e == "IMM"]
    latest = imms[-1] if imms else None
    return dict(stay=completed_years(latest) if latest else None,
                left=int(any(e == "EMI" and d < latest for e, d, _ in hist)) if latest else 0,
                first=completed_years(imms[0]) if imms else None,
                addr=completed_years(_date(rec["ADDRESS_SINCE"])),
                abroad=int(rec["BIRTH_COUNTRY"] != HOME), foreign=int(rec["NATIONALITY"] != HOME),
                age=completed_years(_date(rec["BIRTH_DATE"])), sex=rec["SEX"])


class Pack:
    def __init__(self, target, annulments=True, final_result="last"):
        self.target = target
        reg = _rows(_find(target, r"^population_register_extract_\d+\.txt$"), delimiter="|")
        self.trailer = [r for r in reg if r["PERSON_KEY"] == "TRAILER"]
        self.register = [r for r in reg if r["PERSON_KEY"] != "TRAILER"]
        self.codes = sorted({r["MUN_CODE"] for r in self.register})
        events = _rows(_find(target, r"^population_register_events_extract\.csv$"))
        self.hist = histories(events, annulments)
        dead = {(e["PERSON_KEY"], e["ANNULS_SEQ"]) for e in events if e["EVENT"] == "ANN"}
        self.void = {(e["PERSON_KEY"], e["EVENT"], _date(e["EVENT_DATE"])) for e in events
                     if e["EVENT"] in ("EMI", "OVL") and (e["PERSON_KEY"], e["SEQ"]) in dead}
        self.registered_keys = {e["PERSON_KEY"] for e in events}
        self.sample = _rows(_find(target, r"audit_2026_sample\.csv$"))
        self.shist = histories(_rows(_find(target, r"audit_2026_histories\.csv$")), annulments)
        visits = _rows(_find(target, r"audit_2026_visits\.csv$"))
        last = {}
        for v in visits:
            if final_result == "last":
                if v["AUDIT_NO"] not in last or int(v["VISIT"]) > int(last[v["AUDIT_NO"]]["VISIT"]):
                    last[v["AUDIT_NO"]] = v
            elif v["RESULT"] != "91" and v["AUDIT_NO"] not in last:
                last[v["AUDIT_NO"]] = v
        self.result = {k: v["RESULT"] for k, v in last.items()}
        self.audit = [(features(r, self.shist.get(r["PERSON_KEY"], [])),
                       int(self.result[r["AUDIT_NO"]] in ("20", "30", "40"))) for r in self.sample]
        self.pops = {m: [] for m in self.codes}
        for r in self.register:
            self.pops[r["MUN_CODE"]].append(features(r, self.hist.get(r["PERSON_KEY"], [])))
        self.messages = _rows(_find(target, r"^deregistration_messages_2025\.csv$"))
        self.acks = {a["MESSAGE_ID"]: a for a in _rows(_find(target, r"^hub_acknowledgements_2025\.csv$"))}
        self.nonres = _rows(_find(target, r"^non_resident_records_extract\.csv$"))

    # --------------------------------------------------------------------------------------------- the main call
    def adjusted(self, method=M.GOLDEN, audit=None):
        key = M.RUNGS.get(method) or M.VARIANTS[method]
        return M.adjusted(audit or self.audit, self.pops, key)

    def golden(self):
        adj = self.adjusted()
        return {m: dict(registered=len(self.pops[m]), adjusted=adj[m], rounded=int(round(adj[m])),
                        not_resident=len(self.pops[m]) - int(round(adj[m])),
                        qualifies=int(round(adj[m])) < M.LINE) for m in self.codes}

    def qualifying(self, method=M.GOLDEN):
        return M.qualifying(self.adjusted(method))

    # ----------------------------------------------------------------------------------------------------- asks
    def mun(self, sender):
        return MERGED if sender in FORMER else sender

    def _messages(self, kind, clock="local", acks="accepted", year=True):
        """the messages of one type the municipality's register sent in 2025 (the country's time, or the hub's UTC
        year), accepted by the hub (or every message), with an event date in 2025 (or any)"""
        out = []
        for x in self.messages:
            if x["MESSAGE_TYPE"] != kind:
                continue
            if year and not x["EVENT_DATE"].startswith("2025"):
                continue
            sent = local_date(x["SENT_AT"]) if clock == "local" else dt.date(*map(int, x["SENT_AT"][:10].split("-")))
            if sent.year != 2025:
                continue
            if acks == "accepted" and self.acks[x["MESSAGE_ID"]]["RESULT"] != "ACCEPTED":
                continue
            if self.mun(x["SENDER_MUN"]) in self.pops:
                out.append(x)
        return out

    def departures(self, clock="local", acks="accepted", void="exclude", dedup=False, year=True):
        """DEPARTURES_ABROAD_2025: departures abroad in 2025 recorded from the messages sent in 2025; a departure the
        register annulled did not take place (void "keep" counts it, "drop_registered" drops every departure of a
        person on the 1 January 2026 register, the returners with them)"""
        out = {m: 0 for m in self.codes}
        seen = set()
        for x in self._messages("EMI", clock, acks, year):
            k = x["PERSON_KEY"]
            if void == "exclude" and (k, "EMI", _date(x["EVENT_DATE"])) in self.void:
                continue
            if void == "drop_registered" and k in self.registered_keys:
                continue
            if dedup and k in seen:
                continue
            seen.add(k)
            out[self.mun(x["SENDER_MUN"])] += 1
        return out

    def departures_nonres(self):
        out = {m: 0 for m in self.codes}
        for n in self.nonres:
            if n["DEPARTURE_DATE"].startswith("2025") and n["COUNTRY"] != "0000":
                out[self.mun(n["LAST_MUN_CODE"])] += 1
        return out

    def deaths(self, clock="local", acks="accepted", residency="registered", year=True, void="exclude"):
        """DEATHS_2025: deaths in 2025 recorded from the messages sent in 2025, of persons registered as residents of the
        municipality when they died: not in the non-resident records, or there with a registration that ended after
        the death (residency "none" counts every death, "no_record" drops everyone with a non-resident record,
        "died_home" drops every death abroad); a death the register annulled did not take place (void "keep")"""
        ended = {n["PERSON_KEY"]: n["DEPARTURE_DATE"] for n in self.nonres}
        out = {m: 0 for m in self.codes}
        for x in self._messages("OVL", clock, acks, year):
            k = x["PERSON_KEY"]
            if void == "exclude" and (k, "OVL", _date(x["EVENT_DATE"])) in self.void:
                continue
            if residency == "registered" and k in ended and ended[k] <= x["EVENT_DATE"]:
                continue
            if residency == "no_record" and k in ended:
                continue
            if residency == "died_home" and x["COUNTRY"] != HOME:
                continue
            out[self.mun(x["SENDER_MUN"])] += 1
        return out


def local_date(stamp):
    """the country's calendar date of a UTC time: UTC+2 from 01:00 UTC on the last Sunday of March to 01:00 UTC on the
    last Sunday of October, UTC+1 otherwise"""
    t = dt.datetime.strptime(stamp, "%Y-%m-%dT%H:%M:%SZ")

    def switch(month):
        d = dt.date(t.year, month, 31)
        d -= dt.timedelta(days=(d.weekday() + 1) % 7)
        return dt.datetime(d.year, d.month, d.day, 1, 0, 0)
    return (t + dt.timedelta(hours=2 if switch(3) <= t < switch(10) else 1)).date()
