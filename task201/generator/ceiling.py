#!/usr/bin/env python3
"""task201 pair ceiling, measured on the cut pack.

    python3 generator/ceiling.py

Part 0 weights, unchanged so builds are comparable: a landed call banks 38 (recommendation and
critical components) plus 7 (instruction following); the asks carry 55. A wrong call keeps 5 of the
recommendation weight.

The two responses are scored from DIFFERENT readings of the same pack.

  cracker  the response that landed the call. It therefore has the pre-notification interval by
           section class, so the drill and every graded count are right. It read the dictionary, ran
           the hygiene battery (key uniqueness, exact duplicates, unmatched joins, fan-out, count
           ties) and executed every filed sentence it points at: PR-07's population, window, unit and
           drill, the register's padding convention, the archive's UTC column, the schedule's own
           issue note (so it uses the November revision, not the issued sheet) and the dictionary's
           note that the IVR left the device unwritten between 9 October and 2 November (so it
           resolves those rows through the customer register). It misses three inconsistencies that
           no sentence adjudicates and no sweep performs:
             A1  the grafik holds one row per scheduled job and the dispatch export one row per
                 interruption, so a visit that switched out two or three sections of one feeder is
                 one job and several rows; counting rows counts sections, not jobs
             A2  the contact centre wrote a second row under a fresh notification id when an agent
                 re-saved a ticket, same customer, same minute, same wording, so the key is unique
                 and the exact-duplicate sweep sees nothing
             A3  the preliminary return divided by the customer count at 30 September and the revised
                 one by the count at 31 October, so every untouched month moves by one constant
                 ratio and the October difference is the correction plus that ratio

  mirror   the strongest response that stopped at the default path: recorded customer-hours, which
           names Zanowiec. Its call is wrong. It misses the three inconsistencies as well, and it
           also takes the November windows from the issued sheet and leaves the IVR rows
           unresolved.

Every ask contributes scored figures to both rows. A figure is kept when the response's own path
lands within half the rounding unit the asking sentence states: half a count, 0.05 of an hour,
0.05 of a percentage point.
"""
import os, sys, json
import numpy as np, pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
TGT = os.path.join(TASK, "target")
W_REC, W_INSTR, W_ASK = 38.0, 7.0, 55.0
R_WRONG = 5.0
BR = ["ZAN", "PUS", "GRB", "NIE"]
CH = ["telefon", "IVR", "aplikacja"]


def norm_key(k):
    import re
    m = re.fullmatch(r"([A-Z]{3})-(\d+)-(\d+)/([A-Z])/(\d+)", str(k))
    return ("%s-%02d-%02d/%s/%02d" % (m.group(1), int(m.group(2)), int(m.group(3)),
                                      m.group(4), int(m.group(5)))) if m else str(k)


def load():
    leg = pd.read_csv(os.path.join(TGT, "awarie_oms_2026-10-01_2026-11-07.csv"), comment="#")
    cur = pd.read_csv(os.path.join(TGT, "awarie_oms_2026-11-01_2026-11-15.csv"), comment="#")
    leg = leg.rename(columns=dict(zdarzenie_id="id", linia_sn="linia", urzadzenie="dev",
                                  ts_poczatek="start", ts_zalaczenie="end"))
    cur = cur.rename(columns=dict(id_zdarzenia="id", id_linii="linia", id_urzadzenia="dev",
                                  rodzaj_wylaczenia="rodzaj", poczatek_lokalny="start",
                                  zalaczenie_lokalne="end"))
    c = ["id", "oddzial", "rejon", "linia", "dev", "rodzaj", "start", "end"]
    ev = pd.concat([leg[c], cur[c]], ignore_index=True).drop_duplicates("id")
    ev["start"] = pd.to_datetime(ev.start); ev["end"] = pd.to_datetime(ev.end)
    ev["key"] = ev.dev.map(norm_key)
    reg = pd.read_excel(os.path.join(TGT, "rejestr_urzadzen_sn_nn.xlsx"), sheet_name="urzadzenia")
    ev = ev.merge(reg[["id_urzadzenia", "odbiorcy_za_urzadzeniem"]],
                  left_on="key", right_on="id_urzadzenia", how="left")
    nl = pd.read_csv(os.path.join(TGT, "zgloszenia_klientow_2026.csv"), comment="#")
    ppe = pd.read_csv(os.path.join(TGT, "odbiorcy_ppe.csv"), comment="#")
    sch = pd.read_excel(os.path.join(TGT, "harmonogram_wylaczen_planowanych.xlsx"), sheet_name=None)
    xl = pd.read_excel(os.path.join(TGT, "sprawozdanie_URE_2026_wstepne_i_korekta.xlsx"),
                       sheet_name=None)
    return ev, reg, nl, ppe, sch, xl


