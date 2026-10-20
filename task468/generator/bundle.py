"""Read the shipped pack and determine the 2027 Hospital Quality Bonus from it: Halbrook's claims and Carrisford's
encounters conformed into stays, the measure's index admissions, their expected deaths from the risk scores, the deaths
the bills record, the linkage's returns, the members' later activity, each hospital's deaths and ratio by every route
of the ladder, and each hospital's fiscal 2026 inpatient payments. Only the pack's files are read; the options replay
the natural handlings of the pack's mess (checks.py asserts which leave the call where it was)."""
import csv
import datetime as dt
import os

import numpy as np
import pandas as pd

import methods as M
import world as W

FY0, FY1 = dt.date(2025, 7, 1), dt.date(2026, 6, 30)


def path(target, key):
    return os.path.join(target, W.FILES[key])


def d_iso(s):
    return dt.date.fromisoformat(s)


def d_us2(s):
    m, d, y = s.split("/")
    return dt.date(2000 + int(y), int(m), int(d))


def d_ymd(s):
    return dt.date(int(s[:4]), int(s[4:6]), int(s[6:8]))


class Pack:
    def __init__(self, target):
        self.t = target
        self._c = {}

    # ------------------------------------------------------------------------------------------------ readers
    def roster(self):
        if "roster" not in self._c:
            rows = list(csv.DictReader(open(path(self.t, "roster"), encoding="utf-8")))
            self._c["roster"] = {r["npi"]: r["hospital_name"] for r in rows}
        return self._c["roster"]

    def members(self):
        if "members" not in self._c:
            out, cmg = {}, {}
            for r in csv.DictReader(open(path(self.t, "enrollment"), encoding="utf-8")):
                mm, dd, yy = r["birth_date"].split("/")
                last = r["last_name"]
                cls = "ssn" if r["ssn_last4"] else ("compound" if (" " in last or "-" in last) else "simple")
                out[r["member_id"]] = dict(dob=dt.date(int(yy), int(mm), int(dd)), cls=cls, last=last)
                if r["cmg_member_no"]:
                    cmg[r["cmg_member_no"]] = r["member_id"]
            self._c["members"], self._c["cmg"] = out, cmg
        return self._c["members"]

    def claims(self):
        if "claims" not in self._c:
            self._c["claims"] = pd.read_csv(path(self.t, "claims"), dtype=str, keep_default_na=False)
        return self._c["claims"]

    def encounters(self):
        if "enc" not in self._c:
            rows = []
            for line in open(path(self.t, "encounters"), encoding="utf-8").read().splitlines():
                f = line.split("|")
                if f[0] == "D":
                    rows.append(f[1:])
            cols = ["enc_id", "freq", "orig", "cmg_no", "npi", "admit", "disch", "status", "drg", "dx", "submit",
                    "paid"]
            self._c["enc"] = pd.DataFrame(rows, columns=cols)
        return self._c["enc"]

    # ------------------------------------------------------------------------------------------------ stays
    def plan_chains(self):
        """Halbrook's bills grouped into stays: each original bill (0111) with the replacement (0117) that corrects
        it and the void (0118) that cancels it."""
        if "chains" in self._c:
            return self._c["chains"]
        c = self.claims()
        orig = c[c["type_of_bill"] == "0111"]
        rep = c[c["type_of_bill"] == "0117"].set_index("original_claim_number")
        void = set(c.loc[c["type_of_bill"] == "0118", "original_claim_number"])
        void_amt = c[c["type_of_bill"] == "0118"].set_index("original_claim_number")["paid_amount"].astype(float)
        out = []
        for r in orig.itertuples(index=False):
            k = r.claim_number
            fin = rep.loc[k] if k in rep.index else None
            out.append(dict(root=k, member=r.member_id, npi=r.billing_npi, adm=d_iso(r.admission_date),
                            disch=d_iso(r.statement_thru_date), status=r.patient_status,
                            drg=fin["drg"] if fin is not None else r.drg, a0=float(r.paid_amount),
                            a0_new=r.claim_number.startswith("HC"),
                            rep=float(fin["paid_amount"]) if fin is not None else None,
                            rep_new=fin is not None and str(fin["claim_number"]).startswith("HC"),
                            rep_date=d_iso(fin["paid_date"]) if fin is not None else None,
                            voided=k in void, void=float(void_amt[k]) if k in void else None, src="plan"))
        self._c["chains"] = out
        return out

    def enc_chains(self):
        if "echains" in self._c:
            return self._c["echains"]
        self.members()
        e = self.encounters()
        orig = e[e["freq"] == "1"]
        rep = e[e["freq"] == "7"].set_index("orig")
        dele = set(e.loc[e["freq"] == "8", "orig"])
        out = []
        for r in orig.itertuples(index=False):
            fin = rep.loc[r.enc_id] if r.enc_id in rep.index else None
            out.append(dict(root=r.enc_id, member=self._c["cmg"][r.cmg_no], npi=r.npi, adm=d_us2(r.admit),
                            disch=d_us2(r.disch), status=r.status, drg=fin["drg"] if fin is not None else r.drg,
                            voided=r.enc_id in dele, src="cmg"))
        self._c["echains"] = out
        return out

    def stays(self, plan_only=False, keep_voided=False, roster_drop=()):
        roster = {k: v for k, v in self.roster().items() if k not in roster_drop}
        out = [s for s in self.plan_chains() + ([] if plan_only else self.enc_chains())
               if keep_voided or not s["voided"]]
        for s in out:
            s["hosp"] = roster.get(s["npi"])
        return out

    # ------------------------------------------------------------------------------------------------ the measure
    def index(self, first_only=True, drop_delivery=True, drop_ama=True, adults=True, join_transfers=True,
              keep_voided=False, plan_only=False, roster_drop=()):
        """The measure's index admissions (specification 2.1 to 2.4), each with the stays that continue it."""
        mem = self.members()
        st = [dict(s) for s in self.stays(plan_only=plan_only, keep_voided=keep_voided, roster_drop=roster_drop)
              if s["hosp"]]
        by_m = {}
        for s in st:
            by_m.setdefault(s["member"], []).append(s)
        for v in by_m.values():
            v.sort(key=lambda s: (s["adm"], s["disch"], s["root"]))
        idx = []
        for m, v in sorted(by_m.items()):
            elig = []
            for s in v:
                if not (FY0 <= s["adm"] <= FY1):
                    continue
                if adults and (s["adm"] - mem[m]["dob"]).days < 18 * 365.25:
                    continue
                if drop_delivery and s["drg"] in W.DELIVERY_DRGS:
                    continue
                if drop_ama and s["status"] == "07":
                    continue
                elig.append(s)
            cont = set()
            for s in elig:
                if id(s) in cont:
                    continue
                chain = [s]
                if join_transfers:
                    cur = s
                    while cur["status"] == "02":
                        nxt = [t for t in v if t is not cur and t["hosp"] != cur["hosp"]
                               and 0 <= (t["adm"] - cur["disch"]).days <= 1]
                        if not nxt:
                            break
                        cur = nxt[0]
                        chain.append(cur)
                        cont.add(id(cur))
                idx.append(dict(member=m, hosp=s["hosp"], npi=s["npi"], adm=s["adm"], chain=chain, all=v))
                if first_only:
                    break
        return idx

    def scores(self):
        if "scores" not in self._c:
            import openpyxl
            wb = openpyxl.load_workbook(path(self.t, "scores"), read_only=True)
            ws = wb["Scores"]
            rows = ws.iter_rows(values_only=True)
            head = next(rows)
            ix = {h: i for i, h in enumerate(head)}
            out = {}
            for r in rows:
                if r[0] is None:
                    continue
                out[(str(r[ix["member_id"]]), str(r[ix["admission_date"]])[:10], str(r[ix["facility_npi"]]))] = float(
                    r[ix["p_death_30d"]])
            self._c["scores"] = out
        return self._c["scores"]

    def links(self):
        if "links" not in self._c:
            out = {}
            for r in csv.DictReader(open(path(self.t, "linkage"), encoding="utf-8")):
                out[(r["HCHP_MEMBER_ID"], d_ymd(r["ADMIT_DATE"]))] = (d_ymd(r["DATE_OF_DEATH"]), r["MATCH_PASS"],
                                                                       r["STATE_FILE_NUMBER"])
            self._c["links"] = out
        return self._c["links"]

    def links_by_member(self):
        if "lbm" not in self._c:
            out = {}
            for k, v in self.links().items():
                out.setdefault(k[0], []).append((k, v))
            self._c["lbm"] = out
        return self._c["lbm"]

    def activity(self):
        if "act" not in self._c:
            a = pd.read_csv(path(self.t, "activity"), dtype=str)
            out = {}
            for m, d in zip(a["member_id"], a["service_date"]):
                out.setdefault(m, []).append(d)
            self._c["act"] = {m: sorted(set(d_iso(x) for x in v)) for m, v in out.items()}
        return self._c["act"]

    def frame(self, alive_def="all", link_join="record", window=W.WINDOW, **kw):
        """One row per index admission: hospital, member, identifier class, expected mortality, the death the bills
        record (in the stay or a stay continuing it, or a later stay inside the 30 days), the linkage's return on the
        admission, and whether the member's records show them alive after their linked date of death and after day
        30."""
        key = ("frame", alive_def, link_join, window, tuple(sorted(kw.items())))
        if key in self._c:
            return self._c[key]
        mem, sc, lk, act = self.members(), self.scores(), self.links(), self.activity()
        rows = []
        for i in self.index(**kw):
            m, adm = i["member"], i["adm"]
            w_end = adm + dt.timedelta(days=window)
            in_stay = any(s["status"] == "20" and s["disch"] <= w_end for s in i["chain"])
            death = next((s["disch"] for s in i["chain"] if s["status"] == "20" and s["disch"] <= w_end), None)
            ids = {id(s) for s in i["chain"]}
            later = [s["disch"] for s in i["all"] if s["status"] == "20" and id(s) not in ids
                     and s["adm"] >= adm and s["disch"] <= w_end]
            if death is None and later:
                death = min(later)
            alive = list(act.get(m, []))
            if alive_def != "lines":
                for s in i["all"]:
                    alive.append(s["adm"])
                    if s["status"] != "20":
                        alive.append(s["disch"])
            if link_join == "record":
                l = lk.get((m, adm))
                if l is not None and l[0] > w_end:
                    l = None
            else:                               # any link on any of the member's records dated inside the 30 days
                c = [v for (mm, a), v in self.links_by_member().get(m, []) if adm <= v[0] <= w_end]
                l = min(c) if c else None
            last = mem[m]["last"]
            rows.append(dict(hosp=i["hosp"], member=m, adm=adm, cls=mem[m]["cls"],
                             p=sc[(m, adm.isoformat(), i["npi"])], in_stay=in_stay, known_death=death is not None,
                             known_place="stay" if in_stay else ("later" if death else None), linked=l is not None,
                             link_date=l[0] if l else None, link_pass=l[1] if l else None,
                             contradicted=bool(l is not None and any(d > l[0] for d in alive)),
                             alive_after=any((d >= w_end) if alive_def == "on30" else (d > w_end) for d in alive),
                             comp=(" " in last or "-" in last), space=" " in last, hyphen="-" in last))
        f = pd.DataFrame(rows)
        self._c[key] = f
        return f

    def determination(self, how="golden", by="cls", frame=None, mkw=None, **kw):
        f = self.frame(**kw) if frame is None else frame
        if by == "pass":
            f = f.assign(**{"pass": np.where(f["cls"] == "ssn", "SSN", "NAME")})
        elif by == "all":
            f = f.assign(all="all")
        d = M.deaths(f, how=how, by=by, **(mkw or {}))
        E = f.groupby("hosp")["p"].sum()
        known = f.groupby("hosp")["known_death"].sum()
        n = f.groupby("hosp").size()
        rat = {h: d[h] / E[h] for h in d}
        return dict(deaths=d, expected=E.to_dict(), known=known.to_dict(), n=n.to_dict(), ratio=rat,
                    losers=M.losers(rat), rates=M.rates(f, by))

    def disputes(self):
        """Provider Disputes' log, one dict per dispute, dates as dates."""
        if "pdr" not in self._c:
            import openpyxl
            wb = openpyxl.load_workbook(path(self.t, "disputes"), read_only=True)
            rows = wb["Log"].iter_rows(values_only=True)
            head = [str(h) for h in next(rows)]
            out = []
            for r in rows:
                if r[0] is None:
                    continue
                d = dict(zip(head, r))
                for k in ("Received", "Admit Date", "Discharge Date", "Determination Date", "Payment Date"):
                    if d[k] is not None and hasattr(d[k], "date"):
                        d[k] = d[k].date()
                out.append(d)
            self._c["pdr"] = out
        return self._c["pdr"]

    def awards(self, how="unbilled", basis="discharge"):
        """Each hospital's dispute awards for stays discharged in fiscal 2026. 'unbilled' (the golden): each award
        paid by September 30 that no bill in the claims extract already carries, a bill carrying it when it replaces
        the disputed claim on the award's payment date and changes the payment by the award. 'paid': every award paid.
        'decided': every award decided for the hospital, paid or not. 'disputed': the amount disputed on every dispute
        decided for the hospital. basis 'payment': awards paid in fiscal 2026 whatever the discharge date."""
        roster = self.roster()
        chains = {s["root"]: s for s in self.plan_chains()}
        out = {h: 0.0 for h in W.CANDIDATES}
        for d in self.disputes():
            h = roster.get(str(d["Provider NPI"]))
            if h is None or d["Determination"] not in ("Overturned", "Partially overturned"):
                continue
            paid = d["Payment Date"]
            if basis == "payment":
                if paid is None or not (FY0 <= paid <= FY1):
                    continue
            elif not (FY0 <= d["Discharge Date"] <= FY1):
                continue
            if how == "disputed":
                out[h] += float(d["Amount Disputed"])
                continue
            if how != "decided" and paid is None:
                continue
            a = float(d["Additional Payment"])
            if how == "unbilled":
                c = chains.get(str(d["Claim No."]))
                if c is not None and c["rep"] is not None and c["rep_date"] == paid:
                    change = c["rep"] - c["a0"] if c["rep_new"] else c["rep"]
                    if abs(change - a) < 0.005:
                        continue
            out[h] += a
        return out

    # ------------------------------------------------------------------------------------------------ payments
    def payments(self, how="vintage", basis="discharge", npi_map=True, with_cmg=False, awards="unbilled",
                 award_basis="discharge"):
        """Each hospital's fiscal 2026 inpatient payments from Halbrook's bills and its dispute awards. 'vintage': a
        replacement adjudicated on the former system adds its amount to the original's, one adjudicated on the new
        platform stands in its place; a voided bill pays nothing. 'standard': every replacement stands in its
        original's place. 'sum': every line's amount added. 'net': every replacement added to its original. awards:
        see awards(), or 'none'."""
        roster = self.roster()
        if not npi_map:
            roster = {k: v for k, v in roster.items() if k != "1952407316"}
        out = {h: 0.0 for h in W.CANDIDATES}
        for s in self.plan_chains():
            when = s["disch"] if basis == "discharge" else s["adm"]
            if not (FY0 <= when <= FY1):
                continue
            h = roster.get(s["npi"])
            if h is None:
                continue
            if how == "sum":
                v = s["a0"] + (s["rep"] or 0.0) + (s["void"] or 0.0)
            elif s["voided"]:
                v = 0.0
            elif s["rep"] is None:
                v = s["a0"]
            elif how == "standard":
                v = s["rep"]
            elif how == "net":
                v = s["a0"] + s["rep"]
            else:
                v = s["rep"] if s["rep_new"] else s["a0"] + s["rep"]
            out[h] += v
        if with_cmg:                            # Carrisford's own payments added, as if Halbrook had made them
            e = self.encounters()
            paid = dict(zip(e["enc_id"], e["paid"].astype(float)))
            rep = dict(zip(e.loc[e["freq"] == "7", "orig"], e.loc[e["freq"] == "7", "enc_id"]))
            for s in self.enc_chains():
                h = roster.get(s["npi"])
                if s["voided"] or h is None or not (FY0 <= s["disch"] <= FY1):
                    continue
                out[h] += paid[rep.get(s["root"], s["root"])]
        if awards != "none":
            for h, v in self.awards(how=awards, basis=award_basis).items():
                out[h] += v
        return out

    def bonus(self, **kw):
        pay = self.payments(**kw)
        return {h: W.BONUS_RATE * v for h, v in pay.items()}
