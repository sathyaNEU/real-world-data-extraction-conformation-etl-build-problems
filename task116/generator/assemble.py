"""The whole book: the cast trusts plus every other school Tallybridge holds, and the framework schools it does not."""
import datetime as dt

import numpy as np
import pandas as pd

from book import SCHOOL_ROLES, OFFICER_ROLES, avoid_window, finalise, rand_start, school_row, LGR_NEW
from world import (AS_AT, CUTOVER, LICENCE_START, PILOT_PRICED, RATE, PRICE, MINIMUM, SIGN_RATE_DEN, SIGN_RATE_NUM,
                   annual_value, band_of, rng, term_for, price_year, add_years)
import roles

D = dt.date
SITE_NAMES = [("Lower", 0.55), ("Upper", 0.45)]


def pick(df, n, key):
    h = df["URN"].map(lambda u: rng(key, int(u)).random())
    return df.assign(_h=h).sort_values("_h").head(n).drop(columns="_h")


class Assembly:
    def __init__(self, reg, cast):
        self.reg, self.c = reg, cast
        self.rows = list(cast.rows)
        self.sell = reg.open_state()
        self.groups = reg.groups
        gt = dict(zip(reg.groups["Group UID"].astype(int), reg.groups["Group Type"]))
        self.sell["gtype"] = self.sell["tcode"].map(lambda t: gt.get(int(t)) if not pd.isna(t) else None)
        self.trust_used = set(cast.used)
        self.framework = []

    def free(self):
        used = (set(x["urn_current"] for x in self.rows) | set(f["urn"] for f in self.framework)
                | set(getattr(self, "fed_urns", set())))
        s = self.sell[~self.sell["URN"].isin(used)]
        return s[~s["tcode"].isin(self.trust_used)]

    def plain(self, a, key, months, lo=2018, hi=2025, pre_p=0.0, kind="school"):
        r = rng(key, int(a["URN"]))
        start = rand_start(r, lo, hi, months)
        rec = None
        if pre_p and r.random() < pre_p and not pd.isna(a["open_d"]):
            cs = D(int(a["open_d"].year) - 1, 4, 1)
            if cs.year >= 2015:
                p = roles.pred_eligible(self.reg, int(a["URN"]), cs)
                if p is not None:
                    start, rec = cs, p
        if rec is None and not pd.isna(a["open_d"]) and a["open_d"].date() > start:
            start = avoid_window(D(a["open_d"].year + 1, start.month, 1))
        role = SCHOOL_ROLES[int(r.integers(0, len(SCHOOL_ROLES)))]
        return school_row(self.reg, int(a["URN"]), start, ("head", int(a["URN"])), role, term_for(start, AS_AT)[0],
                          urn_recorded=rec, tag=kind)

    def build(self):
        c = self.c
        # single-academy trusts
        sat = self.free()
        sat = sat[sat["gtype"] == "Single-academy trust"]
        for _, a in pick(sat, 118, "sat").iterrows():
            self.rows.append(self.plain(a, "sat", (4, 9, 4, 9, 4, 1, 11, 3), pre_p=0.18, kind="sat"))
        # maintained schools, mostly on April terms
        la = self.free()
        la = la[la["EstablishmentTypeGroup (name)"] == "Local authority maintained schools"]
        la_pick = pick(la, 905, "la")
        for _, a in la_pick.iterrows():
            self.rows.append(self.plain(a, "la", (4, 4, 4, 4, 9, 9, 1, 3, 11, 6), kind="la"))
        sp = self.free()
        sp = sp[sp["EstablishmentTypeGroup (name)"] == "Special schools"]
        for _, a in pick(sp, 64, "special").iterrows():
            self.rows.append(self.plain(a, "special", (4, 9, 9, 1, 11), kind="special"))
        self.split_sites()
        self.migration_copies()
        self.closing_schools()
        self.framework_schools()
        self.framework_federations()
        self.identical_pair()
        self.ended()
        self.pilot_licences()
        self.cluster_licences()
        self.settle_rounding()
        finalise(self.rows)
        self.crm_writeback()
        return self

    def settle_rounding(self):
        """Every central trust in contention files the same planned pound whether its new recurring revenue is
        rounded first or not: move one or two agreements' billed pupils by a few until that holds."""
        c = self.c

        def ok(net):
            exact = net * SIGN_RATE_NUM / SIGN_RATE_DEN
            return (abs(exact - round(exact)) <= 0.20 and round(round(net) * SIGN_RATE_NUM / SIGN_RATE_DEN) == round(exact)
                    and abs(net - round(net)) <= 0.45)

        for uid in c.central[:15] + c.multi:
            a = roles.academy_frame(self.reg, c.op, uid)
            P = float(a["NumberOfPupils"].sum())
            subs = sorted([x for x in self.rows if x.get("uid") == uid and x["status"] == "In force"],
                          key=lambda z: (z["urn"], z["agreement_start"]))
            base = RATE * P - sum(x["annual_value_gbp"] for x in subs)
            if ok(base):
                c.net[uid] = base
                continue

            def value(x, p):
                if x.get("covers"):
                    from book import group_value
                    ts = x["current_term_start"]
                    base = sum(roles.pupils_billed(int(u), q, ts) for u, q in zip(x["covers"], x["covers_pupils"]))
                    return group_value(x, ts, p - base)
                return annual_value(x["price_band"], x["current_term_start"], p)

            done = False
            deltas = [d for k in range(1, 13) for d in (k, -k)]
            for i, x in enumerate(subs):
                for dlt in deltas:
                    v = value(x, x["pupils_billed"] + dlt)
                    net = base + x["annual_value_gbp"] - v
                    if ok(net):
                        x["pupils_billed"] += dlt
                        x["annual_value_gbp"] = v
                        done = True
                        break
                if done:
                    break
            if not done:
                for i, x in enumerate(subs):
                    for y in subs[i + 1:]:
                        for d1 in deltas[:8]:
                            for d2 in deltas[:8]:
                                v1, v2 = value(x, x["pupils_billed"] + d1), value(y, y["pupils_billed"] + d2)
                                net = base + x["annual_value_gbp"] + y["annual_value_gbp"] - v1 - v2
                                if ok(net):
                                    x["pupils_billed"] += d1
                                    y["pupils_billed"] += d2
                                    x["annual_value_gbp"], y["annual_value_gbp"] = v1, v2
                                    done = True
                                    break
                            if done:
                                break
                        if done:
                            break
                    if done:
                        break
            if not done:
                raise AssertionError("could not settle rounding for trust %s" % uid)
            c.net[uid] = RATE * P - sum(x["annual_value_gbp"] for x in subs)

    # ------------------------------------------------------------------ split sites
    def split_sites(self):
        cand = [i for i, x in enumerate(self.rows) if x["tag"] == "la" and x["pupils_current"] >= 380
                and x["urn"] == x["urn_current"]]
        r = rng("split")
        r.shuffle(cand)
        self.split_urns = []
        for i in sorted(cand[:21], reverse=True):
            x = self.rows.pop(i)
            for site in SITE_NAMES:
                y = school_row(self.reg, x["urn_current"], x["agreement_start"], x["signer_key"], x["signed_by_role"],
                               x["signed_on"], site=site, tag="la")
                self.rows.append(y)
            self.split_urns.append(x["urn_current"])

    # ------------------------------------------------------------------ the 2025 CRM migration
    def migration_copies(self):
        """Accounts re-created by the March 2025 migration: the same agreement under a second account."""
        cand = [x for x in self.rows if x["tag"] == "la" and x["site"] is None and x["agreement_start"] < D(2025, 3, 1)]
        r = rng("mig")
        idx = r.choice(len(cand), 61, replace=False)
        self.copies = []
        for i in sorted(idx):
            x = dict(cand[int(i)])
            x["account_key"] = ("mig", x["urn"])
            x["account_name"] = x["account_name"].upper().replace("&", "AND")
            x["copy_of"] = id(cand[int(i)])
            x["tag"] = "la-copy"
            self.copies.append(x)
        self.rows.extend(self.copies)

    # ------------------------------------------------------------------ customers the register shows proposed to close
    def closing_schools(self):
        """Maintained and special schools still open but proposed to close: they hold agreements like any other."""
        from world import SELL_TYPES
        e = self.reg.est
        o = e[e["EstablishmentStatus (name)"] == "Open, but proposed to close"].copy()
        gt = dict(zip(self.reg.groups["Group UID"].astype(int), self.reg.groups["Group Type"]))
        sat = o["Trusts (code)"].map(lambda t: not pd.isna(t) and gt.get(int(t)) == "Single-academy trust")
        ok = np.zeros(len(o), bool)
        for grp in ("Local authority maintained schools", "Special schools", "Academies"):
            ok |= (o["EstablishmentTypeGroup (name)"] == grp).values & o["TypeOfEstablishment (name)"].isin(
                SELL_TYPES[grp]).values
        o = o[ok & o["PhaseOfEducation (name)"].isin(["Primary", "Secondary", "All-through", "Middle deemed primary",
                                                       "Middle deemed secondary", "Not applicable"]).values]
        o = o[o["NumberOfPupils"].notna() & (o["NumberOfPupils"] > 0) & (o["Trusts (code)"].isna() | sat.loc[o.index])]
        used = set(x["urn_current"] for x in self.rows)
        o = o[~o["URN"].isin(used)]
        self.closing = []
        for _, a in pick(o, 25, "closing").iterrows():
            kind = {"Special schools": "special", "Academies": "sat"}.get(a["EstablishmentTypeGroup (name)"], "la")
            row = self.plain(a, "closing", (4, 4, 4, 9, 9, 1, 11), kind=kind)
            self.rows.append(row)
            self.closing.append(int(a["URN"]))

    # ------------------------------------------------------------------ framework schools, not in the book
    def framework_schools(self):
        """Schools that buy through the public buying framework hold no Tallybridge agreement; the reseller does."""
        lgr_since = {942: D(2023, 4, 1), 943: D(2023, 4, 1), 940: D(2021, 4, 1), 941: D(2021, 4, 1),
                     838: D(2019, 4, 1), 839: D(2019, 4, 1)}
        f = self.free()
        la = f[f["EstablishmentTypeGroup (name)"] == "Local authority maintained schools"]
        lg = la[la["LA (code)"].isin(lgr_since) & la["PreviousLA (code)"].notna()
                & la["PreviousEstablishmentNumber"].notna()]
        picks = [pick(lg, 24, "fw-lgr"), pick(la[~la["URN"].isin(lg["URN"])], 92, "fw-la")]
        sat = f[f["gtype"] == "Single-academy trust"]
        picks.append(pick(sat, 18, "fw-sat"))
        sp = f[f["EstablishmentTypeGroup (name)"] == "Special schools"]
        picks.append(pick(sp, 9, "fw-sp"))
        f2 = self.free()
        f2 = f2[f2["EstablishmentTypeGroup (name)"] == "Local authority maintained schools"]
        f2 = f2[~f2["URN"].isin(set(x["URN"] for d in picks for _, x in d.iterrows()))]
        lapsed = pick(f2, 13, "fw-lapsed")
        for _, a in lapsed.iterrows():
            urn = int(a["URN"])
            start = D(2023, 9, 1) if rng("fwl", urn).random() < 0.5 else D(2024, 9, 1)
            ts, te = D(2025, 9, 1), D(2026, 8, 31)
            band = band_of(a["PhaseOfEducation (name)"])
            pupils = roles.pupils_billed("fw%d" % urn, int(a["NumberOfPupils"]), ts)
            self.framework.append(dict(urn=urn, dfe_number="%d%04d" % (int(a["LA (code)"]), int(a["EstablishmentNumber"])),
                                       name=a["EstablishmentName"], start=start, term_start=ts, term_end=te, band=band,
                                       pupils=pupils, contract_value=annual_value(band, ts, pupils), kind="school",
                                       lapsed=True))
        for df in picks:
            for _, a in df.iterrows():
                urn = int(a["URN"])
                r = rng("fw", urn)
                code = int(a["LA (code)"])
                if code in lgr_since:
                    start = D(int(r.integers(2016, lgr_since[code].year)), (9, 4)[int(r.integers(0, 2))], 1)
                else:
                    start = rand_start(r, 2019, 2025, (9, 9, 4, 4, 1, 11))
                ts, te = term_for(start, AS_AT)
                band = band_of(a["PhaseOfEducation (name)"])
                pupils = roles.pupils_billed("fw%d" % urn, int(a["NumberOfPupils"]), ts)
                if (code in lgr_since and start < lgr_since[code] and not pd.isna(a["PreviousLA (code)"])
                        and not pd.isna(a["PreviousEstablishmentNumber"])):
                    dfe = "%d%04d" % (int(a["PreviousLA (code)"]), int(a["PreviousEstablishmentNumber"]))
                else:
                    dfe = "%d%04d" % (code, int(a["EstablishmentNumber"]))
                self.framework.append(dict(urn=urn, dfe_number=dfe, name=a["EstablishmentName"], start=start,
                                           term_start=ts, term_end=te, band=band, pupils=pupils,
                                           contract_value=annual_value(band, ts, pupils), kind="school"))

    # ------------------------------------------------------------------ federations on one framework contract
    def framework_federations(self):
        """Federations of maintained schools that buy through the framework on one contract for the whole
        federation. The reseller lists the contract against each school it supplies."""
        from world import SELL_TYPES
        e = self.reg.est
        o = e[(e["EstablishmentStatus (name)"] == "Open") & e["Federations (code)"].notna()].copy()
        used = (set(x["urn_current"] for x in self.rows) | set(f["urn"] for f in self.framework if f.get("urn"))
                | set(int(u) for L in getattr(self, "licences", []) for u in L["academy_urns"]))
        picks = {"Local authority maintained schools": [], "Special schools": []}
        for code, g in o.groupby("Federations (code)"):
            if not 2 <= len(g) <= 3 or g["URN"].isin(used).any() or g["Trusts (code)"].notna().any():
                continue
            if g["NumberOfPupils"].isna().any() or (g["NumberOfPupils"] < 60).any():
                continue
            if g["NumberOfPupils"].max() > 0.6 * g["NumberOfPupils"].sum():
                continue
            grp = set(g["EstablishmentTypeGroup (name)"])
            if len(grp) != 1 or list(grp)[0] not in picks:
                continue
            grp = list(grp)[0]
            if not g["TypeOfEstablishment (name)"].isin(SELL_TYPES[grp]).all():
                continue
            phases = set(g["PhaseOfEducation (name)"])
            if grp == "Local authority maintained schools" and phases != {"Primary"}:
                continue
            if grp == "Special schools" and phases != {"Not applicable"}:
                continue
            picks[grp].append((rng("fed", int(code)).random(), int(code), g))
        self.federations, self.fed_urns = [], set()
        for grp, n in (("Local authority maintained schools", 6), ("Special schools", 1)):
            for _, code, g in sorted(picks[grp])[:n]:
                r = rng("fedc", code)
                start = rand_start(r, 2019, 2025, (4, 4, 1, 11))
                ts, te = term_for(start, AS_AT)
                band = band_of(g["PhaseOfEducation (name)"].iloc[0])
                schools = []
                for _, a in g.sort_values("URN").iterrows():
                    urn = int(a["URN"])
                    schools.append(dict(urn=urn, dfe_number="%d%04d" % (int(a["LA (code)"]), int(a["EstablishmentNumber"])),
                                        name=a["EstablishmentName"], roll=int(a["NumberOfPupils"])))
                    self.fed_urns.add(urn)
                pupils = sum(roles.pupils_billed("fw%d" % s_["urn"], s_["roll"], ts) for s_ in schools)
                f = dict(urn=None, dfe_number=None, name=g["Federations (name)"].iloc[0], start=start, term_start=ts,
                         term_end=te, band=band, pupils=pupils, contract_value=annual_value(band, ts, pupils),
                         kind="federation", schools=schools, fed_code=code, group=grp)
                self.framework.append(f)
                self.federations.append(f)

    def identical_pair(self):
        """Two unrelated framework schools whose contracts carry the same pupils, value and dates."""
        e = self.reg.by_urn
        sch = [f for f in self.framework if f["kind"] == "school" and not f.get("lapsed") and f["band"] == "Primary"
               and e.loc[f["urn"], "EstablishmentTypeGroup (name)"] == "Local authority maintained schools"
               and pd.isna(e.loc[f["urn"], "Federations (code)"]) and f["pupils"] >= 200
               and str(f["dfe_number"]).startswith(str(int(e.loc[f["urn"], "LA (code)"])))]
        sch.sort(key=lambda f: (f["pupils"], f["urn"]))
        best = None
        for a_, b_ in zip(sch, sch[1:]):
            if e.loc[a_["urn"], "LA (code)"] == e.loc[b_["urn"], "LA (code)"]:
                continue
            gap = abs(a_["pupils"] - b_["pupils"]) / a_["pupils"]
            if best is None or gap < best[0]:
                best = (gap, a_, b_)
        _, a_, b_ = best
        for k in ("start", "term_start", "term_end", "pupils", "contract_value"):
            b_[k] = a_[k]
        if D(2026, 7, 1) <= a_["term_start"] <= D(2026, 9, 30):
            raise AssertionError("identical pair invoiced in the quarter")
        self.pair = (a_["urn"], b_["urn"])

    # ------------------------------------------------------------------ the CRM after the billing cutover
    def crm_writeback(self):
        """For the move to the new billing platform the CRM's billing fields were reloaded on 1 May from a snapshot
        taken at the close of 31 March, so an agreement that renewed in April shows its new term's dates with the
        pupils and value of the term before. The trust partnerships team keeps its trusts' records by hand."""
        copied = set(x["copy_of"] for x in self.rows if x.get("copy_of"))
        self.stale = []
        for x in self.rows:
            # off the main call's path: schools outside any trust the round can consider (a trust with one academy
            # on an agreement can never meet the two-academy condition)
            if (x["billing_basis"] != "Per pupil" or x["status"] != "In force" or x.get("copy_of") or x.get("site")
                    or x.get("covers") or id(x) in copied or x["tag"] not in ("la", "sat", "special", "single")
                    or (x.get("uid") is not None and x["tag"] != "single")):
                continue
            ts = x["current_term_start"]
            if not D(2026, 4, 1) <= ts < CUTOVER or x["agreement_start"] >= ts:
                continue
            prev = add_years(ts, -1)
            # rolls moved between the two censuses: primary rolls falling, secondary rolls still rising
            r = rng("roll", x["urn_current"])
            f = r.uniform(1.01, 1.08) if x["price_band"] == "Primary" else r.uniform(0.94, 1.0)
            pupils = int(round(x["pupils_billed"] * f))
            value = annual_value(x["price_band"], prev, pupils)
            if value <= MINIMUM[price_year(prev)] + 25 or x["annual_value_gbp"] <= MINIMUM[price_year(ts)] + 25:
                continue
            if abs(value - x["annual_value_gbp"]) < 1.0:
                continue
            x["stale"] = dict(pupils=pupils, value=value, ts=prev)
            self.stale.append(x)

    # ------------------------------------------------------------------ agreements that ended
    def ended(self):
        f = self.free()
        f = f[f["EstablishmentTypeGroup (name)"].isin(["Local authority maintained schools", "Academies",
                                                         "Free Schools"])]
        self.ended_rows = []
        for _, a in pick(f, 283, "ended").iterrows():
            r = rng("end", int(a["URN"]))
            start = rand_start(r, 2018, 2023, (9, 9, 4, 4, 1, 11))
            if not pd.isna(a["open_d"]) and a["open_d"].date() > start:
                continue
            years = int(r.integers(1, 4))
            end = add_years(start, years)
            if end > D(2026, 8, 31) or end < D(2024, 3, 1):
                end = add_years(start, 2) if add_years(start, 2) <= D(2026, 8, 31) else D(2026, 4, 1)
            if end > D(2026, 8, 31) or end <= start:
                continue
            row = school_row(self.reg, int(a["URN"]), start, ("head", int(a["URN"])),
                             SCHOOL_ROLES[int(r.integers(0, len(SCHOOL_ROLES)))], start, status="Ended", end=end,
                             tag="ended")
            row["end_date"] = end - dt.timedelta(days=1)
            self.rows.append(row)
            self.ended_rows.append(row)

    # ------------------------------------------------------------------ the 2026 pilot's licences
    def pilot_licences(self):
        c = self.c
        self.signed = c.pilot[:7]
        self.declined = c.pilot[7:]
        self.framework_licence = self.signed[3]
        self.licences = []
        for uid in c.pilot:
            a = roles.academy_frame(self.reg, c.op, uid)
            subs = [x for x in self.rows if x.get("uid") == uid]
            lic_pupils = int(a["NumberOfPupils"].sum())
            lic_value = round(RATE * lic_pupils, 2)
            rec = dict(uid=uid, academies=len(a), pupils=lic_pupils, licence_value=lic_value,
                       replaced_n=len(subs), replaced_value=round(sum(x["annual_value_gbp"] for x in subs), 2),
                       academy_urns=list(a["URN"].astype(int)), academy_pupils=list(a["NumberOfPupils"].astype(int)))
            rec["net"] = round(rec["licence_value"] - rec["replaced_value"], 2)
            rec["outcome"] = "Signed" if uid in self.signed else "Declined"
            self.licences.append(rec)
            if uid in self.signed:
                for x in subs:
                    x["status"] = "Replaced by Trust Licence"
                    x["end_date"] = D(2026, 8, 31)
                if uid != self.framework_licence:
                    officer = subs[0]["signer_key"]
                    self.rows.append(dict(account_key=("trust", uid), account_name=self.reg.group_name[uid],
                                          urn=None, dfe_number=None, billing_basis="Trust Licence", price_band=None,
                                          pupils_billed=lic_pupils, agreement_start=LICENCE_START,
                                          current_term_start=LICENCE_START, current_term_end=D(2027, 8, 31),
                                          annual_value_gbp=lic_value, status="In force", signer_key=officer,
                                          signed_by_role=subs[0]["signed_by_role"],
                                          signed_on=D(2026, 7, 1) + dt.timedelta(days=int(rng("sig", uid).integers(0, 40))),
                                          urn_current=None, uid=uid, tag="licence", site=None, pupils_current=lic_pupils,
                                          trust_ch=self.reg.group_ch.get(uid)))
                else:
                    self.framework.append(dict(urn=None, dfe_number=None, name=self.reg.group_name[uid],
                                               start=LICENCE_START, term_start=LICENCE_START,
                                               term_end=D(2027, 8, 31), band=None, pupils=lic_pupils,
                                               contract_value=lic_value, kind="trust licence", uid=uid,
                                               trust_ch=self.reg.group_ch.get(uid)))

    # ------------------------------------------------------------------ the 2023-24 cluster licences
    def cluster_licences(self):
        c = self.c
        self.cluster_rows = []
        for uid, outcome in c.cluster:
            if outcome != "won":
                continue
            subs = [x for x in self.rows if x.get("uid") == uid and x["tag"] == "filler"]
            pupils = sum(x["pupils_billed"] for x in subs)
            value = round(sum(max(x["pupils_billed"] * (4.20 if x["price_band"] == "Primary" else 4.90), 790.0)
                              for x in subs) * 0.90, 2)
            start = D(2023, 9, 1) if rng("cl", uid).random() < 0.6 else D(2024, 1, 1)
            row = dict(account_key=("trust", uid), account_name=self.reg.group_name[uid], urn=None, dfe_number=None,
                       billing_basis="Cluster Licence", price_band=None, pupils_billed=pupils, agreement_start=start,
                       current_term_start=start, current_term_end=D(2024, 8, 31), annual_value_gbp=value,
                       status="Ended", signer_key=subs[0]["signer_key"], signed_by_role=subs[0]["signed_by_role"],
                       signed_on=start - dt.timedelta(days=int(rng("cls", uid).integers(20, 60))), urn_current=None,
                       uid=uid, tag="cluster", site=None, pupils_current=pupils, end_date=D(2024, 8, 31),
                       trust_ch=self.reg.group_ch.get(uid))
            self.rows.append(row)
            self.cluster_rows.append(row)
