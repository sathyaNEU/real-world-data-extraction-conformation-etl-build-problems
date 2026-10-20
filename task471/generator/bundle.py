"""Reading the shipped pack: every route the ladder and the asks name, computed from target/ alone (golden.py,
ceiling.py and checks.py use it; verify.py does not). A route is a set of choices: how the anchor's written assignment
enters the link (as scored, put back on the 2025 standard by its validity papers, by every assignment's papers, or
left out), whether the form is equated at all, which method equates, and how the asks' register is matched."""
import csv
import datetime as dt
import os
import re

import numpy as np
import openpyxl

import methods as M
import pack as P
import world as W


def _csv(target, key):
    with open(os.path.join(target, P.FILES[key]), encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


class Pack:
    def __init__(self, target):
        self.target = target
        self._read()

    # ------------------------------------------------------------------------------------------------- reading
    def _read(self):
        wb = openpyxl.load_workbook(os.path.join(self.target, P.FILES["maps"]), read_only=True)
        self.maps = {}
        for form in ("25A", "26A"):
            rows = list(wb["Form %s" % form].iter_rows(min_row=2, values_only=True))
            self.maps[form] = {r[1]: int(r[0]) for r in rows if r[2] == "Multiple choice"}
            self.wa_ids = getattr(self, "wa_ids", {})
            self.wa_ids[form] = [r[1] for r in rows if r[2] == "Written assignment"]
        shared = sorted(set(self.maps["25A"]) & set(self.maps["26A"]))
        self.shared = shared
        self.pos25 = [self.maps["25A"][i] - 1 for i in shared]
        self.shared_wa = [k for k, w in enumerate(self.wa_ids["26A"]) if w in self.wa_ids["25A"]][0]
        # the attempt history: each educator's attempts; a voided attempt is not an attempt
        self.hist = {}
        self.names = {}
        for r in _csv(self.target, "history"):
            if r["RESULT"] == "VOID":
                continue
            self.hist.setdefault(r["EDUCATOR_ID"], []).append((r["TEST_DATE"], r["RESULT"]))
            self.names[r["EDUCATOR_ID"]] = (norm(r["LAST_NAME"]), norm(r["FIRST_NAME"]), _date(r["BIRTH_DATE"]))
        self.first = {e: min(v)[0] for e, v in self.hist.items()}
        self.first_result = {e: min(v)[1] for e, v in self.hist.items()}
        # June 2025: Pellmore's file
        self.s25 = []
        for r in _csv(self.target, "scores25"):
            wa = []
            for a in (1, 2, 3):
                r3 = r["WA%d_R3" % a]
                wa.append(2 * int(r3) if r3 else int(r["WA%d_R1" % a]) + int(r["WA%d_R2" % a]))
            items = r["ITEM_SCORES"]
            mc_anchor = sum(int(items[p]) for p in self.pos25)
            self.s25.append(dict(eid=r["CAND_ID"], raw=int(r["TOTAL_RAW"]), mc_anchor=mc_anchor, wa=wa,
                                 first=self.first.get(r["CAND_ID"]) == "2025-06-14"))
        # June 2026: Arcwright's files through the Board's crosswalk
        cw = {r["REG_ID"]: r["EDUCATOR_ID"] for r in _csv(self.target, "crosswalk")}
        shared_set = set(shared)
        anchor_mc = {}
        with open(os.path.join(self.target, P.FILES["items26"]), encoding="utf-8", newline="") as fh:
            for r in csv.DictReader(fh):
                if r["ITEM_ID"] in shared_set:
                    anchor_mc[r["REG_ID"]] = anchor_mc.get(r["REG_ID"], 0) + int(r["ITEM_SCORE"])
        self.s26 = []
        for r in _csv(self.target, "scores26"):
            if r["STATUS"] != "SCORED":
                continue
            e = cw[r["REG_ID"]]
            self.s26.append(dict(reg=r["REG_ID"], eid=e, raw=int(r["RAW_TOTAL"]), mc_anchor=anchor_mc.get(r["REG_ID"], 0),
                                 wa=[int(r["WA%d_SCORE" % a]) for a in (1, 2, 3)],
                                 first=self.first.get(e) == "2026-06-13"))
        # validity papers
        qc = openpyxl.load_workbook(os.path.join(self.target, P.FILES["qc26"]), read_only=True)
        self.papers = {r[0]: dict(wa=r[1], source=r[2], consensus=int(r[3]))
                       for r in qc["Validity papers"].iter_rows(min_row=2, values_only=True)}
        self.vreads = []
        with open(os.path.join(self.target, P.FILES["reads26"]), encoding="utf-8", newline="") as fh:
            for r in csv.DictReader(fh):
                if r["READ_TYPE"] == "VALIDITY":
                    self.vreads.append((r["RESPONSE_ID"], r["ASSIGNMENT"], int(r["SCORE"])))
        self.conv = {int(r["RAW_SCORE"]): int(r["SCALE_SCORE"]) for r in _csv(self.target, "conv")}

    # --------------------------------------------------------------------------------------------- the anchor
    def arrays(self):
        w = W.WA_WEIGHT
        k = self.shared_wa
        Y = np.array([s["raw"] for s in self.s25 if s["first"]], float)
        VY = np.array([s["mc_anchor"] + w * s["wa"][k] for s in self.s25 if s["first"]], float)
        VYm = np.array([s["mc_anchor"] for s in self.s25 if s["first"]], float)
        X = np.array([s["raw"] for s in self.s26 if s["first"]], float)
        VX = np.array([s["mc_anchor"] + w * s["wa"][k] for s in self.s26 if s["first"]], float)
        VXm = np.array([s["mc_anchor"] for s in self.s26 if s["first"]], float)
        return X, VX, VXm, Y, VY, VYm

    def validity_bias(self, which="carried", per_paper=False):
        """mean of (2026 read minus consensus) over the validity papers: the carried assignment's (from the 2025
        scoring) or every assignment's"""
        wa = "WA%d" % (self.shared_wa + 1)
        sel = [(p, v - self.papers[p]["consensus"]) for p, a, v in self.vreads if which == "all" or a == wa]
        if per_paper:
            by = {}
            for p, d in sel:
                by.setdefault(p, []).append(d)
            return float(np.mean([np.mean(v) for v in by.values()]))
        return float(np.mean([d for _, d in sel]))

    def cut(self, route="golden", method="Tucker (sample weights)"):
        X, VX, VXm, Y, VY, VYm = self.arrays()
        if route == "no equating":
            return M.cut(lambda x: x)[0], lambda x: x
        if route == "raters adjusted, no equating":
            sh = -2 * self.validity_bias() * W.WA_WEIGHT * W.N_WA
            return M.cut(lambda x: x + sh)[0], lambda x: x + sh
        if route == "as scored":
            fam = M.family(X, VX, Y, VY)
        elif route == "multiple-choice anchor":
            fam = M.family(X, VXm, Y, VYm)
        elif route == "every assignment's papers":
            fam = M.family(X, VX, Y, VY, -2 * self.validity_bias("all") * W.WA_WEIGHT)
        elif route == "golden":
            fam = M.family(X, VX, Y, VY, -2 * self.validity_bias() * W.WA_WEIGHT)
        else:
            raise ValueError(route)
        if method == "all":
            return {k: M.cut(e) for k, e in fam.items()}
        e = fam[method]
        return M.cut(e)[0], e

    # -------------------------------------------------------------------------------------------- completers
    def completers(self):
        """the 2025-26 completers of each program's elementary pathway, from its Title II list"""
        wb = openpyxl.load_workbook(os.path.join(self.target, P.FILES["completers"]), read_only=True)
        out = {}
        for k, pr in enumerate(W.PROGRAMS):
            rows = list(wb[pr[1]].iter_rows(values_only=True))
            head = rows[4]
            seen = set()
            ids = []
            for r in rows[5:]:
                if not r or r[0] is None:
                    continue
                d = dict(zip(head, r))
                eid, area, done = parse_row(d)
                if not (W.PROGRAM_YEAR[0] <= done <= W.PROGRAM_YEAR[1]):
                    continue
                if not is_elementary(area):
                    continue
                if eid in seen:
                    continue
                seen.add(eid)
                ids.append(eid)
            out[k] = ids
        return out

    def rates(self, cut26, comp=None):
        """each program's completers with a first attempt by June 13, 2026, passers and rate"""
        comp = comp or self.completers()
        res26 = {s["eid"]: s["raw"] >= cut26 for s in self.s26 if s["first"]}
        out = {}
        for k, ids in comp.items():
            n = p = 0
            for e in ids:
                f = self.first.get(e)
                if f is None or f > "2026-06-13":
                    continue
                n += 1
                if f == "2026-06-13":
                    p += int(res26[e])
                else:
                    p += int(self.first_result[e] == "PASS")
            out[k] = (n, p)
        return out

    # ----------------------------------------------------------------------------------------------- the ask
    def prior_year(self, match="golden"):
        """each program's 2024-25 elementary completers with a first attempt by June 14, 2025, and their passers:
        matched to the history by educator ID, and (golden) by name and birth date where the ID finds no attempts"""
        code = {pr[1]: k for k, pr in enumerate(W.PROGRAMS)}
        by_name = {}
        for e, (ln, fn, dob) in self.names.items():
            by_name.setdefault((ln, fn, dob), []).append(e)
        out = {k: [0, 0] for k in range(len(W.PROGRAMS))}
        for r in _csv(self.target, "register"):
            if r["PROGRAM_YEAR"] != "2024-25" or not is_elementary(r["PATHWAY"]) or r["PROGRAM_CODE"] not in code:
                continue
            e = r["EDUCATOR_ID"]
            if e not in self.hist and match == "golden":
                cand = by_name.get((norm(r["LAST_NAME"]), norm(r["FIRST_NAME"]), _date(r["BIRTH_DATE"])), [])
                if len(cand) == 1:
                    e = cand[0]
            f = self.first.get(e)
            if f is None or f > "2025-06-14":
                continue
            k = code[r["PROGRAM_CODE"]]
            out[k][0] += 1
            out[k][1] += int(self.first_result[e] == "PASS")
        return {k: tuple(v) for k, v in out.items()}


def norm(s):
    return re.sub(r"[^A-Z]", "", (s or "").upper())


def _date(s):
    s = str(s).strip()
    for fmt in ("%m/%d/%Y", "%Y-%m-%d", "%B %d, %Y"):
        try:
            return dt.datetime.strptime(s, fmt).date()
        except ValueError:
            pass
    raise ValueError(s)


def parse_row(d):
    """an educator ID, a pathway and a completion date from any of the three layouts"""
    if "Educator ID" in d:
        return d["Educator ID"], d["Pathway"], _date(d["Completion Date"])
    if "STATE ID" in d:
        return "E" + str(d["STATE ID"]).zfill(7), d["PROGRAM AREA"], _date(d["DATE COMPLETED"])
    return "E" + str(d["Educator #"]).replace("E-", "").zfill(7), d["Licensure Area"], _date(d["Residency Exit"])


def is_elementary(area):
    a = (area or "").upper()
    return a.startswith("ELEM")
