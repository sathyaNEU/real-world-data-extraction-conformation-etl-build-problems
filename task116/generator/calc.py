"""The ladder, computed from frames shaped exactly like the shipped files.

Every function here takes the shipped tables (register, links, groups, agreements export, pilot sheet) and
returns what a solver at that rung would file. The golden and the verifier recompute the same figures on their
own code paths; this module is the generator's view, used for tuning and for the assertions.
"""
import datetime as dt
from collections import defaultdict

import numpy as np
import pandas as pd

AS_AT = pd.Timestamp("2026-10-01")
RATE = 4.05
SIGN = 7 / 13
CAP = 10


def successor_map(links, est):
    """Closed URN -> the URN its successor link points to, followed to an open record."""
    st = dict(zip(est["URN"], est["EstablishmentStatus (name)"]))
    s = links[links["LinkType"] == "Successor"].groupby("URN")["LinkURN"].apply(list).to_dict()
    out = {}
    for u in s:
        cur, seen = u, set()
        while st.get(cur) == "Closed" and len(s.get(cur, [])) == 1 and cur not in seen:
            seen.add(cur)
            cur = s[cur][0]
        if cur != u and st.get(cur) == "Open":
            out[u] = cur
    return out


def in_force(book, on=AS_AT):
    b = book[(book["status"] == "In force") & book["urn"].notna()].copy()
    ts = pd.to_datetime(b["term_start"])
    te = pd.to_datetime(b["term_end"])
    b = b[(ts <= on) & (te >= on)].copy()
    b["urn"] = b["urn"].astype(int)
    return b.drop_duplicates("agreement_ref")


def trust_table(est, groups, book, links, *, follow=True, pilot_names=(), basis="net", on=AS_AT, identity="contact",
                cover=None, sign=SIGN):
    est_o = est[est["EstablishmentStatus (name)"] == "Open"]
    mats = groups[(groups["Group Type"] == "Multi-academy trust") & (groups["Group Status"] == "Open")]
    mat_uid = set(mats["Group UID"].astype(int))
    names = dict(zip(mats["Group UID"].astype(int), mats["Group Name"]))
    tcode = dict(zip(est_o["URN"], est_o["Trusts (code)"]))
    pupils = est_o[est_o["Trusts (code)"].isin(mat_uid)].groupby("Trusts (code)")["NumberOfPupils"].sum()
    b = in_force(book, on)
    if follow:
        sm = successor_map(links, est)
        b["cur"] = b["urn"].map(lambda u: sm.get(u, u))
    else:
        b["cur"] = b["urn"]
    b["uid"] = b["cur"].map(lambda u: tcode.get(u))
    b = b[b["uid"].notna()]
    b["uid"] = b["uid"].astype(int)
    b = b[b["uid"].isin(mat_uid)]
    # the academies each agreement covers: its key alone, or every school its invoice bills (cover)
    b["covers"] = [[c] + (list((cover or {}).get(ref, [c]))[1:]) for c, ref in zip(b["cur"], b["agreement_ref"])]
    rows = []
    for uid, grp in b.groupby("uid"):
        nm = names[uid]
        if nm in pilot_names:
            continue
        acad = est_o[est_o["Trusts (code)"] == uid]
        covered = set(u for lst in grp["covers"] for u in lst)
        n_sub = len(covered)
        if n_sub < 2:
            continue
        lic = RATE * float(acad["NumberOfPupils"].sum())
        replaced = float(grp["annual_value_gbp"].sum())
        uncovered_pupils = float(acad[~acad["URN"].isin(covered)]["NumberOfPupils"].sum())
        net = {"net": lic - replaced, "gross": RATE * uncovered_pupils, "licence": lic}[basis]
        # who counts as the same person: the CRM contact (the filed reading), the name as typed, the surname alone,
        # or a reading that admits a trust where one contact signed for most of its academies
        key = {"contact": grp["signed_by_contact_id"], "name": grp["signed_by"],
               "surname": grp["signed_by"].str.split().str[-1]}.get(identity, grp["signed_by_contact_id"])
        signers = key.nunique()
        central = signers == 1
        if identity == "most":
            central = key.value_counts().iloc[0] * 2 > len(grp)
        rows.append(dict(uid=uid, trust=nm, academies=len(acad), subscribing=n_sub, pupils=int(acad["NumberOfPupils"].sum()),
                         licence=round(lic, 2), replaced=round(replaced, 2), value=round(net, 2),
                         planned=int(round(net * sign)), signers=signers,
                         mode="central" if central else "devolved"))
    t = pd.DataFrame(rows)
    return t.sort_values(["planned", "trust"], ascending=[False, True]).reset_index(drop=True)


