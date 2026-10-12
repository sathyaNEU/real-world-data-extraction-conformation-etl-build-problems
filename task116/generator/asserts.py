"""The assertion regime. Every rule in the design note that a later edit could break is checked here, on the
files as shipped, and the build fails loudly when one breaks."""
import datetime as dt
import json
import re
from collections import Counter
from pathlib import Path

import numpy as np
import pandas as pd

import calc
import golden_calc as G

N = 0
LOG = []


def check(cond, msg):
    global N
    N += 1
    if not cond:
        raise AssertionError("ASSERT %d FAILED: %s" % (N, msg))
    LOG.append(msg)


def pct(a, b):
    return 100.0 * (a / b - 1.0)


def run(T, reg, c, A, out):
    T = Path(T)
    d, m, sch, AA, BB, CC = G.compute(T)
    book, est, links, groups = d["book"], d["est"], d["links"], d["groups"]
    offers = d["offers"]
    pilot_names = set(offers["Trust"])

    # ------------------------------------------------------------ input gates
    files = sorted(p.name for p in T.iterdir() if p.is_file())
    check(len(files) >= 10, "ten or more files (%d)" % len(files))
    fmts = set(p.suffix for p in T.iterdir() if p.is_file())
    check(len(fmts) >= 3, "three or more formats (%s)" % sorted(fmts))
    check(len(d["est"]) >= 25000 and len(d["usage"]) >= 25000,
          "files of 25,000 or more rows: register %d, usage %d" % (len(d["est"]), len(d["usage"])))
    check(not any(f.startswith(".") for f in files), "no hidden files in target")

    # ------------------------------------------------------------ the ladder, by name
    cover = G.coverage(d)
    L = calc.ladder(est, groups, book, links, pilot_names, cover=cover)
    ans = L["R4 answer"]
    check(list(m["slate"]["trust"]) == ans["slate"], "golden slate equals the generator's answer rung")
    check(m["total"] == ans["total"], "round total %d agrees across golden and generator" % m["total"])
    r0, r1, r2 = L["R0 licence fee, recorded URN"], L["R1 net, recorded URN"], L["R2 net, successors"]
    r3 = L["R3 signing condition, academies by the agreement's key"]
    for a_, b_, nm_ in [(r0, r1, "0 and 1"), (r1, r2, "1 and 2"), (r2, r3, "2 and 3"), (r3, ans, "3 and the answer")]:
        check(set(a_["slate"]) != set(b_["slate"]), "rungs %s name different slates" % nm_)
    check(len(set(r3["slate"]) & set(ans["slate"])) <= 8 and set(ans["slate"]) - set(r3["slate"]),
          "rung 3 (academies by the agreement's key) holds at most eight answer trusts (%d)"
          % len(set(r3["slate"]) & set(ans["slate"])))
    check(ans["slate"][0] not in r3["slate"], "the answer's first trust is not on rung 3's slate at all")
    check(len(set(r2["slate"]) & set(ans["slate"])) <= 4, "the mirror slate holds at most four answer trusts (%d)"
          % len(set(r2["slate"]) & set(ans["slate"])))
    check(abs(pct(r0["total"], r1["total"])) >= 5.0, "rung 0 and rung 1 totals at least 5 per cent apart")
    check(abs(pct(r2["total"], r1["total"])) >= 6.0, "rung 1 and rung 2 totals at least 6 per cent apart")
    check(pct(ans["total"], r3["total"]) >= 15.0, "the answer sits at least 15 per cent above rung 3 (%.1f)"
          % pct(ans["total"], r3["total"]))
    UP = lambda follow, basis, ident, rate: (basis != "net" or not follow or ident in ("surname", "most", "none")
                                             or rate == "pilot")
    DOWN = lambda ident, cov: ident == "name" or cov == "key"
    # the full grid: successors followed or not, three bases, five readings of who may be offered it, and
    # academies counted by the agreement's key or by what its invoices bill
    grid = {}
    for follow in (True, False):
        for basis in ("licence", "gross", "net"):
            for ident in ("contact", "name", "surname", "most", "none"):
                for cov in ("invoice", "key"):
                    for rate in ("closed", "pilot"):
                        t_ = calc.trust_table(est, groups, book, links, follow=follow, pilot_names=pilot_names,
                                              basis=basis, identity="contact" if ident == "none" else ident,
                                              cover=cover if cov == "invoice" else None,
                                              sign=7 / 13 if rate == "closed" else 7 / 12)
                        grid[(follow, basis, ident, cov, rate)] = calc.slate(t_, ident != "none")
    for cell, (sl, total) in grid.items():
        if cell == (True, "net", "contact", "invoice", "closed"):
            check(sl == ans["slate"] and total == ans["total"], "grid: the filed reading reproduces the answer")
            continue
        follow, basis, ident, cov, rate = cell
        near = abs(pct(total, ans["total"])) < 6.0
        # a cell inside the floor needs errors pulling both ways (one that inflates, refuted by the pilot, the filed
        # condition or the offers closed to date, and one that deflates: counting names, or academies by the
        # agreement's key), and it names another ten
        two_ways = UP(follow, basis, ident, rate) and DOWN(ident, cov) and len(set(sl) ^ set(ans["slate"])) >= 4
        check(not near or two_ways, "grid cell %s at %d sits %.1f per cent from the answer%s"
              % (cell, total, pct(total, ans["total"]), " (opposite errors, another ten)" if near else ""))
    A.grid = grid
    t2 = r2["table"]
    check(sum(t2.head(10)["mode"] == "devolved") >= 6, "the mirror slate is mostly trusts whose academies buy alone")

    # ------------------------------------------------------------ the cut and the order
    cs = m["central"]
    pv = list(cs["planned_if_signed"])
    check(pv[9] / pv[10] >= 1.15, "tenth beats eleventh central trust by %.3fx" % (pv[9] / pv[10]))
    for i in range(14):
        check(pv[i] > pv[i + 1] * 1.01, "adjacent planned values %d and %d are at least 1 per cent apart" % (i + 1, i + 2))
    for _, r in cs.head(15).iterrows():
        net = r["new_recurring_revenue"]
        exact = net * 7 / 13
        check(abs(exact - round(exact)) <= 0.20 and round(round(net) * 7 / 13) == round(exact),
              "planned value of %s files the same pound on either rounding path" % r["trust"])
    check(m["sign"] == (7, 13), "sign rate is seven of the thirteen Trust Licence offers closed to date")
    tlo = d["crm"][d["crm"]["opportunity_type"] == "Trust Licence"]
    check(len(tlo) == 13 and set(d["offers"]["Trust"]) < set(tlo["account_name"]),
          "the CRM holds the twelve pilot offers and one more Trust Licence offer")
    late = tlo[~tlo["account_name"].isin(set(d["offers"]["Trust"]))].iloc[0]
    check(late["stage"] == "Closed Lost" and late["close_date"] == "2026-09-30" and late["created_date"] > "2026-08-31",
          "the thirteenth offer was made after the pilot and declined on 30 September")
    check(len(d["offers"]) == 12 and (d["offers"]["Outcome"] == "Signed").sum() == 7,
          "the pilot sheet lists its own twelve offers, seven signed")
    oc = c.offcycle
    check(oc not in set(m["table"]["uid"]) or m["table"].set_index("uid").loc[oc, "mode"] == "devolved",
          "the trust offered the licence in September is not one the plan can offer it to")
    rate_rung = L["sign rate of the pilot's twelve offers"]
    check(rate_rung["slate"] == ans["slate"] and pct(rate_rung["total"], ans["total"]) >= 8.0,
          "at the pilot's own rate the ten are the same and the round is %.1f per cent higher" % pct(rate_rung["total"], ans["total"]))
    check(m["total"] % 1000 not in (0, 500) and m["total"] % 100 != 0, "round total not on a round number")

    # ------------------------------------------------------------ the pilot back-test (L1, L2)
    for nm, (follow, basis), lo, hi in [("rung 2 and 3", (True, "net"), 12, 12), ("rung 1", (False, "net"), 0, 7),
                                        ("rung 0", (False, "licence"), 0, 0)]:
        rep = calc.pilot_replication(est, groups, book, links,
                                     offers.rename(columns={"Trust": "trust"}), follow=follow, basis=basis)
        hits = sum(abs(rep[r["Trust"]] - r["Net new recurring revenue (GBP)"]) < 0.005 for _, r in offers.iterrows())
        check(lo <= hits <= hi, "%s reproduces %d of 12 pilot offers" % (nm, hits))
    # every pilot trust buys for its academies: one signatory each
    eo = est[est["EstablishmentStatus (name)"] == "Open"]
    sm = G.successor_map(links, est)
    tcode = dict(zip(eo["URN"], eo["Trusts (code)"]))
    uid_of = dict(zip(groups["Group Name"], groups["Group UID"]))
    pb = book[book["urn"].notna() & book["status"].isin(["In force", "Replaced by Trust Licence"])].drop_duplicates("agreement_ref").copy()
    pb["cur"] = pb["urn"].astype(int).map(lambda u: sm.get(u, u))
    pb["uid"] = pb["cur"].map(tcode)
    for _, o in offers.iterrows():
        g = pb[pb["uid"] == uid_of[o["Trust"]]]
        check(g["signed_by"].nunique() == 1 and len(g) >= 2,
              "pilot trust %s: %d agreements, one signatory" % (o["Trust"], len(g)))
    check(sum(1 for L_ in A.licences if any(x["urn"] != x["urn_current"] for x in A.rows if x.get("uid") == L_["uid"])) >= 5,
          "at least five pilot trusts hold an academy under its old URN")

    # ------------------------------------------------------------ the refusal record, absolute
    cl = m["cluster"]
    check(cl["devolved"] == {"offered": 17, "won": 0}, "cluster record: no trust whose schools sign alone ever signed")
    check(cl["central"]["offered"] == 13 and cl["central"]["won"] == 6, "cluster record: 6 of 13 central trusts signed")
    tt = m["table"]
    mixed_names = set(c.reg.group_name[u] for u in c.mixed)
    for _, r in tt.iterrows():
        check(r["signatories"] in (1, r["subscribing"]) or (r["trust"] in mixed_names and r["mode"] == "devolved"),
              "trust %s: one person, one per academy, or a designed mixed trust (%d people, %d academies)"
              % (r["trust"], r["signatories"], r["subscribing"]))
    check(len(tt) >= 120 and (tt["mode"] == "central").sum() >= 40, "about 140 eligible trusts, both kinds")
    check(not tt.empty and not any("devolved" in s or "central" in s for s in book["signed_by_role"].fillna("")),
          "no role title names a purchasing style")

    from book import RESERVED
    check(not set(book["signed_by"].dropna()) & RESERVED,
          "no customer agreement is signed by one of Tallybridge's own people")
    # ------------------------------------------------------------ who the same person is
    nm_ = dict(zip(groups["Group UID"].astype(int), groups["Group Name"]))
    tb_ = tt.set_index("uid")
    bi = G.in_force(book)
    bi = bi[bi["urn"].notna()].copy()
    smi = G.successor_map(links, est)
    bi["cur"] = bi["urn"].astype(int).map(lambda u: smi.get(u, u))
    bi["uid"] = bi["cur"].map(dict(zip(eo["URN"], eo["Trusts (code)"])))
    for u in c.variant:
        r, g = tb_.loc[u], bi[bi["uid"] == u]
        check(r["signatories"] == 1 and r["names"] == 2 and r["mode"] == "central",
              "%s: one CRM contact, two spellings of the name, offered the licence" % nm_[u])
        check(g["signed_by"].str.split().str[-1].nunique() == 1 and g["signed_by_role"].nunique() == 1
              and g["signed_on"].nunique() == 1, "%s: both spellings share surname, role and signing date" % nm_[u])
    for u in c.mixed:
        r = tb_.loc[u]
        check(2 <= r["signatories"] < r["subscribing"] and r["mode"] == "devolved",
              "%s: one contact signed for two academies, the rest for their own, not offered it" % nm_[u])
    g = bi[bi["uid"] == c.same_surname]
    firsts = g.groupby("signed_by_contact_id")["signed_by"].first().str.split().str[0]
    check(g["signed_by_contact_id"].nunique() == 2 and g["signed_by"].str.split().str[-1].nunique() == 1
          and firsts.nunique() == 2 and g["signed_by_role"].nunique() == 2,
          "%s: two people, one surname, different first names and roles" % nm_[c.same_surname])
    homonyms = bi.groupby("signed_by")["signed_by_contact_id"].nunique()
    check((homonyms == 1).all(), "no full name is shared by two contacts anywhere in the book")
    prof = lambda us: set((int(tb_.loc[u, "names"]), int(tb_.loc[u, "subscribing"])) for u in us)
    check(bool(prof(c.variant) & prof(c.mixed)),
          "an eligible two-spelling trust and an ineligible mixed trust share a profile %s" % sorted(prof(c.variant) & prof(c.mixed)))
    check(sum(nm_[u] in ans["slate"] for u in c.variant) == 2 and nm_[c.variant[2]] == m["first_below"],
          "two trusts on the round and the first below the line carry two spellings of their officer's name")
    for nm_p in pilot_names:
        gp = pb[pb["uid"] == uid_of[nm_p]]
        check(gp["signed_by"].nunique() == 1 and gp["signed_by_contact_id"].nunique() == 1,
              "pilot trust %s: one name, one contact" % nm_p)
    cl_rows = d["crm"][d["crm"]["opportunity_type"] == "Cluster Licence"]
    ch_uid = dict(zip(groups["Companies House Number"], groups["Group UID"]))
    for chn in cl_rows["companies_house_no"]:
        gc = bi[bi["uid"] == ch_uid.get(chn)]
        check(gc["signed_by"].nunique() == gc["signed_by_contact_id"].nunique() and len(gc) >= 2,
              "cluster trust %s reads the same by name and by contact" % chn)
    for u in c.twin_pair:
        gt = bi[bi["uid"] == u]
        check(gt["signed_by"].nunique() == gt["signed_by_contact_id"].nunique(), "twin %s reads the same by name and contact" % nm_[u])
    gn = grid[(True, "net", "name", "invoice", "closed")]
    check(set(gn[0]) - set(ans["slate"]) and set(ans["slate"]) - set(gn[0]),
          "counting names files a different ten in both directions (%s)" % gn[1])
    check(nm_[c.same_surname] in grid[(True, "net", "surname", "invoice", "closed")][0], "counting surnames lets the same-surname trust in")
    check(any(nm_[u] in grid[(True, "net", "most", "invoice", "closed")][0] for u in c.mixed[:4]),
          "a reading that admits a trust whose contact signed for most academies takes a mixed trust")

    # ------------------------------------------------------------ one agreement, several academies
    eo_ = est[est["EstablishmentStatus (name)"] == "Open"].set_index("URN")
    multi_refs = sorted(ref for ref, cv in cover.items() if len(cv) > 1)
    check(len(multi_refs) == len(c.multi), "%d agreements bill more than one school (%d cast)" % (len(multi_refs), len(c.multi)))
    for ref in multi_refs:
        cv, row = cover[ref], book[book["agreement_ref"] == ref].iloc[0]
        trusts = set(eo_.loc[cv, "Trusts (code)"])
        kinds = set(zip(eo_.loc[cv, "EstablishmentTypeGroup (name)"], eo_.loc[cv, "PhaseOfEducation (name)"]))
        roll = float(eo_.loc[cv, "NumberOfPupils"].sum())
        check(len(cv) in (3, 4) and len(trusts) == 1 and kinds == {("Academies", "Primary")}
              and row["price_band"] == "Primary", "%s bills %d primary academies of one trust" % (ref, len(cv)))
        check(abs(row["pupils_billed"] / roll - 1) <= 0.06 and row["pupils_billed"] > 2.2 * eo_.loc[cv[0], "NumberOfPupils"],
              "%s: pupils billed (%d) are the named schools' roll (%d), not the lead school's" % (ref, row["pupils_billed"], roll))
    # every school an invoice names resolves to exactly one open academy of the lead school's trust, and the text the
    # parser splits on (": " before the names, "; " between them) appears in no school or account name
    led_ = d["ledger"]
    inv_ = led_[(led_["document_type"] == "Invoice") & led_["description"].str.contains(" subscription ", na=False)]
    check(not inv_["description"].str.split(": ", n=1).str[1].isna().any(), "every subscription invoice names what it bills")
    # the parser takes everything after the first ": " and splits it on "; ", so no name an invoice can carry may hold "; "
    check(not book["account_name"].dropna().str.contains("; ").any(), "no account name on an agreement carries '; '")
    multi_lines = inv_[inv_["description"].str.contains("; ")]
    for desc in multi_lines["description"]:
        for n_ in desc.split(": ", 1)[1].split("; "):
            hits = eo[eo["EstablishmentName"] == n_]
            check(len(hits) >= 1, "group invoice school '%s' is an open school" % n_)
    for ref in multi_refs:
        lead_trust = eo_.loc[cover[ref][0], "Trusts (code)"]
        for u in cover[ref]:
            same = eo[(eo["EstablishmentName"] == eo_.loc[u, "EstablishmentName"]) & (eo["Trusts (code)"] == lead_trust)]
            check(len(same) == 1, "%s: '%s' is one open academy of the lead's trust" % (ref, eo_.loc[u, "EstablishmentName"]))
    check(set(multi_lines["agreement_ref"]) == set(multi_refs) | set(multi_lines["agreement_ref"]) and
          len(set(multi_lines["agreement_ref"])) == len(c.multi), "only the group agreements' invoices name more than one school")
    mu = [nm_[u] for u in c.multi]
    check(mu[0] == ans["slate"][0] and mu[1] in ans["slate"], "the two group-agreement trusts in contention are on the round")
    check(not set(mu) & set(r3["slate"]), "counting academies by the agreement's key drops every group-agreement trust")
    check(not set(mu[2:]) & set(m["central"].head(15)["trust"]), "the two other group-agreement trusts sit outside the chart")
    keyed = calc.trust_table(est, groups, book, links, pilot_names=pilot_names)
    check(not set(mu) & set(keyed["trust"]), "by the agreement's key each group-agreement trust holds one academy, so none is eligible")
    pilot_uids = set(uid_of[t] for t in pilot_names)
    check(not any(int(eo_.loc[cover[r_][0], "Trusts (code)"]) in pilot_uids for r_ in multi_refs if cover[r_][0] in eo_.index),
          "no pilot trust holds a group agreement, so the pilot cannot see the unit")
    cl_ch = set(d["crm"][d["crm"]["opportunity_type"] == "Cluster Licence"]["companies_house_no"])
    check(not any(c.reg.group_ch.get(u) in cl_ch for u in c.multi), "no group-agreement trust is in the cluster record")

    # ------------------------------------------------------------ the twin pair
    cu, dv = c.twin_pair
    nm = dict(zip(groups["Group UID"].astype(int), groups["Group Name"]))
    a_c, a_d = tt[tt["uid"] == cu].iloc[0], tt[tt["uid"] == dv].iloc[0]
    check(a_c["academies"] == a_d["academies"] and a_c["subscribing"] == a_d["subscribing"],
          "twins share academies and subscribing academies")
    check(abs(a_c["pupils"] - a_d["pupils"]) / a_d["pupils"] <= 0.02, "twins' pupils within 2 per cent")
    check(abs(a_c["new_recurring_revenue"] - a_d["new_recurring_revenue"]) / a_d["new_recurring_revenue"] <= 0.05,
          "twins' new recurring revenue within 5 per cent")
    check(a_c["mode"] == "central" and a_d["mode"] == "devolved", "twins buy differently")
    check(nm[cu] in ans["slate"] and nm[dv] in r2["slate"] and nm[dv] not in ans["slate"],
          "central twin on the answer, devolved twin on the mirror only")
    check(c.g.loc[cu, "region"] == c.g.loc[dv, "region"], "twins in the same region")

    # ------------------------------------------------------------ determinism closures
    b = G.in_force(book)
    ts, te = pd.to_datetime(b["term_start"]), pd.to_datetime(b["term_end"])
    near = ((ts > pd.Timestamp("2026-09-10")) & (ts < pd.Timestamp("2026-10-22"))) | (
        (te > pd.Timestamp("2026-09-10")) & (te < pd.Timestamp("2026-10-22")))
    check(int(near.sum()) == 0, "no agreement term starts or ends within three weeks of 1 October")
    cand_uids = set(tt["uid"])
    status = est[est["Trusts (code)"].isin(cand_uids)]["EstablishmentStatus (name)"]
    check(not status.isin(["Open, but proposed to close", "Proposed to open"]).any(),
          "no candidate trust holds a proposed or closing academy")
    contention = set(cs.head(15)["uid"]) | set(t2.head(15)["uid"])
    cont_est = eo[eo["Trusts (code)"].isin(contention)]
    check(cont_est["NumberOfPupils"].notna().all() and (cont_est["CensusDate"] == "15-01-2026").all(),
          "every academy in contention has a January 2026 pupil number")
    check(not set(int(u) for u in cont_est["URN"]) - set(int(u) for u in reg.open_state()["URN"]),
          "every academy in contention is a type Tallybridge sells to")
    for L_ in A.licences:
        check(L_["uid"] not in reg.moved_since_june, "pilot trust membership unchanged since June 2026")
    # declined pilot trusts: no renewal between the June pricing and 1 October
    for L_ in A.licences:
        if L_["outcome"] != "Declined":
            continue
        for x in A.rows:
            if x.get("uid") == L_["uid"]:
                check(not (dt.date(2026, 6, 15) < x["current_term_start"] <= dt.date(2026, 10, 1)),
                      "declined pilot agreement %s did not renew after pricing" % x.get("agreement_ref"))
    sum_round = sum(int(round(v * 7 / 13)) for v in cs.head(10)["new_recurring_revenue"])
    round_sum = int(round(sum(cs.head(10)["new_recurring_revenue"]) * 7 / 13))
    check(abs(sum_round - round_sum) <= 3, "rounding path moves the round by at most three pounds (%d vs %d)"
          % (sum_round, round_sum))

    # ------------------------------------------------------------ separation: no device row on the main path
    main_uids = cand_uids | set(uid_of[t] for t in pilot_names)
    copies = [x for x in A.rows if x.get("copy_of")]
    check(len(copies) == 61, "61 agreements carried twice by the 2025 migration")
    check(all(reg.info[x["urn_current"]]["Trusts (code)"] not in main_uids for x in copies),
          "zero migration copies inside the main call's trusts")
    fw_urns = [f["urn"] for f in A.framework if f["urn"]]
    check(all(reg.info[u]["Trusts (code)"] not in main_uids for u in fw_urns),
          "zero framework schools inside the main call's trusts")
    check(all(reg.info[x["urn_current"]]["Trusts (code)"] not in main_uids
              for x in A.rows if x["status"] == "Ended" and x["billing_basis"] == "Per pupil"),
          "zero ended school agreements inside the main call's trusts")
    split = [x for x in A.rows if x.get("site")]
    check(len(split) == 42 and all(reg.info[x["urn_current"]]["EstablishmentTypeGroup (name)"]
                                   == "Local authority maintained schools" for x in split),
          "21 split-site schools, all maintained")
    dup_refs = book[book["agreement_ref"].duplicated(keep=False)]
    check(dup_refs["agreement_ref"].nunique() == 61, "61 agreement references appear twice")

    # ------------------------------------------------------------ the clean-data test: repair the stale URN field
    sm_all = G.successor_map(links, est)
    repaired = book.copy()
    repaired["urn"] = repaired["urn"].map(lambda u: sm_all.get(int(u), int(u)) if not pd.isna(u) else u).astype("Int64")
    d_rep = dict(d, book=repaired)
    m_rep = G.main_call(d_rep)
    check(list(m_rep["slate"]["trust"]) == list(m["slate"]["trust"]) and m_rep["total"] == m["total"],
          "clean-data test: with every URN brought up to date the answer is unchanged")
    L_rep = calc.ladder(est, groups, repaired, links, pilot_names)
    check(L_rep["R2 net, successors"]["total"] == r2["total"] and L_rep["R2 net, successors"]["slate"] == r2["slate"],
          "clean-data test: the mirror's slate and round are unchanged by the repair")
    check(set(m["slate"]["trust"]) != set(r2["slate"]), "clean-data test: answer and mirror still differ")
    check(len(set(m["slate"]["trust"]) - set(r2["slate"])) >= 5,
          "lens test: the answer is not the mirror's population re-read; seven of its trusts are off the mirror slate")
    # the decisive rung is a construction: no single book column separates the central trusts
    tcols = ["billing_basis", "price_band", "status", "signed_by_role"]
    bb = G.in_force(book)
    bb = bb[bb["urn"].notna()].copy()
    bb["cur"] = bb["urn"].astype(int).map(lambda u: sm_all.get(u, u))
    bb["uid"] = bb["cur"].map(tcode)
    modes = dict(zip(tt["uid"], tt["mode"]))
    bb["mode"] = bb["uid"].map(modes)
    bb = bb[bb["mode"].notna()]
    for col in tcols:
        sep = bb.groupby(col)["mode"].nunique()
        check((sep > 1).any() or bb[col].nunique() == 1, "column %s does not separate the two kinds of trust" % col)

    # ------------------------------------------------------------ ask A: the book by type and band
    gold_a = AA
    check(gold_a[("Special schools", "Primary")]["pupils"] == 0, "no special school in the primary band")
    stops = ask_a_stops(d)
    for name, cells in stops.items():
        diff = [k for k in gold_a if cells[k] != gold_a[k]]
        check(len(diff) >= 1, "ask A stop '%s' moves %d cells" % (name, len(diff)))
    na = lambda res: sum(1 for k in AA if AA[k]["pupils"] and (res[k]["pupils"] != AA[k]["pupils"] or res[k]["revenue"] != AA[k]["revenue"]))
    n_cells = sum(1 for k in AA if AA[k]["pupils"])
    check(na(stops["CRM pupils and value as exported"]) == n_cells,
          "the CRM's pupils and value taken as exported move every book cell (%d of %d)"
          % (na(stops["CRM pupils and value as exported"]), n_cells))
    nf = lambda res: sum(1 for k in AA for f in ("pupils", "revenue") if AA[k]["pupils"] and res[k][f] != AA[k][f])
    check(nf(stops["CRM pupils and value as exported"]) >= 2 * n_cells - 1,
          "taken as exported, %d of %d book figures are wrong" % (nf(stops["CRM pupils and value as exported"]), 2 * n_cells))
    check(na(stops["reseller lines summed"]) >= 2, "summing the reseller's lines moves %d book cells"
          % na(stops["reseller lines summed"]))
    check(na(stops["reseller lines with matching figures collapsed"]) >= 1,
          "collapsing reseller lines whose figures match moves %d book cells"
          % na(stops["reseller lines with matching figures collapsed"]))
    # the CRM after the cutover: an April renewal shows its new term with the term before's pupils and value
    stale = sch[sch["channel"] == "direct, invoiced"]
    check(len(stale) == len(A.stale) and len(stale) >= 300, "%d agreements carry the term before's pupils and value"
          % len(stale))
    st_uids = set()
    bkx = book.drop_duplicates("agreement_ref").set_index("agreement_ref")
    led_ = d["ledger"]
    tinv = G.term_invoices(led_, set(bkx.index))
    for x in A.stale:
        ref = x["agreement_ref"]
        row = bkx.loc[ref]
        ts = pd.Timestamp(row["term_start"])
        prev = ts - pd.DateOffset(years=1)
        check(ts.month == 4 and ts.year == 2026, "%s renewed in April 2026" % ref)
        check(abs(row["annual_value_gbp"] - round(max(G.PRICE[("2025-26", row["price_band"])] * row["pupils_billed"],
                                                      820.0), 2)) < 0.006,
              "%s: the CRM's value is the 2025-26 price on the CRM's pupils" % ref)
        check(abs(tinv[(ref, prev)] - row["annual_value_gbp"]) < 0.006,
              "%s: the CRM holds exactly the term before's invoice" % ref)
        billed = tinv[(ref, ts)]
        n = billed / G.PRICE[("2026-27", row["price_band"])]
        check(abs(n - round(n)) < 1e-6 and billed > 850.0 + 20, "%s: the current invoice is the 2026-27 price on a whole "
              "number of pupils, above the minimum" % ref)
        st_uids.add(reg.info[x["urn_current"]]["Trusts (code)"])
    main_uids0 = set(tt["uid"]) | set(uid_of[t] for t in pilot_names)
    check(not any(not pd.isna(u) and int(u) in main_uids0 for u in st_uids),
          "zero agreements with the term before's figures inside the main call's trusts")
    for cell in [k for k in AA if AA[k]["pupils"]]:
        check(((stale["type"] == cell[0]) & (stale["band"] == cell[1])).sum() >= 1,
              "the book cell %s holds at least one agreement with the term before's figures" % (cell,))
    # every other per-pupil agreement in force: the CRM agrees with the invoice for its current term
    pp = G.in_force(book)
    pp = pp[(pp["billing_basis"] == "Per pupil") & ~pp["agreement_ref"].isin(set(x["agreement_ref"] for x in A.stale))]
    agree = [abs(tinv[(r_, pd.Timestamp(t_))] - v_) < 0.006 for r_, t_, v_ in
             zip(pp["agreement_ref"], pp["term_start"], pp["annual_value_gbp"])]
    check(all(agree), "every other agreement in force agrees with its current invoice (%d of %d)" % (sum(agree), len(agree)))
    # the reseller: a federation's contract repeats on each of its schools' lines; two unrelated schools share figures
    rem = d["remit"][d["remit"]["reseller_ref"] != "TOTAL"]
    fed_lines = sch[sch["urn"].isin(A.fed_urns)]
    check(len(A.federations) == 7 and len(fed_lines) == sum(len(f["schools"]) for f in A.federations)
          and (fed_lines["pupils"] > 0).sum() == 7,
          "seven federations on one contract each, %d lines, pupils and value counted once a contract" % len(fed_lines))
    other_fed = sch[sch["channel"].str.startswith("framework") & ~sch["urn"].isin(A.fed_urns)]
    keys = rem.assign(f=rem["dfe_number"].map(lambda x: None))
    check(len(other_fed[other_fed["pupils"] == 0]) == 0, "no other reseller line is read as part of another's contract")
    eidx = est.set_index("URN")
    for f in A.federations:
        urns = [s_["urn"] for s_ in f["schools"]]
        roll = float(eidx.loc[urns, "NumberOfPupils"].sum())
        check(len(set(eidx.loc[urns, "Federations (code)"])) == 1 and abs(f["pupils"] / roll - 1) <= 0.06,
              "%s: one register federation, the contract's pupils within 6 per cent of its schools' roll" % f["name"])
        check(all(f["pupils"] > 1.4 * eidx.loc[u, "NumberOfPupils"] for u in urns),
              "%s: each line's pupils are well above the school's own roll" % f["name"])
        check(len(set((eidx.loc[u, "EstablishmentTypeGroup (name)"], G.band_of(eidx.loc[u, "PhaseOfEducation (name)"]))
                      for u in urns)) == 1, "%s: every school in one book cell" % f["name"])
        check(not any(not pd.isna(eidx.loc[u, "Trusts (code)"]) for u in urns), "%s: no school in a trust" % f["name"])
    a_, b_ = A.pair
    ra = rem[rem["dfe_number"].isin([x_["dfe_number"] for x_ in A.framework if x_.get("urn") in (a_, b_)])]
    cols = ["contract_start", "contract_end", "pupils", "annual_contract_value_gbp"]
    check(len(ra) == 2 and len(ra[cols].drop_duplicates()) == 1 and eidx.loc[a_, "LA (code)"] != eidx.loc[b_, "LA (code)"]
          and pd.isna(eidx.loc[a_, "Federations (code)"]) and pd.isna(eidx.loc[b_, "Federations (code)"]),
          "two unrelated schools in different authorities carry identical contract figures")
    for f in A.federations:
        lines = rem[rem["dfe_number"].isin([s_["dfe_number"] for s_ in f["schools"]])]
        check(len(lines) == len(f["schools"]) and lines["contract_ref"].nunique() == 1,
              "%s: its lines share one contract reference" % f["name"])
    fed_refs = set(rem[rem["dfe_number"].isin([s_["dfe_number"] for f in A.federations for s_ in f["schools"]])]["contract_ref"])
    others_ = rem[~rem["contract_ref"].isin(fed_refs)]
    check(not others_["contract_ref"].duplicated().any() and ra["contract_ref"].nunique() == 2,
          "every other line, the identical pair included, has a contract reference of its own")
    tot = d["remit"][d["remit"]["reseller_ref"] == "TOTAL"].iloc[0]
    check(abs(tot["pupils"] - rem["pupils"].sum()) < 0.5 and abs(tot["annual_contract_value_gbp"]
                                                                 - rem["annual_contract_value_gbp"].sum()) < 0.01,
          "the reseller's total line sums its lines, repeats included")
    check(not d["remit"]["reseller_ref"].duplicated().any(), "every reseller line has its own reference")
    # ------------------------------------------------------------ ask B: the pilot licences billed
    stops_b = ask_b_stops(d)
    nb = lambda res: sum(1 for k in BB if abs(res[k]["credit"] - BB[k]["credit"]) >= 1 or abs(res[k]["net"] - BB[k]["net"]) >= 1
                         or abs(res[k]["fee"] - BB[k]["fee"]) >= 1)
    for name, res in stops_b.items():
        check(nb(res) >= 1, "ask B stop '%s' moves %d licences" % (name, nb(res)))
    check(nb(stops_b["a filled VAT field read as on the new platform"]) >= 5,
          "reading a filled VAT field as the new platform's moves %d of 7 licences"
          % nb(stops_b["a filled VAT field read as on the new platform"]))
    check(nb(stops_b["amounts as recorded"]) >= 5, "amounts as recorded move %d licences" % nb(stops_b["amounts as recorded"]))
    check(nb(stops_b["every credit against the replaced terms' invoices"]) == 7,
          "taking every credit against the replaced terms' invoices moves %d of 7 licences"
          % nb(stops_b["every credit against the replaced terms' invoices"]))
    check(nb(stops_b["credits found by agreement reference"]) >= 4,
          "credits found by agreement reference move %d of 7 licences" % nb(stops_b["credits found by agreement reference"]))
    leg = [x for x in A.replacement_credits if x["legacy"]]
    check(len(set(x["uid"] for x in leg)) >= 5, "old-system replacement credits on %d of 7 licences"
          % len(set(x["uid"] for x in leg)))
    led = d["ledger"]
    lcn = led[led["document_no"].str.startswith("L") & (led["document_type"] == "Credit note")]
    check(len(lcn) > 0 and lcn["agreement_ref"].isna().all() and lcn["reference"].notna().all(),
          "every old-system credit note carries the invoice it credits and no agreement reference (%d)" % len(lcn))
    others = led[~led.index.isin(lcn.index)]
    check(others["agreement_ref"].notna().all(), "every other ledger document carries its agreement reference")
    when = pd.to_datetime(led["document_date"])
    oldd = led[led["document_no"].str.startswith("L")]
    check(len(oldd) > 1000 and oldd["vat_gbp"].notna().all() and ((oldd["vat_gbp"] - oldd["amount_gbp"] / 6).abs()
                                                                   < 0.011).all(),
          "every old-system document's VAT field holds the VAT inside its amount, a sixth of it (%d)" % len(oldd))
    check(not oldd[when[oldd.index] >= "2026-05-01"]["document_type"].eq("Invoice").any(),
          "the old system raised no invoice from 1 May 2026")
    newd = led[~led["document_no"].str.startswith("L")]
    check(((newd["vat_gbp"] - 0.2 * newd["amount_gbp"]).abs() < 0.011).all(),
          "every new-platform document carries its VAT beside a net amount")
    # the VAT inside an old-system invoice, forced by arithmetic: before 1 May every current-term invoice is 1.2 x the
    # term's value as the CRM holds it, except where the CRM holds the term before
    bk = book.drop_duplicates("agreement_ref").set_index("agreement_ref")
    per_pupil = set(bk.index[bk["billing_basis"] == "Per pupil"]) - set(x["agreement_ref"] for x in A.stale)
    inv = led[(led["document_type"] == "Invoice") & led["agreement_ref"].isin(per_pupil)].copy()
    inv["ts"] = inv["description"].map(G.term_start_of)
    inv = inv[inv["ts"] == pd.to_datetime(inv["agreement_ref"].map(bk["term_start"]))]
    inv["val"] = inv["agreement_ref"].map(bk["annual_value_gbp"]).astype(float)
    old, new = inv[inv["document_no"].str.startswith("L")], inv[~inv["document_no"].str.startswith("L")]
    check(len(old) > 100 and ((old["amount_gbp"] - 1.2 * old["val"]).abs() < 0.011).all(),
          "every other old-system current-term invoice is 1.2 x the book's annual value (%d)" % len(old))
    check(len(new) > 100 and ((new["amount_gbp"] - new["val"]).abs() < 0.011).all(),
          "every new-platform current-term invoice is the book's annual value (%d)" % len(new))
    stc = getattr(A, "same_term_corrections", {})
    check(len(stc) == 7, "%d licences carry a correction to a replaced agreement's current term" % len(stc))
    dec = pd.to_datetime(d["offers"]["Decided on"]).min()
    pre = led[(led["document_type"] == "Credit note") & (when < G.LICENCE_START) & (when >= "2026-05-01")]
    check(len(pre) >= len(stc) and (pd.to_datetime(pre["document_date"]) < dec).all(),
          "every credit note raised from May to August precedes the first licence decision (%s)" % dec.date())
    # each replacement credit is the unexpired share of its term as billed after any earlier correction, to the penny
    repl = book[book["status"] == "Replaced by Trust Licence"].drop_duplicates("agreement_ref").set_index("agreement_ref")
    cut_ = G.current_term_invoices(led, repl.reset_index())
    cn_ = led[(led["document_type"] == "Credit note") & led["reference"].isin(cut_)]
    inv_ = led[led["document_no"].isin(cut_)].set_index("document_no")
    n_ok = 0
    for ref_inv, g in cn_.groupby("reference"):
        dates = pd.to_datetime(g["document_date"])
        pre_ = g[dates < G.LICENCE_START]
        corr = -sum(G.ex_vat(n_, a_, v_) for n_, a_, v_ in zip(pre_["document_no"], pre_["amount_gbp"], pre_["vat_gbp"]))
        sept = g[dates >= G.LICENCE_START]
        if not len(sept):
            continue
        ag = repl.loc[inv_.loc[ref_inv, "agreement_ref"]]
        ts_, te_ = pd.Timestamp(ag["term_start"]), pd.Timestamp(ag["term_end"])
        share = (te_ - pd.Timestamp("2026-08-31")).days / ((te_ - ts_).days + 1)
        want = round((G.ex_vat(ref_inv, inv_.loc[ref_inv, "amount_gbp"], inv_.loc[ref_inv, "vat_gbp"]) - corr) * share, 2)
        got = -sum(G.ex_vat(n_, a_, v_) for n_, a_, v_ in zip(sept["document_no"], sept["amount_gbp"], sept["vat_gbp"]))
        n_ok += abs(want - got) <= 0.011
    check(n_ok == len(A.replacement_credits), "every replacement credit is the unexpired share of its term as billed "
          "after any earlier correction (%d of %d)" % (n_ok, len(A.replacement_credits)))
    pcs = getattr(A, "prior_corrections", [])
    check(3 <= len(pcs) <= 5 and all(x["uid"] in A.signed for x in pcs),
          "%d pupil-number corrections sit on earlier terms of agreements the signed licences replaced" % len(pcs))
    texts_l = led[led["document_type"] == "Credit note"]["description"]
    check(texts_l.str.match(r"^(Credit against L\d{6}|Credit note for INV-\d{7}|Cancels INV-\d{7}: .*)$").all(),
          "every credit note says only what it credits")
    # ------------------------------------------------------------ ask C: usage
    stops_c = ask_c_stops(d)
    ncc = lambda res: sum(1 for k in CC if CC[k] is not None and res[k] is not None and abs(res[k] - CC[k]) >= 0.1)
    for name, res in stops_c.items():
        check(ncc(res) >= 1, "ask C stop '%s' moves %d cells" % (name, ncc(res)))
    check(ncc(stops_c["only schools with usage this term counted"]) >= 5,
          "the rate over schools that reported moves %d of 7 usage cells" % ncc(stops_c["only schools with usage this term counted"]))
    check(ncc(stops_c["labels at face value"]) >= 2,
          "weeks cut on their labels move %d usage cells" % ncc(stops_c["labels at face value"]))
    uu = d["usage"].copy()
    rr = uu[uu["batch_id"].str.endswith("-R1")]
    orig = uu[uu["batch_id"] == "UXW-2026-39"]
    both = rr.merge(orig, on="school_ref", suffixes=("", "_o"))
    check(len(both) == len(rr) and 0.3 <= len(rr) / A.resend["region_rows"] <= 0.8
          and (both["active_pupils"] >= both["active_pupils_o"]).all()
          and (both["active_pupils"] > both["active_pupils_o"]).mean() >= 0.5
          and (both["active_pupils"] == both["active_pupils_o"]).any(),
          "the re-sent batch carries part of one region's week (%d of %d rows), most of them fuller than the first load"
          % (len(rr), A.resend["region_rows"]))
    check((pd.to_datetime(rr["loaded_at"]) > pd.to_datetime(both["loaded_at_o"]).max()).all(),
          "every re-sent row was loaded after the week's first load")
    uu["wk"] = uu["batch_id"].map(G.week_of_batch)
    uu["ws"] = pd.to_datetime(uu["week_start"])
    sunday = uu[uu["ws"].dt.weekday == 6]
    check(((uu["ws"].dt.weekday == 0) & (uu["ws"] == uu["wk"]) | (uu["ws"].dt.weekday == 6)
           & (uu["ws"] + pd.Timedelta(days=1) == uu["wk"])).all(),
          "every row's label is its batch week's Monday, or the Sunday before it")
    lic_urns = set(int(x) for x in d["sched"]["URN"])
    sm_u = G.successor_map(links, est)
    check(len(sunday) > 0 and sunday["urn"].astype(int).map(lambda x: sm_u.get(x, x)).isin(lic_urns).all(),
          "only licence academies carry Sunday labels (%d rows)" % len(sunday))
    check((uu["active_pupils"] > 0).all(), "no usage row records a week with no pupil answering")
    check(uu.groupby("school_ref")["urn"].nunique().max() == 1, "every platform school id belongs to one school")
    check(not uu.duplicated(["school_ref", "batch_id"]).any(), "a load reports a school once")
    cov_extra = set(u for ref, cv in cover.items() for u in cv[1:])
    check(not set(uu["urn"].astype(int)) & cov_extra, "a group agreement's schools report under the lead school's record")

    # ------------------------------------------------------------ separation: the new devices sit off the main path
    closing = list(getattr(A, "closing", []))
    check(15 <= len(closing) <= 30 and all(pd.isna(reg.info[u]["Trusts (code)"])
                                           or int(reg.info[u]["Trusts (code)"]) not in reg.mat_uids for u in closing),
          "%d customers proposed to close, none in a multi-academy trust" % len(closing))
    check(all(reg.info[u]["EstablishmentStatus (name)"] == "Open, but proposed to close" for u in closing),
          "each of them is shown open but proposed to close in the register")
    check(set(closing) <= set(sch["urn"]), "every customer proposed to close is on Tallybridge at 1 October")
    quiet = set(sch[sch["pupils"] > 0]["urn"]) - used_this_term(d)
    trust_of = {int(u): reg.info[int(u)]["Trusts (code)"] for u in quiet}
    check(len(quiet) >= 50 and not any(not pd.isna(t) and int(t) in main_uids for t in trust_of.values()),
          "%d schools on Tallybridge have no usage this term, none in a trust the main call reads" % len(quiet))
    q_share = sch[sch["urn"].isin(quiet)]["pupils"].sum() / sch["pupils"].sum()
    check(0.025 <= q_share <= 0.06, "schools with no usage this term hold %.1f per cent of pupils billed" % (100 * q_share))
    check(not set(A.fed_urns) & set(int(u) for u in eo[eo["Trusts (code)"].isin(main_uids)]["URN"]),
          "zero federation schools inside the main call's trusts")

    # ------------------------------------------------------------ either way of taking VAT out lands the same figures
    exact_ex_vat = G.ex_vat
    G.ex_vat = lambda n_, a_, v_: a_ / 1.2 if str(n_).startswith("L") else a_
    try:
        sch_d = G.schools_on_tallybridge(d)
        AA_d, BB_d, CC_d = G.ask_book(d, sch_d), G.ask_pilot(d), G.ask_usage(d, sch_d)
    finally:
        G.ex_vat = exact_ex_vat
    check(AA_d == AA and CC_d == CC and all(round(BB_d[k][f]) == round(BB[k][f]) for k in BB for f in ("credit", "net")),
          "amount less its VAT field and amount divided by 1.2 file the same book, pilot and usage figures")
    # ------------------------------------------------------------ decoupled: neither main-call move reaches an ask figure
    keyed_sch = sch[~((sch["channel"] == "direct") & (sch["pupils"] == 0) & (sch["revenue"] == 0))]
    check(len(keyed_sch) < len(sch) and G.ask_book(d, keyed_sch) == AA and G.ask_usage(d, keyed_sch) == CC,
          "counting an agreement as one school moves no book or usage figure (%d schools dropped)"
          % (len(sch) - len(keyed_sch)))
    check(not any(x.get("uid") in main_uids for x in A.stale), "the CRM's stale rows sit outside every candidate trust")
    # ------------------------------------------------------------ the pair simulation, ask layer
    sheets = battery_sheets(d)
    A.pair_sim = {}
    for nm_s, sh in sheets.items():
        h, tot_ = criteria_matched(AA, BB, CC, *sh)
        A.pair_sim[nm_s] = (h, tot_)
    print("pair simulation, ask layer: %s" % ", ".join("%s %d of %d" % (k, v[0], v[1]) for k, v in A.pair_sim.items()))
    hs, tot_ = A.pair_sim["strict"]
    hn, _ = A.pair_sim["natural"]
    hc, _ = A.pair_sim["crm_reader"]
    check(hs / tot_ <= 0.30, "the strict sheet keeps %.0f per cent of the ask figures" % (100 * hs / tot_))
    check(hn / tot_ <= 0.25, "the natural sheet keeps %.0f per cent of the ask figures" % (100 * hn / tot_))
    check(hc / tot_ <= 0.25, "the CRM reader keeps %.0f per cent of the ask figures" % (100 * hc / tot_))
    # ------------------------------------------------------------ every graded ask figure clear of its rounding edge
    import settle as S
    exact_a = S.book_revenue_exact(sch)
    for k, v in exact_a.items():
        check(not v or S.frac_ok(v), "book revenue %s sits clear of a rounding edge" % (k,))
    check(not S.check_pilot(BB), "every pilot licence figure rounds the same on every path")
    check(not S.check_usage(CC), "every usage figure sits clear of a rounding edge")

    # ------------------------------------------------------------ single statements, and no trap vocabulary
    texts = {f: (T / f).read_text(errors="ignore") for f in files if f.endswith((".md", ".txt"))}
    for f in ["tallybridge_trust_licence_terms_2026.pdf", "tallybridge_price_list_2026-27.pdf"]:
        texts[f] = pdf_text(T / f)
    texts["trust_partnerships_plan_2027.docx"] = docx_text(T / "trust_partnerships_plan_2027.docx")
    allt = "\n".join(texts.values()).lower()
    for w in ["devolved", "centrally", "central office", "buys for", "purchasing style", "signator", "who signed for",
              "successor", "predecessor", "converted"]:
        check(w not in allt, "no shipped document uses '%s'" % w)
    plan_txt = texts["trust_partnerships_plan_2027.docx"].lower()
    check(sum("same person signed" in t.lower() for t in texts.values()) == 1 and "same person signed" in plan_txt,
          "the signing condition is filed once, in the plan's eligibility paragraph")
    terms_txt = texts["tallybridge_trust_licence_terms_2026.pdf"].lower()
    check("accounting officer" not in terms_txt and "delegates" not in terms_txt,
          "the licence terms say nothing about who may sign for a trust")
    check(sum("4.05" in t for t in texts.values()) == 1, "the licence rate is stated in one document")
    check(sum("sign rate" in t.lower() for t in texts.values()) == 1, "the plan's sign-rate convention is stated once")
    check(not any("sunday before" in t.lower() or "labels a week by" in t.lower() for t in texts.values()),
          "no document says how either reporting service labels its weeks")
    check(sum("iso week" in t.lower() for t in texts.values()) == 1, "the load-naming rule is stated once")
    check(not any("including vat" in t.lower() or "split the vat" in t.lower() or "vat included" in t.lower()
                  for t in texts.values()), "no document says how either billing system records VAT")
    for phrase in ["**the book**", "**pupils billed**", "as the term in force is invoiced", "the later load is the one of record",
                   "`contract_ref`"]:
        check(sum(phrase in t.lower() or phrase in t for t in texts.values()) == 1, "'%s' is filed once" % phrase)
    check(sum("at least one of its pupils answered" in t.lower() for t in texts.values()) == 1,
          "the usage grain (a row only for a week with a pupil answering) is stated once")
    check(sum("as the issuing system holds it" in t.lower() for t in texts.values()) == 1,
          "the ledger's amount field is described once, neutrally")
    prompt = (T.parent / "prompt.md").read_text().lower()
    for w in ["clean", "unduplicated", "reconcile", "attribution", " mix", "standardis", "grain", "signator", "devolved",
              "central", "framework", "successor", "urn", "vat strip", "sunday", "cluster"]:
        check(w not in prompt, "prompt does not use '%s'" % w.strip())
    print("asserts: %d passed" % N)
    return N


