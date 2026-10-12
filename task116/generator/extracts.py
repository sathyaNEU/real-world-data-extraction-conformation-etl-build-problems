"""The operating extracts around the book: CRM opportunity history, billing ledger, reseller remittance, usage."""
import datetime as dt
import string

import numpy as np
import pandas as pd

import roles
from book import avoid_window, group_value, rand_start
from world import (AS_AT, CUTOVER, LICENCE_START, RATE, add_years, annual_value, band_of, rng, term_for, TERM_WEEK0)

D = dt.date
LOST_NEW = ["Budget", "Budget", "Chose a competitor", "Chose a competitor", "No decision", "Timing", "Other"]
LOST_RENEW = ["Budget", "Low usage", "Chose a competitor", "Timing", "No decision", "Other"]
VAT = 0.20
OWNERS = ["Leah O'Neill", "Joel Bailey", "Philip Saunders"]


def opp_id(*key):
    r = rng("opp", *key)
    alpha = string.ascii_uppercase + string.ascii_lowercase + string.digits
    return "0064K00" + "".join(alpha[i] for i in r.integers(0, len(alpha), 11))


def value_at(x, ts):
    """An agreement's annual value for the term starting `ts`, billed on the pupils published then."""
    if x["billing_basis"] != "Per pupil" or ts == x["current_term_start"]:
        return x["annual_value_gbp"]
    if x.get("stale") and ts == x["stale"]["ts"]:
        return x["stale"]["value"]
    if x.get("covers"):
        return group_value(x, ts)
    billed = roles.pupils_billed(x["urn_current"] if x["site"] is None else "%s/%s" % (x["urn_current"], x["site"]),
                                 x["pupils_current"] if x["site"] is None else x["pupils_current"], ts)
    return annual_value(x["price_band"], ts, billed)


