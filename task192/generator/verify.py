"""An independent read of the shipped bundle: nothing from the generator, its own code path.

Builds the actions from a dictionary of keys rather than the generator's objects, reads the two error
rates off the hand-coding file as counts, and writes the correction as the inverted confusion matrix
over the observed counts instead of the rates applied to the observed share.
"""
import csv
import datetime as dt
import json
import os

CONF = {"CF", "RF", "DP"}
P0, P1 = dt.date(2026, 5, 1), dt.date(2026, 10, 30)
EXTRACT = dt.date(2026, 11, 6)
DST = dt.date(2026, 10, 25)
RATE = {"P01": 6.40, "P02": 5.95, "P03": 7.25, "P04": 5.45, "P05": 6.75, "P06": 8.15, "P07": 6.40}
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


def to_local(m, utc):
    return m + dt.timedelta(hours=1 if (utc and (m + dt.timedelta(hours=1)).date() < DST) else 0) \
        if utc else m


def run(target, figures):
    global N
    N = 0
    f = json.load(open(figures))
    loc_of, muni_of = {}, {}
    for r in table(target, "gazeteiro_localidades.csv"):
        loc_of[r["nome"]] = r["codigo_localidade"]
        muni_of[r["codigo_localidade"]] = r["codigo_municipio"]

    recs, seen = [], set()
    for r in table(target, "registo_itens_imprensa.csv"):
        if r["estado"] != "aceite" or r["id_relato"] in seen:
            continue
        seen.add(r["id_relato"])
        recs.append(("IMP", r["id_relato"], r["orgao"], r["tema"], r["codigo_acao"],
                     r["local_texto"], dt.date.fromisoformat(r["data_ocorrencia"]),
                     moment(r["inicio_acao"]), to_local(moment(r["carimbo_recepcao"]), True)))
    for r in table(target, "relatos_rede_parceiros.csv"):
        recs.append(("PAR", r["id_relato"], r["codigo_parceiro"], r["tema"], r["codigo_acao"],
                     r["local_texto"], dt.date.fromisoformat(r["data_ocorrencia"]),
                     moment(r["inicio_acao"]), to_local(moment(r["carimbo_entrega_utc"]), True)))
    for r in table(target, "relatos_linha_publica.csv"):
        recs.append(("LIN", r["id_relato"], "LIN", r["tema"], r["codigo_acao"], r["local_texto"],
                     dt.date.fromisoformat(r["data_ocorrencia"]), moment(r["inicio_acao"]),
                     to_local(moment(r["carimbo_recepcao"]), False)))

    press_code, filer_code, routes_of, muni_key = {}, {}, {}, {}
    for route, ident, src, theme, code, place, day, start, recv in recs:
        loc = loc_of.get(place)
        if loc is None:
            continue
        k = (theme, loc, day)
        routes_of.setdefault(k, set()).add(route)
        muni_key[k] = muni_of[loc]
        if route == "IMP":
            press_code[k] = code
        else:
            filer_code.setdefault(k, code)
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

    tp = fn = fp = tn = 0
    for r in table(target, "amostra_dupla_codificacao.csv"):
        m, h = r["codigo_monitor"] in CONF, r["codigo_manual"] in CONF
        tp, fn, fp, tn = tp + (m and h), fn + (h and not m), fp + (m and not h), \
            tn + (not m and not h)
    ok("sample.cells", (tp, fn, fp, tn) == (f["sample_tp"], f["sample_fn"], f["sample_fp"],
                                            f["sample_tn"]), str((tp, fn, fp, tn)))
    se = tp / (tp + fn)
    fmr = fp / (fp + tn)
    ok("sample.recall", abs(se - f["classifier_recall"]) < 5e-5, "%.5f" % se)
    ok("sample.false_mark", abs(fmr - f["classifier_false_mark_rate"]) < 5e-5, "%.5f" % fmr)
    # the inverted confusion matrix over the observed counts, not the rates over the observed share
    n = len(pressed)
    true_marked = (O - n * fmr) / (se - fmr)
    total = H + true_marked
    ok("call.total", round(total) == f["call_actions"], "%.4f" % total)
    ok("call.raw", abs(total - f["raw_total"]) < 0.01, "%.4f" % total)
    ok("rung0", H + O == f["rung0_actions"], "%d" % (H + O))
    ok("rung1", round(H + O * tp / (tp + fp)) == f["rung1_actions"])
    ok("rung2", round(H + O / se) == f["rung2_actions"])
    ok("ladder.order", H + O * tp / (tp + fp) < H + O < total < H + O / se)

    bounds, start, k = [], P0, 1
    while start <= P1:
        end = min(start + dt.timedelta(days=13), P1)
        if (P1 - end).days < 7:
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
        placed, ids = [], set()
        for r in recs:
            if r[0] != route or r[1] in ids:
                continue
            ids.add(r[1])
            if P0 <= r[8].date() <= P1:
                placed.append(r)
        unp = [e for e in exc if e["via"] == route
               and P0 <= moment(e["carimbo_recepcao"]).date() <= P1]
        got = f["routes"][route]
        ok("a2.%s.received" % route, len(placed) + len(unp) == got["received"],
           "%d" % (len(placed) + len(unp)))
        ok("a2.%s.unplaceable" % route, len(unp) == got["unplaceable"])
        mins = sorted((r[8] - r[7]).total_seconds() / 60.0 for r in placed)
        mid = (mins[len(mins) // 2] if len(mins) % 2 else
               (mins[len(mins) // 2 - 1] + mins[len(mins) // 2]) / 2.0)
        ok("a2.%s.median" % route, abs(mid - got["median_minutes"]) < 0.051, "%.1f" % mid)

    first = {}
    for r in recs:
        if r[0] == "PAR":
            first.setdefault(r[1], r)
    for code, rate in sorted(RATE.items()):
        mine = [r for r in first.values()
                if (r[2] if r[2] in RATE else "P07") == code and P0 <= r[6] <= P1]
        late = [r for r in mine if r[8].date() > P1]
        euros = 0.0
        for r in mine:
            if r[8].date() > P1:
                continue
            euros += 6.20 if (code == "P04" and r[8].date() >= dt.date(2026, 8, 1)) else rate
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