def pdf_text(p):
    from pypdf import PdfReader
    return "\n".join(pg.extract_text() or "" for pg in PdfReader(str(p)).pages)


def docx_text(p):
    from docx import Document
    return "\n".join(par.text for par in Document(str(p)).paragraphs)


# ---------------------------------------------------------------- the ask ladders' stops
def ask_a_stops(d):
    """Ask A on each wrong reading a solver can complete without an error: every one files a full grid."""
    sch = G.schools_on_tallybridge(d)
    out = {}
    out["CRM pupils and value as exported"] = G.ask_book(d, G.schools_on_tallybridge(d, crm_values=True))
    out["reseller lines summed"] = G.ask_book(d, G.schools_on_tallybridge(d, fed="lines"))
    out["reseller lines with matching figures collapsed"] = G.ask_book(d, G.schools_on_tallybridge(d, fed="content"))
    out["book only"] = G.ask_book(d, sch[sch["channel"].isin(["direct", "direct, invoiced", "licence"])])
    s2 = sch.copy()
    fw = s2["channel"].str.startswith("framework")
    s2.loc[fw, "revenue"] = s2.loc[fw, "revenue"] / 0.88
    out["framework at contract value"] = G.ask_book(d, s2)
    # the 2025 migration's second rows counted again
    dup = d["book"][d["book"]["agreement_ref"].duplicated(keep="first")]
    dup = G.in_force(dup.assign(agreement_ref=dup["agreement_ref"] + "-copy"))
    sm = G.successor_map(d["links"], d["est"])
    info = d["est"].set_index("URN")
    extra = pd.DataFrame([dict(urn=sm.get(int(x["urn"]), int(x["urn"])),
                               type=info.loc[sm.get(int(x["urn"]), int(x["urn"])), "EstablishmentTypeGroup (name)"],
                               band=x["price_band"], pupils=int(x["pupils_billed"]), revenue=float(x["annual_value_gbp"]),
                               channel="copy") for _, x in dup.iterrows()])
    out["migration copies kept"] = G.ask_book(d, pd.concat([sch, extra], ignore_index=True))
    out["one agreement per URN"] = G.ask_book(d, sch.drop_duplicates(["urn", "channel"]))
    st = dict(zip(d["est"]["URN"], d["est"]["EstablishmentStatus (name)"]))
    out["register read as open schools only"] = G.ask_book(d, sch[sch["urn"].map(st) == "Open"])
    return out