# ---------------------------------------------------------------------- CRM opportunities
def crm(reg, A):
    rows = []
    agreements = [x for x in A.rows if not x.get("copy_of") and x["billing_basis"] == "Per pupil"]
    for x in agreements:
        start = x["agreement_start"]
        r = rng("crm", x["agreement_ref"])
        created = start - dt.timedelta(days=int(r.integers(25, 120)))
        rows.append(dict(opportunity_id=opp_id(x["agreement_ref"], "new"), account_id=x["account_id"],
                         account_name=x["account_name"], account_type="School", urn=x["urn"],
                         companies_house_no=None, opportunity_type="New business",
                         lead_source=["Inbound", "Inbound", "Outbound", "Event", "Referral"][int(r.integers(0, 5))],
                         stage="Closed Won", created_date=created,
                         close_date=start - dt.timedelta(days=int(r.integers(3, 20))),
                         amount_gbp=value_at(x, start), lost_reason=None,
                         owner=OWNERS[int(r.integers(0, 3))]))
        k = 1
        end = x.get("end_date")
        while True:
            ts = add_years(start, k)
            if ts > AS_AT:
                break
            if end is not None and ts > end:
                rows.append(dict(opportunity_id=opp_id(x["agreement_ref"], "ren", k), account_id=x["account_id"],
                                 account_name=x["account_name"], account_type="School", urn=x["urn"],
                                 companies_house_no=None, opportunity_type="Renewal", lead_source="Existing customer",
                                 stage="Closed Lost", created_date=ts - dt.timedelta(days=75),
                                 close_date=ts - dt.timedelta(days=int(r.integers(1, 30))),
                                 amount_gbp=value_at(x, ts),
                                 lost_reason=LOST_RENEW[int(r.integers(0, len(LOST_RENEW)))],
                                 owner=OWNERS[int(r.integers(0, 3))]))
                break
            if x["status"] == "Replaced by Trust Licence" and ts >= LICENCE_START:
                break
            rows.append(dict(opportunity_id=opp_id(x["agreement_ref"], "ren", k), account_id=x["account_id"],
                             account_name=x["account_name"], account_type="School", urn=x["urn"],
                             companies_house_no=None, opportunity_type="Renewal", lead_source="Existing customer",
                             stage="Closed Won", created_date=ts - dt.timedelta(days=75),
                             close_date=ts - dt.timedelta(days=int(r.integers(1, 20))), amount_gbp=value_at(x, ts),
                             lost_reason=None, owner=OWNERS[int(r.integers(0, 3))]))
            k += 1
    # schools that looked and did not buy
    held = (set(x["urn_current"] for x in A.rows if x.get("urn_current")) | set(f["urn"] for f in A.framework if f["urn"])
            | set(getattr(A, "fed_urns", set())))
    pool = reg.open_state()
    pool = pool[~pool["URN"].isin(held)]
    h = pool["URN"].map(lambda u: rng("lostpick", int(u)).random())
    for _, s in pool.assign(_h=h).sort_values("_h").head(3150).iterrows():
        urn = int(s["URN"])
        r = rng("lost", urn)
        created = D(2022, 1, 10) + dt.timedelta(days=int(r.integers(0, 1700)))
        close = created + dt.timedelta(days=int(r.integers(20, 150)))
        band = band_of(s["PhaseOfEducation (name)"])
        amt = annual_value(band, close, int(s["NumberOfPupils"]))
        stage, reason = "Closed Lost", LOST_NEW[int(r.integers(0, len(LOST_NEW)))]
        if close > AS_AT:
            stage, reason = "Open", None
        rows.append(dict(opportunity_id=opp_id("lost", urn), account_id=None, account_name=s["EstablishmentName"],
                         account_type="School", urn=urn, companies_house_no=None, opportunity_type="New business",
                         lead_source=["Inbound", "Outbound", "Outbound", "Event", "Webinar"][int(r.integers(0, 5))],
                         stage=stage, created_date=created, close_date=close, amount_gbp=amt, lost_reason=reason,
                         owner=OWNERS[int(r.integers(0, 3))]))
    # trust-level offers: the 2023-24 cluster licence and the 2026 pilot
    c = A.c
    for uid, outcome in c.cluster:
        r = rng("clopp", uid)
        created = D(2023, 9, 4) + dt.timedelta(days=int(r.integers(0, 170)))
        close = created + dt.timedelta(days=int(r.integers(30, 120)))
        subs = [x for x in A.rows if x.get("uid") == uid and x["billing_basis"] == "Per pupil"]
        amt = round(sum(max(x["pupils_billed"] * (4.20 if x["price_band"] == "Primary" else 4.90), 790.0)
                        for x in subs) * 0.90, 2)
        if outcome == "won":
            cl = [z for z in A.cluster_rows if z["uid"] == uid][0]
            close = cl["signed_on"]
            created = close - dt.timedelta(days=int(r.integers(30, 80)))
            amt = cl["annual_value_gbp"]
        reason = None
        if outcome == "lost":
            reason = (["No decision", "No decision", "No decision", "Budget", "Timing"] if c.mode[uid] == "devolved"
                      else ["Budget", "Timing", "Chose a competitor", "No decision"])[int(r.integers(0, 4))]
        rows.append(dict(opportunity_id=opp_id("cluster", uid), account_id=None,
                         account_name=reg.group_name[uid], account_type="Trust", urn=None,
                         companies_house_no=reg.group_ch.get(uid), opportunity_type="Cluster Licence",
                         lead_source="Outbound", stage="Closed Won" if outcome == "won" else "Closed Lost",
                         created_date=created, close_date=close, amount_gbp=amt, lost_reason=reason,
                         owner=["Philip Saunders", "Leah O'Neill"][int(r.integers(0, 2))]))
    for L in A.licences:
        uid = L["uid"]
        r = rng("pilotopp", uid)
        created = D(2026, 2, 2) + dt.timedelta(days=int(r.integers(0, 80)))
        close = D(2026, 6, 22) + dt.timedelta(days=int(r.integers(0, 50)))
        rows.append(dict(opportunity_id=opp_id("pilot", uid), account_id=None, account_name=reg.group_name[uid],
                         account_type="Trust", urn=None, companies_house_no=reg.group_ch.get(uid),
                         opportunity_type="Trust Licence", lead_source="Inbound",
                         stage="Closed Won" if L["outcome"] == "Signed" else "Closed Lost", created_date=created,
                         close_date=close, amount_gbp=L["licence_value"],
                         lost_reason=None if L["outcome"] == "Signed" else ["Budget", "Timing", "No decision"][
                             int(r.integers(0, 3))], owner=["Leah O'Neill", "Joel Bailey"][int(r.integers(0, 2))]))
    # an inbound request after the pilot, offered the licence in September and declined
    u = c.offcycle
    r = rng("offcycleopp", u)
    pupils = float(reg.trust_academies(u)["NumberOfPupils"].fillna(0).sum())
    rows.append(dict(opportunity_id=opp_id("offcycle", u), account_id=None, account_name=reg.group_name[u],
                     account_type="Trust", urn=None, companies_house_no=reg.group_ch.get(u),
                     opportunity_type="Trust Licence", lead_source="Inbound", stage="Closed Lost",
                     created_date=D(2026, 9, 1) + dt.timedelta(days=int(r.integers(0, 10))), close_date=D(2026, 9, 30),
                     amount_gbp=round(RATE * pupils, 2), lost_reason="No decision", owner="Joel Bailey"))
    df = pd.DataFrame(rows)
    df["urn"] = df["urn"].astype("Int64")
    for col in ["created_date", "close_date"]:
        df[col] = pd.to_datetime(df[col]).dt.strftime("%Y-%m-%d")
    return df.sort_values(["created_date", "opportunity_id"]).reset_index(drop=True)


