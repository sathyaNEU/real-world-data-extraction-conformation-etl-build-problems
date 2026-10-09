"""Ask-layer assertions (DESIGN_NOTE.md, Assertion plan 34 to 47), on the files as written."""
import re

import numpy as np
import openpyxl
import pandas as pd

import askcheck as AC
from common import k_top

A1_FLOOR = 1.0       # every stop and every composed subset at least 1 per cent from the golden
A1_TARGET = 1.2


def read_paper(path):
    rows = []
    for line in open(path, encoding="ascii"):
        line = line.rstrip("\n")
        rows.append((int(line[0:6]), int(line[6:10]), int(line[10:19]), int(line[19:28]), int(line[28:32]),
                     int(line[32:43]), int(line[43:53]), line[53:61], line[61:63]))
    return pd.DataFrame(rows, columns=["batch", "seq", "employer_ein", "employee_tin", "tax_year", "state_wages",
                                       "state_tax_withheld", "keyed", "keyer"])


def load(tgt, FILES):
    led = pd.read_parquet(tgt / FILES["ledger"])
    led["source_ref"] = led.source_ref.fillna("")
    ri = pd.read_csv(tgt / FILES["returned"], dtype={"represented_result": str}).fillna({"represented_result": ""})
    reg = pd.read_csv(tgt / FILES["register"])
    reg["resolved_tin"] = reg.resolved_tin.fillna(0).astype(np.int64)
    ef = pd.read_parquet(tgt / FILES["efile"])
    pp = read_paper(tgt / FILES["paper"])
    ext = pd.read_csv(tgt / FILES["schd"])
    log = pd.read_csv(tgt / FILES["amended"])
    return led, ri, reg, ef, pp, ext, log


def rel(v, g):
    return 100.0 * (v - g) / g