def pilot_variant(d, vat="L", credits="from_start"):
    """Ask B on a reading. vat: "L" (the golden: every old-system document holds its amount with VAT in it), "field"
    (every amount with a VAT field beside it read as net, the new platform's way), "none" (amounts as recorded). credits: "from_start" (the golden: credit
    notes against the term each replaced agreement was in, raised from the licence start), "term" (every credit note
    against that term's invoice), "any" (every credit note tied to a replaced agreement, whichever term), "agreement"
    (credit notes found by agreement reference only)."""
    led, book, offers, rem = d["ledger"], d["book"], d["offers"], d["remit"]
    sm = G.successor_map(d["links"], d["est"])
    eo = d["est"][d["est"]["EstablishmentStatus (name)"] == "Open"]
    tcode = dict(zip(eo["URN"], eo["Trusts (code)"]))
    uid_of = dict(zip(d["groups"]["Group Name"], d["groups"]["Group UID"]))

    def amt(r):
        if vat == "L":
            return G.ex_vat(r["document_no"], r["amount_gbp"], r["vat_gbp"])
        if vat == "field":
            return r["amount_gbp"]
        return r["amount_gbp"]

    out = {}
    for _, o in offers[offers["Outcome"] == "Signed"].iterrows():
        trust, uid = o["Trust"], int(uid_of[o["Trust"]])
        lic = book[(book["billing_basis"] == "Trust Licence") & (book["account_name"] == trust)]
        if len(lic):
            fee = float(led[led["agreement_ref"] == lic.iloc[0]["agreement_ref"]].apply(amt, axis=1).sum())
        else:
            fee = float(rem[rem["establishment_name"] == trust].iloc[0]["annual_contract_value_gbp"])
        rep = book[book["status"] == "Replaced by Trust Licence"].copy()
        rep["cur"] = rep["urn"].astype(int).map(lambda u: sm.get(u, u))
        rep = rep[rep["cur"].map(tcode) == uid]
        refs = set(rep["agreement_ref"])
        cn = led[led["document_type"] == "Credit note"]
        if credits == "agreement":
            cn = cn[cn["agreement_ref"].isin(refs) & (pd.to_datetime(cn["document_date"]) >= G.LICENCE_START)]
        elif credits == "any":
            invs = set(led[(led["document_type"] == "Invoice") & led["agreement_ref"].isin(refs)]["document_no"])
            cn = cn[cn["agreement_ref"].isin(refs) | cn["reference"].isin(invs)]
        else:
            cut = G.current_term_invoices(led, rep)
            cn = cn[cn["reference"].isin(cut)]
            if credits == "from_start":
                cn = cn[pd.to_datetime(cn["document_date"]) >= G.LICENCE_START]
        credit = -float(cn.apply(amt, axis=1).sum()) if len(cn) else 0.0
        out[trust] = dict(fee=round(fee, 2), credit=round(credit, 2), net=round(fee - credit, 2))
    return out


