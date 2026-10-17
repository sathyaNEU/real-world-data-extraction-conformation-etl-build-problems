"""An independent read of the shipped bundle: nothing from the generator, its own code path.

Builds the actions from a dictionary of keys rather than the generator's objects, reads the
classifier's two error rates off the hand-coding worksheet as counts, and writes the correction as
the inverted confusion matrix over the marked counts instead of the rates applied to the marked
share. Converts every moment through the offsets the monitor's configuration states.
"""
import csv
import datetime as dt
import json
import os

CONF = {"CF", "RF", "DP"}
P0, P1 = dt.date(2026, 5, 1), dt.date(2026, 10, 30)
EXTRACT = dt.date(2026, 11, 6)
DST = dt.date(2026, 10, 25)
AZORES = "Acores"
RATE = {"P01": 6.35, "P02": 5.95, "P03": 7.20, "P04": 5.45, "P05": 6.90, "P06": 8.10, "P07": 6.15}
AMENDED = ("P04", dt.date(2026, 8, 1), 6.30)
GRAIN = 50
N = 0


def ok(label, cond, detail=""):
    global N
    N += 1
    if not cond:
        raise AssertionError("verify %s failed %s" % (label, detail))


def table(target, name):
    with open(os.path.join(target, name), encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def moment(s):
    s = s.strip().rstrip("Z").replace("T", " ")
    return dt.datetime(int(s[0:4]), int(s[5:7]), int(s[8:10]), int(s[11:13]), int(s[14:16]))


def off(district, local_day):
    if district == AZORES:
        return 0 if local_day < DST else -1
    return 1 if local_day < DST else 0


def grain(x):
    return int(round(x / float(GRAIN))) * GRAIN


def run(target, figures):
    global N
    N = 0
    f = json.load(open(figures))
    loc_of, muni_of, dist_of = {}, {}, {}
    for r in table(target, "gazeteiro_localidades.csv"):
        loc_of[r["nome"]] = r["codigo_localidade"]
        muni_of[r["codigo_localidade"]] = r["codigo_municipio"]
        dist_of[r["codigo_localidade"]] = r["distrito"]

    recs, first = [], {}
    for r in table(target, "registo_itens_imprensa.csv"):
        if r["estado"] != "aceite":
            continue
        m = moment(r["carimbo_recepcao"])
        if r["id_relato"] in first:
            if m < first[r["id_relato"]][0]:
                first[r["id_relato"]] = (m, r)
            continue
        first[r["id_relato"]] = (m, r)
    for ident, (m, r) in first.items():
        recs.append(["IMP", ident, r["orgao"], r["tema"], r["codigo_acao"], r["local_texto"],
                     dt.date.fromisoformat(r["data_ocorrencia"]), moment(r["inicio_acao"]), m])
    for r in table(target, "relatos_rede_parceiros.csv"):
        recs.append(["PAR", r["id_relato"], r["codigo_parceiro"], r["tema"], r["codigo_acao"],
                     r["local_texto"], dt.date.fromisoformat(r["data_ocorrencia"]),
                     moment(r["inicio_acao"]), moment(r["carimbo_entrega_utc"])])
    for r in table(target, "relatos_linha_publica.csv"):
        local = moment(r["carimbo_recepcao"])
        recs.append(["LIN", r["id_relato"], "LIN", r["tema"], r["codigo_acao"], r["local_texto"],
                     dt.date.fromisoformat(r["data_ocorrencia"]), moment(r["inicio_acao"]),
                     local - dt.timedelta(hours=off("Lisboa", local.date()))])

    press_code, filer_code, routes_of, muni_key, idents = {}, {}, {}, {}, {}
    lag_of, recv_of = {}, {}
    for route, ident, src, theme, code, place, day, start, recv_utc in recs:
        loc = loc_of.get(place)
        if loc is None:
            continue
        k = (theme, loc, day)
        routes_of.setdefault(k, set()).add(route)
        muni_key[k] = muni_of[loc]
        if route == "IMP":
            press_code[k] = code
            idents.setdefault(k, set()).add(ident)
        else:
            filer_code.setdefault(k, code)
        start_utc = start - dt.timedelta(hours=off(dist_of[loc], start.date()))
        lag_of[(route, ident)] = (recv_utc - start_utc).total_seconds() / 60.0
        recv_of[(route, ident)] = recv_utc + dt.timedelta(hours=off("Lisboa", recv_utc.date()))
    keys = sorted(routes_of)
    ok("actions", len(keys) > 0)
    inper = [k for k in keys if P0 <= k[2] <= P1]
    ok("actions_in_period", len(inper) == f["actions_in_period"], "%d" % len(inper))
    pressed = [k for k in inper if k in press_code]
    other = [k for k in inper if k not in press_code]
    ok("press_reported", len(pressed) == f["press_only_actions"], "%d" % len(pressed))
    ok("other_actions", len(other) == f["actions_with_a_filer_report"])
    H = sum(1 for k in other if filer_code[k] in CONF)
    O = sum(1 for k in pressed if press_code[k] in CONF)
    ok("hand_conf", H == f["hand_coded_confrontational"], "%d" % H)
    ok("press_marked", O == f["press_marked_confrontational"], "%d" % O)

    sample = table(target, "amostra_dupla_codificacao.csv")
    tp = fn = fp = tn = 0
    for r in sample:
        m, h = r["codigo_monitor"] in CONF, r["codigo_manual"] in CONF
        tp, fn, fp, tn = tp + (m and h), fn + (h and not m), fp + (m and not h), \
            tn + (not m and not h)
    ok("sample.cells", (tp, fn, fp, tn) == (f["sample_tp"], f["sample_fn"], f["sample_fp"],
                                            f["sample_tn"]), str((tp, fn, fp, tn)))
    se = tp / float(tp + fn)
    fmr = fp / float(fp + tn)
    ok("sample.recall", abs(se - f["classifier_recall"]) < 5e-5, "%.5f" % se)
    ok("sample.false_mark", abs(fmr - f["classifier_false_mark_rate"]) < 5e-5, "%.5f" % fmr)
    # the inverted confusion matrix over the marked counts, not the rates over the marked share
    n = len(pressed)
    true_marked = (O - n * fmr) / (se - fmr)
    total = H + true_marked
    ok("call.total", grain(total) == f["call_actions"], "%.4f" % total)
    ok("call.raw", abs(total - f["raw_total"]) < 0.01, "%.4f" % total)
    ok("call.grain", f["grain"] == GRAIN)

    # every other route the record leaves standing
    ppv = tp / float(tp + fp)
    npv = fn / float(fn + tn)
    sid = {r["id_relato"] for r in sample}
    hand_true = sum(1 for r in sample if r["codigo_manual"] in CONF)
    unsampled_marked = sum(1 for k in pressed
                           if press_code[k] in CONF and not (idents[k] & sid))
    routes = {"naive": float(H + O), "remove_fp_ppv": H + O * ppv,
              "remove_fp_fpr": H + O - fmr * n, "recall_only": H + O / se,
              "pv_pooled": H + O * ppv + (n - O) * npv,
              "audit_prevalence": H + (tp + fn) / float(len(sample)) * n,
              "hand_where_audited": float(H + hand_true + unsampled_marked)}
    for name, value in sorted(routes.items()):
        ok("route.%s" % name, abs(value - f["candidates"][name]) < 0.01,
           "%s %.4f against %.4f" % (name, value, f["candidates"][name]))
        ok("route.%s.cell" % name, grain(value) != f["call_actions"],
           "%s lands in the committed cell" % name)
        ok("route.%s.six" % name, abs(value - total) >= 0.06 * total,
           "%s is %.2f per cent away" % (name, 100 * abs(value - total) / total))
    # the stratified families have no rate for the autumn, which the audit never reached
    audit_months = sorted({dt.date.fromisoformat(r["data_ocorrencia"]).month for r in sample})
    ok("strata.audit_months", audit_months == f["audit_months"], str(audit_months))
    ok("strata.population_months",
       sorted({k[2].month for k in pressed}) == [5, 6, 7, 8, 9, 10])
    audit_themes = {r["tema"] for r in sample}
    missing = sorted({k[0] for k in pressed} - audit_themes)
    ok("strata.themes_without_a_rate", missing == f["themes_without_an_audited_report"],
       str(missing))

    bounds, start, k = [], P0, 1
    while start <= P1:
        end = min(start + dt.timedelta(days=13), P1)
        if (P1 - end).days < 14:
            end = P1
        bounds.append(("Q%d" % k, start, end))
        start, k = end + dt.timedelta(days=1), k + 1
    ok("fortnights", len(bounds) == f["fortnight_rows"])
    total_actions = 0
    for label, a, bb in bounds:
        inside = [k2 for k2 in keys if a <= k2[2] <= bb]
        exp = f["fortnights"][label]
        ok("a1.%s.actions" % label, len(inside) == exp["actions"], "%d" % len(inside))
        ok("a1.%s.muni" % label, len({muni_key[k2] for k2 in inside}) == exp["municipalities"])
        par = [k2 for k2 in inside if "PAR" in routes_of[k2]]
        ok("a1.%s.share" % label,
           abs(round(100.0 * len(par) / len(inside), 1) - exp["partner_share_pct"]) < 0.051)
        marked = [k2 for k2 in inside
                  if (press_code[k2] if k2 in press_code else filer_code[k2]) in CONF]
        ok("a1.%s.marked" % label, len(marked) == exp["marked_actions"])
        total_actions += len(inside)
    ok("a1.total", total_actions == f["actions_in_period"])

    exc = table(target, "excecoes_geocodificacao.csv")
    for route in ("IMP", "PAR", "LIN"):
        seen, placed = set(), []
        for r in recs:
            if r[0] != route or r[1] in seen:
                continue
            seen.add(r[1])
            if r[5] not in loc_of:
                continue
            if P0 <= recv_of[(route, r[1])].date() <= P1:
                placed.append(r)
        unp = [e for e in exc if e["via"] == route
               and P0 <= moment(e["carimbo_recepcao"]).date() <= P1]
        got = f["routes"][route]
        ok("a2.%s.received" % route, len(placed) + len(unp) == got["received"],
           "%d" % (len(placed) + len(unp)))
        ok("a2.%s.unplaceable" % route, len(unp) == got["unplaceable"])
        mins = sorted(lag_of[(route, r[1])] for r in placed)
        mid = (mins[len(mins) // 2] if len(mins) % 2 else
               (mins[len(mins) // 2 - 1] + mins[len(mins) // 2]) / 2.0)
        ok("a2.%s.median" % route, abs(mid - got["median_minutes"]) < 0.051, "%.1f" % mid)

    first_par = {}
    for r in recs:
        if r[0] == "PAR":
            first_par.setdefault(r[1], r)
    for code, rate in sorted(RATE.items()):
        mine = [r for r in first_par.values()
                if (r[2] if r[2] in RATE else "P07") == code and P0 <= r[6] <= P1]
        late = [r for r in mine if recv_of[("PAR", r[1])].date() > P1]
        euros = 0.0
        for r in mine:
            day = recv_of[("PAR", r[1])].date()
            if day > P1:
                continue
            euros += AMENDED[2] if (code == AMENDED[0] and day >= AMENDED[1]) else rate
        got = f["partners"][code]
        ok("a3.%s.filed" % code, len(mine) == got["filed"], "%d" % len(mine))
        ok("a3.%s.late" % code, len(late) == got["after_close"])
        ok("a3.%s.euros" % code, round(euros) == got["euros"], "%.2f" % euros)

    files = sorted(os.listdir(target))
    ok("gate.files", len(files) >= 10, "%d" % len(files))
    ok("gate.formats", len({os.path.splitext(x)[1] for x in files}) >= 3)
    big = max(sum(1 for _ in open(os.path.join(target, x), encoding="utf-8")) - 1
              for x in files if x.endswith(".csv"))
    ok("gate.bulk", big >= 25000, "%d" % big)
    return N