def run(K, W, RS, SS, A, tgt, FILES, texts):
    rec = {}
    led, ri, reg, ef, pp, ext, log = load(tgt, FILES)
    r25, s25 = RS[2025], SS[2025]
    rt, tt, tagi, fl = AC.membership(r25, s25)
    rtF, ttF, tagiF, flF = AC.membership(r25, s25, unit="ffu")
    K(fl == [214_000, 318_000, 742_000] and flF == [197_000, 293_000, 594_000], "a34.tier_floors")
    # (34) goldens
    g1 = AC.receipts(led, ri, reg, tt)
    g2 = AC.gains(ext, log, rt)
    sh = AC.share_exact(g2, tagi)
    g3 = AC.withholding(ef, pp, reg, tt)
    K(len(g1) == 12 and len(g2) == 3 and len(g3) == 3 and all(v > 0 for v in list(g1.values()) + list(g2.values()) + list(g3.values())), "a34.goldens")
    rec["asks"] = {"A1_receipts": {f"tier{t} inst{k}": v for (t, k), v in sorted(g1.items())},
                   "A2_net_capital_gain": {f"tier{t}": g2[t] for t in (1, 2, 3)},
                   "A2_share_pct": {f"tier{t}": round(sh[t], 1) for t in (1, 2, 3)},
                   "A2_share_exact": {f"tier{t}": round(sh[t], 4) for t in (1, 2, 3)},
                   "A3_withholding": {f"tier{t}": g3[t] for t in (1, 2, 3)},
                   "tier_agi": tagi}
    # (35) stops S1 to S4 per figure
    stops = {}
    s1 = AC.receipts(led, ri, reg, tt, clock=False, xfer=False, returned=False, register=False)
    s2 = AC.receipts(led, ri, reg, tt, clock=True, xfer=False, returned=False, register=False)
    s3 = AC.receipts(led, ri, reg, tt, overclean=True)
    s4 = AC.receipts(led, ri, reg, ttF)
    for lab, s in (("S1", s1), ("S2", s2), ("S3", s3), ("S4", s4)):
        d = {c: rel(s[c], g1[c]) for c in g1}
        for c, x in d.items():
            K(abs(x) >= A1_FLOOR, f"a35.A1.{lab}.{c}", x)
        stops[f"A1.{lab}"] = (round(min(d.values()), 2), round(max(d.values()), 2))
    t2 = {"S1": AC.gains(ext, log, rt, versions=False, loss_limit=False), "S2": AC.gains(ext, log, rt, versions=True, loss_limit=False),
          "S3": AC.gains(ext, log, rt, original=True), "S4": AC.gains(ext, log, rtF)}
    for lab, s in t2.items():
        d = {t: rel(s[t], g2[t]) for t in g2}
        ag = tagiF if lab == "S4" else tagi
        sv = AC.share_exact(s, ag)
        for t in (1, 2, 3):
            K(abs(d[t]) >= (4.0 if lab == "S1" else A1_FLOOR), f"a35.A2.{lab}.{t}", d[t])
            K(round(sv[t], 1) != round(sh[t], 1), f"a35.A2share.{lab}.{t}", (sv[t], sh[t]))
            if lab == "S1":
                K(abs(sv[t] - sh[t]) >= 0.3, f"a35.A2share_lazy.{t}", (sv[t], sh[t]))
        stops[f"A2.{lab}"] = {t: round(d[t], 2) for t in d}
    t3 = {"S1": AC.withholding(ef, pp, reg, tt, paper_on=False, register=False), "S2": AC.withholding(ef, pp, reg, tt, paper_on=True, register=False),
          "S3": AC.withholding(ef, pp, reg, tt, overclean=True), "S4": AC.withholding(ef, pp, reg, ttF)}
    for lab, s in t3.items():
        d = {t: rel(s[t], g3[t]) for t in g3}
        for t in (1, 2, 3):
            K(abs(d[t]) >= (3.0 if lab == "S1" else A1_FLOOR), f"a35.A3.{lab}.{t}", d[t])
        stops[f"A3.{lab}"] = {t: round(d[t], 2) for t in d}
    rec["stops"] = stops
    # (36) composed subsets of mishandlings, every figure
    worst = {"A1": 99.0, "A2": 99.0, "A3": 99.0}
    single = {}
    for sub in AC.subsets(AC.A1_DEVICES):
        v = AC.receipts(led, ri, reg, tt, **{d: (d not in sub) for d in AC.A1_DEVICES})
        for c in g1:
            if v[c] != g1[c]:
                x = abs(rel(v[c], g1[c]))
                K(x >= A1_FLOOR, f"a36.A1.{'+'.join(sub)}.{c}", x)
                worst["A1"] = min(worst["A1"], x)
        if len(sub) == 1:
            single[sub[0]] = {f"{c[0]}{c[1]}": round(rel(v[c], g1[c]), 2) for c in g1}
    for sub in AC.subsets(AC.A2_DEVICES):
        v = AC.gains(ext, log, rt, **{d: (d not in sub) for d in AC.A2_DEVICES})
        sv = AC.share_exact(v, tagi)
        for t in (1, 2, 3):
            x = abs(rel(v[t], g2[t]))
            K(x >= A1_FLOOR and round(sv[t], 1) != round(sh[t], 1), f"a36.A2.{'+'.join(sub)}.{t}", (x, sv[t]))
            worst["A2"] = min(worst["A2"], x)
        if len(sub) == 1:
            single[sub[0] + "(A2)"] = {t: round(rel(v[t], g2[t]), 2) for t in (1, 2, 3)}
    for sub in AC.subsets(AC.A3_DEVICES):
        v = AC.withholding(ef, pp, reg, tt, **{d: (d not in sub) for d in AC.A3_DEVICES})
        for t in (1, 2, 3):
            x = abs(rel(v[t], g3[t]))
            K(x >= A1_FLOOR, f"a36.A3.{'+'.join(sub)}.{t}", x)
            worst["A3"] = min(worst["A3"], x)
        if len(sub) == 1:
            single[sub[0] + "(A3)"] = {t: round(rel(v[t], g3[t]), 2) for t in (1, 2, 3)}
    rec["worst_subset_delta_pct"] = {k: round(v, 2) for k, v in worst.items()}
    rec["single_device_effects_pct"] = single
    # (37) separation: the main call reads no ask file and no ask column; zeroing the credit
    # election column and dropping every ask file leaves households, floors and hit counts as they are
    import constructions as C
    r0 = r25.copy()
    r0["overpayment_credit_elect"] = 0
    r0["state_taxable_income"] = 0
    u0 = C.units(r0, s25, "code1", "ffu", "attached")
    K(len(u0) == 582_544 and [round(x / 1000.0) * 1000 for x in C.nearest_rank_floors(u0.agi)] == [214_000, 318_000, 742_000], "a37.separation")
    main_cols = {"return_id", "filer_tin", "federal_primary_tin", "residency_code", "county_code", "federal_agi"}
    K(main_cols.isdisjoint({"txn_id", "account_tin", "employee_tin", "amount_in_agi", "net_gain_loss", "state_tax_withheld"}), "a37.columns")
    # (38) necessity matrix: each device alone moves only its asks
    K(all(abs(x) > 0 for c, x in single["clock"].items()), "a38.clock_moves_A1")
    K(all(single["xfer"][f"{t}{k}"] == 0 for t in (1, 2, 3) for k in (3, 4)) and all(abs(single["xfer"][f"{t}{k}"]) >= A1_FLOOR for t in (1, 2, 3) for k in (1, 2)), "a38.xfer_april_june_only")
    K(all(abs(x) >= A1_FLOOR for x in single["returned"].values()), "a38.returned_every_cell")
    K(all(abs(x) >= A1_FLOOR for x in single["register"].values()) and all(abs(x) >= A1_FLOOR for x in single["register(A3)"].values()), "a38.register_A1_A3")
    K(all(abs(x) >= A1_FLOOR for x in single["versions(A2)"].values()) and all(abs(x) >= A1_FLOOR for x in single["loss_limit(A2)"].values()), "a38.A2_devices")
    K(all(abs(x) >= 3.0 for x in single["paper_on(A3)"].values()), "a38.paper_channel")
    # (39) hygiene battery on the wrong paths comes back clean
    K(led.txn_id.is_unique and not led.duplicated().any(), "a39.ledger_keys")
    refs = led.source_ref[led.txn_type == "TRF"]
    r24ids = set(RS[2024].return_id.astype(str))
    txset = set(led.txn_id.astype(str))
    K(refs.apply(lambda s: s in r24ids or (len(s) == 11 and s in txset)).all(), "a39.transfer_refs_resolve")
    K(ri.txn_id.isin(led.txn_id).all() and ri.txn_id.is_unique, "a39.returned_join")
    K(ef.statement_id.is_unique and not ef.duplicated().any() and not pp.duplicated().any(), "a39.statement_keys")
    K(ext.return_id.is_unique and ext.return_id.isin(r25.return_id).all() and log.return_id.isin(r25.return_id).all(), "a39.schedule_joins")
    K(not log.duplicated(["return_id", "amendment_seq"]).any(), "a39.log_keys")
    K(reg.reported_tin.is_unique, "a39.register_keys")
    # a household's records: no wage statement or payment belongs to a dependent who does not file
    nonfiling = set(s25.dependent_tin) - set(r25.filer_tin)
    ok = reg[reg.case_status == "RESOLVED"]
    rmap = dict(zip(ok.reported_tin, ok.resolved_tin))
    owners = [rmap.get(t, t) for t in pd.concat([ef.employee_tin, pp.employee_tin, led.account_tin]).astype("int64")]
    K(not nonfiling & set(owners), "a39.no_records_for_nonfiling_dependents")
    raw = set(pd.concat([ef.employee_tin, pp.employee_tin, led.account_tin, reg.reported_tin]).astype("int64"))
    listed = set(s25.dependent_tin.astype("int64"))
    for yy in (2022, 2023, 2024):
        listed |= set(SS[yy].dependent_tin.astype("int64"))
    K(not raw & (listed - set(r25.filer_tin)), "a39.reported_tins_clear_of_listed_dependents")
    # (40) over-cleaners land off the golden (S3 above)
    K(all(abs(rel(s3[c], g1[c])) >= A1_FLOOR for c in g1), "a40.A1_overclean")
    # (41) fairness: the version of record agrees with the returns file's AGI
    acc = log[log.disposition == "ACCEPTED"].sort_values(["return_id", "amendment_seq"]).groupby("return_id").tail(1)
    agi_of = r25.set_index("return_id").federal_agi
    K((acc.federal_agi.to_numpy() == agi_of.loc[acc.return_id].to_numpy()).all(), "a41.version_of_record_ties")
    cr = led[(led.txn_type == "TRF") & (led.source_ref.str.len() == 10)]
    ce = RS[2024].set_index("return_id").overpayment_credit_elect
    K((cr.amount.to_numpy() == ce.loc[cr.source_ref.astype(np.int64)].to_numpy()).all() and (ce > 0).sum() == len(cr), "a41.credit_elect_antidote")
    # (42) boundary households carry nothing the asks read; asks identical under rank membership
    bound_check(K, r25, s25, led, ef, pp, reg, ext, rt)
    # (43) shares sit off the rounding edges and are not round figures
    for t in (1, 2, 3):
        frac = (sh[t] * 10) % 1
        K(abs(frac - 0.5) >= 0.2, f"a43.share_edge.{t}", sh[t])
        K(round(sh[t], 1) * 10 % 10 != 0, f"a43.share_not_round.{t}", sh[t])
        K(min(frac, 1 - frac) >= 0.1, f"a43.share_off_round_value.{t}", sh[t])
    # (44) the referee: the reconciliation summary equals the two channels exactly
    wb = openpyxl.load_workbook(tgt / FILES["recon"], data_only=True)
    ws = wb.active
    rows = {r[0]: r for r in ws.iter_rows(min_row=5, values_only=True) if r[0]}
    K(rows["Electronic (platform)"][4] == int(ef.state_tax_withheld.sum()) and rows["Paper (capture vendor)"][4] == int(pp.state_tax_withheld.sum()), "a44.referee_channels")
    K(rows["All channels"][4] == int(ef.state_tax_withheld.sum() + pp.state_tax_withheld.sum()), "a44.referee_total")
    K(rows["Electronic (platform)"][2] == len(ef) and rows["Paper (capture vendor)"][2] == len(pp), "a44.referee_counts")
    # (45) no marker isolates device rows
    marker_check(K, led, ri, ef, pp, reg)
    # (46) oracle sweep: no shipped figure equals a tier-level golden
    gold_vals = set(g1.values()) | set(g2.values()) | set(g3.values())
    for name, t in texts.items():
        nums = set(int(x.replace(",", "")) for x in re.findall(r"(?<![\d.])\d[\d,]{5,}(?![\d.])", t))
        K(not (nums & gold_vals), f"a46.oracle.{name}")
    for col in ("amount",):
        K(not set(led[col].abs()) & gold_vals, "a46.oracle.ledger")
    K(not set(ef.state_tax_withheld) & gold_vals and not set(pp.state_tax_withheld) & gold_vals, "a46.oracle.statements")
    # (47) every device's organ stated once; no file narrates a device
    once = {"UTC": "research_extract_record_layouts.txt", "11:59:59 pm Central": "research_extract_record_layouts.txt",
            "version of record": "research_extract_record_layouts.txt", "two channels": "research_extract_record_layouts.txt",
            "credited from a prior year's return": "income_tax_tier_methodology.pdf",
            "amount entering AGI": "income_tax_tier_methodology.pdf", "employers' wage statements": "income_tax_tier_methodology.pdf",
            "latest version of the schedule received": "research_extract_record_layouts.txt",
            "recorded as received": "research_extract_record_layouts.txt"}
    norm = {k: re.sub(r"\s+", " ", v) for k, v in texts.items()}
    for phrase, home in once.items():
        n = {k: v.count(phrase) for k, v in norm.items() if v.count(phrase)}
        K(n == {home: 1}, f"a47.once.{phrase}", n)
    for word in ("misapplied", "dishonour", "loss limit", "keyed wrong", "typo", "late evening", "rolled", "duplicate", "missing statements"):
        for k, v in norm.items():
            K(word not in v.lower(), f"a47.narration.{word}.{k}")
    return rec


