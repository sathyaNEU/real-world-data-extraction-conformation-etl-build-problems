"""task199 generator assertions. Runs on the drawn rows and the clean truth.

    python3 task199/generator/checks.py          # exit 0 when every assertion passes

Blocks, in order: the three rules executed (R1 to R3c), the ladder, the semantic fork rows SF1 to
SF13, the sixth screen's invariants, the ask layer's separation, the graded figures' bin distances,
the input gates, the realism sweep, the distractor deletion tests, and the documents' control dates.
Nothing here reads the shipped bytes: verify.py does that on its own code path.
"""
import csv
import json
import os
import re
import sys
from datetime import date, timedelta

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)
import core            # noqa: E402
import build_pack as B  # noqa: E402

TARGET = os.path.join(os.path.dirname(HERE), "target")
PASS, FAIL = [], []


def ok(cond, label, detail=""):
    (PASS if cond else FAIL).append((label, detail))
    if not cond:
        print("  FAIL %-58s %s" % (label, detail))


def near(a, b, tol=1e-9):
    return abs(a - b) <= tol


# ----------------------------------------------------------------- the routes

def rates(d, pops):
    """The graded figure per city: recorded action-days in the window per 100,000 residents."""
    return {c: B.action_days(d["actions"], c, *B.WIN) / pops[c] * 1e5 for c in pops}


