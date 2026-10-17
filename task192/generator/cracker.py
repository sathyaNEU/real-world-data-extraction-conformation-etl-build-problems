"""Run the cracker's path for every row of the design note's cracker sheet, on the cut pack.

The sheet is read by a gate, so its figures are measured here and not by hand. Each row below is the
golden's own figure beside the figure a competent solver reaches on the named wrong path, computed from
the shipped bundle through `golden.py`'s readers. Usage: python3 cracker.py [target_dir]
"""
import csv
import datetime as dt
import os
import statistics
import sys

import golden as G
import world as W

HERE = os.path.dirname(os.path.abspath(__file__))
CONF = set(W.CONFRONTATIONAL)


def rows_of(target, name):
    with open(os.path.join(target, name), encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def run(target):
    g = G.compute(target)
    b = G.load(target)
    acts = G.actions(b["reports"])
    par_rows = rows_of(target, "relatos_rede_parceiros.csv")
    items = rows_of(target, "registo_itens_imprensa.csv")
    gaz = {r["nome"]: r for r in rows_of(target, "gazeteiro_localidades.csv")}
    recv = {}
    for r in b["reports"]:
        if r["route"] == "PAR":
            recv[r["ident"]] = r["recv"].date()
    fort = {label: (a, bb) for label, a, bb in W.fortnights()}
    out = []

    # ---- A1, the partner column: the three paths the sheet names
    for label, path in (("Q8", "rows"), ("Q10", "delivery"), ("Q11", "only")):
        a, bb = fort[label]
        inside = [x for x in acts if a <= x["day"] <= bb]
        gold = len([x for x in inside if "PAR" in x["routes"]])
        if path == "rows":
            got = sum(1 for r in par_rows if a <= G.pdate(r["data_ocorrencia"]) <= bb)
            why = "counts the network's rows, so the reposted August load counts twice"
        elif path == "delivery":
            got = len({(x["theme"], x["loc"], x["day"]) for x in acts if "PAR" in x["routes"]
                       for r in x["reports"] if r["route"] == "PAR" and a <= recv[r["ident"]] <= bb})
            why = "dates the column by the delivery rather than the action"
        else:
            got = len([x for x in inside if x["routes"] == {"PAR"}])
            why = "counts only the actions no other route reported"
        out.append(("A1 actions the partner network reported, fortnight %s" % label[1:], why,
                    got, gold))

    # ---- A2, the route table
    a, bb = W.PERIOD_FROM, W.PERIOD_TO
    counter = sum(int(r["relatos_recebidos"]) for r in b["totals"]
                  if r["via"] == "PAR" and a <= G.pdate(r["data"]) <= bb)
    out.append(("A2 reports received, the partner network",
                "sums the ingest counter, which counts the reposted load again",
                counter, g["a2"]["PAR"]["received"]))
    out.append(("A2 reports that could not be placed, the press monitor",
                "the item log alone, which holds only the items it placed",
                0, g["a2"]["IMP"]["unplaceable"]))
    raw = sorted((r["recv_utc"] - r["start"]).total_seconds() / 60.0 for r in b["reports"]
                 if r["route"] == "IMP" and a <= r["recv"].date() <= bb)
    out.append(("A2 median minutes from the action to the report, the press monitor",
                "reads the monitor's reception stamp as local time",
                round(statistics.median(raw), 1), g["a2"]["IMP"]["median_minutes"]))
    every = []
    for r in items:
        if r["estado"] != "aceite":
            continue
        gz = gaz.get(r["local_texto"])
        if gz is None:
            continue
        st, rc = G.pts(r["inicio_acao"]), G.pts(r["carimbo_recepcao"])
        if not (a <= G.to_lisbon(rc).date() <= bb):
            continue
        every.append((rc - (st - dt.timedelta(
            hours=G.offset(gz["distrito"], st.date())))).total_seconds() / 60.0)
    out.append(("A2 median minutes, the press monitor, every item",
                "takes every item of a report rather than the first",
                round(statistics.median(sorted(every)), 1), g["a2"]["IMP"]["median_minutes"]))

    # ---- A3, the partner table
    seen = {}
    for r in par_rows:
        seen.setdefault(r["id_relato"], r)
    rate = dict((p[0], p[3]) for p in W.PARTNERS)
    flat = sum(rate[W.AMENDED[0]] for r in seen.values()
               if r["codigo_parceiro"] == W.AMENDED[0]
               and W.PERIOD_FROM <= G.pdate(r["data_ocorrencia"]) <= W.PERIOD_TO
               and recv[r["id_relato"]] <= W.PERIOD_TO)
    out.append(("A3 euros paid, the amended partner",
                "the schedule's rate for the whole period, without the July adenda",
                round(flat), g["a3"][W.AMENDED[0]]["euros"]))
    one = [r for r in seen.values() if r["codigo_parceiro"] == W.MERGED[0]
           and W.PERIOD_FROM <= G.pdate(r["data_ocorrencia"]) <= W.PERIOD_TO]
    out.append(("A3 reports filed, the merged partner",
                "one delivery code, without the September addendum",
                len(one), g["a3"][W.MERGED[0]]["filed"]))
    paid_one = [r for r in one if recv[r["id_relato"]] <= W.PERIOD_TO]
    out.append(("A3 euros paid, the merged partner",
                "one delivery code, without the September addendum",
                round(rate[W.MERGED[0]] * len(paid_one)), g["a3"][W.MERGED[0]]["euros"]))
    allrows = len(seen)
    out.append(("A3 reports filed, all seven partners",
                "every row of the partner file rather than the period's actions",
                allrows, sum(v["filed"] for v in g["a3"].values())))
    return out


if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "target")
    table = run(target)
    print("| Ask figure | Cracker's path | Cracker's figure | Golden | Result |")
    print("|---|---|---|---|---|")
    bad = 0
    for ask, why, got, gold in table:
        hit = got == gold
        bad += 1 if hit else 0
        print("| %s | %s | %s | %s | %s |" % (ask, why, got, gold, "KEEPS" if hit else "miss"))
    print()
    print("%d rows, %d kept by the cracker" % (len(table), bad))
    sys.exit(1 if bad else 0)