# ---------------------------------------------------------------------- billing ledger
LEDGER_FROM, LEDGER_TO = D(2025, 4, 1), D(2026, 9, 30)


class Ledger:
    def __init__(self):
        self.rows = []
        self.n_legacy, self.n_inv, self.n_cn = 404118, 2011903, 2004417

    def doc(self, kind, when, legacy):
        r = rng("docno", kind, when.isoformat(), len(self.rows))
        if legacy:
            self.n_legacy += 1 + int(r.integers(0, 3))
            return "L%06d" % self.n_legacy
        if kind == "Invoice":
            self.n_inv += 1 + int(r.integers(0, 2))
            return "INV-%07d" % self.n_inv
        self.n_cn += 1 + int(r.integers(0, 2))
        return "CN-%07d" % self.n_cn

    def add(self, kind, when, x_account_id, x_account_name, ref, value, description, reference=None, legacy=None):
        legacy = (when < CUTOVER) if legacy is None else legacy
        no = self.doc(kind, when, legacy)
        sign = -1 if kind == "Credit note" else 1
        if legacy:
            # the old system holds the amount with VAT in it, and the VAT within that amount in its own field
            amount = round(sign * value * (1 + VAT), 2)
            vat = round(sign * value * VAT, 2)
        else:
            amount, vat = round(sign * value, 2), round(sign * value * VAT, 2)
        # the old system's credit notes are raised by hand against an invoice and carry no agreement reference
        self.rows.append(dict(document_no=no, document_type=kind, document_date=when, account_id=x_account_id,
                              account_name=x_account_name,
                              agreement_ref=None if (legacy and kind == "Credit note") else ref,
                              reference=reference, description=description, amount_gbp=amount, vat_gbp=vat))
        return no


def credit_text(no):
    return ("Credit against %s" if no.startswith("L") else "Credit note for %s") % no


def billed_names(reg, x):
    """The schools an invoice bills: the account's school, or every school a group agreement covers."""
    if x.get("covers"):
        return "; ".join(reg.info[int(s)]["EstablishmentName"] for s in x["covers"])
    return x["account_name"]


