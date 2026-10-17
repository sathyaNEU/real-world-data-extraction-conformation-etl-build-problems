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


def fmt(x):
    return "%.4f" % x


def rows_of(target, name):
    with open(os.path.join(target, name), encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def cohort_of(reports):
    acts = G.actions(reports)
    eps = G.register(acts)
    coh = [e for e in eps if W.PERIOD_FROM <= e["open"] <= W.PERIOD_TO]
    return acts, coh


def four(coh):
    rows = [(e["t"], e["cause"]) for e in coh]
    n = len(rows)
    E = sum(1 for t, c in rows if c == 1)
    C = sum(1 for t, c in rows if c == 2)
    cifc, sc, kmc = G.curves(rows)
    return dict(n=n, E=E, C=C, Z=n - E - C, cif=cifc[-1][1] * n, km=kmc[-1][1] * n,
                known=E / (E + C) * n, pct=round(100 * cifc[-1][1]))


def run(target, g=None):
    global N
    N = 0
    g = g or G.compute(target)
    b = G.load(target)
    files = sorted(os.listdir(target))

    # ---------------------------------------------------------------- input gates
    ok("gate.files", len(files) >= 10, "%d files" % len(files))
    exts = {os.path.splitext(f)[1] for f in files}
    ok("gate.formats", len(exts) >= 3, str(exts))
    big = max(sum(1 for _ in open(os.path.join(target, f), encoding="utf-8")) - 1
              for f in files if f.endswith(".csv"))
    ok("gate.bulk", big >= 25000, "%d rows" % big)
    meta = json.load(open(os.path.join(os.path.dirname(target), "metadata.json")))
    ok("gate.distractors", len(meta["distractor_files"]) >= 2)
    for dd in meta["distractor_files"]:
        ok("gate.distractor.present", dd["file"] in files, dd["file"])
    ok("gate.no_answer_key",
       not any(k in open(os.path.join(target, f), encoding="utf-8", errors="replace").read(200000).lower()
               for f in files if f.endswith((".csv", ".json"))
               for k in ("is_correct", "should_exclude", "taxa_de_confronto", "confrontation_rate")))

    # ---------------------------------------------------------------- the call reproduces
    ok("call.cohort", g["cohort"] == 635, g["cohort"])
    ok("call.recorded", g["recorded"] == 89, g["recorded"])
    ok("call.closed", g["closed_quiet"] == 312, g["closed_quiet"])
    ok("call.open", g["still_open"] == 234, g["still_open"])
    ok("call.rate", g["rate_pct"] == 17, g["rate_pct"])
    ok("call.episodes", g["episodes"] == 108, g["episodes"])
    ok("call.parts_sum", g["recorded"] + g["closed_quiet"] + g["still_open"] == g["cohort"])

    # ---------------------------------------------------------------- the ladder
    ok("ladder.rung0", (g["rung0_pct"], g["rung0_episodes"]) == (14, 89))
    ok("ladder.rung1", (g["rung1_pct"], g["rung1_episodes"]) == (22, 141))
    ok("ladder.rung2", (g["rung2_pct"], g["rung2_episodes"]) == (28, 178))
    vals = [g["rung0_episodes"], g["raw_episodes"], g["raw_rung1"], g["raw_rung2"]]
    ok("ladder.order", vals[0] < vals[1] < vals[2] < vals[3], str(vals))
    gaps = [(vals[i + 1] - vals[i]) / vals[i] for i in range(3)]
    ok("ladder.separation", min(gaps) >= 0.20, str([round(x, 3) for x in gaps]))
    pcts = [g["rung0_pct"], g["rate_pct"], g["rung1_pct"], g["rung2_pct"]]
    ok("ladder.distinct_pct", len(set(pcts)) == 4, str(pcts))
    ok("ladder.decisive_move_largest",
       (vals[3] - vals[1]) > max(vals[1] - vals[0], vals[2] - vals[1]), str(vals))

    # ---------------------------------------------------------------- bins and variants
    ok("bin.episodes", abs(g["raw_episodes"] - g["episodes"]) <= 0.15, fmt(g["raw_episodes"]))
    ok("bin.rate", abs(g["raw_rate"] - g["rate_pct"]) <= 0.35, fmt(g["raw_rate"]))
    ok("variant.weekly", round(g["weekly_episodes"]) == 108 and
       round(100 * g["weekly_episodes"] / g["cohort"]) == 17, fmt(g["weekly_episodes"]))
    ok("variant.fortnightly", round(g["fortnightly_episodes"]) == 108 and
       round(100 * g["fortnightly_episodes"] / g["cohort"]) == 17, fmt(g["fortnightly_episodes"]))
    ok("variant.episode_by_episode", abs(g["projected_episodes"] - g["raw_episodes"]) < 1e-6,
       fmt(g["projected_episodes"]))
    ok("variant.plateau", g["at_risk_at_last"] >= 70, g["at_risk_at_last"])

    # ---------------------------------------------------------------- R1, the field's raw material
    heads = []
    for f in files:
        if f.endswith(".csv"):
            with open(os.path.join(target, f), encoding="utf-8") as fh:
                heads += next(csv.reader(fh))
    ok("R1.raw_rows", any(h == "id_relato" for h in heads) and any(h == "data_ocorrencia" for h in heads))
    ok("R1.no_episode_table", not any("episodio" in h.lower() for h in heads), str(heads))
    ok("R1.no_deciding_quantity", not any(h.lower().startswith(("taxa", "estado_episodio", "risco"))
                                          for h in heads))
    acts, coh = cohort_of(b["reports"])
    ok("R1.register_from_rows", len(coh) == 635 and len(acts) == g["actions_total"])

    # ---------------------------------------------------------------- R2, every mess item neutral
    def call_of(reports):
        return four(cohort_of(reports)[1])

    base = call_of(b["reports"])
    ok("R2.base", (base["n"], base["E"], round(base["cif"])) == (635, 89, 108))
    # one report per action against every report its own action
    per_report = []
    for i, r in enumerate(b["reports"]):
        rr = dict(r)
        rr["loc"] = r["loc"] + "#%d" % i if False else r["loc"]
        per_report.append(rr)
    ok("R2.duplicate_routes", call_of(per_report)["n"] == base["n"])
    # the re-imported month: drop the second load
    one_load = [r for r in b["reports"] if r.get("load") != "C20260802"]
    v = call_of(one_load)
    ok("R2.reimport", (v["n"], v["E"], round(v["cif"])) == (635, 89, 108), str(v))
    # the second language edition of the Atlantic group
    no_twin = [r for r in b["reports"] if r.get("src") != W.TWIN_FEED[1]]
    v = call_of(no_twin)
    ok("R2.twin_feed", (v["n"], v["E"], round(v["cif"])) == (635, 89, 108), str(v))
    # the former gazetteer names: resolve them away first
    cur = {}
    for r in rows_of(target, "gazeteiro_localidades.csv"):
        if r["estado_nome"] == "atual":
            cur[r["codigo_localidade"]] = r["nome"]
    renamed = [dict(r, place=cur.get(r["loc"], r["place"])) for r in b["reports"]]
    v = call_of(renamed)
    ok("R2.former_names", (v["n"], v["E"], round(v["cif"])) == (635, 89, 108), str(v))
    # the clocks: the call reads no reception stamp
    shifted = [dict(r, recv=r["recv"] + dt.timedelta(hours=1)) for r in b["reports"]]
    v = call_of(shifted)
    ok("R2.clocks", (v["n"], v["E"], round(v["cif"])) == (635, 89, 108), str(v))
    # the exceptions file carries no action and no report id the route files hold
    ids = {r["ident"] for r in b["reports"]}
    ok("R2.exceptions_disjoint", not ({e["ident"] for e in b["exceptions"]} & ids))
    # every distractor deleted leaves the call and every ask where they were
    for dd in meta["distractor_files"]:
        ok("R2.distractor_unused", dd["file"] not in ("registo_itens_imprensa.csv",
                                                      "relatos_rede_parceiros.csv",
                                                      "relatos_linha_publica.csv",
                                                      "gazeteiro_localidades.csv",
                                                      "excecoes_geocodificacao.csv",
                                                      "totais_por_via.csv"), dd["file"])

    # ---------------------------------------------------------------- R3a, the analyst test
    ok("R3a.analyst_test", base["E"] == 89 and round(base["cif"]) == 108 and base["E"] != 108)
    ok("R3a.analyst_pct", round(100 * base["E"] / base["n"]) == 14)
    # ---------------------------------------------------------------- R3b, the decisive step alone
    ok("R3b.decisive_only", round(base["km"]) == 178 and round(base["cif"]) == 108,
       "%s %s" % (fmt(base["km"]), fmt(base["cif"])))
    ok("R3b.known_outcomes", round(base["known"]) == 141)
    ok("R3b.each_rung_wrong", len({89, 141, 178} & {108}) == 0)
    # ---------------------------------------------------------------- R3c, no plant
    with open(os.path.join(target, "registo_itens_imprensa.csv"), encoding="utf-8") as fh:
        lines = fh.read().splitlines()[1:]
    blocks = {}
    for i in range(0, len(lines) - 20, 20):
        blocks.setdefault("|".join(x.split(",", 1)[1] for x in lines[i:i + 20]), 0)
        blocks["|".join(x.split(",", 1)[1] for x in lines[i:i + 20])] += 1
    ok("R3c.no_copied_block", max(blocks.values()) == 1)
    text = ""
    for f in files:
        if f.endswith((".csv", ".json")):
            text += open(os.path.join(target, f), encoding="utf-8", errors="replace").read(400000)
    for word in ("risco", "censur", "sobreviv", "incidencia", "estimativa de", "em risco"):
        ok("R3c.no_method_word.%s" % word, word not in text.lower(), word)
    ok("R3c.no_rate_published", "108" not in open(os.path.join(target, "boletins_anteriores_2026.pdf"),
                                                  "rb").read().decode("latin-1"))

    # ---------------------------------------------------------------- the semantic fork table
    # SF1 the episode unit: locality instead of municipality, or municipality whatever the theme
    by_loc = {}
    for a in acts:
        by_loc.setdefault((a["loc"], a["theme"]), []).append(a)
    ok("SF1.locality_unit", len(by_loc) != 635)
    ok("SF2.action_grain", g["actions_total"] < len(b["reports"]))
    confcodes = {c for c, _, f in W.ACTION_CODES if f}
    ok("SF3.codes", confcodes == {"CF", "RF", "DP"})
    ok("SF4.window", min(e["open"] for e in coh) >= W.PERIOD_FROM
       and max(e["open"] for e in coh) <= W.PERIOD_TO)
    ok("SF5.cohort_includes_open", g["still_open"] > 0 and round(base["known"]) == 141)
    # SF6 the record cut at the period's close: the same whole percentage
    cut = [r for r in b["reports"] if r["day"] <= W.PERIOD_TO]
    acts_c = G.actions(cut)
    eps_c = G.register(acts_c)
    for e in eps_c:
        e["closed"] = (W.PERIOD_TO - e["last"]).days >= W.QUIET_DAYS
        if e["conf"] is not None:
            e["t"], e["cause"] = (e["conf"] - e["open"]).days, 1
        elif e["closed"]:
            e["t"], e["cause"] = (e["last"] - e["open"]).days, 2
        else:
            e["t"], e["cause"] = (W.PERIOD_TO - e["open"]).days, 0
    cc = four([e for e in eps_c if W.PERIOD_FROM <= e["open"] <= W.PERIOD_TO])
    ok("SF6.cut_at_close", cc["pct"] == 17, str(cc))
    ok("SF7.episode_dates", all(e["last"] >= e["open"] for e in coh))
    ok("SF8.clear_days", W.QUIET_DAYS == 21)
    ok("SF9.place_resolution", all(r["loc"] for r in b["reports"]))
    ok("SF10.municipality", all(e["muni"] for e in coh))
    ok("SF11.action_date_fixed", all(r["start"].date() == r["day"] for r in b["reports"]))
    ok("SF12.reimport_neutral", round(call_of(one_load)["cif"]) == 108)
    ok("SF13.twin_neutral", round(call_of(no_twin)["cif"]) == 108)
    ok("SF14.rounding", abs(g["raw_rate"] - 17) < 0.35 and abs(g["raw_episodes"] - 108) < 0.15)
    ok("SF15.ties", len({14, 17, 22, 28}) == 4)
    ok("SF16.accepted_only", all(r["route"] != "IMP" or r["ident"] for r in b["reports"]))
    ok("SF17.extract", max(r["day"] for r in b["reports"]) <= W.EXTRACT)
    ok("SF18.no_carry_in", min(r["day"] for r in b["reports"]) >= W.OPEN_DAY)

    # ---------------------------------------------------------------- the realism sweep
    acts_by_fn = [v["actions"] for v in g["a1"].values()]
    ok("real.no_identical_periods", max(acts_by_fn.count(x) for x in acts_by_fn) <= 2, str(acts_by_fn))
    ok("real.no_round_call", g["raw_episodes"] % 1 != 0 and g["raw_rate"] % 1 != 0)
    for route, a2 in g["a2"].items():
        ok("real.median_not_round.%s" % route, a2["median_minutes"] % 10 != 0,
           "%s %s" % (route, a2["median_minutes"]))
        ok("real.median_one_reading.%s" % route, a2["median_pair_equal"],
           "%s %s" % (route, a2["median_minutes"]))
    for p, a3 in g["a3"].items():
        ok("real.euros_not_round.%s" % p, a3["euros"] % 100 != 0, "%s %s" % (p, a3["euros"]))
    for name in W.PEOPLE.values():
        hit = [f for f in files if name.split()[0].encode() in open(os.path.join(target, f), "rb").read()]
        ok("real.persona_only_where_filed.%s" % name.split()[0],
           all(f.endswith((".pdf", ".xlsx")) for f in hit), str(hit))
    ok("real.extract_coherent", all(r["recv"].date() <= W.EXTRACT for r in b["reports"]))
    man = {r["ficheiro"]: r for r in rows_of(target, "manifesto_extracao.csv")}
    ok("real.manifest_covers", set(files) - set(man) == {"manifesto_extracao.csv"},
       str(set(files) - set(man)))
    ok("real.manifest_extract_date",
       all(r["extraido_em"] == W.EXTRACT.isoformat() for r in man.values()))
    ok("real.item_rows_match",
       int(man["registo_itens_imprensa.csv"]["linhas"]) == big)

    # ---------------------------------------------------------------- the ask layer
    ok("ask.a1_fortnights", len(g["a1"]) == 13)
    ok("ask.a1_last_fortnight",
       W.fortnights()[-1][2] == W.PERIOD_TO and (W.fortnights()[-1][2] - W.fortnights()[-1][1]).days == 14)
    ok("ask.a1_total", sum(v["actions"] for v in g["a1"].values()) < g["actions_total"])
    ok("ask.a2_routes", len(g["a2"]) == 3 and all(v["unplaceable"] > 0 for v in g["a2"].values()))
    ok("ask.a3_partners", len(g["a3"]) == 7 and all(v["filed"] > 0 for v in g["a3"].values()))
    # the cracker's paths, each outside the ask's bin
    par_rows = rows_of(target, "relatos_rede_parceiros.csv")
    ok("cracker.a2_received", len(par_rows) != g["a2"]["PAR"]["received"],
       "%d %d" % (len(par_rows), g["a2"]["PAR"]["received"]))
    ok("cracker.a2_unplaceable_zero", g["a2"]["IMP"]["unplaceable"] > 0)
    naive_med = statistics.median(sorted(
        (r["recv"] - dt.timedelta(hours=1) - r["start"]).total_seconds() / 60.0
        for r in b["reports"] if r["route"] == "IMP"
        and W.PERIOD_FROM <= r["recv"].date() <= W.PERIOD_TO))
    ok("cracker.a2_median", abs(naive_med - g["a2"]["IMP"]["median_minutes"]) > 5,
       "%s %s" % (fmt(naive_med), g["a2"]["IMP"]["median_minutes"]))
    amended = g["a3"][W.AMENDED[0]]
    flat = 0.0
    seen = {}
    for r in b["reports"]:
        if r["route"] == "PAR":
            seen.setdefault(r["ident"], r)
    for r in seen.values():
        if r["src"] == W.AMENDED[0] and W.PERIOD_FROM <= r["day"] <= W.PERIOD_TO \
                and r["recv"].date() <= W.PERIOD_TO:
            flat += dict((p[0], p[3]) for p in W.PARTNERS)[W.AMENDED[0]]
    ok("cracker.a3_amendment", round(flat) != amended["euros"], "%d %d" % (round(flat), amended["euros"]))
    one_code = sum(1 for r in seen.values() if r["src"] == W.MERGED[0]
                   and W.PERIOD_FROM <= r["day"] <= W.PERIOD_TO)
    ok("cracker.a3_merged", one_code != g["a3"][W.MERGED[0]]["filed"],
       "%d %d" % (one_code, g["a3"][W.MERGED[0]]["filed"]))
    fn14 = [x for x in acts if W.PERIOD_TO < x["day"] <= W.PERIOD_TO + dt.timedelta(days=7)]
    ok("cracker.a1_scope", len(fn14) > 0, "%d actions after the period's close" % len(fn14))

    # ---------------------------------------------------------------- the separation line
    ok("sep.devices_outside_call",
       all(e["ident"] not in ids for e in b["exceptions"]))
    ok("sep.agreements_carry_no_action", "data_ocorrencia" not in
       open(os.path.join(target, "acordos_dados_parceiros.pdf"), "rb").read().decode("latin-1"))
    ok("sep.totals_carry_no_action",
       set(rows_of(target, "totais_por_via.csv")[0]) == {"data", "via", "relatos_recebidos"})
    return N
