"""Every graded figure, computed from the shipped files in target/ and nothing else."""
import datetime as dt
import json
import re
from pathlib import Path

import numpy as np
import pandas as pd

RATE = 4.05
AS_AT = pd.Timestamp("2026-10-01")
WEEK0 = pd.Timestamp("2026-09-07")
LICENCE_START = pd.Timestamp("2026-09-01")
# the price list: terms starting on or after 1 April 2026 at 2026-27 prices, earlier terms at 2025-26 prices
PRICE = {("2025-26", "Primary"): 4.40, ("2025-26", "Secondary"): 5.10,
         ("2026-27", "Primary"): 4.60, ("2026-27", "Secondary"): 5.30}
PRICE_FROM = pd.Timestamp("2026-04-01")
TYPES = ["Academies", "Free Schools", "Local authority maintained schools", "Special schools"]
BANDS = ["Primary", "Secondary"]


def load(T):
    T = Path(T)
    est = pd.read_csv(T / "edubasealldata20261007.csv", encoding="latin-1", low_memory=False)
    links = pd.read_csv(T / "links_edubasealldata20261007.csv", encoding="latin-1", low_memory=False)
    groups = pd.read_csv(T / "allgroupsdata20261007.csv", encoding="latin-1", low_memory=False,
                         dtype={"Companies House Number": str})
    book = pd.read_csv(T / "tb_agreements_2026-10-01.csv", dtype={"companies_house_no": str, "dfe_number": str,
                                                                    "signed_by_contact_id": str})
    crm = pd.read_csv(T / "tb_crm_opportunities_2022-2026.csv", dtype={"companies_house_no": str}, low_memory=False)
    ledger = pd.read_csv(T / "tb_billing_ledger_2025-04_2026-09.csv")
    remit = pd.read_csv(T / "orrin_remittance_2026Q3.csv", dtype={"dfe_number": str, "companies_house_no": str})
    usage = pd.read_parquet(T / "tb_weekly_usage_2025-09_2026-10.parquet")
    offers = pd.read_excel(T / "trust_licence_pilot_2026.xlsx", sheet_name="Offers", dtype={"Companies House no.": str})
    sched = pd.read_excel(T / "trust_licence_pilot_2026.xlsx", sheet_name="Schedules")
    return dict(est=est, links=links, groups=groups, book=book, crm=crm, ledger=ledger, remit=remit, usage=usage,
                offers=offers, sched=sched)


def successor_map(links, est):
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


def band_of(phase):
    return "Primary" if phase in ("Primary", "Middle deemed primary") else "Secondary"


def ex_vat(doc_no, amount, vat):
    """The old system (L numbers) holds a document's amount with VAT in it and the VAT within it in vat_gbp; the new
    platform holds the amount net with the VAT beside it."""
    return round(amount - vat, 2) if str(doc_no).startswith("L") else amount


def term_invoices(led, refs, vat_as_net=False):
    """(agreement_ref, term start) -> the invoice for that term, net of VAT. vat_as_net is the wrong reading that takes
    every amount with a VAT field beside it as net, the new platform's way."""
    inv = led[(led["document_type"] == "Invoice") & led["agreement_ref"].isin(refs)].copy()
    inv["ts"] = inv["description"].map(term_start_of)
    inv["net"] = [a if vat_as_net else ex_vat(n, a, v) for n, a, v in zip(inv["document_no"], inv["amount_gbp"], inv["vat_gbp"])]
    return {(r, t): n for r, t, n in zip(inv["agreement_ref"], inv["ts"], inv["net"])}


def in_force(book):
    b = book[(book["status"] == "In force")].copy()
    ts, te = pd.to_datetime(b["term_start"]), pd.to_datetime(b["term_end"])
    return b[(ts <= AS_AT) & (te >= AS_AT)].drop_duplicates("agreement_ref")