def ask_b_stops(d):
    base = G.ask_pilot(d)
    out = {}
    out["a filled VAT field read as on the new platform"] = pilot_variant(d, vat="field")
    out["amounts as recorded"] = pilot_variant(d, vat="none")
    out["every credit against the replaced terms' invoices"] = pilot_variant(d, credits="term")
    out["every credit on the replaced agreements"] = pilot_variant(d, credits="any")
    out["credits found by agreement reference"] = pilot_variant(d, credits="agreement")
    led = d["ledger"]
    res = {k: dict(v) for k, v in base.items()}
    for _, x in led[led["description"].str.startswith("Cancels", na=False)].iterrows():
        t = x["account_name"]
        res[t] = dict(fee=res[t]["fee"] + abs(x["amount_gbp"]), credit=res[t]["credit"] + abs(x["amount_gbp"]),
                      net=res[t]["net"])
    out["void counted as replacement"] = res
    rem = d["remit"]
    res2 = {k: dict(v) for k, v in base.items()}
    for k in res2:
        if k in set(rem["establishment_name"]):
            res2[k] = dict(fee=0.0, credit=res2[k]["credit"], net=-res2[k]["credit"])
    out["reseller invoice missed"] = res2
    return out


def usage_variant(d, sch, mode):
    """Ask C with the re-sent week read another way: "first" keeps the first load of a school's week, "both" keeps
    both loads, "rerun" lets the re-sent batch replace its whole week."""
    if mode in ("first", "both"):
        return G.ask_usage(d, sch, dedupe="first" if mode == "first" else False)
    u = d["usage"]
    rerun = u[u["batch_id"].str.endswith("-R1")]
    base_batch = rerun["batch_id"].str.replace("-R1", "", regex=False).iloc[0]
    return G.ask_usage(dict(d, usage=u[u["batch_id"] != base_batch]), sch)


