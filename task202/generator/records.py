"""The tables the foundation's own systems would export, built from the simulated truth.

The split that matters: the claim returns state a total and an award count per partner, band and
month for every accredited partner, and the partner claim portal holds the two pilot provinces'
awards one row at a time. Nothing else in the pack carries an individual award amount.
"""
import datetime as dt

import numpy as np
import pandas as pd

import params as P
import sim

MONTHS = sim.MONTHS


def mlabel(t, new=False):
    return "%s-%d" % (dt.date(t[0], t[1], 1).strftime("%b"), t[0]) if new else "%04d-%02d" % t


def band_code(b):
    return "B%d" % b


def legacy_band(b):
    return "HH%d" % b


class Records:
    def __init__(self, W):
        self.W = W
        self.parts = W["parts"]
        self.ledger = {}
        self.portal_id = {}
        self.portal_ref = {}
        for pt in self.parts:
            prov = pt["province"].split("-")[1]
            self.ledger[pt["idx"]] = "HRG-%s-%03d" % (prov, 1 + pt["slot"] * 7 % 71)
        # the portal was procured years after the grants ledger and stores the partner reference in
        # its own style, loaded once from a flat file
        for i, pt in enumerate([p for p in self.parts if p["portal"]]):
            code = self.ledger[pt["idx"]]
            self.portal_id[pt["idx"]] = "PP-%04d" % (1200 + 37 * i + pt["slot"])
            style = i % 7
            if style == 3:
                ref = code + " "
            elif style == 5:
                ref = code.replace("-", "_")
            else:
                ref = code.lower().replace("-", "_")
            self.portal_ref[pt["idx"]] = ref
        self._prelim = None

    # ---------------------------------------------------------------- the spine
    def portal_awards(self):
        rows = []
        seq = {}
        for a in sorted(self.W["por"], key=lambda a: (a["paid"], a["partner"], a["amount"])):
            pt = self.parts[a["partner"]]
            y = a["paid"].year
            seq[y] = seq.get(y, 0) + 1
            rows.append({
                "portal_award_ref": "PCP-%d-%06d" % (y, 100 * seq[y] + (a["partner"] * 7 + 3) % 97),
                "portal_partner_id": self.portal_id[a["partner"]],
                "partner_ref_portal": self.portal_ref[a["partner"]],
                "province_code": pt["province"],
                "claim_return_month": mlabel(a["month"]),
                "application_date": (a["decided"] - dt.timedelta(days=4 + (a["partner"] % 9))).isoformat(),
                "decision_date": a["decided"].isoformat(),
                "payment_date": a["paid"].isoformat(),
                "household_size": a["size"],
                "size_band": band_code(a["band"]),
                "component_code": a["component"],
                "award_amount_php": "%.2f" % a["amount"],
            })
        return pd.DataFrame(rows)

    # ---------------------------------------------------------------- the claim returns
    def prelim(self):
        """The reopened months' preliminary returns: what each refiling partner first sent in."""
        if self._prelim is not None:
            return self._prelim
        out = {}
        for mi, mo in enumerate(P.REVISED_MONTHS):
            r = sim.stream(11, mi)
            live = [pt["idx"] for pt in self.parts if pt["first_month"] <= mo <= pt["last_month"]]
            k = 17 if mi == 0 else 11
            refile = sorted(r.choice(live, size=k, replace=False).tolist())
            for pi in refile:
                cells = [(b, self.W["cells"][(pi, mo, b)]) for b in P.BANDS if (pi, mo, b) in self.W["cells"]]
                if len(cells) < 2:
                    continue
                rr = sim.stream(12, mi, pi)
                pick = rr.choice(len(cells), size=min(2, len(cells)), replace=False)
                for j in pick:
                    b, (n, tot) = cells[int(j)]
                    aws = sorted([a for a in self.W["awards"]
                                  if a["partner"] == pi and a["month"] == mo and a["band"] == b],
                                 key=lambda a: (a["paid"], a["amount"]))
                    if rr.random() < 0.72 and n > 3:
                        d = int(rr.integers(1, 4))                   # paperwork arrived late
                        drop = aws[-d:]
                        out[(mo, pi, b)] = (n - d, round(tot - sum(x["amount"] for x in drop), 2))
                    else:
                        d = int(rr.integers(1, 3))                   # later disallowed at review
                        lvl = P.BASE * self.parts[pi]["level"] * (P.SCALE3[b] / 1000.0) * P.BAND_LEVEL_TILT[b]
                        extra = np.round(lvl * np.exp(rr.normal(-0.03, 0.26, d)) / sim.UPPER_NORM, 2)
                        out[(mo, pi, b)] = (n + d, round(tot + float(extra.sum()), 2))
        self._prelim = out
        return out

    def returns_rows(self, months):
        """One row per partner, band and claim month, as the claims system exports it."""
        pre = self.prelim()
        rows = []
        for mo in months:
            revised = sorted({pi for (m, pi, b) in pre if m == mo})
            for pt in self.parts:
                pi = pt["idx"]
                if not (pt["first_month"] <= mo <= pt["last_month"]):
                    continue
                cells = [(b, self.W["cells"][(pi, mo, b)]) for b in P.BANDS
                         if (pi, mo, b) in self.W["cells"]]
                if not cells:
                    continue
                if mo in P.REVISED_MONTHS:
                    # the month was opened as preliminary pending the reconciliation exercise
                    for b, (n, tot) in cells:
                        pn, pt_ = pre.get((mo, pi, b), (n, tot))
                        rows.append((mo, self.ledger[pi], b, pn, pt_, "PRELIM"))
                    if pi in revised:
                        for b, (n, tot) in cells:
                            rows.append((mo, self.ledger[pi], b, n, tot, "REVISED"))
                else:
                    for b, (n, tot) in cells:
                        rows.append((mo, self.ledger[pi], b, n, tot, "FINAL"))
        return rows

    def recovery_row(self):
        """One partner's recovered award, shown as a negative claim line in its own month."""
        pr = P.RECOVERY
        pi = [pt["idx"] for pt in self.parts
              if pt["province"] == pr["province"] and pt["slot"] == pr["slot"]][0]
        aws = sorted([a for a in self.W["awards"] if a["partner"] == pi and a["band"] == pr["band"]
                      and a["month"] < pr["month"]], key=lambda a: (a["paid"], a["amount"]))
        a = aws[-1]
        return (pr["month"], self.ledger[pi], pr["band"], -1, -a["amount"], a["paid"])

    # ---------------------------------------------------------------- reference tables
    def register(self):
        rows = []
        for pt in self.parts:
            st, sd = "ACTIVE", ""
            first = dt.date(pt["first_month"][0], pt["first_month"][1], 1)
            acc = first if pt["first_month"] != P.RETURNS_FROM else dt.date(
                2016 + (pt["idx"] % 8), 1 + (pt["idx"] * 5) % 12, 1 + (pt["idx"] * 11) % 27)
            if pt["last_month"] != (2027, 3):
                st = "WITHDRAWN"
                sd = P.EXIT_PARTNER["withdrawn"].isoformat()
            rows.append({"partner_code": self.ledger[pt["idx"]], "partner_name": pt["name"],
                         "province_code": pt["province"], "municipality": pt["town"],
                         "accredited_from": acc.isoformat(), "accreditation_status": st,
                         "status_date": sd})
        r = sim.stream(21)
        for j in range(P.LAPSED_CODES):
            prov = P.PROVINCES[(j * 3) % len(P.PROVINCES)]
            town = P.TOWNS[prov[0]][(j * 4 + 2) % P.PARTNERS_PER_PROVINCE]
            rows.append({"partner_code": "HRG-%s-%03d" % (prov[0].split("-")[1], 900 + j),
                         "partner_name": P.FORMS[(j * 5 + 2) % len(P.FORMS)].format(t=town),
                         "province_code": prov[0], "municipality": town,
                         "accredited_from": dt.date(2014 + j, 3 + j, 1 + 6 * j).isoformat(),
                         "accreditation_status": "LAPSED",
                         "status_date": dt.date(2023, 4 + 2 * j, 28 - j).isoformat()})
        return pd.DataFrame(rows).sort_values("partner_code").reset_index(drop=True)

    def crosswalk(self):
        rows = []
        for pt in self.parts:
            if not pt["portal"]:
                continue
            rows.append({"portal_partner_id": self.portal_id[pt["idx"]],
                         "partner_ref_portal": self.portal_ref[pt["idx"]],
                         "ledger_partner_code": self.ledger[pt["idx"]],
                         "enrolled_date": "2025-01-06", "account_status": "LIVE"})
        # two accounts opened for a province that was considered for the pilot and never went live
        for j, (prov, slot) in enumerate([("P-ILI", 2), ("P-ILI", 6)]):
            pt = [p for p in self.parts if p["province"] == prov and p["slot"] == slot][0]
            code = self.ledger[pt["idx"]]
            rows.append({"portal_partner_id": "PP-%04d" % (1900 + 11 * j),
                         "partner_ref_portal": code.lower().replace("-", "_"),
                         "ledger_partner_code": code,
                         "enrolled_date": "2025-09-15", "account_status": "OPENED_NOT_LIVE"})
        return pd.DataFrame(rows).sort_values("portal_partner_id").reset_index(drop=True)

    def bands(self):
        return pd.DataFrame([
            {"band_code": band_code(b), "legacy_band_code": legacy_band(b),
             "band_label": P.BAND_LABEL[b], "household_size_from": b,
             "household_size_to": "" if b == 6 else b} for b in P.BANDS])

    def provinces(self):
        pilot = {self.parts[i]["province"] for i in range(len(self.parts)) if self.parts[i]["portal"]}
        rows = []
        for code, name, psgc, region in P.PROVINCES:
            rows.append({"province_code": code, "province_name": name, "psgc_province_code": psgc,
                         "region": region, "field_office": "%s field office" % name,
                         "portal_pilot_from": "2025-01-01" if code in pilot else ""})
        return pd.DataFrame(rows)

    # ---------------------------------------------------------------- the distractors
    def treasury(self):
        """Fortnightly payment runs: what left the foundation, net of recoveries."""
        rec = self.recovery_row()
        half = {}
        for a in self.W["awards"]:
            if a["month"] < (2026, 1):
                continue
            h = 1 if a["paid"].day <= 15 else 2
            k = (a["month"], h, a["partner"])
            half[k] = round(half.get(k, 0.0) + a["amount"], 2)
        rows = []
        for (mo, h, pi), gross in sorted(half.items()):
            y, m = mo
            nm = (y + (m == 12), m % 12 + 1)
            run = dt.date(nm[0], nm[1], 8 if h == 1 else 22)
            r = 0.0
            if mo == rec[0] and self.ledger[pi] == rec[1] and h == 2:
                r = -rec[4]
            rows.append({"run_ref": "DR-%04d%02d-%d" % (nm[0], nm[1], h),
                         "run_date": run.strftime("%d/%m/%Y"),
                         "value_date": (run + dt.timedelta(days=2)).strftime("%d/%m/%Y"),
                         "partner_code": self.ledger[pi],
                         "claim_months_covered": mlabel(mo),
                         "gross_php": "%.2f" % gross, "recoveries_php": "%.2f" % r,
                         "net_php": "%.2f" % round(gross - r, 2)})
        return pd.DataFrame(rows)

    def followup(self):
        """The 2026 household follow-up survey: service quality, no amounts."""
        r = sim.stream(31)
        pool = [a for a in self.W["awards"] if (2026, 1) <= a["month"] <= (2026, 12)]
        idx = sorted(r.choice(len(pool), size=940, replace=False).tolist())
        rows = []
        for j, i in enumerate(idx):
            a = pool[i]
            pt = self.parts[a["partner"]]
            days = int((a["paid"] - a["decided"]).days)
            rows.append({"survey_ref": "FS26-%04d" % (1 + j),
                         "interview_date": (a["paid"] + dt.timedelta(days=30 + int(r.integers(0, 60)))).isoformat(),
                         "partner_code": self.ledger[a["partner"]], "province_code": pt["province"],
                         "household_size": a["size"], "days_to_payment": days,
                         "adequacy_rating": int(r.integers(1, 6)),
                         "repeat_application": "Y" if r.random() < 0.18 else "N",
                         "interviewer": "FS-%02d" % (1 + int(r.integers(0, 14)))})
        return pd.DataFrame(rows)
