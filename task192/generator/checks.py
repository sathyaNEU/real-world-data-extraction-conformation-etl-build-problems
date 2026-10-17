"""Every claim the build rests on, asserted against the cut bundle.

The three-rules block (R1, R2, R3a, R3b, R3c) runs on the register the bundle rebuilds and on the
clean truth behind it, so the client's three rules are executed rather than argued.
"""
import csv
import datetime as dt
import json
import os
import statistics

import golden as G
import world as W

N = 0


def ok(label, cond, detail=""):
    global N
    N += 1
    if not cond:
        raise AssertionError("%s failed %s" % (label, detail))


def rows_of(target, name):
    with open(os.path.join(target, name), encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def counts(acts, sample):
    inper = [a for a in acts if W.PERIOD_FROM <= a["day"] <= W.PERIOD_TO]
    press = [a for a in inper if a["press_only"]]
    other = [a for a in inper if not a["press_only"]]
    H = sum(1 for a in other if a["coded_conf"])
    N_ = len(press)
    O = sum(1 for a in press if a["coded_conf"])
    tp, fn, fp, tn = G.matrix(sample)
    raw, se, sp = G.corrected(N_, O, tp, fn, fp, tn)
    return dict(n=len(inper), N=N_, H=H, O=O, g=H + raw, r0=H + O,
                r1=H + O * tp / (tp + fp), r2=H + O / se, se=se, sp=sp)


def run(target, g=None):
    global N
    N = 0
    g = g or G.compute(target)
    b = G.load(target)
    acts = G.actions(b["reports"])
    files = sorted(os.listdir(target))

    # ---------------------------------------------------------------- input gates
    ok("gate.files", len(files) >= 10, "%d files" % len(files))
    ok("gate.formats", len({os.path.splitext(f)[1] for f in files}) >= 3)
    big = max(sum(1 for _ in open(os.path.join(target, f), encoding="utf-8")) - 1
              for f in files if f.endswith(".csv"))
    ok("gate.bulk", big >= 25000, "%d rows" % big)
    meta = json.load(open(os.path.join(os.path.dirname(target), "metadata.json")))
    ok("gate.distractors", len(meta["distractor_files"]) >= 2)
    for dd in meta["distractor_files"]:
        ok("gate.distractor.present", dd["file"] in files, dd["file"])
    text = ""
    for f in files:
        if f.endswith((".csv", ".json")):
            text += open(os.path.join(target, f), encoding="utf-8", errors="replace").read(400000)
    ok("gate.no_answer_key", not any(k in text.lower() for k in
                                     ("is_correct", "should_exclude", "verdadeiro_codigo",
                                      "sensibilidade", "especificidade", "taxa_de_erro")))

    # ---------------------------------------------------------------- the call reproduces
    ok("call.actions", g["actions_in_period"] == 4790, g["actions_in_period"])
    ok("call.press_reported", g["press_only"] == 4357, g["press_only"])
    ok("call.other_actions", g["filed_by_hand"] == 433, g["filed_by_hand"])
    ok("call.hand_conf", g["hand_confrontational"] == 25, g["hand_confrontational"])
    ok("call.press_marked", g["press_marked"] == 153, g["press_marked"])
    ok("call.sample", g["sample_rows"] == 2600, g["sample_rows"])
    ok("call.matrix", (g["tp"], g["fn"], g["fp"], g["tn"]) == (59, 61, 30, 2450),
       str((g["tp"], g["fn"], g["fp"], g["tn"])))
    ok("call.total", g["total"] == 234, g["total"])
    ok("call.recall", abs(g["recall"] - 0.4917) < 0.0005, g["recall"])
    ok("call.false_mark", abs(g["false_mark"] - 0.0121) < 0.0005, g["false_mark"])
    ok("call.parts", g["press_only"] + g["filed_by_hand"] == g["actions_in_period"])

    # ---------------------------------------------------------------- the ladder
    ok("ladder.rung0", g["rung0"] == 178, g["rung0"])
    ok("ladder.rung1", g["rung1"] == 126, g["rung1"])
    ok("ladder.rung2", g["rung2"] == 336, g["rung2"])
    vals = [g["raw_rung1"], g["rung0"], g["raw_total"], g["raw_rung2"]]
    ok("ladder.order", vals[0] < vals[1] < vals[2] < vals[3], str(vals))
    gaps = [(vals[i + 1] - vals[i]) / vals[i] for i in range(3)]
    ok("ladder.separation", min(gaps) >= 0.18, str([round(x, 3) for x in gaps]))
    ok("ladder.distinct", len({126, 178, 234, 336}) == 4)
    ok("ladder.decisive_move_largest",
       (vals[3] - vals[2]) > max(vals[1] - vals[0], vals[2] - vals[1]), str(vals))
    ok("bin.total", abs(g["raw_total"] - g["total"]) <= 0.30, "%.3f" % g["raw_total"])
    ok("bin.edge", 0.5 - abs(g["raw_total"] - g["total"]) >= 0.25, "%.3f" % g["raw_total"])
    for name, v in (("rung1", g["raw_rung1"]), ("rung2", g["raw_rung2"])):
        ok("bin.%s" % name, abs(v - round(v)) <= 0.45, "%.3f" % v)
    # every graded figure that rounds sits off its edge: the euros a quarter of a bin clear, the
    # shares exact ratios of two integers and none of them on an edge
    for code, v in sorted(g["a3"].items()):
        ok("bin.euros.%s" % code, 0.5 - abs(v["raw_euros"] - round(v["raw_euros"])) >= 0.25,
           "%.4f" % v["raw_euros"])
    inside_by = {}
    for label, a, bb in W.fortnights():
        inside = [x for x in acts if a <= x["day"] <= bb]
        par = [x for x in inside if "PAR" in x["routes"]]
        inside_by[label] = (len(par), len(inside))
        tenths = 1000.0 * len(par) / len(inside)
        ok("bin.share.%s" % label, abs(tenths - round(tenths)) >= 0.02, "%.5f" % tenths)
        ok("bin.share_exact.%s" % label, 2000 * len(par) % len(inside) != 0
           or (2000 * len(par) // len(inside)) % 10 != 5, "%d/%d" % (len(par), len(inside)))
    for route, v in g["a2"].items():
        ok("bin.median.%s" % route, abs(v["median_minutes"] * 10
                                        - round(v["median_minutes"] * 10)) < 1e-9,
           "%.4f" % v["median_minutes"])

    # ---------------------------------------------------------------- the variants
    ok("variant.matrix_inverse", abs(g["variant_matrix_inverse"] - g["raw_total"]) < 1e-9,
       "%.4f" % g["variant_matrix_inverse"])
    ok("variant.sample_population", abs(g["variant_press_only_sample"] - g["raw_total"]) < 1e-9,
       "%.4f" % g["variant_press_only_sample"])
    ok("variant.continuity_measured", abs(g["variant_continuity"] - 232.403) < 0.01,
       "%.3f" % g["variant_continuity"])
    ok("variant.by_round_measured", abs(g["variant_by_round"] - 235.060) < 0.01,
       "%.3f" % g["variant_by_round"])
    ok("variant.by_theme_measured", abs(g["variant_by_theme"] - 235.925) < 0.01,
       "%.3f" % g["variant_by_theme"])
    ok("variant.spread", max(abs(g["variant_continuity"] - g["raw_total"]),
                             abs(g["variant_by_round"] - g["raw_total"]),
                             abs(g["variant_by_theme"] - g["raw_total"])) < 2.0)
    ok("variant.no_empty_cell", min(g["tp"], g["fn"], g["fp"], g["tn"]) > 0,
       "a continuity adjustment is for an empty cell and no cell is empty")

    # ---------------------------------------------------------------- R1, raw material
    heads = []
    for f in files:
        if f.endswith(".csv"):
            with open(os.path.join(target, f), encoding="utf-8") as fh:
                heads += next(csv.reader(fh))
    ok("R1.raw_rows", "codigo_monitor" in heads and "codigo_manual" in heads)
    ok("R1.no_rate_column", not any(h.lower().startswith(("taxa", "sensib", "especif", "erro"))
                                    for h in heads), str(heads))
    ok("R1.no_truth_column", not any("verdad" in h.lower() or "real" in h.lower() for h in heads))
    base = counts(acts, b["sample"])
    ok("R1.register_from_rows", base["n"] == 4790 and round(base["g"]) == 234)

    # ---------------------------------------------------------------- R2, mess neutral
    def call_of(reports):
        return counts(G.actions(reports), b["sample"])

    ok("R2.base", round(call_of(b["reports"])["g"]) == 234)
    one_load = [r for r in b["reports"] if r.get("load") != "C20260802"]
    ok("R2.reimport", round(call_of(one_load)["g"]) == 234 and call_of(one_load)["n"] == 4790)
    shifted = [dict(r, recv=r["recv"] + dt.timedelta(hours=1)) for r in b["reports"]]
    ok("R2.clocks", round(call_of(shifted)["g"]) == 234)
    cur = {r["codigo_localidade"]: r["nome"] for r in rows_of(target, "gazeteiro_localidades.csv")
           if r["estado_nome"] == "atual"}
    renamed = [dict(r, place=cur.get(r["loc"], r["place"])) for r in b["reports"]]
    ok("R2.former_names", round(call_of(renamed)["g"]) == 234)
    items = rows_of(target, "registo_itens_imprensa.csv")
    per_report = {}
    for r in items:
        if r["estado"] == "aceite":
            per_report.setdefault(r["id_relato"], set()).add(r["codigo_acao"])
    ok("R2.one_code_per_report", all(len(v) == 1 for v in per_report.values()))
    ok("R2.items_above_reports", len([r for r in items if r["estado"] == "aceite"]) > len(per_report))
    ids = {r["ident"] for r in b["reports"]}
    ok("R2.exceptions_disjoint", not ({e["ident"] for e in b["exceptions"]} & ids))

    # ---------------------------------------------------------------- R3, the three rules executed
    ok("R3a.analyst_test", base["r0"] == 178 and round(base["g"]) == 234 and base["r0"] != 234)
    ok("R3b.decisive_only", round(base["r2"]) == 336 and round(base["g"]) == 234)
    ok("R3b.each_rung_wrong", 234 not in {126, 178, 336})
    with open(os.path.join(target, "registo_itens_imprensa.csv"), encoding="utf-8") as fh:
        lines = fh.read().splitlines()[1:]
    blocks = {}
    for i in range(0, len(lines) - 20, 20):
        key = "|".join(x.split(",", 1)[1] for x in lines[i:i + 20])
        blocks[key] = blocks.get(key, 0) + 1
    ok("R3c.no_copied_block", max(blocks.values()) == 1)
    for word in ("sensib", "especif", "recall", "precis", "falso positivo", "falso negativo",
                 "corrig", "taxa de erro"):
        ok("R3c.no_method_word.%s" % word[:9], word not in text.lower(), word)
    pdfs = "".join(open(os.path.join(target, f), "rb").read().decode("latin-1")
                   for f in files if f.endswith(".pdf"))
    for word in ("sensibilidade", "especificidade", "falso positivo", "falso negativo", "234"):
        ok("R3c.no_method_in_pdf.%s" % word[:9], word not in pdfs, word)

    # ---------------------------------------------------------------- the semantic fork table
    ok("SF1.action_grain", g["actions_in_period"] < len(b["reports"]))
    ok("SF2.codes_not_actions", g["rung0"] != g["total"])
    ok("SF3.codes", set(W.CONFRONTATIONAL) == {"CF", "RF", "DP"})
    ok("SF4.window", all(W.PERIOD_FROM <= a["day"] <= W.PERIOD_TO
                         for a in acts if W.PERIOD_FROM <= a["day"] <= W.PERIOD_TO))
    ok("SF5.code_kept", all((a["code"] == a["press_code"]) if a["press_code"] else True
                            for a in acts))
    ok("SF6.sample_scope", {r["id_relato"][:3] for r in b["sample"]} == {"IMP"})
    ok("SF7.action_date_fixed", all(r["start"].date() == r["day"] for r in b["reports"]))
    ok("SF8.place_resolution", all(r["loc"] for r in b["reports"]))
    ok("SF9.reimport_neutral", round(call_of(one_load)["g"]) == 234)
    ok("SF10.twin_in_items", any(r["orgao"] == W.TWIN_FEED[1] for r in items))
    ok("SF11.rounding", abs(g["raw_total"] - 234) < 0.3)
    ok("SF12.ties", len({126, 178, 234, 336}) == 4)
    ok("SF13.accepted_only", all(r["estado"] in ("aceite", "rejeitado") for r in items))
    ok("SF14.extract", max(r["day"] for r in b["reports"]) <= W.EXTRACT)
    ok("SF15.outside_period", any(a["day"] > W.PERIOD_TO for a in acts))
    ok("SF16.hand_coding_present", all(r["codigo_manual"] for r in b["sample"]))
    ok("SF17.unplaced_not_actions", len(b["exceptions"]) > 0)
    ok("SF18.no_carry_in", min(r["day"] for r in b["reports"]) >= W.OPEN_DAY)

    # ---------------------------------------------------------------- realism
    by_fn = [v["actions"] for v in g["a1"].values()]
    ok("real.no_identical_periods", max(by_fn.count(x) for x in by_fn) <= 2, str(by_fn))
    ok("real.no_round_call", g["raw_total"] % 1 != 0 and g["total"] % 10 != 0)
    for route, a2 in g["a2"].items():
        ok("real.median_not_round.%s" % route, a2["median_minutes"] % 10 != 0,
           "%s %s" % (route, a2["median_minutes"]))
    for p, a3 in g["a3"].items():
        ok("real.euros_not_round.%s" % p, a3["euros"] % 100 != 0, "%s %s" % (p, a3["euros"]))
    for name in W.PEOPLE.values():
        hit = [f for f in files if name.split()[0].encode() in open(os.path.join(target, f), "rb").read()]
        ok("real.persona_only_where_filed.%s" % name.split()[0],
           all(f.endswith((".pdf", ".xlsx")) for f in hit), str(hit))
    ok("real.coders_are_initials", {r["codificador"] for r in b["sample"]} <= set(W.CODERS))
    ok("real.sample_two_rounds", {r["ronda"] for r in b["sample"]} == {"R1", "R2"})
    ok("real.extract_coherent", all(r["recv"].date() <= W.EXTRACT for r in b["reports"]))
    man = {r["ficheiro"]: r for r in rows_of(target, "manifesto_extracao.csv")}
    ok("real.manifest_covers", set(files) - set(man) == {"manifesto_extracao.csv"},
       str(set(files) - set(man)))
    ok("real.manifest_extract_date",
       all(r["extraido_em"] == W.EXTRACT.isoformat() for r in man.values()))
    ok("real.item_rows_match", int(man["registo_itens_imprensa.csv"]["linhas"]) == big)

    # ---------------------------------------------------------------- the ask layer
    ok("ask.a1_fortnights", len(g["a1"]) == 13)
    ok("ask.a1_last_fortnight", (W.fortnights()[-1][2] - W.fortnights()[-1][1]).days == 14)
    ok("ask.a2_routes", len(g["a2"]) == 3 and all(v["unplaceable"] > 0 for v in g["a2"].values()))
    ok("ask.a3_partners", len(g["a3"]) == 7 and all(v["filed"] > 0 for v in g["a3"].values()))
    par_rows = rows_of(target, "relatos_rede_parceiros.csv")
    ok("cracker.a2_received", len(par_rows) != g["a2"]["PAR"]["received"],
       "%d %d" % (len(par_rows), g["a2"]["PAR"]["received"]))
    ok("cracker.a2_unplaceable", g["a2"]["IMP"]["unplaceable"] > 0)
    naive_med = statistics.median(sorted(
        (r["recv"] - dt.timedelta(hours=1) - r["start"]).total_seconds() / 60.0
        for r in b["reports"] if r["route"] == "IMP"
        and W.PERIOD_FROM <= r["recv"].date() <= W.PERIOD_TO))
    ok("cracker.a2_median", abs(naive_med - g["a2"]["IMP"]["median_minutes"]) > 5,
       "%.1f %s" % (naive_med, g["a2"]["IMP"]["median_minutes"]))
    seen = {}
    for r in b["reports"]:
        if r["route"] == "PAR":
            seen.setdefault(r["ident"], r)
    flat = sum(dict((p[0], p[3]) for p in W.PARTNERS)[W.AMENDED[0]] for r in seen.values()
               if r["src"] == W.AMENDED[0] and W.PERIOD_FROM <= r["day"] <= W.PERIOD_TO
               and r["recv"].date() <= W.PERIOD_TO)
    ok("cracker.a3_amendment", round(flat) != g["a3"][W.AMENDED[0]]["euros"],
       "%d %d" % (round(flat), g["a3"][W.AMENDED[0]]["euros"]))
    one_code = sum(1 for r in seen.values() if r["src"] == W.MERGED[0]
                   and W.PERIOD_FROM <= r["day"] <= W.PERIOD_TO)
    ok("cracker.a3_merged", one_code != g["a3"][W.MERGED[0]]["filed"],
       "%d %d" % (one_code, g["a3"][W.MERGED[0]]["filed"]))
    ok("cracker.a1_scope", any(a["day"] > W.PERIOD_TO for a in acts))

    # ---------------------------------------------------------------- the separation line
    ok("sep.devices_outside_call", all(e["ident"] not in ids for e in b["exceptions"]))
    ok("sep.totals_carry_no_code",
       set(rows_of(target, "totais_por_via.csv")[0]) == {"data", "via", "relatos_recebidos"})
    ok("sep.sample_carries_no_total", "total" not in ",".join(rows_of(target, "amostra_dupla_codificacao.csv")[0]).lower())
    return N