def bound_check(K, r25, s25, led, ef, pp, reg, ext, rt):
    import constructions as C
    u = C.units(r25, s25, "code1", "ffu", "attached")
    v = u.sort_values("agi", ascending=False, kind="stable").reset_index(drop=True)
    keys = set()
    for p in (10, 5, 1):
        k = k_top(len(v), p)
        keys.update(v.key.iloc[k - 3:k + 2].tolist())
    res = r25[r25.residency_code == 1]
    rid = res.return_id[res.federal_primary_tin.isin(keys)]
    tins = set(res.filer_tin[res.federal_primary_tin.isin(keys)]) | set(res.spouse_tin[res.federal_primary_tin.isin(keys)]) - {0}
    ok = reg[reg.case_status == "RESOLVED"]
    rmap = dict(zip(ok.reported_tin, ok.resolved_tin))
    def owner(t):
        return rmap.get(t, t)
    K(not led.account_tin.map(owner).isin(tins).any(), "a42.boundary_no_payments")
    K(not ef.employee_tin.map(owner).isin(tins).any() and not pp.employee_tin.map(owner).isin(tins).any(), "a42.boundary_no_statements")
    K(not ext.return_id.isin(rid).any(), "a42.boundary_no_schedule")
    K(not s25.claimant_return_id.isin(rid).any() or not res.filer_tin.isin(s25.dependent_tin[s25.claimant_return_id.isin(rid)]).any(), "a42.boundary_no_filing_dependents")


def marker_check(K, led, ri, ef, pp, reg):
    L = led[(led.tax_year == 2025) & (led.txn_type == "ES")]
    late_utc = AC.instalment(L.txn_utc.to_numpy(), False) != AC.instalment(L.txn_utc.to_numpy(), True)
    K(L.channel[late_utc].nunique() >= 2 and L.channel[~late_utc].nunique() >= 2, "a45.clock_rows_blend")
    rch = led.set_index("txn_id").channel.loc[ri.txn_id]
    tot_ch = led[led.txn_type == "ES"].channel.value_counts()
    share = (rch.value_counts() / tot_ch.loc[rch.value_counts().index]).max()
    K(rch.nunique() >= 2 and share < 0.15, "a45.returned_rows_blend", share)
    mis = led.account_tin.isin(reg.reported_tin)
    K(led.channel[mis & (led.txn_type == "ES")].nunique() >= 2, "a45.register_rows_blend")
    K(ef.employee_tin.isin(reg.reported_tin).sum() > 0 and pp.employee_tin.isin(reg.reported_tin).sum() > 0, "a45.register_both_channels")
    K(ef.employer_ein.isin(pp.employer_ein).sum() > 0, "a45.channels_share_employers")