def slate(t, central_only):
    s = t[t["mode"] == "central"] if central_only else t
    s = s.head(CAP)
    return list(s["trust"]), int(s["planned"].sum())


def ladder(est, groups, book, links, pilot_names, cover=None):
    """Every rung counts academies by the agreement's key, except the answer, which counts what the invoices bill."""
    out = {}
    for name, follow, basis, central in [("R0 licence fee, recorded URN", False, "licence", False),
                                         ("gross, recorded URN", False, "gross", False),
                                         ("R1 net, recorded URN", False, "net", False),
                                         ("R2 net, successors", True, "net", False),
                                         ("R3 signing condition, academies by the agreement's key", True, "net", True),
                                         ("gross, successors", True, "gross", False),
                                         ("central, gross, recorded", False, "gross", True),
                                         ("central, net, recorded", False, "net", True),
                                         ("central, gross, successors", True, "gross", True),
                                         ("licence fee, successors", True, "licence", False),
                                         ("central, licence fee, successors", True, "licence", True)]:
        t = trust_table(est, groups, book, links, follow=follow, pilot_names=pilot_names, basis=basis)
        sl, total = slate(t, central)
        out[name] = dict(slate=sl, total=total, table=t)
    t = trust_table(est, groups, book, links, follow=True, pilot_names=pilot_names, basis="net", cover=cover)
    sl, total = slate(t, True)
    out["R4 answer"] = dict(slate=sl, total=total, table=t)
    # the answer's construction at the pilot's own rate, 7 of 12, read off the pilot sheet
    t = trust_table(est, groups, book, links, follow=True, pilot_names=pilot_names, basis="net", cover=cover,
                    sign=7 / 12)
    sl, total = slate(t, True)
    out["sign rate of the pilot's twelve offers"] = dict(slate=sl, total=total, table=t)
    t = trust_table(est, groups, book, links, follow=True, pilot_names=pilot_names, basis="net", sign=7 / 12)
    sl, total = slate(t, True)
    out["R3 at the pilot's rate"] = dict(slate=sl, total=total, table=t)
    for name, ident in [("people counted by name as typed", "name"), ("people counted by surname", "surname"),
                        ("one contact signed for most academies", "most")]:
        t = trust_table(est, groups, book, links, follow=True, pilot_names=pilot_names, basis="net", identity=ident,
                        cover=cover)
        sl, total = slate(t, True)
        out[name] = dict(slate=sl, total=total, table=t)
    return out


def pilot_replication(est, groups, book, links, pilot, *, follow, basis):
    """Each pilot trust's net new recurring revenue as the rung would compute it at the June pricing."""
    est_o = est[est["EstablishmentStatus (name)"] == "Open"]
    names = dict(zip(groups["Group UID"].astype(int), groups["Group Name"]))
    uid_of = {v: k for k, v in names.items()}
    tcode = dict(zip(est_o["URN"], est_o["Trusts (code)"]))
    b = book[book["urn"].notna() & book["status"].isin(["In force", "Replaced by Trust Licence"])].copy()
    ts = pd.to_datetime(b["term_start"])
    te = pd.to_datetime(b["term_end"])
    on = pd.Timestamp("2026-06-15")
    # an agreement in force at the June pricing: its current term, or the term before it, covered 15 June
    b["urn"] = b["urn"].astype(int)
    b = b.drop_duplicates("agreement_ref")
    if follow:
        sm = successor_map(links, est)
        b["cur"] = b["urn"].map(lambda u: sm.get(u, u))
    else:
        b["cur"] = b["urn"]
    b["uid"] = b["cur"].map(lambda u: tcode.get(u))
    res = {}
    for _, p in pilot.iterrows():
        uid = uid_of[p["trust"]]
        acad = est_o[est_o["Trusts (code)"] == uid]
        grp = b[b["uid"] == uid]
        lic = RATE * float(acad["NumberOfPupils"].sum())
        if basis == "net":
            v = lic - float(grp["annual_value_gbp"].sum())
        elif basis == "licence":
            v = lic
        else:
            v = RATE * float(acad[~acad["URN"].isin(set(grp["cur"]))]["NumberOfPupils"].sum())
        res[p["trust"]] = round(v, 2)
    return res
