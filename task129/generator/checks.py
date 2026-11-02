"""task129 checks: the input gates, the three rules executed on the clean truth (R1 to R3c), the ladder's rungs, the
contractor and regrowth comparisons, the major event days, the semantic fork rows (SF1 to SF10), Layer 1 neutrality,
the ask devices and their separation from the call, the registers, the distractors and the realism sweep"""
import hashlib
import json
import os
import re
import zipfile

import numpy as np
import pandas as pd

import estim as E
import params as P

PEOPLE = ["Lori Rodriguez", "Dennis Garcia", "Wesley Thomas", "Brian Montgomery"]
# the 10-14 pack (target.zip d6bd8f7d): the files the main call reads, byte for byte
SHIPPED = {
    "trim_unit_register.csv": "7b6aee0f96161681a96f76816dfb21c684f61ee3383a234419d35e381c53e9b5",
    "row_tree_survey_2023-2024.parquet": "f3f4833ef51450982ee240086c8d197b137c87fa5b49b8695709c2fb2090d36c",
    "weather_daily_2016-2025.csv": "1e193cec91ab1b3f362cd36701e991a0f6daa2c4bffc63fde0098e3c3aae1b72",
    "member_counts_2015-2025.csv": "0a5600277dca33551d5c758b1e1176b6e6fafe283bafbdef0654c44ef90e3144",
    "trimming_contracts_register.xlsx": "ec4ab99d4d546bbbc1cd76b3efd5df08f2b316c65b8730c495220fea3b309c70",
    "right_of_way_maintenance_policy.pdf": "b68d87ed5d2e4f07786226351f5cd72e5e7e44ded3602a0df6eaebf3ea39a19b",
    "reliability_reporting_policy.docx": "57810d034e7bf548cff50aa15e48d34fe97596e2448997e22d48bd8c1bbb82bd",
    "statewide_cooperative_reliability_2020-2024.csv": "74d73e9ddd58368ff6d739a2ab037c3950f063627e1d6fd857ad4a7d3740179b",
    "ami_momentary_events_2025.csv": "c16acc2b23560a1cd5051a19a5d28fd2a7045f231042d4037e1265ba983ec3f2",
}
SHIPPED_EXPORT = "c4115fa1a11ab72e370e17f1c7ca4de90f5a8f7eb62d97b2648a12b4a43c846d"
# the completions less their record number (the one column the call never reads, renumbered at the 11-02 leak read)
SHIPPED_COMPLETIONS = "386ee725ab187f2f4ec885f7283bbbfa8271d76f746a7aa05f445b465a904a32"


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def docx_text(p):
    with zipfile.ZipFile(p) as z:
        return " ".join(re.findall(r"<w:t[^>]*>([^<]*)</w:t>", z.read("word/document.xml").decode("utf-8")))


def pdf_text(p):
    from pypdf import PdfReader
    return " ".join(pg.extract_text() for pg in PdfReader(p).pages)


def bin_dist(x, step=0.1):
    """distance of a value from the nearest rounding edge at the given step"""
    k = x / step
    return abs((k - np.floor(k)) - 0.5) * step