def ledger(reg, A):
    L = Ledger()
    term_invoice = {}
    agreements = [x for x in A.rows if not x.get("copy_of") and x["billing_basis"] == "Per pupil"]
    for x in sorted(agreements, key=lambda z: (z["agreement_start"], z["agreement_ref"])):
        start = x["agreement_start"]
        end = x.get("end_date")
        k = 0
        while True:
            ts = add_years(start, k)
            k += 1
            if ts > LEDGER_TO:
                break
            if end is not None and ts > end:
                break
            if x["status"] == "Replaced by Trust Licence" and ts >= LICENCE_START:
                break
            if ts < LEDGER_FROM:
                continue
            when = ts + dt.timedelta(days=int(rng("invday", x["agreement_ref"], k).integers(0, 4)))
            te = add_years(ts, 1) - dt.timedelta(days=1)
            desc = "Tallybridge Maths subscription %s to %s: %s" % (ts.strftime("%d/%m/%Y"), te.strftime("%d/%m/%Y"),
                                                                billed_names(reg, x))
            no = L.add("Invoice", when, x["account_id"], x["account_name"], x["agreement_ref"], value_at(x, ts), desc)
            term_invoice[(x["agreement_ref"], ts)] = (no, when < CUTOVER, value_at(x, ts))
    # the pilot licences, one invoice voided and raised again
    lic_rows = {x["uid"]: x for x in A.rows if x["billing_basis"] == "Trust Licence"}
    direct_signed = [u for u in A.signed if u != A.framework_licence]
    A.void_uid = direct_signed[1]
    for uid in direct_signed:
        lic = lic_rows[uid]
        desc = "Tallybridge Trust Licence 01/09/2026 to 31/08/2027"
        if uid == A.void_uid:
            wrong = round(lic["annual_value_gbp"] * 1.0437, 2)
            first = L.add("Invoice", D(2026, 9, 1), lic["account_id"], lic["account_name"], lic["agreement_ref"],
                          wrong, desc, legacy=False)
            L.add("Credit note", D(2026, 9, 8), lic["account_id"], lic["account_name"], lic["agreement_ref"], wrong,
                  "Cancels %s: pupil numbers taken from the January 2025 census" % first, reference=first,
                  legacy=False)
            L.add("Invoice", D(2026, 9, 8), lic["account_id"], lic["account_name"], lic["agreement_ref"],
                  lic["annual_value_gbp"], desc, legacy=False)
        else:
            L.add("Invoice", D(2026, 9, 1), lic["account_id"], lic["account_name"], lic["agreement_ref"],
                  lic["annual_value_gbp"], desc, legacy=False)
    # pupil-number corrections raised in May and June against the current term of an agreement each licence later
    # replaced, months before any licence was decided
    A.same_term_corrections = {}
    for uid in A.signed:
        reps = sorted([x for x in A.rows if x.get("uid") == uid and x["status"] == "Replaced by Trust Licence"
                       and x["current_term_end"] > D(2026, 8, 31) and x["current_term_start"] <= D(2026, 6, 1)],
                      key=lambda z: (z["current_term_start"] >= CUTOVER, z["agreement_ref"]))
        if not reps:
            continue
        r = rng("sametermcorr", uid)
        old_sys = [x for x in reps if x["current_term_start"] < CUTOVER]
        pool = old_sys or reps
        x = pool[int(r.integers(0, len(pool)))]
        no, legacy, value = term_invoice[(x["agreement_ref"], x["current_term_start"])]
        amt = round(value * float(r.uniform(0.03, 0.08)), 2)
        lo = max(D(2026, 5, 11), x["current_term_start"] + dt.timedelta(days=9))
        when = lo + dt.timedelta(days=int(r.integers(0, max(1, (D(2026, 6, 20) - lo).days))))
        L.add("Credit note", when, x["account_id"], x["account_name"], x["agreement_ref"], amt,
              credit_text(no), reference=no, legacy=legacy)
        A.same_term_corrections[x["agreement_ref"]] = amt
    # credits for the unexpired part of every agreement a licence replaced
    A.replacement_credits = []
    for x in A.rows:
        if x["status"] != "Replaced by Trust Licence":
            continue
        ts, te = x["current_term_start"], x["current_term_end"]
        if te <= D(2026, 8, 31):
            continue
        days = (te - ts).days + 1
        left = (te - D(2026, 8, 31)).days
        billed = x["annual_value_gbp"] - A.same_term_corrections.get(x["agreement_ref"], 0.0)
        credit = round(billed * left / days, 2)
        no, legacy, _ = term_invoice[(x["agreement_ref"], ts)]
        when = D(2026, 9, 14) + dt.timedelta(days=int(rng("cr", x["agreement_ref"]).integers(0, 6)))
        cn = L.add("Credit note", when, x["account_id"], x["account_name"], x["agreement_ref"], credit,
                   credit_text(no), reference=no, legacy=legacy)
        A.replacement_credits.append(dict(uid=x["uid"], agreement_ref=x["agreement_ref"], credit=credit,
                                          legacy=legacy, document_no=cn))
    # pupil-number corrections to an earlier term's invoice on some of the agreements a licence later replaced
    A.prior_corrections = []
    rep = sorted([x for x in A.rows if x["status"] == "Replaced by Trust Licence"],
                 key=lambda z: z["agreement_ref"])
    prior = [(x, k) for x in rep for k in term_invoice
             if k[0] == x["agreement_ref"] and k[1] < x["current_term_start"]]
    r = rng("priorcorr")
    for i in sorted(r.choice(len(prior), min(5, len(prior)), replace=False)):
        x, (ref, ts) = prior[int(i)]
        no, legacy, value = term_invoice[(ref, ts)]
        amt = round(value * float(r.uniform(0.03, 0.08)), 2)
        when = ts + dt.timedelta(days=int(r.integers(25, 60)))
        cn = L.add("Credit note", when, x["account_id"], x["account_name"], ref, amt,
                   credit_text(no), reference=no, legacy=legacy)
        A.prior_corrections.append(dict(uid=x["uid"], agreement_ref=ref, credit=amt, legacy=legacy, document_no=cn))
    # ordinary corrections through the year
    pool = [k for k in term_invoice if k[1] >= D(2025, 6, 1) and add_years(k[1], 1) <= AS_AT]
    r = rng("corrections")
    for i in r.choice(len(pool), 27, replace=False):
        ref, ts = pool[int(i)]
        no, legacy, value = term_invoice[(ref, ts)]
        x = next(z for z in agreements if z["agreement_ref"] == ref)
        if x["uid"] in A.signed:
            continue
        amt = round(value * float(r.uniform(0.02, 0.09)), 2)
        when = ts + dt.timedelta(days=int(r.integers(20, 70)))
        if when > LEDGER_TO:
            continue
        L.add("Credit note", when, x["account_id"], x["account_name"], ref, amt,
              credit_text(no), reference=no, legacy=legacy)
    df = pd.DataFrame(L.rows)
    df["document_date"] = pd.to_datetime(df["document_date"]).dt.strftime("%Y-%m-%d")
    return df.sort_values(["document_date", "document_no"]).reset_index(drop=True)