def coverage(d):
    """Agreement ref -> current URNs of every school the agreement's current-term invoice bills, the lead first.
    The export keys an agreement to the school whose account it sits on; a group agreement's invoice names each
    school it covers, matched by name to the open academies of the lead school's trust."""
    est, links, book, led = d["est"], d["links"], d["book"], d["ledger"]
    sm = successor_map(links, est)
    eo = est[est["EstablishmentStatus (name)"] == "Open"]
    tcode = dict(zip(eo["URN"], eo["Trusts (code)"]))
    by_name = {(t, n): int(u) for u, t, n in zip(eo["URN"], eo["Trusts (code)"], eo["EstablishmentName"]) if not pd.isna(t)}
    bk = in_force(book)
    bk = bk[(bk["billing_basis"] == "Per pupil") & bk["urn"].notna()]
    start = dict(zip(bk["agreement_ref"], pd.to_datetime(bk["term_start"])))
    inv = led[(led["document_type"] == "Invoice") & led["agreement_ref"].isin(start)].copy()
    inv["ts"] = inv["description"].map(term_start_of)
    inv = inv[inv["ts"] == inv["agreement_ref"].map(start)]
    named = dict(zip(inv["agreement_ref"], inv["description"].str.split(": ", n=1).str[1]))
    out = {}
    for ref, urn in zip(bk["agreement_ref"], bk["urn"]):
        lead = sm.get(int(urn), int(urn))
        cov = [lead]
        names = str(named.get(ref, "")).split("; ")
        if len(names) > 1:
            for nm_ in names:
                u = by_name.get((tcode.get(lead), nm_))
                if u is not None and u not in cov:
                    cov.append(u)
        out[ref] = cov
    return out


def main_call(d):
    est, links, groups, book = d["est"], d["links"], d["groups"], d["book"]
    eo = est[est["EstablishmentStatus (name)"] == "Open"]
    mats = groups[(groups["Group Type"] == "Multi-academy trust") & (groups["Group Status"] == "Open")]
    mat_uid = set(mats["Group UID"].astype(int))
    name = dict(zip(mats["Group UID"].astype(int), mats["Group Name"]))
    ch = dict(zip(mats["Group UID"].astype(int), mats["Companies House Number"]))
    pilot_ch = set(d["offers"]["Companies House no."].dropna())
    sm = successor_map(links, est)
    b = in_force(book)
    b = b[b["urn"].notna()].copy()
    b["cur"] = b["urn"].astype(int).map(lambda u: sm.get(u, u))
    cov = coverage(d)
    b["covers"] = b["agreement_ref"].map(cov)
    tcode = dict(zip(eo["URN"], eo["Trusts (code)"]))
    b["uid"] = b["cur"].map(tcode)
    b = b[b["uid"].isin(mat_uid)]
    b["uid"] = b["uid"].astype(int)
    crm = d["crm"]
    tl = crm[(crm["opportunity_type"] == "Trust Licence") & crm["stage"].isin(["Closed Won", "Closed Lost"])]
    won, closed = int((tl["stage"] == "Closed Won").sum()), len(tl)
    rows = []
    for uid, g in b.groupby("uid"):
        covered = set(u for lst in g["covers"] for u in lst)
        if ch.get(uid) in pilot_ch or len(covered) < 2:
            continue
        acad = eo[eo["Trusts (code)"] == uid]
        lic = RATE * float(acad["NumberOfPupils"].fillna(0).sum())
        rep = float(g["annual_value_gbp"].sum())
        net = lic - rep
        # the same person is the same CRM contact, whichever way the name was typed on the agreement
        mode = "central" if g["signed_by_contact_id"].nunique() == 1 else "devolved"
        rows.append(dict(trust=name[uid], uid=uid, companies_house_no=ch.get(uid), academies=len(acad),
                         subscribing=len(covered), pupils=int(acad["NumberOfPupils"].fillna(0).sum()),
                         licence_value=round(lic, 2), replaced=round(rep, 2), new_recurring_revenue=round(net, 2),
                         planned_if_signed=int(round(net * won / closed)), mode=mode,
                         signatories=int(g["signed_by_contact_id"].nunique()), names=int(g["signed_by"].nunique())))
    t = pd.DataFrame(rows).sort_values(["planned_if_signed", "trust"], ascending=[False, True]).reset_index(drop=True)
    c = t[t["mode"] == "central"].reset_index(drop=True)
    slate = c.head(10)
    behind = c.iloc[10:15]
    # the 2023-24 cluster record, classified the same way
    cl = crm[crm["opportunity_type"] == "Cluster Licence"]
    modes = {}
    for uid, g in b.groupby("uid"):
        modes[ch.get(uid)] = "central" if g["signed_by_contact_id"].nunique() == 1 else "devolved"
    cl = cl.assign(mode=cl["companies_house_no"].map(modes))
    cluster = {m: dict(offered=int((cl["mode"] == m).sum()), won=int(((cl["mode"] == m) & (cl["stage"] == "Closed Won")).sum()))
               for m in ("central", "devolved")}
    return dict(table=t, central=c, slate=slate, behind=behind, sign=(won, closed), cluster=cluster,
                total=int(slate["planned_if_signed"].sum()),
                first_below=behind.iloc[0]["trust"], gap=int(slate.iloc[-1]["planned_if_signed"] - behind.iloc[0]["planned_if_signed"]))