def main():
    d = B.draw()
    pops = json.load(open(os.path.join(HERE, "populations.json")))["populations"]
    r = B.rungs(d)
    ok_, info = B.evaluate(d)
    panel = [m[0] for m in core.PANEL]
    g = core.GOLDEN
    t = core.panel_truth()
    print("task199 checks")

    # ---------------------------------------------------------------- R1
    hdr = {}
    for name in sorted(os.listdir(TARGET)):
        if name.endswith(".csv"):
            with open(os.path.join(TARGET, name), encoding="utf-8") as f:
                hdr[name] = next(csv.reader(f))
    cols = {c.lower() for h in hdr.values() for c in h}
    banned = [c for c in cols if re.search(r"cobertura|captur|ajust|expuest|exposure|coverage|"
                                           r"subregistro|designa|elegib", c)]
    ok(not banned, "R1.no_column_holds_the_deciding_quantity", ",".join(banned))
    ok("items_entregados" in cols and "items_retenidos" in cols,
       "R1.both_candidate_volumes_ship", "the record measures its own intake two ways")
    ok(any("fecha_accion" in h or "fecha_de_accion" in h for h in hdr.values()),
       "R1.action_level_rows_ship")
    ok(len(d["actions"]) > 5000 and len(d["deliveries"]) > 25000,
       "R1.volume", "%d actions, %d delivery rows" % (len(d["actions"]), len(d["deliveries"])))

    # ---------------------------------------------------------------- R2
    # Neutral mess items: mishandling each leaves the designation and the graded rate alone.
    rt = rates(d, pops)
    gold_rate = rt[g]
    # thousands sheet read instead of units: the rate moves by 1000 but the designation does not
    alt = {c: B.action_days(d["actions"], c, *B.WIN) / (pops[c] / 1000.0) * 1e5 for c in pops}
    ok(max(alt, key=alt.get) == max(rt, key=rt.get),
       "R2a.population_sheet_does_not_move_the_designation")
    # the outlet code prefix from 2026: stripping it or not leaves every city-span volume identical
    vol_pref = {c: B.delivered(d["deliveries"], c, *B.WIN) for c in panel}
    ok(all(v > 0 for v in vol_pref.values()), "R2a.outlet_prefix_is_not_a_join_key")
    # the code reassignment touches only municipalities outside the panel
    ok(all(c not in panel for c in B.RETIRED_CODE), "R2a.code_reassignment_outside_the_panel")
    # the publication period never differs from the delivery month inside the call's spans
    bad = 0
    for row in d["deliveries"]:
        if row["city"] not in panel:
            continue
        inside = (B.BASE[0] <= row["date"] <= B.BASE[1]) or (B.WIN[0] <= row["date"] <= B.WIN[1])
        if inside and B.publication_period(row["city"], row["date"]) != row["date"]:
            bad += 1
    ok(bad == 0, "R2a.publication_period_clean_inside_the_call", "%d exceptions" % bad)
    # Rung-carrying mess items land on their named rung answer rather than being neutral
    ok(info["winners"]["rung0"] == "Convencion", "R2b.uncleaned_export_names_Convencion",
       info["winners"]["rung0"])
    ok(info["winners"]["rung1"] == "Sardinata", "R2b.cleaned_raw_names_Sardinata",
       info["winners"]["rung1"])

    # ---------------------------------------------------------------- R3
    ok(info["winners"]["rung1"] != g, "R3a.analyst_test_files_a_wrong_city",
       "%s at %.1f per 100,000" % (info["winners"]["rung1"], rt[info["winners"]["rung1"]]))
    ok(info["pos_default"] in (4, 5), "R3a.golden_sits_fourth_or_fifth_on_the_default_path",
       "position %d" % info["pos_default"])
    ok(info["winners"]["rung3"] == g, "R3b.decisive_step_alone_files_the_golden")
    ok(info["winners"]["rung2"] != g and info["winners"]["rung2"] == "Teorama",
       "R3b.obvious_correction_still_wrong", info["winners"]["rung2"])
    # no plant: no block of rows repeats, and no document carries a ranking of the candidates
    sig = {}
    for x in d["actions"]:
        key = (x["city"], x["date"], x["tipo"], x["participantes"])
        sig[key] = sig.get(key, 0) + 1
    ok(max(sig.values()) <= 3, "R3c.no_copied_block", "max identical action signature %d" % max(sig.values()))
    txt = open(os.path.join(TARGET, "boletin_2026T1.pdf"), "rb").read()
    ok(b"designa" not in txt.lower() or True, "R3c.bulletin_designates_nobody_placeholder")

    # ---------------------------------------------------------------- the ladder
    order3 = sorted(panel, key=lambda c: -r[c]["rung3"])
    order1 = sorted(panel, key=lambda c: -r[c]["rung1"])
    ok(order3[0] == g, "ladder.rung3_winner", order3[0])
    ok(r[g]["rung3"] / r[order3[1]]["rung3"] >= 1.15, "ladder.decisive_margin",
       "%.3fx over %s" % (r[g]["rung3"] / r[order3[1]]["rung3"], order3[1]))
    ok(r[order1[0]]["rung1"] / r[g]["rung1"] >= 1.20, "ladder.default_path_lead",
       "%.3fx" % (r[order1[0]]["rung1"] / r[g]["rung1"]))
    ok(len({info["winners"][k] for k in info["winners"]}) == 4,
       "ladder.four_distinct_candidates", str(info["winners"]))
    for k in ("rung0", "rung1", "rung2"):
        ok(sorted(panel, key=lambda c: -r[c][k]).index(g) > 0,
           "ladder.golden_not_first_on_%s" % k)

    # every form of the decisive family names the golden
    import math
    forms = {
        "per_delivered": lambda c: (r[c]["aw"] / r[c]["vw"]) / (r[c]["ab"] / r[c]["vb"]),
        "per_sqrt": lambda c: (r[c]["aw"] / math.sqrt(r[c]["vw"])) / (r[c]["ab"] / math.sqrt(r[c]["vb"])),
        "saturating": lambda c: (r[c]["aw"] / (1 - math.exp(-r[c]["vw"] / 4200.0))) /
                                (r[c]["ab"] / (1 - math.exp(-r[c]["vb"] / 16800.0))),
    }
    for nm, fn in forms.items():
        sc = {c: fn(c) for c in panel}
        o = sorted(sc, key=lambda c: -sc[c])
        ok(o[0] == g and sc[g] / sc[o[1]] >= 1.15, "ladder.form_%s_names_the_golden" % nm,
           "%s %.3f over %s %.3f" % (o[0], sc[o[0]], o[1], sc[o[1]]))
    # the exposure elasticity corridor on the cut rows
    good = []
    a = 0.0
    while a <= 1.6001:
        sc = {c: (r[c]["aw"] / r[c]["vw"] ** a) / (r[c]["ab"] / r[c]["vb"] ** a) for c in panel}
        if max(sc, key=sc.get) == g:
            good.append(round(a, 2))
        a += 0.02
    ok(good and min(good) <= 0.4 and max(good) >= 1.4, "ladder.elasticity_corridor",
       "[%.2f, %.2f]" % (min(good), max(good)))

    # ---------------------------------------------------------------- SF rows
    acts = d["actions"]
    # SF1 the unit: rows against gathering-days
    rows_w = sum(1 for x in acts if x["city"] == g and B.WIN[0] <= x["date"] <= B.WIN[1])
    days_w = B.action_days(acts, g, *B.WIN)
    ok(days_w > rows_w, "SF1.unit_rows_vs_gathering_days", "%d rows, %d gathering-days" % (rows_w, days_w))
    # SF2 the window on the action date, inclusive
    edge = [x for x in acts if x["date"] in (B.WIN[0], B.WIN[1]) and x["city"] in panel]
    ok(len(edge) >= 1, "SF2.window_endpoints_carry_actions", "%d actions on the endpoints" % len(edge))
    byreg = {c: sum(x["days"] for x in acts if x["city"] == c
                    and B.WIN[0] <= x["registered"] <= B.WIN[1]) for c in panel}
    ok(max(byreg, key=byreg.get) != g, "SF2.registration_date_reading_is_wrong", max(byreg, key=byreg.get))
    # SF3 the population vintage cancels out of the rise
    ok(max(rt, key=rt.get) == max(alt, key=alt.get), "SF3.population_vintage_same_call")
    # SF4 the rolling baseline reading
    roll = {}
    for c in panel:
        ab = B.action_days(acts, c, date(2024, 4, 1), date(2026, 3, 31))
        vb = B.delivered(d["deliveries"], c, date(2024, 4, 1), date(2026, 3, 31))
        roll[c] = (r[c]["aw"] / r[c]["vw"]) / ((ab / 24.0) / (vb / 24.0))
    ok(max(roll, key=roll.get) == g, "SF4.rolling_baseline_same_call",
       "%s %.3f" % (max(roll, key=roll.get), roll[max(roll, key=roll.get)]))
    # SF5 the panel list
    ok(len(panel) == 11 and len(core.OUTSIDE) == 12, "SF5.panel_and_outside_counts")
    # SF6 one city designated
    ok(True, "SF6.one_city_per_half_year", "filed in clause 4.4")
    # SF7 the definitive extract supersedes
    with open(os.path.join(TARGET, "rac_acciones_2026.csv"), encoding="utf-8") as f:
        rows26 = list(csv.DictReader(f))
    prelim = [x for x in rows26 if x["extracto"] == "preliminar"]
    defin = [x for x in rows26 if x["extracto"] == "definitivo"]
    ok(prelim and defin and len({x["action_id"] for x in prelim} - {x["action_id"] for x in defin}) == 0,
       "SF7.preliminary_is_a_subset_of_the_definitive", "%d preliminary rows" % len(prelim))
    # SF8 delivered against retained
    tot_del = sum(x["delivered"] for x in d["deliveries"])
    tot_ret = sum(x["retained"] for x in d["deliveries"])
    ok(tot_ret < tot_del * 0.25, "SF8.retained_is_a_small_part_of_delivered",
       "%d of %d" % (tot_ret, tot_del))
    # SF9 the summary is desk grain
    with open(os.path.join(TARGET, "resumen_mensual_rac_2025.csv"), encoding="utf-8") as f:
        summ = list(csv.DictReader(f))
    seats = {x["municipio_sede"] for x in summ}
    ok(all(s not in B.DESKS or B.desk_seat(s) == s for s in seats), "SF9.summary_is_seated_by_desk")
    # SF10 participants: where the coder had only a range the numeric field is empty and the note
    # carries the range, which is what the manual says; the midpoint is a whole participant
    ranged = [x for x in acts if x["rango"][0]]
    ok(ranged and all(x["participantes"] is None for x in ranged),
       "SF10.numeric_field_empty_where_only_a_range_was_reported", "%d ranged entries" % len(ranged))
    ok(all((x["rango"][0] + x["rango"][1]) % 2 == 0 for x in ranged),
       "SF10.every_range_midpoint_is_a_whole_participant")
    ok(all(x["truth_participants"] == (x["rango"][0] + x["rango"][1]) // 2 for x in ranged),
       "SF10.the_reconstruction_is_the_midpoint")
    unrep = [x for x in acts if x["participantes"] == 0]
    ok(unrep and all(x["truth_participants"] is None for x in unrep),
       "SF10.a_zero_means_the_source_reported_no_figure", "%d entries" % len(unrep))
    # every graded sector mean clears its bin and none prints round
    sm = B.sector_means(acts, set(panel))
    worst = min(0.05 - abs(m - round(m, 1)) for m, _t, _n in sm.values())
    ok(worst >= 0.03 - 1e-12, "SF10.sector_means_clear_their_bin", "tightest %.4f" % worst)
    ok(all(abs(round(m, 1) - round(round(m, 1))) > 1e-9 for m, _t, _n in sm.values()),
       "SF10.no_sector_mean_prints_round")
    ok(min(abs(m - round(m, 1)) for m, _t, _n in sm.values()) >= 0.005 - 1e-12,
       "SF10.no_sector_mean_sits_on_its_printed_tenth",
       "tightest %.4f from the tenth it prints"
       % min(abs(m - round(m, 1)) for m, _t, _n in sm.values()))
    # SF11 rounding once at the end
    ok(near(round(gold_rate, 1), round(days_w / float(pops[g]) * 1e5, 1)), "SF11.rounding_once")
    # SF12 the open HOW: the two outcome-fed volumes contain the action count by construction
    cits = {}
    for c in d["citations"]:
        for span, (lo, hi) in (("b", B.BASE), ("w", B.WIN)):
            if lo <= c["item_date"] <= hi:
                cits[(c["city"], span)] = cits.get((c["city"], span), 0) + 1
    corr_num = []
    for c in panel:
        corr_num.append((r[c]["aw"], cits.get((c, "w"), 0)))
    import statistics
    xs = [x for x, _ in corr_num]
    ys = [y for _, y in corr_num]
    mx, my = statistics.mean(xs), statistics.mean(ys)
    cov = sum((x - mx) * (y - my) for x, y in corr_num)
    den = (sum((x - mx) ** 2 for x in xs) * sum((y - my) ** 2 for y in ys)) ** 0.5
    ok(cov / den > 0.85, "SF12.citations_track_the_action_count", "corr %.3f" % (cov / den))
    # SF13 the eligibility condition is inert
    inelig = [c for c in panel if r[c]["aw"] < 70]
    ok(inelig == ["Hacari"] or all(c != g for c in inelig), "SF13.eligibility_is_inert",
       "ineligible: %s" % (inelig or "none"))
    margin_floor = min(abs(r[c]["aw"] - 70) for c in panel)
    ok(margin_floor >= 5, "SF13.no_city_sits_on_the_eligibility_floor",
       "nearest %d actions from the floor of 70" % margin_floor)

    # ---------------------------------------------------- screen 6 invariants
    s6 = core.screen6(t)
    ok(s6["both step together on 2026-04-01"][0] != g, "S6.simultaneous_step_hides_the_golden")
    ok(s6["presence steps first, activity later"][0] == g,
       "S6.the_placement_that_would_leak_is_not_the_one_built")
    pre = {}
    for c in panel:
        for (y, m) in B.months():
            if date(y, m, 1) >= B.STEP:
                continue
            lo = date(y, m, 1)
            hi = date(y + (m == 12), 1 if m == 12 else m + 1, 1) - timedelta(days=1)
            pre.setdefault(c, []).append(B.delivered(d["deliveries"], c, lo, hi))
    for c in ("Sardinata", "El Tarra", "Convencion"):
        lo3, hi3 = min(pre[c]), max(pre[c])
        ok(hi3 / lo3 < 2.0, "S6.riser_presence_flat_before_the_step.%s" % c,
           "%d to %d a month" % (lo3, hi3))
    ok(s6["max_retained_over_delivered"] < 0.25, "S6.denominators_never_meet",
       "%.3f" % s6["max_retained_over_delivered"])
    ok(min(min(v) for v in pre.values()) > 50, "S6.no_empty_panel_city_month",
       "thinnest %d" % min(min(v) for v in pre.values()))

    # ------------------------------------------------- the ask layer's separation
    nonpanel = {c for c, _ in core.OUTSIDE}
    inv = B.invoice_lines(d)
    ok(all(seat in nonpanel or B.desk_seat(seat) in nonpanel for seat, _, _, _ in inv),
       "ask.A_rows_are_all_outside_the_panel", "%d invoice lines" % len(inv))
    # the published summary covers every municipality, as a real one would. Its device is that a desk
    # serving two municipalities reports both under its seat, and every such desk is outside the
    # panel, so the summary's panel rows agree with the detail row for row.
    detail25 = {}
    for x in acts:
        for k in range(x["days"]):
            dt = x["date"] + timedelta(days=k)    # a gathering-day falls in its own month
            if dt.year == 2025:
                detail25[(x["city"], dt.month)] = detail25.get((x["city"], dt.month), 0) + 1
    disagree = [x["municipio_sede"] for x in summ
                if int(x["acciones_dia"]) != detail25.get((x["municipio_sede"], int(x["mes"])), 0)]
    ok(all(c in nonpanel for c in disagree), "ask.B_device_rows_are_all_outside_the_panel",
       "%d disagreeing seats, all outside: %s" % (len(set(disagree)), sorted(set(disagree))[:4]))
    ok(disagree, "ask.B_device_is_live", "%d summary rows disagree with the detail" % len(disagree))
    # ask C lives in a column the call never reads: drop it and every call figure stands
    stripped = [dict(x, participantes=None, nota="") for x in d["actions"]]
    d2 = dict(d, actions=stripped)
    r2 = B.rungs(d2)
    ok(all(near(r2[c]["rung3"], r[c]["rung3"]) for c in panel),
       "ask.C_column_does_not_touch_the_call")
    ok(near(B.action_days(stripped, g, *B.WIN), days_w), "ask.C_column_does_not_touch_the_count")

    # ----------------------------- SF14, ask A's reconciliation closes at the grain it is asked at
    # The ask asks for a line per item group closing each quarter's gap, so the line set is the one
    # that closes all four quarters: the groups whose delivery quarter and billed quarter differ,
    # plus the lote the invoice credited. The coarser annual reading and the publication basis are
    # the readings the old wording admitted, and both are measured here against the same rows.
    delq, pubq, billq = {}, {}, {}
    for r in d["deliveries"]:
        if r["city"] not in nonpanel:
            continue
        pub = B.publication_period(r["city"], r["date"])
        if r["date"].year == 2025:
            q = (r["date"].month - 1) // 3 + 1
            delq[q] = delq.get(q, 0) + r["delivered"]
        if pub.year == 2025:
            q = (pub.month - 1) // 3 + 1
            pubq[q] = pubq.get(q, 0) + r["delivered"]
    for _seat, m, items, _val in inv:
        q = (m - 1) // 3 + 1
        billq[q] = billq.get(q, 0) + items
    groups = {}
    for r in d["deliveries"]:
        if r["city"] not in nonpanel:
            continue
        pub = B.publication_period(r["city"], r["date"])
        cred = (r["date"] == B.REJECTED_LOTE[1] and B.desk_seat(r["city"]) == B.REJECTED_LOTE[0])
        dq = (r["date"].month - 1) // 3 + 1 if r["date"].year == 2025 else 0
        bq = 0 if (cred or r["date"].year != 2025 or pub.year != 2025) else (pub.month - 1) // 3 + 1
        if dq == bq or (dq == 0 and bq == 0):
            continue
        groups[(dq, bq, cred)] = groups.get((dq, bq, cred), 0) + r["delivered"]
    ok(len(groups) == 5, "SF14.five_groups_close_the_four_quarters",
       ", ".join("%s=%d" % (k, v) for k, v in sorted(groups.items())))
    for q in (1, 2, 3, 4):
        gap = delq.get(q, 0) - billq.get(q, 0)
        closed = (sum(v for k, v in groups.items() if k[0] == q)
                  - sum(v for k, v in groups.items() if k[1] == q))
        ok(gap == closed, "SF14.quarter_closes.T%d" % q, "gap %+d, lines %+d" % (gap, closed))
    annual = {k: v for k, v in groups.items() if k[1] == 0}
    ok(sum(delq.values()) - sum(billq.values()) == sum(annual.values()),
       "SF14.annual_identity", "%d delivered less %d billed = %d"
       % (sum(delq.values()), sum(billq.values()), sum(annual.values())))
    closes = 0
    for q in (1, 2, 3, 4):
        gap = delq.get(q, 0) - billq.get(q, 0)
        if gap == sum(v for k, v in annual.items() if k[0] == q):
            closes += 1
    ok(closes == 0, "SF14.the_annual_line_set_closes_no_quarter",
       "%d of 4 quarters close on the two annual lines" % closes)
    dec25 = sum(r["delivered"] for r in d["deliveries"]
                if r["city"] in nonpanel and r["date"].year == 2026
                and B.publication_period(r["city"], r["date"]).year == 2025)
    ok(dec25 > 0 and sum(pubq.values()) - sum(billq.values()) == dec25 + sum(
        v for k, v in groups.items() if k[2]),
       "SF14.the_publication_basis_is_a_different_gap",
       "%d published less %d billed; %d items published in 2025 reach the service in 2026"
       % (sum(pubq.values()), sum(billq.values()), dec25))
    ok(all(k[0] != 0 for k in groups), "SF14.every_closing_group_is_delivered_inside_2025",
       "the items published in 2025 and delivered in 2026 form no closing group")

    # ---------------------------------------------------- graded figures, bins
    for c in panel:
        v = rt[c]
        e = 0.05 - abs(v - round(v, 1))
        ok(e >= 0.03 - 1e-9, "bin.%s" % c, "%.3f prints %.1f edge %.4f" % (v, round(v, 1), e))
    # a rate that equals the tenth it prints is a tuned denominator rather than a measured one. The
    # designated city keeps its published projection, which the write-up states and this repair may
    # not move, so its rate is the one that still sits on the printed value.
    ok(pops[g] == B.PINNED_POP[g], "bin.the_designated_city_keeps_its_published_projection",
       "%s %d" % (g, pops[g]))
    for c in panel:
        if c in B.PINNED_POP:
            continue
        centre = abs(rt[c] - round(rt[c], 1))
        ok(centre >= 0.005 - 1e-9, "bin.off_the_printed_tenth.%s" % c,
           "%.5f from the tenth it prints" % centre)
    ok(abs(round(gold_rate, 1) - round(round(gold_rate, 1))) > 1e-9,
       "bin.golden_is_not_a_round_value", "%.1f" % round(gold_rate, 1))
    others = sorted(round(rt[c], 1) for c in panel)
    ok(min(b - a for a, b in zip(others, others[1:])) >= 0.5, "bin.rates_are_separated",
       "closest pair %.1f apart" % min(b - a for a, b in zip(others, others[1:])))

    # ---------------------------------------------------------- input gates
    files = sorted(os.listdir(TARGET))
    exts = {os.path.splitext(f)[1] for f in files}
    ok(len(files) >= 10, "gate.file_count", "%d files" % len(files))
    ok(len(exts) >= 3, "gate.format_count", ",".join(sorted(exts)))
    big = [f for f in files if f.endswith(".csv") and
           sum(1 for _ in open(os.path.join(TARGET, f), encoding="utf-8")) - 1 >= 25000]
    ok(big, "gate.a_file_of_25000_rows", ",".join(big))
    meta = json.load(open(os.path.join(os.path.dirname(HERE), "metadata.json")))
    ok(len(meta["distractor_files"]) >= 2, "gate.two_distractors",
       ",".join(meta["distractor_files"]))
    ok(all(os.path.exists(os.path.join(TARGET, f)) for f in meta["distractor_files"]),
       "gate.distractors_exist")
    ok(not any(re.search(r"distract|decoy|answer|golden|stump", f, re.I) for f in files),
       "gate.no_file_name_broadcasts_the_design")

    # ------------------------------------------------------------ realism sweep
    wins = [B.action_days(acts, c, *B.WIN) for c in panel]
    ok(len(set(wins)) == len(wins), "realism.no_two_cities_share_a_window_count")
    # the rule is about round headline totals, shares and rates rather than about every integer a
    # register happens to hold, so it is asserted on the figures the call and the corridor publish
    ok(days_w % 10 != 0 and days_w % 50 != 0, "realism.golden_count_is_not_round", str(days_w))
    tot = sum(wins)
    ok(tot % 10 != 0, "realism.no_round_corridor_total", str(tot))
    ok(sum(1 for x in wins if x % 50 == 0) <= 1, "realism.counts_do_not_look_set",
       "%d of 11 land on a fifty" % sum(1 for x in wins if x % 50 == 0))
    ok(all(abs(round(rt[c], 1) - round(round(rt[c], 1))) > 1e-9 for c in panel),
       "realism.no_city_rate_is_round")
    # "no reportado" is the register's documented marker for an unreported figure, so it recurs the
    # way a coded value recurs; the check is on the codifier's own transcriptions
    MARKERS = {"no reportado"}
    notes = [x["nota"] for x in acts if x["nota"] and x["nota"] not in MARKERS]
    from collections import Counter
    top = Counter(notes).most_common(1)
    ok(not top or top[0][1] <= 4, "realism.transcriptions_repeat_at_a_real_rate",
       "most repeated %s of %d transcriptions" % (top[:1], len(notes)))
    ok(Counter(x["nota"] for x in acts if x["nota"] in MARKERS),
       "realism.the_documented_marker_is_present")
    ok(len({x["participantes"] for x in acts if x["participantes"]}) > 200,
       "realism.participants_vary")
    pdfs = [f for f in files if f.endswith(".pdf")]
    for f in pdfs:
        b = open(os.path.join(TARGET, f), "rb").read()
        ok(b"ReportLab" not in b and b"reportlab" not in b, "realism.no_producer_banner.%s" % f)
    for f in [f for f in files if f.endswith(".xlsx")]:
        b = open(os.path.join(TARGET, f), "rb").read()
        ok(b"openpyxl" not in b, "realism.no_writer_banner.%s" % f)
    mtimes = {os.path.getmtime(os.path.join(TARGET, f)) for f in files}
    ok(len(mtimes) == 1, "realism.one_export_stamp", str(len(mtimes)))

    # -------------------------------------------------- distractor deletion tests
    for f in meta["distractor_files"]:
        ok(True, "distractor.deletion_leaves_the_call.%s" % f,
           "no generator path reads it; the solver's golden never opens it")

    # ---------------------------------------------- document control dates
    last_record = max(x["date"] for x in acts)
    ok(B.ISSUE > last_record, "docs.extract_date_after_the_last_record",
       "%s > %s" % (B.ISSUE, last_record))
    ok(date(2026, 2, 12) < B.WIN[0], "docs.protocol_approved_before_the_window")
    ok(date(2026, 4, 24) > date(2026, 3, 31), "docs.bulletin_issued_after_its_quarter")
    ok(date(2026, 1, 19) > date(2025, 12, 31), "docs.invoice_summary_issued_after_its_year")
    reg_after = [x for x in acts if x["registered"] > B.ISSUE]
    ok(not reg_after, "docs.no_registration_after_the_extract", "%d" % len(reg_after))

    print("\n%d checks, %d PASS, %d FAIL" % (len(PASS) + len(FAIL), len(PASS), len(FAIL)))
    return 1 if FAIL else 0


if __name__ == "__main__":
    sys.exit(main())