def run(target, golden, res, A, D, ev, collect=None):
    n = [0]

    def ok(c, label):
        if collect is not None and not c:
            collect.append(label)
            return
        assert c, label
        n[0] += 1

    files = sorted(os.listdir(target))
    task = os.path.dirname(target)
    meta = json.load(open(os.path.join(task, "metadata.json")))
    # ---------------------------------------------------------------- input gates
    ok(len(files) >= 10, "gate: 10 or more files")
    ok(len({f.rsplit(".", 1)[1] for f in files}) >= 3, "gate: 3 or more formats")
    ok(max(res["counts"]["survey"], res["counts"]["outages"], res["counts"]["completions"]) >= 25000,
       "gate: a file of 25,000 rows or more")
    ok(len(meta["distractor_files"]) >= 2 and all(d in files for d in meta["distractor_files"]), "gate: two distractors")
    ok(not any("distractor" in f.lower() for f in files), "gate: no file named after its role")
    # ---------------------------------------------------------------- R1: the field's raw material ships
    X = D["X"]
    ok(set(["start_local", "step", "step_restored_local", "members_restored", "unit_id", "cause_code"]) <= set(X.columns),
       "R1: the outage export ships at restoration-step grain with the unit and cause")
    ok({"unit_id", "completed_date", "audit_status", "contractor"} <= set(D["T"].columns),
       "R1: the trimming history ships unit by unit with its contractor")
    ok({"span_id", "species_code", "trees_within_falling_distance"} <= set(D["S"].columns),
       "R1: the span survey ships by species")
    for f in files:
        if f.endswith(".csv"):
            head = open(os.path.join(target, f), encoding="utf-8").readline().lower()
            ok(not any(w in head for w in ("growth", "fall_in", "beyond", "driver", "rate")),
               "R1: no column names a driver or holds a rate (%s)" % f)
    ok("cause_code" in X.columns and set(X.cause_code.unique()) <= {"TREE", "ANIMAL", "EQUIPMENT", "LIGHTNING", "VEHICLE",
                                                                     "UNKNOWN", "PLANNED"},
       "R1: one TREE code; nothing separates a tree growing in from one falling in")
    # ---------------------------------------------------------------- the clean truth (generator side)
    O, K = res["O"], res["K"]
    O = O.assign(year=[s.year for s in O.start])
    dur = np.array([m[-1] for m in O.steps_min])
    clean = O[(O.cause == "TREE") & (O.level == "PRIMARY") & (dur > 5) & (~O.storm)]
    mi = {y: E.miles_avg(D["R"], y) for y in range(2021, 2026)}
    truth_rate = {y: {d: 100.0 * ((clean.year == y) & (clean.district == d)).sum() / mi[y][d] for d in E.DISTRICTS}
                  for y in range(2021, 2026)}
    t_rise = {d: truth_rate[2025][d] - np.mean([truth_rate[y][d] for y in E.BASE]) for d in E.DISTRICTS}
    ok(max(t_rise, key=t_rise.get) == "North", "truth: North carries the largest rise")
    by_kind = clean.groupby(["year", "district", "kind"]).size()
    kr = lambda y, d, k: by_kind.get((y, d, k), 0) / mi[y][d] * 100.0
    fall_rise = {d: kr(2025, d, "fall") - np.mean([kr(y, d, "fall") for y in E.BASE]) for d in E.DISTRICTS}
    grow_rise = {d: kr(2025, d, "grow") - np.mean([kr(y, d, "grow") for y in E.BASE]) for d in E.DISTRICTS}
    tot = sum(t_rise[d] * mi[2025][d] for d in E.DISTRICTS)
    ok(fall_rise["North"] * mi[2025]["North"] / tot >= 0.6,
       "truth: North's falling-in rise is %.2f of the cooperative's rise" % (fall_rise["North"] * mi[2025]["North"] / tot))
    ok(grow_rise["East"] > 0 and fall_rise["East"] < 0.5 * grow_rise["East"] + 1.0,
       "truth: East's rise is growing-in on the regrowth clock")
    # R3a: the default path on the clean truth files the re-bid
    lead = max(t_rise, key=t_rise.get)
    ok(lead in E.HANDOVER, "R3a: the district carrying the rise changed contractor (the default path files a re-bid)")
    ok(A["default"] == "contractor", "R3a: on the bundle, the default path files %s" % A["default"])
    # R3b: the decisive step alone files the golden
    ok(A["call"] == "beyond", "R3b: the decisive step files hazard-tree removal (got %s)" % A["call"])
    # R3c: no plant
    rel = docx_text(os.path.join(target, "reliability_reporting_policy.docx"))
    row = pdf_text(os.path.join(target, "right_of_way_maintenance_policy.pdf"))
    for txt, name in ((rel, "reliability policy"), (row, "right-of-way policy")):
        ok(not re.search(r"\b(ash|dieback|mortality|emerald)\b", txt, re.I), "R3c: the %s names no tree disease" % name)
        ok("2025" not in txt and "Garrity" not in txt, "R3c: the %s names no year's rise and no contractor" % name)
    ok("6.3 Hazard-tree removal answers trees falling onto the line from beyond the right-of-way" in row.replace("\n", " "),
       "SF7: the right-of-way policy assigns each driver its programme")
    # ---------------------------------------------------------------- the rungs and comparisons (bundle side)
    bb = ev["by_band"]["North"]
    base = bb.loc[list(E.BASE)].mean()
    now = bb.loc[E.YEAR]
    rises = [now[b] - base[b] for b in range(4)]
    ok(min(rises) > 6.0, "decisive: North's 2025 rate rose at every time since trim (min %.1f)" % min(rises))
    mr = float(np.mean(rises))
    ok(all(0.75 * mr <= x <= 1.25 * mr for x in rises),
       "decisive: North's 2025 rise is alike at every time since trim (%s)" % [round(x, 1) for x in rises])
    tN, EN = ev["t"][ev["t"].district == "North"], ev["E"][ev["E"].district == "North"]

    def pooled_rise(bands):
        r_ = lambda y: tN[(tN.year == y) & tN.band.isin(bands)].shape[0] / EN[(EN.yr == y) & EN.band.isin(bands)].mi_yr.sum()
        return 100.0 * (r_(E.YEAR) - np.mean([r_(y) for y in E.BASE]))
    yo = pooled_rise([0, 1]) / pooled_rise([2, 3])
    ok(0.85 <= yo <= 1.18, "decisive: the rise within two years of a trim is the rise two to four years after (%.2f)" % yo)
    std = ev["std"]
    for c in (E.OUTGOING, E.INCOMING):
        ok(0.85 <= std[c][2] <= 1.15, "contractor: %s's units fail at %.2f times North's 2025 rate at their time since trim"
           % (c, std[c][2]))
        ok(bin_dist(std[c][2], 0.01) >= 0.0005, "bins: %s's standardised ratio sits inside its two-decimal bin" % c)
    ok(min(std[c][0] for c in std) >= 40, "contractor: the standardised comparison holds forty outages a side")
    same = ev["same"]
    ratio = same[E.INCOMING][2] / same[E.OUTGOING][2]
    ok(0.80 <= ratio <= 1.25, "contractor: units each firm trimmed during 2024 fail alike in 2025 (ratio %.2f)" % ratio)
    cb = ev["by_con_band"]
    for b in (0, 1):
        r_ = cb.loc[E.INCOMING, b] / cb.loc[E.OUTGOING, b]
        ok(0.75 <= r_ <= 1.33, "contractor: at %s years since trim the firms' 2025 rates are %.2f apart" % (E.BAND_NAMES[b], r_))
    ba = ev["by_ash"]
    ash_rise = [ba.loc[E.YEAR, q] - ba.loc[list(E.BASE), q].mean() for q in range(4)]
    ok(ash_rise[3] >= 2.0 * max(ash_rise[0], 1.0) and ash_rise[3] > ash_rise[1],
       "decisive: North's rise climbs with the ash share (%s)" % [round(x, 1) for x in ash_rise])
    sh = ev["shares"]
    ok(sh["trees beyond the right-of-way (North)"] >= 0.6, "ladder: North's shift is %.2f of the rise" %
       sh["trees beyond the right-of-way (North)"])
    ok(0.05 <= sh["units past the cycle (East)"] <= 0.35 and sh["weather (South)"] <= 0.25,
       "ladder: East's units past the cycle and South's weather carry the rest (%.2f, %.2f)"
       % (sh["units past the cycle (East)"], sh["weather (South)"]))
    eb = ev["by_band"]["East"]
    Ee = ev["E"]
    past25 = Ee[(Ee.district == "East") & (Ee.yr == E.YEAR) & (Ee.band == 4)].mi_yr.sum()
    pastb = np.mean([Ee[(Ee.district == "East") & (Ee.yr == y) & (Ee.band == 4)].mi_yr.sum() for y in E.BASE])
    ok(past25 > 8 * max(pastb, 1.0), "rung R2: East's units past the cycle in 2025 (%.0f mile-years against %.0f)" % (past25, pastb))
    Wd = D["W"]
    Wd = Wd.assign(g=Wd.peak_gust_mph.astype(float), yr=Wd.date_utc.str[:4].astype(int), r=Wd.precipitation_in.astype(float))
    sg = Wd[Wd.station_id == "VSY03"].groupby("yr").g.mean()
    ok(sg[2025] > sg[list(E.BASE)].mean() + 2.5, "rung R3: South's 2025 was windier")
    ng = Wd[Wd.station_id == "VSY01"].groupby("yr").g.mean()
    ok(abs(ng[2025] - ng[list(E.BASE)].mean()) < 1.5, "rung R3 dies in North: North's 2025 gusts at their usual level")
    nr = Wd[(Wd.station_id == "VSY01") & Wd.date_utc.str[5:7].isin(["05", "06", "07", "08", "09"])].groupby("yr").r.sum()
    ok(nr[2024] > 1.3 * nr[[2021, 2022, 2023]].mean(), "rung R1: North's May to September 2024 was wet (the regrowth reading)")
    ok(min(now[b] - base[b] for b in (2, 3)) > 3.0, "rung R1: North's units late in their cycle rose too (the regrowth reading's support)")
    # ---------------------------------------------------------------- major event days
    Ot = E.outage_table(D["X"])
    Ou = E.one_per_interruption(Ot)
    meds = E.major_event_days(Ou, D["M"])
    ms = E.med_set(meds)
    storms = {pd.Timestamp(d) for d, _ in P.STORMS if d.year >= 2021}
    ok(ms == storms, "MED: the major event days are the storm days")
    hi, lo = E.threshold_margin(Ou, D["M"], meds)
    ok(hi >= 2.0 and lo <= 0.8, "MED: every major event day at least twice its threshold, every other day under 0.8 (%.2f, %.2f)" % (hi, lo))
    ok(E.med_set(E.major_event_days(Ou, D["M"], ddof=0)) == ms, "SF9: the population standard deviation gives the same days")
    ok(E.med_set(E.major_event_days(Ot, D["M"])) == ms, "SF9: every record kept gives the same days")
    ok(E.med_set(E.major_event_days(Ou, D["M"], cm="cm_naive")) == ms, "SF9: members times final minutes gives the same days")
    Op = Ou.copy()
    Op["cause"] = Op.cause.replace("PLANNED", "UNKNOWN")
    ok(E.med_set(E.major_event_days(Op, D["M"])) == ms, "SF9: planned outages counted give the same days")
    # ---------------------------------------------------------------- semantic fork rows and Layer 1 neutrality
    def call_under(rt):
        lead_ = max(E.DISTRICTS, key=lambda d: rt[E.YEAR][d] - np.mean([rt[y][d] for y in E.BASE]))
        return lead_

    for mode in ("with_secondary", "with_momentary", "records"):
        rt = E.rates(D, mode)
        ok(call_under(rt) == "North", "SF1/SF3: %s leaves North carrying the rise" % mode)
    rt_med = {}
    t_all = E.tree_outages(D, "with_med")
    for y in range(2021, 2026):
        m_ = E.miles_avg(D["R"], y)
        c_ = t_all[t_all.year == y].groupby("district").size()
        rt_med[y] = {d: 100.0 * c_.get(d, 0) / m_[d] for d in E.DISTRICTS}
    ok(call_under(rt_med) == "North", "SF1: major event days kept leave North carrying the rise")
    Xs = D["X"].assign(ticket_no=D["X"].ticket_no + "-" + D["X"].step.astype(str))
    ok(call_under(E.rates(dict(D, X=Xs))) == "North", "SF3: each restoration step read as an outage leaves North carrying the rise")
    top = max(sh, key=sh.get)
    ok(top == "trees beyond the right-of-way (North)" and sh[top] > 0.5,
       "SF6: the driver accounting for most of the rise is the same under 'most' and 'the largest'")
    rt_inc = E.rates(D, basis="inclusive")
    ok(round(rt_inc[E.YEAR]["all"], 1) == round(A["comp"]["rate_2025"], 1)
       and round(float(np.mean([rt_inc[y]["all"] for y in E.BASE])), 1) == round(A["comp"]["rate_base"], 1),
       "SF2: a unit counted in service on its retirement date gives the same one-decimal rates")
    for basis in ("year_end", "year_start"):
        ok(call_under(E.rates(D, basis=basis)) == "North", "SF2: %s miles leave the call" % basis)
    rt = A["rates"]
    for alt in ((2021, 2022, 2023, 2024),):
        lead_ = max(E.DISTRICTS, key=lambda d: rt[E.YEAR][d] - np.mean([rt[y][d] for y in alt]))
        ok(lead_ == "North", "SF5: the rise against %s still sits in North" % (alt,))
    Xu = D["X"].copy()
    Xu["start_local"] = (pd.to_datetime(Xu.start_local) + pd.Timedelta(hours=6)).dt.strftime("%Y-%m-%d %H:%M")
    Xu["step_restored_local"] = (pd.to_datetime(Xu.step_restored_local) + pd.Timedelta(hours=6)).dt.strftime("%Y-%m-%d %H:%M")
    Du = dict(D, X=Xu)
    ok(call_under(E.rates(Du)) == "North", "SF4: UTC start times leave the call")
    ev_acc = E.evidence(D, "accepted")
    ok(E.golden_call(ev_acc) == "beyond", "SF8: the clock run from the acceptance date files the same call")
    reg = E.register(D["R"])
    ok(reg.groupby("unit_id").district.nunique().max() == 1, "SF10: every unit sits in one district")
    xd = D["X"][["unit_id", "service_area"]].drop_duplicates().merge(D["R"][["unit_id", "district"]], on="unit_id")
    ok((xd.service_area == xd.district).all(), "SF10: the export's service area is the unit's district")
    ok(A["comp"]["rate_base"] > 0 and abs(float(np.mean([rt[y]["all"] for y in E.BASE])) - A["comp"]["rate_base"]) < 1e-9,
       "SF5: the base is the mean of the three years' rates")
    pooled = sum(rt[y]["all"] * E.miles_avg(D["R"], y).sum() for y in E.BASE) / sum(E.miles_avg(D["R"], y).sum() for y in E.BASE)
    ok(round(pooled, 1) == round(A["comp"]["rate_base"], 1), "SF5: pooled mile-years give the same one-decimal base")
    for k in ("rate_2025", "rate_base"):
        ok(bin_dist(A["comp"][k]) >= 0.008, "bins: %s %.3f sits inside its one-decimal bin" % (k, A["comp"][k]))
    for k, v in (("North 2025", rt[E.YEAR]["North"]), ("North 2021 to 2023", np.mean([rt[y]["North"] for y in E.BASE])),
                 ("North's shift within two years of a trim", ev["young"]["North"])):
        ok(bin_dist(v) >= 0.005, "bins: %s %.3f sits inside its one-decimal bin" % (k, v))
    # R2: each Layer 1 item mishandled leaves the call and its evidence: a rebuilt unit's clock not restarted at its
    # in-service date; the 2024 re-survey's species list read as the 2023 one (its ash not counted); storm-mode
    # tickets and re-trips kept as outages (SF1/SF3 records row above)
    ev_nr = E.evidence(D, "no_rebuild")
    ok(E.golden_call(ev_nr) == "beyond", "R2: rebuilt units' clocks left running file the same call")
    S = D["S"]
    sh23 = (S[S.species_code == "FRAX"].groupby("unit_id").trees_within_falling_distance.sum()
            .reindex(S.unit_id.unique()).fillna(0) / S.groupby("unit_id").trees_within_falling_distance.sum())
    ga = E.ash_gradient(ev["t"], ev["E"], sh23)
    g_rise = [ga.loc[E.YEAR, q] - ga.loc[list(E.BASE), q].mean() for q in range(4)]
    ok(g_rise[3] >= 2.0 * max(g_rise[0], 1.0), "R2: the ash gradient holds with the re-survey's codes misread")
    # ---------------------------------------------------------------- the call's files against the shipped pack
    # the main call reads the export (every ticket's restoration steps for the major event days, the TREE outages for
    # the rate), the register, the completions, the survey, the weather, the member counts, the contracts register
    # and the two policies; every one of them is the 10-14 pack's byte for byte, except that the export names its
    # ticket column ticket_no and carries the storm-mode re-trip steps on 2025's two major event days
    for f, h in SHIPPED.items():
        ok(sha(os.path.join(target, f)) == h, "separation: %s is the shipped file byte for byte" % f)
    comp = open(os.path.join(target, "row_trim_completions_2012-2025.csv"), encoding="utf-8").read().split("\n")
    ok(hashlib.sha256("\n".join(",".join(l.split(",")[1:]) if l else l for l in comp).encode("utf-8")).hexdigest()
       == SHIPPED_COMPLETIONS, "separation: the completions less their record number are the shipped file byte for byte")
    rid = D["T"].record_id.str[2:].astype(int).diff().dropna()
    ok(rid.min() >= 1 and rid.nunique() >= 5, "realism: completion record numbers rise with uneven steps")
    raw = open(os.path.join(target, "oms_outage_export_2016-2025.csv"), encoding="utf-8").read().split("\n")
    parsed = [r.split(",") for r in raw[1:] if r]
    first_neg = {}
    for q in parsed:
        if int(q[-1]) < 0:
            first_neg[q[0]] = min(first_neg.get(q[0], 10 ** 9), int(q[-3]))
    kept = [",".join(q) for q in parsed if not (q[0] in first_neg and int(q[-3]) >= first_neg[q[0]])]
    reduced = "\n".join([raw[0].replace("ticket_no", "outage_id", 1)] + kept) + "\n"
    ok(hashlib.sha256(reduced.encode("utf-8")).hexdigest() == SHIPPED_EXPORT,
       "separation: the export less the re-trip steps, under its 10-14 header, is the shipped export byte for byte")
    rtk = K[K.storm_retrip]
    days25 = set(meds[E.YEAR][1])
    ok(len(rtk) == len(first_neg) and set(rtk.ticket_no) == set(first_neg),
       "separation: the negative steps sit on the storm-mode re-trip tickets only (%d)" % len(rtk))
    ok(set(pd.to_datetime(rtk.start).dt.normalize()) <= days25, "separation: every re-trip ticket opened on a 2025 major event day")
    Xr = D["X"][D["X"].ticket_no.isin(rtk.ticket_no)]
    negs = Xr[Xr.members_restored.astype(int) < 0]
    ok(set(pd.to_datetime(negs.step_restored_local).dt.normalize()) <= days25,
       "separation: every re-trip's second opening starts on the same major event day")
    ok(all(rtk.groupby("district").size().reindex(list(E.DISTRICTS)).fillna(0) >= 3), "ask B: every district holds three or more re-trips")
    for mode in ("net", "drop"):
        by = E.openings(Xr, mode).groupby("ticket").cm.sum()
        Om = Ot.copy()
        Om["cm"] = Om.outage_id.map(by).fillna(Om.cm)
        ok(E.med_set(E.major_event_days(E.one_per_interruption(Om), D["M"])) == ms,
           "separation: the re-trips read the %s way leave every year's major event days" % mode)
    g_open = E.openings(Xr, "golden")
    ok((g_open.groupby("ticket").size() >= 2).all(), "SF11: each re-trip ticket holds two device openings (2.1, one device opening)")
    lit = Ot[Ot.outage_id.isin(rtk.ticket_no)].set_index("outage_id").cm
    ok(np.allclose(g_open.groupby("ticket").cm.sum().reindex(lit.index).values, lit.values),
       "fairness: split at the re-trip, the customer-minutes add to the steps' own total (so the major event days hold)")
    ok(all(int(g.members_out.iloc[0]) == int(g.members_restored.astype(int).sum()) for _, g in Xr.groupby("ticket_no")),
       "silence: every re-trip ticket's members restored add to its members out")
    ok(all((-negs.members_restored.astype(int)).values == negs.members_out.astype(int).values),
       "SF11: each re-trip takes off every member the device had restored")
    # ---------------------------------------------------------------- asks
    bill = A["billing"]
    ok(all(abs(E.ask_billing(D, "service_month")[k] - bill[k]) >= 0.15 for k in bill),
       "ask A: the cracker's read (service month, credits netted) misses every cell")
    for m in ("own_month", "positive"):
        alt = E.ask_billing(D, m)
        ok(all(abs(alt[k] - bill[k]) >= 0.15 for k in bill), "ask A: the %s read misses every cell" % m)
    lag = E.ask_billing(D, "lag")
    ok(sum(abs(lag[k] - bill[k]) >= 0.15 for k in bill) >= 6, "ask A: the invoice month less one misses six or more cells")
    ok(all(bin_dist(v) >= 0.003 for v in bill.values()), "ask A: every cell sits inside its bin")
    dbill = A["district_billing"]
    ok(all(abs(E.ask_district(D, "service_month")[d] - dbill[d]) >= 0.15 for d in E.DISTRICTS),
       "ask C: the cracker's read misses every district")
    for m in ("own_month", "positive"):
        alt = E.ask_district(D, m)
        ok(all(abs(alt[d] - dbill[d]) >= 0.15 for d in E.DISTRICTS), "ask C: the %s read misses every district" % m)
    ok(all(bin_dist(v) >= 0.003 for v in dbill.values()), "ask C: every district sits inside its bin")
    ok(abs(sum(dbill.values()) - sum(bill.values())) < 1e-6, "ask C: the districts add to the contractors' 2025 miles")
    wd = E.wo_district(D)
    ok(all(len(v) == 1 for v in wd.values), "ask C: every work order sits in one district")
    I_ = D["I"]
    IY = res["IY"]
    J = I_.merge(IY, on=["invoice_no"], how="left", suffixes=("", "_t"))
    J = J[J.line_no.astype(int) == J.line_no_t.astype(int)]
    tr = J[J.item_code.str.startswith("TRIM")]
    stated = tr.description.map(E.stated_month)
    ok(((stated == tr.work_month) | ~tr.portal).all() and (stated[tr.portal] != "").all(),
       "SF12: every portal trimming line states the month of the work it bills")
    pap = tr[~tr.portal & (tr.doc_type == "INVOICE")]
    ok((pap.service_month == pap.work_month).all() and (stated[~tr.portal] == "").all(),
       "fairness: every paper invoice carries the month of the work as its service month and states no period")
    ok((tr[tr.portal].service_month == tr[tr.portal].invoice_date.str[:7]).all(),
       "SF12: every portal line's service month is its own document's month")
    gold_m = E.trim_lines(D, "golden").set_index(["invoice_no", "line_no"]).svc
    ok((gold_m.reindex(pd.MultiIndex.from_frame(tr[["invoice_no", "line_no"]])).values == tr.work_month.values).all(),
       "fairness: the golden reading recovers the month of the work on every trimming line")
    ok(I_.service_month.str.len().le(7).all() and (I_.service_month[I_.doc_type == "INVOICE"] != "").all(),
       "silence: every invoice carries a service month")
    for v in (E.OUTGOING, E.INCOMING):
        pv = tr[(tr.vendor == v) & tr.portal]
        ok(len(pv) > 0 and (tr[(tr.vendor == v) & ~tr.portal].invoice_date.max() < pv.invoice_date.min()),
           "realism: %s moved to the portal once, its paper invoices all dated before" % v)
    med = A["med"]
    for m in ("cracker", "drop", "records", "primary_only", "tree_only", "outage_minutes"):
        alt, _ = E.ask_med(D, m)
        moved = sum(alt[d][i] != med[d][i] for d in E.DISTRICTS for i in range(3))
        ok(moved == 9, "ask B: the %s read moves %d of 9 figures" % (m, moved))
    alt, _ = E.ask_med(D, "literal")
    ok(all(alt[d][0] != med[d][0] and alt[d][1] != med[d][1] for d in E.DISTRICTS),
       "ask B: one outage a ticket undercounts every district's outages and members")
    # separation: no ask device reaches the call's population
    dup = K[K.kind == "duplicate"]
    ok(dup.storm.all() and len(dup) > 0, "separation: the storm-mode tickets fall on storm days only")
    d21 = dup[pd.to_datetime(dup.start).dt.year >= 2021]
    ok(not set(pd.to_datetime(d21.start).dt.normalize()) - ms, "separation: no 2021 to 2025 storm-mode ticket off a major event day")
    folded = len(Ot) - len(Ou)
    ok(folded == len(dup), "fairness: the records folded are exactly the storm-mode second tickets (%d folded, %d tickets)"
       % (folded, len(dup)))
    ok("a device is in one outage at a time" in rel, "ask B: policy 2.1 files that a device is in one outage at a time")
    ok(A["call"] == E.golden_call(E.evidence(dict(D, X=D["X"][~D["X"].ticket_no.isin(dup.ticket_no)]))),
       "separation: dropping every storm-mode ticket leaves the call")
    import inspect
    src = "".join(inspect.getsource(f) for f in (E.tree_outages, E.rates, E.components, E.evidence, E.trim_history,
                                                   E.exposure, E.clock_at, E.ash_share, E.default_path, E.golden_call))
    ok('D["I"]' not in src and "invoice" not in src, "separation: the call never reads the invoices")
    # ---------------------------------------------------------------- no describing file
    ok(not any(re.search(r"dictionary|manifest|readme|codebook|field_notes|notes", f, re.I) for f in files),
       "no file describes the data")
    # ---------------------------------------------------------------- H16: nothing dated after the extract
    exp = P.EXPORT.isoformat()
    ok(D["T"].completed_date.max() <= exp and D["T"].accepted_date.max() <= exp, "H16: completions on or before the extract")
    ok(D["I"].invoice_date.max() <= exp, "H16: invoices and credit memos on or before the extract")
    ok(D["X"].step_restored_local.max() <= exp, "H16: outages restored before the extract")
    ok(D["W"].date_utc.max() <= exp and str(D["S"].survey_date.max())[:10] <= exp, "H16: weather and survey before the extract")
    ahead = D["R"][D["R"].retired_date > exp]
    ok(len(ahead) > 0 and ahead.retire_reason.eq("UNDERGROUND").all(),
       "H16: the register's dates past the extract are scheduled conversions to underground (the allow-list)")
    # ---------------------------------------------------------------- distractors
    src = open(E.__file__).read()
    ok(not any(d in src for d in meta["distractor_files"]), "distractors: the golden route never reads them")
    # ---------------------------------------------------------------- realism sweep
    for f in files:
        if f.endswith(".csv"):
            txt = open(os.path.join(target, f), encoding="utf-8").read()
            ok("—" not in txt and "–" not in txt, "realism: no em or en dash (%s)" % f)
    for t_ in (rel, row):
        ok("—" not in t_ and "–" not in t_, "realism: no dash in the policies")
    names = set(re.findall(r"[A-Z][a-z]+ [A-Z][a-z]+", rel + " " + row))
    ok(any(p in rel + row for p in PEOPLE), "realism: personas drawn by the guard")
    yearly = [rt[y]["all"] for y in range(2021, 2026)]
    ok(len(set(round(v, 1) for v in yearly)) == 5, "realism: no two years share a rate")
    per_year = Ou.groupby("year").size()
    ok(all(v % 100 != 0 for v in per_year.values), "realism: no round yearly outage count")
    ok(len(D["R"]) > 7000 and len(D["S"]) > 100000, "realism: the network has thousands of units and the survey its spans")
    return n[0]