def schools_on_tallybridge(d, crm_values=False, fed="contract", vat_as_net=False):
    """Every school on Tallybridge at 1 October: direct agreements, licence academies, framework contracts.
    crm_values and fed select wrong readings for the ask ladders: the CRM's pupils and value taken as exported, and
    the reseller's lines summed ("lines") or collapsed wherever their figures match ("content")."""
    est, links, book = d["est"], d["links"], d["book"]
    info = est.set_index("URN")
    sm = successor_map(links, est)
    out = []
    b = in_force(book)
    direct = b[b["billing_basis"] == "Per pupil"]
    cov = coverage(d)
    inv = term_invoices(d["ledger"], set(direct["agreement_ref"]), vat_as_net=vat_as_net)
    for _, x in direct.iterrows():
        cur = sm.get(int(x["urn"]), int(x["urn"]))
        pupils, revenue, channel = int(x["pupils_billed"]), float(x["annual_value_gbp"]), "direct"
        billed = inv.get((x["agreement_ref"], pd.Timestamp(x["term_start"])))
        if billed is not None and abs(billed - revenue) > 0.005 and not crm_values:
            # the CRM still holds last term's pupils and value; the invoice for the current term is what it bills
            py = "2026-27" if pd.Timestamp(x["term_start"]) >= PRICE_FROM else "2025-26"
            pupils, revenue, channel = int(round(billed / PRICE[(py, x["price_band"])])), billed, "direct, invoiced"
        out.append(dict(urn=cur, type=info.loc[cur, "EstablishmentTypeGroup (name)"], band=x["price_band"],
                        pupils=pupils, revenue=revenue, channel=channel))
        # the other schools a group agreement bills are on Tallybridge too; its pupils and value sit on the lead row
        for u in cov.get(x["agreement_ref"], [cur])[1:]:
            out.append(dict(urn=u, type=info.loc[u, "EstablishmentTypeGroup (name)"], band=x["price_band"],
                            pupils=0, revenue=0.0, channel="direct"))
    lic = b[b["billing_basis"] == "Trust Licence"]
    sched = d["sched"]
    for _, x in lic.iterrows():
        for _, a in sched[sched["Trust"] == x["account_name"]].iterrows():
            u = int(a["URN"])
            out.append(dict(urn=u, type=info.loc[u, "EstablishmentTypeGroup (name)"],
                            band=band_of(info.loc[u, "PhaseOfEducation (name)"]), pupils=int(a["Pupils priced"]),
                            revenue=RATE * float(a["Pupils priced"]), channel="licence"))
    rem = d["remit"]
    rem = rem[rem["reseller_ref"] != "TOTAL"].copy()
    rem["cs"] = pd.to_datetime(rem["contract_start"], format="%d/%m/%Y")
    rem["ce"] = pd.to_datetime(rem["contract_end"], format="%d/%m/%Y")
    rem = rem[(rem["cs"] <= AS_AT) & (rem["ce"] >= AS_AT)]
    shared = rem["contract_ref"].value_counts().to_dict()
    key = {}
    for _, e in est.iterrows():
        if not pd.isna(e["EstablishmentNumber"]):
            key.setdefault("%d%04d" % (int(e["LA (code)"]), int(e["EstablishmentNumber"])), []).append(e["URN"])
        if not pd.isna(e.get("PreviousLA (code)")) and not pd.isna(e.get("PreviousEstablishmentNumber")):
            key.setdefault("%d%04d" % (int(e["PreviousLA (code)"]), int(e["PreviousEstablishmentNumber"])), []).append(e["URN"])
    seen = set()
    for _, x in rem.iterrows():
        margin = 1 - x["reseller_margin_pct"] / 100.0
        if pd.isna(x["dfe_number"]):
            # a trust licence bought through the framework: its academies from the pilot schedule
            for _, a in sched[sched["Trust"] == x["establishment_name"]].iterrows():
                u = int(a["URN"])
                out.append(dict(urn=u, type=info.loc[u, "EstablishmentTypeGroup (name)"],
                                band=band_of(info.loc[u, "PhaseOfEducation (name)"]), pupils=int(a["Pupils priced"]),
                                revenue=RATE * float(a["Pupils priced"]) * margin, channel="framework licence"))
            continue
        cands = [u for u in key.get(x["dfe_number"], []) if info.loc[u, "EstablishmentStatus (name)"] == "Open"]
        u = int(cands[0])
        # a contract covering several schools is listed against each of them with the contract's pupils and value:
        # every school is on Tallybridge, the pupils and value count once for the contract
        k = x["contract_ref"]
        if fed == "content":
            k = (x["contract_start"], x["contract_end"], x["pupils"], x["annual_contract_value_gbp"])
        elif fed == "lines":
            k = None
        first = k is None or k not in seen
        seen.add(k)
        out.append(dict(urn=u, type=info.loc[u, "EstablishmentTypeGroup (name)"],
                        band=band_of(info.loc[u, "PhaseOfEducation (name)"]), pupils=int(x["pupils"]) if first else 0,
                        revenue=float(x["annual_contract_value_gbp"]) * margin if first else 0.0,
                        channel="framework" if shared.get(x["contract_ref"], 1) == 1 else "framework, federation"))
    return pd.DataFrame(out)