def ask_c_stops(d):
    sch = G.schools_on_tallybridge(d)
    out = {}
    out["labels at face value"] = G.ask_usage(d, sch, face=True)
    out["first load of a school's week kept"] = usage_variant(d, sch, "first")
    out["both loads kept"] = usage_variant(d, sch, "both")
    out["re-sent batch replaces its week"] = usage_variant(d, sch, "rerun")
    out["framework left out"] = G.ask_usage(d, sch[~sch["channel"].str.startswith("framework")])
    out["only schools with usage this term counted"] = G.ask_usage(d, sch[sch["urn"].isin(used_this_term(d))])
    out["CRM pupils as exported"] = G.ask_usage(d, G.schools_on_tallybridge(d, crm_values=True))
    out["reseller lines summed"] = G.ask_usage(d, G.schools_on_tallybridge(d, fed="lines"))
    return out


def used_this_term(d):
    """Current URNs of the schools with at least one usage row in the six autumn weeks."""
    sm = G.successor_map(d["links"], d["est"])
    u = d["usage"].copy()
    u["monday"] = u["batch_id"].map(G.week_of_batch)
    u = u[(u["monday"] >= G.WEEK0) & (u["monday"] <= G.WEEK0 + pd.Timedelta(days=35))]
    return set(u["urn"].astype(int).map(lambda x: sm.get(x, x)))