# ---------------------------------------------------------------------- reseller remittance
def remittance(reg, A):
    rows, crefs = [], set()
    for f in sorted(A.framework, key=lambda z: (z["kind"], z["name"])):
        ts, te = f["term_start"], f["term_end"]
        invoiced = f["contract_value"] if D(2026, 7, 1) <= ts <= D(2026, 9, 30) else 0.0
        margin = round(invoiced * 0.12, 2)
        sites = f["schools"] if f["kind"] == "federation" else [dict(dfe_number=f["dfe_number"], name=f["name"],
                                                                     urn=f.get("urn"))]
        if f["kind"] == "federation" and invoiced:
            raise AssertionError("a federation contract invoiced in the quarter")
        while True:
            cref = "OFC-%06d" % int(rng("cref", f["name"], f.get("urn"), len(crefs)).integers(100000, 999999))
            if cref not in crefs:
                crefs.add(cref)
                break
        for site in sites:
            r = rng("rref", site["name"], site.get("urn"))
            rows.append(dict(reseller_ref="OES-%05d" % int(r.integers(10000, 99999)), contract_ref=cref,
                             dfe_number=site["dfe_number"],
                             establishment_name=site["name"], companies_house_no=f.get("trust_ch"),
                             contract_start=ts, contract_end=te, pupils=f["pupils"],
                             annual_contract_value_gbp=f["contract_value"], invoiced_in_quarter_gbp=round(invoiced, 2),
                             reseller_margin_pct=12.0, reseller_margin_gbp=margin,
                             remitted_gbp=round(invoiced - margin, 2)))
    df = pd.DataFrame(rows).sort_values(["establishment_name", "reseller_ref"]).reset_index(drop=True)
    for col in ["contract_start", "contract_end"]:
        df[col] = pd.to_datetime(df[col]).dt.strftime("%d/%m/%Y")
    tot = dict(reseller_ref="TOTAL", contract_ref=None, dfe_number=None, establishment_name="%d lines" % len(df),
               companies_house_no=None, contract_start=None, contract_end=None, pupils=int(df["pupils"].sum()),
               annual_contract_value_gbp=round(df["annual_contract_value_gbp"].sum(), 2),
               invoiced_in_quarter_gbp=round(df["invoiced_in_quarter_gbp"].sum(), 2), reseller_margin_pct=None,
               reseller_margin_gbp=round(df["reseller_margin_gbp"].sum(), 2), remitted_gbp=round(df["remitted_gbp"].sum(), 2))
    return pd.concat([df, pd.DataFrame([tot])], ignore_index=True)