def ask_book(d, sch=None):
    sch = schools_on_tallybridge(d) if sch is None else sch
    cells = {}
    for t in TYPES:
        for bnd in BANDS:
            s = sch[(sch["type"] == t) & (sch["band"] == bnd)]
            cells[(t, bnd)] = dict(pupils=int(s["pupils"].sum()), revenue=int(round(s["revenue"].sum())))
    return cells


def term_start_of(description):
    m = re.search(r"(\d{2}/\d{2}/\d{4}) to \d{2}/\d{2}/\d{4}", str(description))
    return pd.to_datetime(m.group(1), format="%d/%m/%Y") if m else pd.NaT


def current_term_invoices(led, rep):
    """The invoice for the term each replaced agreement was in when the licence started."""
    inv = led[(led["document_type"] == "Invoice") & led["agreement_ref"].isin(rep["agreement_ref"])].copy()
    inv["ts"] = inv["description"].map(term_start_of)
    start = dict(zip(rep["agreement_ref"], pd.to_datetime(rep["term_start"])))
    return set(inv[inv["ts"] == inv["agreement_ref"].map(start)]["document_no"])


def week_of_batch(batch):
    """batch_id names the load by year and ISO week: UXW-2026-37 is the week beginning Monday 7 September 2026."""
    y, w = str(batch).split("-")[1:3]
    return pd.Timestamp(dt.date.fromisocalendar(int(y), int(w), 1))


def ask_pilot(d):
    led, book, offers = d["ledger"], d["book"], d["offers"]
    est, links = d["est"], d["links"]
    sm = successor_map(links, est)
    eo = est[est["EstablishmentStatus (name)"] == "Open"]
    tcode = dict(zip(eo["URN"], eo["Trusts (code)"]))
    groups = d["groups"]
    uid_of = dict(zip(groups["Group Name"], groups["Group UID"]))

    def net(row):
        return ex_vat(row["document_no"], row["amount_gbp"], row["vat_gbp"])

    res = {}
    signed = offers[offers["Outcome"] == "Signed"]
    rem = d["remit"]
    for _, o in signed.iterrows():
        trust = o["Trust"]
        uid = int(uid_of[trust])
        lic = book[(book["billing_basis"] == "Trust Licence") & (book["account_name"] == trust)]
        if len(lic):
            ref = lic.iloc[0]["agreement_ref"]
            docs = led[led["agreement_ref"] == ref]
            fee = float(docs.apply(net, axis=1).sum())
        else:
            line = rem[rem["establishment_name"] == trust].iloc[0]
            fee = float(line["annual_contract_value_gbp"])
        rep = book[book["status"] == "Replaced by Trust Licence"].copy()
        rep["cur"] = rep["urn"].astype(int).map(lambda u: sm.get(u, u))
        rep = rep[rep["cur"].map(tcode) == uid]
        cut = current_term_invoices(led, rep)
        # credited against the term each replaced agreement was in, from the day the licence took over
        cn = led[(led["document_type"] == "Credit note") & led["reference"].isin(cut)
                 & (pd.to_datetime(led["document_date"]) >= LICENCE_START)]
        credit = -float(cn.apply(net, axis=1).sum())
        res[trust] = dict(fee=round(fee, 2), credit=round(credit, 2), net=round(fee - credit, 2))
    return res