def battery_sheets(d):
    """Answer sheets for the ask layer, scored against a reader who reads every sentence in every document, profiles
    every column and executes every filed rule and every symptom the habitual battery shows: duplicates dropped by
    agreement reference, split sites kept, successors followed, the reseller channel added at its margin, weeks read
    from their batch, the later load of a school's week kept, credits tied through the invoice they credit, the void
    netted. What it does not do is test an identity nothing invites: the CRM's billing fields against the invoices
    and the price list, the reseller's lines against the register's federations, an old-system document's VAT field
    one row at a time, or a credit note's date against the licence it is meant to be for.

    strict: that reader, executing the filed definitions (the book as invoiced, contracts once, the later load), but
    reading every amount with a VAT field beside it as net, the new platform's way, and taking every credit against
    the term each replaced agreement was in.
    strict_l: the same reader with the VAT ratio checked: every figure right but the credits. It is the floor against
    a solver that executes everything filed, not a pass condition.
    crm_reader: a reader who executes everything but takes pupils billed and recurring revenue from the CRM's columns
    of those names, and still takes every credit against the replaced terms.
    natural: the same solver without the battery: the re-sent week kept twice, weeks cut on their labels, the
    register read as its open schools, amounts as recorded, credits found by agreement reference."""
    st = dict(zip(d["est"]["URN"], d["est"]["EstablishmentStatus (name)"]))
    sch_v = G.schools_on_tallybridge(d, vat_as_net=True)
    strict = (G.ask_book(d, sch_v), pilot_variant(d, vat="field", credits="term"), G.ask_usage(d, sch_v))
    sch = G.schools_on_tallybridge(d)
    strict_l = (G.ask_book(d, sch), pilot_variant(d, vat="L", credits="term"), G.ask_usage(d, sch))
    sch_x = G.schools_on_tallybridge(d, crm_values=True, fed="lines")
    s_open = sch_x[sch_x["urn"].map(st) == "Open"]
    natural = (G.ask_book(d, s_open), pilot_variant(d, vat="none", credits="agreement"),
               G.ask_usage(d, s_open, face=True, dedupe=False))
    crm_reader = (G.ask_book(d, G.schools_on_tallybridge(d, crm_values=True)), pilot_variant(d, vat="L", credits="term"),
                  G.ask_usage(d, G.schools_on_tallybridge(d, crm_values=True)))
    return dict(strict=strict, strict_l=strict_l, natural=natural, crm_reader=crm_reader)


def criteria_matched(gold_a, gold_b, gold_c, a, b, c):
    """Count the graded figures a sheet gets right: pupils and revenue per book cell (one for an empty cell), the credit
    and the net per pilot licence, one per usage cell (one for an empty cell)."""
    hit = tot = 0
    for k, g in gold_a.items():
        if g["pupils"] == 0:
            tot += 1
            hit += a[k]["pupils"] == 0
            continue
        for f in ("pupils", "revenue"):
            tot += 1
            hit += a[k][f] == g[f]
    for k, g in gold_b.items():
        for f in ("credit", "net"):
            tot += 1
            hit += round(b[k][f]) == round(g[f])
    for k, g in gold_c.items():
        tot += 1
        hit += c[k] == g
    return hit, tot
