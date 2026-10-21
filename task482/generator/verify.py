"""An independent recomputation of every graded figure from the cut pack, written apart from bundle.py (pandas and
numpy's busday_count), compared with generator/figures.json.

    python3 task482/generator/verify.py [target]"""
import json
import os
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)


def main(target=None, gdir=None):
    target = target or os.path.join(TASK, "target")
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    hol = np.array(pd.read_csv(os.path.join(target, "cro_public_holidays_2026.csv"))["date"].tolist(),
                   dtype="datetime64[D]")
    old = pd.read_csv(os.path.join(target, "cro_registrations_legacy_system_2026-07.csv"))
    new = pd.read_csv(os.path.join(target, "cro_registrations_case_system_2026-08_to_2026-10.csv"))
    reg = pd.concat([
        pd.DataFrame({"o": "CRO-" + old.Office, "rec": pd.to_datetime(old.Received, dayfirst=True),
                      "c": pd.to_datetime(old.Complete, dayfirst=True), "g": pd.to_datetime(old.Registered,
                                                                                            dayfirst=True)}),
        pd.DataFrame({"o": new.office_code, "rec": pd.to_datetime(new.received_on), "c": pd.to_datetime(new.clock_start),
                      "g": pd.to_datetime(new.registered_on)})])
    reg = reg[(reg.rec >= "2026-07-01") & (reg.rec <= "2026-09-30")]
    op = pd.read_csv(os.path.join(target, "cro_open_caseload_snapshot_2026-10-09.csv"), parse_dates=["received_on",
                                                                                                      "clock_start"])
    op = op[(op.received_on >= "2026-07-01") & (op.received_on <= "2026-09-30")]

    def bd(a, c):
        # working days after a up to and including c
        a = np.array(a.dt.strftime("%Y-%m-%d").tolist(), dtype="datetime64[D]")
        c = np.array(c.dt.strftime("%Y-%m-%d").tolist(), dtype="datetime64[D]")
        return np.busday_count(a + 1, c + 1, holidays=hol)
    reg["t"] = bd(reg.c, reg.g)
    op["t"] = bd(op.clock_start, pd.Series(pd.Timestamp("2026-10-09"), index=op.index))
    planned = []
    for u in sorted(reg.o.unique()):
        t = np.concatenate([reg[reg.o == u].t.values, np.repeat(op[op.office_code == u].t.values,
                                                                op[op.office_code == u].open_applications.values)])
        e = np.concatenate([np.ones((reg.o == u).sum(), bool), np.zeros(int(op[op.office_code == u].open_applications.sum()),
                                                                         bool)])
        s = 1.0
        med = None
        for tt in np.unique(t):
            at = (t >= tt).sum()
            d = ((t == tt) & e).sum()
            s *= 1 - d / at
            if s <= 0.5:
                med = tt
                break
        if med > 20:
            planned.append(u)
    bad = int(planned != fig["call"]["planned"])
    pays = pd.read_csv(os.path.join(target, "cro_card_payments_settled_2026-07_to_2026-10.csv"))
    bat = pd.read_csv(os.path.join(target, "cro_card_settlement_batches_2026q3.csv"))
    pays = pays.merge(bat[["batch_id", "terminal_date"]], on="batch_id")
    q = pays[(pays.terminal_date >= "2026-07-01") & (pays.terminal_date <= "2026-09-30")]
    g = q.groupby("office_code").amount_eur.agg(["size", "sum"])
    for u, v in fig["ask"].items():
        bad += int(g.loc[u, "size"]) != v["payments"]
        bad += int(round(g.loc[u, "sum"])) != v["amount"]
    print("verify: %d figures differ from figures.json" % bad)
    return bad == 0


if __name__ == "__main__":
    sys.exit(0 if main(sys.argv[1] if len(sys.argv) > 1 else None) else 1)