def ask_usage(d, sch=None, face=False, dedupe=True):
    sch = schools_on_tallybridge(d) if sch is None else sch
    est, links = d["est"], d["links"]
    sm = successor_map(links, est)
    u = d["usage"].copy()
    u["week_start"] = pd.to_datetime(u["week_start"])
    u = u.sort_values(["loaded_at", "school_ref"], kind="mergesort")
    if face:
        if dedupe:
            u = u.drop_duplicates(["school_ref", "week_start"], keep=dedupe if isinstance(dedupe, str) else "last")
        u = u[(u["week_start"] >= WEEK0) & (u["week_start"] <= WEEK0 + pd.Timedelta(days=35))]
    else:
        u["monday"] = u["batch_id"].map(week_of_batch)
        if dedupe:
            u = u.drop_duplicates(["school_ref", "monday"], keep=dedupe if isinstance(dedupe, str) else "last")
        weeks = [WEEK0 + pd.Timedelta(days=7 * i) for i in range(6)]
        u = u[u["monday"].isin(weeks)]
    u["cur"] = u["urn"].astype(int).map(lambda x: sm.get(x, x))
    present = set(sch["urn"])
    u = u[u["cur"].isin(present)]
    typ = sch.groupby("urn")[["type", "band"]].first()
    u = u.join(typ, on="cur")
    out = {}
    for t in TYPES:
        for bnd in BANDS:
            pupils = sch[(sch["type"] == t) & (sch["band"] == bnd)]["pupils"].sum()
            act = u[(u["type"] == t) & (u["band"] == bnd)]["active_pupils"].sum()
            out[(t, bnd)] = round(100.0 * act / 6.0 / pupils, 1) if pupils else None
    return out


def compute(T):
    d = load(T)
    m = main_call(d)
    sch = schools_on_tallybridge(d)
    return d, m, sch, ask_book(d, sch), ask_pilot(d), ask_usage(d, sch)


if __name__ == "__main__":
    import sys
    d, m, sch, A, B, C = compute(sys.argv[1] if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent / "target")
    print(m["slate"][["trust", "academies", "subscribing", "pupils", "new_recurring_revenue", "planned_if_signed"]].to_string())
    print("behind"); print(m["behind"][["trust", "new_recurring_revenue", "planned_if_signed"]].to_string())
    print("total", m["total"], "first below", m["first_below"], "gap", m["gap"], "sign", m["sign"], "cluster", m["cluster"])
    for k, v in A.items():
        print(k, v)
    for k, v in B.items():
        print(k, v)
    for k, v in C.items():
        print(k, v)
    print(sch.groupby("channel").size())


def figures(T):
    d, m, sch, A, B, C = compute(T)
    import calc
    pn = set(d["offers"]["Trust"])
    L = calc.ladder(d["est"], d["groups"], d["book"], d["links"], pn, cover=coverage(d))
    s = m["slate"]
    out = dict(
        round=dict(slate=list(s["trust"]), planned=[int(v) for v in s["planned_if_signed"]],
                   new_recurring_revenue=[round(float(v), 2) for v in s["new_recurring_revenue"]],
                   academies=[int(v) for v in s["academies"]], subscribing=[int(v) for v in s["subscribing"]],
                   pupils=[int(v) for v in s["pupils"]], licence_value=[round(float(v), 2) for v in s["licence_value"]],
                   replaced=[round(float(v), 2) for v in s["replaced"]], total=int(m["total"]),
                   running=[int(v) for v in s["planned_if_signed"].cumsum()],
                   share=[round(100.0 * float(v) / m["total"], 1) for v in s["planned_if_signed"]],
                   first_below=m["first_below"], gap=int(m["gap"]),
                   behind=[dict(trust=r["trust"], planned=int(r["planned_if_signed"]),
                                new_recurring_revenue=round(float(r["new_recurring_revenue"]), 2))
                           for _, r in m["behind"].iterrows()],
                   sign_rate=list(m["sign"]), cluster=m["cluster"],
                   eligible=dict(trusts=len(m["table"]), central=int((m["table"]["mode"] == "central").sum()),
                                 devolved=int((m["table"]["mode"] == "devolved").sum())),
                   rivals=[dict(trust=r["trust"], planned_if_signed=int(r["planned_if_signed"]))
                           for _, r in m["table"][m["table"]["mode"] == "devolved"].head(2).iterrows()]),
        book={"%s|%s" % k: v for k, v in A.items()},
        book_invoiced=int((sch["channel"] == "direct, invoiced").sum()),
        pilot=B,
        usage={"%s|%s" % k: v for k, v in C.items()},
        ladder={k: dict(total=v["total"], slate=v["slate"]) for k, v in L.items()},
    )
    return out


def write_figures(T, path):
    f = figures(T)
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(json.dumps(f, indent=1))
    return f