# ---------------------------------------------------------------------- weekly usage
HOLIDAY = {D(2025, 10, 27): 0.14, D(2025, 12, 22): 0.05, D(2025, 12, 29): 0.04, D(2026, 2, 16): 0.15,
           D(2026, 3, 30): 0.08, D(2026, 4, 6): 0.07, D(2026, 5, 25): 0.15}


def season(week):
    if week in HOLIDAY:
        return HOLIDAY[week]
    if D(2026, 7, 20) <= week <= D(2026, 8, 31):
        return 0.03 if week < D(2026, 8, 31) else 0.10
    if D(2025, 7, 21) <= week <= D(2025, 9, 1):
        return 0.03
    if week == D(2026, 9, 7) or week == D(2025, 9, 8):
        return 0.74
    if week == D(2026, 9, 14) or week == D(2025, 9, 15):
        return 0.91
    return 1.0


def usage(reg, A):
    weeks = [D(2025, 9, 1) + dt.timedelta(days=7 * i) for i in range(59)]
    gor = {u: v["GOR (name)"] for u, v in reg.info.items()}
    schools = []   # (school_ref, urn on the platform, current urn, pupils billed, start, end, licence trust)
    sref = {}

    taken = set()

    def ref_for(key):
        if key not in sref:
            salt = 0
            while True:
                r = rng("sref", *[str(k) for k in key], *(["again", salt] if salt else []))
                ref = "TBS-%06d" % int(r.integers(100000, 999999))
                if ref not in taken:
                    break
                salt += 1
            taken.add(ref)
            sref[key] = ref
        return sref[key]

    direct = [x for x in A.rows if not x.get("copy_of") and x["billing_basis"] == "Per pupil"]
    # schools that have not used the platform since the summer: no pupil has answered a question this term
    quiet = set()
    for x in direct:
        if (x["tag"] in ("la", "sat", "special") and x["status"] == "In force" and x["agreement_start"] < D(2026, 3, 1)
                and rng("quiet", x["urn_current"]).random() < 0.055):
            quiet.add(x["urn_current"])
    A.quiet_schools = quiet
    replaced_urn = {}
    for x in direct:
        key = ("school", x["urn"], x["site"])
        end = x.get("end_date") or D(2027, 12, 31)
        if x["urn_current"] in quiet:
            end = min(end, D(2026, 7, 19))
        # a group agreement's schools share the lead school's platform record, so its pupils report there
        schools.append((ref_for(key), x["urn"], x["urn_current"], x["pupils_billed"], x["agreement_start"], end, None))
        if x["status"] == "Replaced by Trust Licence":
            replaced_urn[x["urn_current"]] = (x["urn"], ref_for(key))
    for f in A.framework:
        if f["kind"] == "federation":
            for site in f["schools"]:
                schools.append((ref_for(("fw", site["urn"])), site["urn"], site["urn"],
                                roles.pupils_billed("fw%d" % site["urn"], site["roll"], f["term_start"]), f["start"],
                                D(2027, 12, 31), None))
            continue
        if f["kind"] != "school":
            continue
        end = f["term_end"] if f.get("lapsed") else D(2027, 12, 31)
        schools.append((ref_for(("fw", f["urn"])), f["urn"], f["urn"], f["pupils"], f["start"], end, None))
    lic_school = []
    for L in A.licences:
        if L["outcome"] != "Signed":
            continue
        for urn, pup in zip(L["academy_urns"], L["academy_pupils"]):
            plat_urn, ref = replaced_urn.get(urn, (urn, None))
            if ref is None:
                ref = ref_for(("lic", urn))
            lic_school.append((ref, plat_urn, urn, pup, LICENCE_START, D(2027, 12, 31), L["uid"]))
    rows = []
    for ref, purn, curn, pupils, start, end, lic in schools + lic_school:
        r = rng("eng", ref)
        band = band_of(reg.info[curn]["PhaseOfEducation (name)"])
        typ = reg.info[curn]["EstablishmentTypeGroup (name)"]
        base = {"Primary": 0.63, "Secondary": 0.37}[band] * (0.85 if typ == "Special schools" else 1.0)
        eng = min(0.96, base * float(r.uniform(0.62, 1.32)))
        for w in weeks:
            if w + dt.timedelta(days=6) < start or w > end:
                continue
            if lic is None and w >= LICENCE_START - dt.timedelta(days=1) and curn in replaced_urn:
                continue
            noise = float(r.normal(1.0, 0.05))
            act = int(round(pupils * eng * season(w) * max(0.7, noise)))
            if act <= 0:
                continue
            label = w
            if lic is not None:
                label = w - dt.timedelta(days=1)
            rows.append(dict(school_ref=ref, urn=purn, week_start=label, active_pupils=act,
                             batch_id="UXW-%d-%02d" % w.isocalendar()[:2],
                             loaded_at=dt.datetime(w.year, w.month, w.day, 6, 10) + dt.timedelta(days=8, minutes=int(r.integers(0, 40))),
                             _gor=gor.get(curn), _cur=curn, _lic=lic))
    df = pd.DataFrame(rows)
    # settle tweaks: a few more active pupils for one school in a group, in the week beginning 28 September
    tweak = getattr(A, "usage_tweak", {})
    if tweak:
        on = set(getattr(A, "on_tallybridge", set()))
        for (typ, bnd), add in sorted(tweak.items()):
            cand = df[(df["week_start"].isin([D(2026, 9, 28), D(2026, 9, 27)])) & df["_cur"].isin(on)]
            cand = cand[cand["_cur"].map(lambda u: reg.info[u]["EstablishmentTypeGroup (name)"] == typ
                                         and band_of(reg.info[u]["PhaseOfEducation (name)"]) == bnd)]
            i = cand.sort_values("school_ref").index[0]
            df.loc[i, "active_pupils"] += add
    # the week beginning 21 September 2026: part of the South West's load was cut short, and those schools were
    # re-sent in full under a second batch on 2 October
    w = D(2026, 9, 21)
    sw = df[(df["week_start"] == w) & (df["_gor"] == "South West")].sort_values("school_ref")
    r = rng("resend")
    take = r.random(len(sw)) < 0.55
    rs = sw[take].copy()
    short = r.random(len(rs)) < 0.7
    keep = np.maximum(1, np.round(rs["active_pupils"].values * r.uniform(0.45, 0.8, len(rs)))).astype(int)
    df.loc[rs.index, "active_pupils"] = np.where(short, keep, rs["active_pupils"].values)
    rs["batch_id"] = "UXW-2026-39-R1"
    rs["loaded_at"] = dt.datetime(2026, 10, 2, 14, 37)
    A.resend = dict(rows=len(rs), short=int(short.sum()), region_rows=len(sw))
    df = pd.concat([df, rs], ignore_index=True)
    A.usage_internal = df
    out = df.drop(columns=["_gor", "_cur", "_lic"]).copy()
    out["urn"] = out["urn"].astype("Int64")
    out["week_start"] = pd.to_datetime(out["week_start"])
    out = out.sort_values(["week_start", "school_ref", "loaded_at"]).reset_index(drop=True)
    return out
