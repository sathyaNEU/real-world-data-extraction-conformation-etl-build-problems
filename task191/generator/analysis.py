"""The golden reading of the pack and the readings the ladder and the fork table test, all from target/ alone."""
import bisect
import csv
import datetime as dt
import json
import os

import common as C
from pack import FILES

DAY = 86400.0


def _t(s):
    return dt.datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ") if s else None


class Pack:
    def __init__(self, target=C.TARGET):
        p = lambda k: os.path.join(target, FILES[k])
        with open(p("runs"), encoding="utf-8") as f:
            self.runs = {r["run_id"]: r for r in csv.DictReader(f)}
        with open(p("cases"), encoding="utf-8") as f:
            self.cases = {c["case_id"]: c for c in json.load(f)["cases"]}
        with open(p("alerts"), encoding="utf-8") as f:
            self.raw = list(csv.DictReader(f))
        with open(p("sars"), encoding="utf-8") as f:
            self.sars = list(csv.DictReader(f))
        self.X = C.EXTRACT_UTC
        self.alerts = []
        for r in self.raw:
            a = dict(id=r["alert_id"], code=r["scenario_code"], run=r["run_id"], gen=_t(r["created_at_utc"]),
                     triage=r["triage_status"], tclosed=_t(r["triage_closed_at_utc"]), outcome=r["triage_outcome"],
                     case=r["case_id"] or None)
            a["scenario"] = {v: k for k, v in C.REPLACEMENT.items()}.get(a["code"], a["code"])
            a["bdate"] = dt.date.fromisoformat(self.runs[a["run"]]["business_date"])
            a["edate"] = C.to_eastern(a["gen"]).date()
            # where the alert stands on the extract
            if a["triage"] == "OPEN":
                a["state"], a["decided"] = None, None
            elif a["outcome"] in ("NSA", "DUP"):
                a["state"], a["decided"] = "NO_SAR", a["tclosed"]
            else:
                c = self.cases[a["case"]]
                if c["status"] == "CLOSED":
                    a["state"] = "SAR" if c["disposition"] == "SAR filed" else "NO_SAR"
                    a["decided"] = _t(c["decided_at"])
                else:
                    a["state"], a["decided"] = None, None
            a["opener"] = bool(a["case"]) and a["tclosed"] == _t(self.cases[a["case"]]["opened_at"])
            a["age"] = int((self.X - a["gen"]).total_seconds() // DAY)
            a["dage"] = int((a["decided"] - a["gen"]).total_seconds() // DAY) if a["decided"] else None
            self.alerts.append(a)

    def period(self, code, dups=False, by="run", apart=False):
        key = "bdate" if by == "run" else ("edate" if by == "eastern" else None)
        out = []
        for a in self.alerts:
            if (a["code"] if apart else a["scenario"]) != code or (a["outcome"] == "DUP" and not dups):
                continue
            d = a[key] if key else a["gen"].date()
            if C.P0 <= d <= C.P1:
                out.append(a)
        return out

    # ---------------------------------------------------------------- the golden reading
    def history(self, code, min_age=330, apart=False):
        """The scenario's alerts raised long enough before the extract that their decisions are in: (decision age,
        ended in a SAR), sorted by decision age."""
        h = [(a["dage"], a["state"] == "SAR") for a in self.alerts
             if (a["code"] if apart else a["scenario"]) == code and a["outcome"] != "DUP" and a["age"] >= min_age
             and a["state"] is not None]
        h.sort()
        return h

    def p_sar_given_open(self, code, min_age=330, apart=False):
        """P(the alert ends in a SAR | it is still undecided at age a), read from the history."""
        h = self.history(code, min_age, apart)
        ages = [x[0] for x in h]
        suffix = [0] * (len(h) + 1)
        for i in range(len(h) - 1, -1, -1):
            suffix[i] = suffix[i + 1] + h[i][1]

        def f(age):
            i = bisect.bisect_right(ages, age)
            k = len(h) - i
            return suffix[i] / k if k else 1.0
        return f

    def productivity(self, code, method="golden", **kw):
        per = self.period(code, dups=kw.get("dups", False), by=kw.get("by", "run"), apart=kw.get("apart", False))
        if kw.get("opener_only"):
            # an alert added to an investigation it did not open read as not ending in a SAR
            per = [dict(a, state="NO_SAR" if a["state"] == "SAR" and not a["opener"] else a["state"]) for a in per]
        n = len(per)
        sar = sum(a["state"] == "SAR" for a in per)
        und = [a for a in per if a["state"] is None]
        dec = n - len(und)
        if method == "golden":
            f = self.p_sar_given_open(code, kw.get("min_age", 330), kw.get("apart", False))
            return 100.0 * (sar + sum(f(a["age"]) for a in und)) / n
        if method == "decided_only":
            return 100.0 * sar / dec
        if method == "open_as_no":
            return 100.0 * sar / n
        if method == "project_decided_share":
            return 100.0 * (sar + len(und) * sar / dec) / n
        if method == "status":
            q = self.investigation_share(code, mature=kw.get("mature", True))
            return 100.0 * (sar + sum(q if a["case"] else sar / dec for a in und)) / n
        if method == "mature":
            cut = (self.X - dt.timedelta(days=int(kw["months"] * 30.44))).date()
            m = [a for a in per if a["bdate"] <= cut and a["state"] is not None]
            return 100.0 * sum(a["state"] == "SAR" for a in m) / len(m)
        if method == "prior_quarter":
            m = [a for a in self.alerts if a["scenario"] == code and a["outcome"] != "DUP"
                 and dt.date(2025, 7, 1) <= a["bdate"] <= dt.date(2025, 9, 30) and a["state"] is not None]
            return 100.0 * sum(a["state"] == "SAR" for a in m) / len(m)
        if method == "all_open_investigations_sar":
            return 100.0 * (sar + sum(1 for a in und if a["case"])) / n
        raise ValueError(method)

    def investigation_share(self, code, mature=True):
        esc = [a for a in self.alerts if a["scenario"] == code and a["case"] and a["state"] is not None
               and (a["age"] >= 330 or not mature)]
        return sum(a["state"] == "SAR" for a in esc) / max(len(esc), 1)

    def counts(self, code):
        per = self.period(code)
        und = [a for a in per if a["state"] is None]
        return dict(alerts=len(per), sar_decided=sum(a["state"] == "SAR" for a in per), undecided=len(und),
                    undecided_in_investigation=sum(1 for a in und if a["case"]),
                    decided=len(per) - len(und))

    def call(self, method="golden", **kw):
        prod = {code: self.productivity(code, method, **kw) for code in C.CODES}
        return sorted(c for c, v in prod.items() if v < C.FLOOR), prod

    # ---------------------------------------------------------------- the asks
    def ask_investigations(self, attribute="opening", clock="eastern", quarter="opened"):
        """Investigations each scenario's alerts opened in each quarter of the tuning year, by the opening date.
        attribute: "opening" (the alert whose escalation opened it), "lowest_id" (the case's first alert number),
        "every" (once for each scenario among its alerts). quarter: "opened" (the investigation's opening date) or
        "alert" (the opening alert's business date)."""
        by_case = {}
        for a in self.alerts:
            if a["case"]:
                by_case.setdefault(a["case"], []).append(a)
        out = {}
        for cid, c in self.cases.items():
            t = _t(c["opened_at"])
            al = by_case.get(cid, [])
            d = C.to_eastern(t).date() if clock == "eastern" else t.date()
            if quarter == "alert":
                if not al:
                    continue
                d = min(al, key=lambda a: a["id"])["bdate"]
            if not (C.P0 <= d <= C.P1):
                continue
            if quarter == "alert":
                codes = [min(al, key=lambda a: a["id"])["scenario"]]
            elif attribute == "opening":
                codes = [a["scenario"] for a in al if a["tclosed"] == t]
                assert len(codes) == 1, cid
            elif attribute == "lowest_id":
                codes = [min(al, key=lambda a: a["id"])["scenario"]]
            else:
                codes = sorted({a["scenario"] for a in al})
            for code in codes:
                k = (code, C.quarter_label(d))
                out[k] = out.get(k, 0) + 1
        return out

    def sar_kinds(self, read="chain"):
        """Each filing's kind. chain (the golden): a case's first filing is its initial report; a later filing that
        covers the same activity as the report it cites is a correction; a later filing covering activity after the
        case's previous report is a continuing activity report, whether or not its prior-report field is filled.
        field: the prior-report field read alone (empty is initial, filled with the cited period is a correction,
        filled with a new period is continuing). prior_only: every filing citing a prior is continuing."""
        by_id = {s["bsa_id"]: s for s in self.sars}
        kinds = {}
        if read == "chain":
            by_case = {}
            for s in sorted(self.sars, key=lambda s: (s["filed_at_utc"], s["bsa_id"])):
                by_case.setdefault(s["case_id"], []).append(s)
            for cid, fl in by_case.items():
                last_end = None
                for k, s in enumerate(fl):
                    pr = by_id.get(s["prior_bsa_id"]) if s["prior_bsa_id"] else None
                    if s["prior_bsa_id"] and pr is None:
                        # cites a report filed before the log opens: the tail of an older chain
                        kinds[s["bsa_id"]] = "before_log"
                        last_end = max(last_end or s["activity_end"], s["activity_end"])
                        continue
                    if k == 0 and not s["prior_bsa_id"]:
                        kinds[s["bsa_id"]] = "initial"
                        last_end = s["activity_end"]
                        continue
                    if pr is not None and (s["activity_start"], s["activity_end"]) == (pr["activity_start"], pr["activity_end"]):
                        kinds[s["bsa_id"]] = "correction"
                        continue
                    assert last_end is not None and s["activity_start"] > last_end, s["bsa_id"]
                    kinds[s["bsa_id"]] = "continuing"
                    last_end = s["activity_end"]
            return kinds
        for s in self.sars:
            if not s["prior_bsa_id"]:
                kinds[s["bsa_id"]] = "initial"
            elif read == "prior_only" or s["prior_bsa_id"] not in by_id:
                kinds[s["bsa_id"]] = "continuing"
            else:
                pr = by_id[s["prior_bsa_id"]]
                same = (s["activity_start"], s["activity_end"]) == (pr["activity_start"], pr["activity_end"])
                kinds[s["bsa_id"]] = "correction" if same else "continuing"
        return kinds

    def ask_sars(self, read="chain", clock="eastern", corrections=False):
        """SARs filed in each month of 2026 to October: initial reports and continuing activity reports."""
        kinds = self.sar_kinds(read)
        out = {}
        for s in self.sars:
            t = _t(s["filed_at_utc"])
            d = C.to_eastern(t).date() if clock == "eastern" else t.date()
            if d.year != 2026 or d.month > 10:
                continue
            kind = kinds[s["bsa_id"]]
            assert kind != "before_log", s["bsa_id"]
            if kind == "correction":
                if not corrections:
                    continue
                kind = "continuing"
            k = (d.strftime("%Y-%m"), kind)
            out[k] = out.get(k, 0) + 1
        return out