def a1_path(ev, sch, nov_sheet, by_job):
    plan = ev[ev.rodzaj == "planowane"].copy()
    plan["godziny"] = (plan.odbiorcy_za_urzadzeniem *
                       (plan.end - plan.start).dt.total_seconds() / 3600.0)
    jobs = pd.concat([sch["pazdziernik_wydanie_1"], sch[nov_sheet]], ignore_index=True)
    jobs["okno_od"] = pd.to_datetime(jobs.okno_od); jobs["okno_do"] = pd.to_datetime(jobs.okno_do)
    plan = plan.sort_values("start"); jobs = jobs.sort_values("okno_od")
    plan = pd.merge_asof(plan, jobs[["okno_od", "okno_do", "id_pracy", "id_linii"]],
                         left_on="start", right_on="okno_od", left_by="linia", right_by="id_linii",
                         direction="backward", tolerance=pd.Timedelta(hours=26))
    plan = plan.dropna(subset=["id_pracy"])
    if by_job:
        g = plan.groupby("id_pracy").agg(oddzial=("oddzial", "first"), end=("end", "max"),
                                         okno_do=("okno_do", "max"), godziny=("godziny", "sum"))
        over = g[g.end > g.okno_do]
        counts = {b: int((over.oddzial == b).sum()) for b in BR}
        hours = round(float((over.end - over.okno_do).dt.total_seconds().sum() / 3600.0), 1)
        ch = {b: round(float(over[over.oddzial == b].godziny.sum()), 1) for b in BR}
    else:
        over = plan[plan.end > plan.okno_do]
        counts = {b: int((over.oddzial == b).sum()) for b in BR}
        hours = round(float((over.end - over.okno_do).dt.total_seconds().sum() / 3600.0), 1)
        ch = {b: round(float(over[over.oddzial == b].godziny.sum()), 1) for b in BR}
    return counts, hours, ch


def a2_path(nl, reg, ppe, dedup, resolve):
    d = nl.copy()
    if dedup:
        d = d.drop_duplicates(["nr_ppe", "ts_przyjecia", "opis", "kanal"])
    orph = d[d.id_zdarzenia.isna()].copy()
    dev_br = dict(zip(reg.id_urzadzenia, reg.oddzial))
    dev_cu = dict(zip(reg.id_urzadzenia, reg.odbiorcy_za_urzadzeniem))
    pm = dict(zip(ppe.nr_ppe, ppe.id_urzadzenia))
    if resolve:
        orph["dev"] = orph.id_urzadzenia.fillna(orph.nr_ppe.map(pm))
    else:
        orph["dev"] = orph.id_urzadzenia
    orph["br"] = orph.dev.map(dev_br)
    g = orph.groupby(["br", "kanal"]).size()
    counts = {"%s|%s" % (b, c): int(g.get((b, c), 0)) for b in BR for c in CH}
    total = int(len(orph)) if resolve else int(orph.br.notna().sum())
    cu = orph.dev.map(dev_cu).groupby(orph.br).sum()
    cust = {b: int(cu.get(b, 0)) for b in BR}
    return counts, total, cust


def a3_path(xl, rebase):
    pre, rev = xl["wstepne_2026"], xl["korekta_1_2026"]
    m = rev.miesiac != "2026-10"
    ratio = float(pre[m].saidi_planowane_min_na_odb.sum() / rev[m].saidi_planowane_min_na_odb.sum()) if rebase else 1.0
    out = {}
    for v in ["SN", "nN"]:
        a = float(rev[(rev.miesiac == "2026-10") & (rev.poziom == v)].saidi_awaryjne_min_na_odb.iloc[0])
        b = float(pre[(pre.miesiac == "2026-10") & (pre.poziom == v)].saidi_awaryjne_min_na_odb.iloc[0]) / ratio
        out["%s|min" % v] = round(a - b, 1)
        out["%s|pct" % v] = round((a - b) / b * 100.0, 1)
    return out


def score(golden, got, tol):
    return 1 if abs(float(golden) - float(got)) <= tol else 0


def main():
    figs = json.load(open(os.path.join(HERE, "figures.json")))
    g1, g2, g3 = figs["a1"], figs["a2"], figs["a3"]["korekta_pazdziernik"]
    ev, reg, nl, ppe, sch, xl = load()

    rows = {}
    # the cracker: revision sheet, row grain, resolves the IVR gap, no re-save dedup, no re-basing
    rows["cracker"] = dict(
        a1=a1_path(ev, sch, "listopad_wydanie_2", by_job=False),
        a2=a2_path(nl, reg, ppe, dedup=False, resolve=True),
        a3=a3_path(xl, rebase=False))
    # the mirror: issued sheet, row grain, no resolution, no dedup, no re-basing
    rows["mirror"] = dict(
        a1=a1_path(ev, sch, "listopad_wydanie_1", by_job=False),
        a2=a2_path(nl, reg, ppe, dedup=False, resolve=False),
        a3=a3_path(xl, rebase=False))

    out = {}
    for name, r in rows.items():
        hits, tot, detail = 0, 0, []
        c, h, ch = r["a1"]
        tot += 1; k = score(g1["prac_przekroczonych_total"], sum(c.values()), 0.5); hits += k
        detail.append(("a1.jobs_over_total", g1["prac_przekroczonych_total"], sum(c.values()), k))
        tot += 1; k = score(g1["przekroczenie_godz_total"], h, 0.05); hits += k
        detail.append(("a1.hours_over", g1["przekroczenie_godz_total"], h, k))
        for b in BR:
            tot += 1; k = score(g1["godziny_prac_przekroczonych"][b], ch[b], 0.05); hits += k
            detail.append(("a1.cust_hours.%s" % b, g1["godziny_prac_przekroczonych"][b], ch[b], k))
        cc, ct, cu = r["a2"]
        for key, v in sorted(g2["bez_zdarzenia"].items()):
            tot += 1; k = score(v, cc.get(key, 0), 0.5); hits += k
            detail.append(("a2.%s" % key, v, cc.get(key, 0), k))
        tot += 1; k = score(g2["bez_zdarzenia_total"], ct, 0.5); hits += k
        detail.append(("a2.total", g2["bez_zdarzenia_total"], ct, k))
        for b in BR:
            tot += 1; k = score(g2["odbiorcy_za_urzadzeniami"][b], cu[b], 0.5); hits += k
            detail.append(("a2.customers.%s" % b, g2["odbiorcy_za_urzadzeniami"][b], cu[b], k))
        for key in ["SN|min", "SN|pct", "nN|min", "nN|pct"]:
            tot += 1; k = score(g3[key], r["a3"][key], 0.05); hits += k
            detail.append(("a3.%s" % key, g3[key], r["a3"][key], k))
        out[name] = (hits, tot, detail)

    print("ask figures scored from each response's own reading\n")
    for name in ["cracker", "mirror"]:
        hits, tot, detail = out[name]
        print("%s: keeps %d of %d ask figures" % (name, hits, tot))
        for lab, gold, got, k in detail:
            if k:
                print("    KEPT %-26s golden %s, response %s" % (lab, gold, got))
        print()
    ck, ctot, _ = out["cracker"]; mk, mtot, _ = out["mirror"]
    Lc, Lm = ck / ctot, mk / mtot
    C = W_REC + W_INSTR + W_ASK * Lc
    S = R_WRONG + W_INSTR + W_ASK * Lm
    print("cracker lands the call:  38 + 7 + 55 x %.4f = %.1f" % (Lc, C))
    print("mirror misses the call:   5 + 7 + 55 x %.4f = %.1f" % (Lm, S))
    print("\nPair ceiling: %.1f" % ((C + S) / 2.0))
    print("Mirror leakage: %.1f per cent of ask weight" % (100 * Lm))
    print("\nThe asks consume nothing the call's construction produces (A1 reads only planned rows, "
          "A2 only notifications no interruption matches, A3 only the concession returns), so the "
          "two rows are scored from different device readings rather than from the same list; "
          "generator/checks.py sep.a1, sep.a2_rows, sep.a2_volume and sep.a3 assert the separation.")


if __name__ == "__main__":
    main()
