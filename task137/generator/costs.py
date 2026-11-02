"""Own-damage repairs, the bodyshop's invoices and their accounts-payable postings, and the recoveries other insurers
paid. Every amount is computed forward from the collisions."""
import datetime as dt

import numpy as np

import params as P

SITES = {"CRA": "Washington", "GAT": "Washington", "CAR": "Carlisle", "DAR": "Stockton"}


def next_tuesday(d):
    k = (1 - d.weekday()) % 7
    return d + dt.timedelta(days=k if k else 7)


def in_double_send(d):
    return any(a <= d <= b for a, b in P.DOUBLE_SEND)


def money(x):
    return float(np.round(x + 1e-9, 2))


def adas_fit(W, seed):
    """Each truck's forward sensors: a windscreen camera on every truck, a front radar beside it on most newer ones."""
    rng = np.random.default_rng([seed, 3])
    newer = ("21", "71", "22", "72", "23", "73", "24", "74", "25", "75")
    for v in W["vehicles"]:
        p = 0.78 if v["reg"][2:4] in newer else 0.30
        v["adas"] = "Camera and radar" if rng.random() < p else "Camera"


def build(W, seed=P.SEED):
    adas_fit(W, seed)
    fit = {v["reg"]: v["adas"] for v in W["vehicles"]}
    rng = np.random.default_rng([seed, 2])
    jobs, invoices = [], []
    jn = 600000 + int(rng.integers(0, 4000))
    for i, c in enumerate(W["claims"]):
        c["idx"] = i
        if not c["od"] or c["shop_in"] is None:
            continue
        jn += int(rng.integers(3, 29))
        job = "BAR%07d" % jn
        done = c["shop_out"]
        total = float(np.exp(np.log(P.REPAIR_MEDIAN) + P.REPAIR_SIGMA * rng.normal()))
        total = min(max(total, 380.0), 16500.0)
        nsup = 2 if rng.random() < P.P_SUPP2 else (1 if rng.random() < P.P_SUPP1 / (1 - P.P_SUPP2) else 0)
        parts = [1.0] + list(rng.uniform(0.08, 0.30, nsup))
        parts = np.array(parts) / sum(parts)
        nadas = 0
        if rng.random() < P.P_ADAS:
            nadas = 2 if fit[c["reg"]] == "Camera and radar" else 1
        late = int(rng.integers(2, 7)) if (nadas == 2 and rng.random() < P.P_LATE_CERT) else 0
        rec = rng.random() < P.P_RECOVERY
        items = []
        for k, p in enumerate(parts):
            items.append(("Accident repair" if k == 0 else "Supplementary repair", money(total * p), 0))
        for k in range(nadas):
            items.append(("ADAS calibration", P.ADAS_NET, late if k == 1 else 0))
        if rec:
            items.append(("Recovery and storage", money(P.RECOVERY_FEE + 18.0 * int(rng.integers(1, 6))), 0))
        c["job"] = job
        c["od_net"] = money(sum(x[1] for x in items))
        jobs.append({"job": job, "claim": i, "site": SITES[c["depot"]], "in": c["shop_in"], "out": done,
                     "reg": c["reg"], "nadas": nadas, "kind": "repair"})
        # invoices, every one dated at the job's completion; the radar calibration's waits for its certificate
        for desc, net, lag in items:
            sent = done + dt.timedelta(days=lag)
            invoices.append({"job": job, "claim": i, "inv_date": done, "sent": sent, "desc": desc, "net": net,
                             "copy": False})
            if in_double_send(sent):
                invoices.append({"job": job, "claim": i, "inv_date": done, "sent": sent + dt.timedelta(days=7),
                                 "desc": desc, "net": net, "copy": True})
    # write-offs: the engineer's inspection and the storage until the salvage agent collects
    for c in W["claims"]:
        if c["od"] and c["write_off"]:
            jn += int(rng.integers(3, 29))
            job = "BAR%07d" % jn
            d = c["date"] + dt.timedelta(days=int(rng.integers(3, 12)))
            net = money(165.0 + 18.0 * int(rng.integers(6, 21)))
            c["job"], c["od_net"] = job, net
            jobs.append({"job": job, "claim": c["idx"], "site": SITES[c["depot"]], "in": c["date"], "out": d,
                         "reg": c["reg"], "nadas": 0, "kind": "total loss"})
            invoices.append({"job": job, "claim": c["idx"], "inv_date": d, "sent": d, "desc": "Inspection and storage",
                             "net": net, "copy": False})
            if in_double_send(d):
                invoices.append({"job": job, "claim": c["idx"], "inv_date": d, "sent": d + dt.timedelta(days=7),
                                 "desc": "Inspection and storage", "net": net, "copy": True})
    # accounts payable postings: the weekly Tuesday import numbers documents in posting order
    invoices = [x for x in invoices if next_tuesday(x["sent"]) <= P.LISTING_AS_AT]
    invoices.sort(key=lambda x: (next_tuesday(x["sent"]), x["sent"], x["job"], x["desc"], x["copy"]))
    doc = 5100000 + int(rng.integers(0, 9000))
    for x in invoices:
        doc += int(rng.integers(1, 4))
        x["posted"] = next_tuesday(x["sent"])
        x["ap_doc"] = "PI%07d" % doc
    W["jobs"], W["invoices"] = jobs, invoices
    recoveries(W, rng)


def recoveries(W, rng):
    """Other insurers pay the share of the own-damage outlay their policyholder was liable for, net of VAT, in one
    payment; some quote Tarnfield's claim number, some only their own reference."""
    rec = []
    ref_n = {}
    for c in W["claims"]:
        if c["liability"] not in ("theirs", "shared") or not c.get("od_net") or c["write_off"]:
            continue
        share = 1.0 if c["liability"] == "theirs" else c["share"]
        lag = int(rng.integers(*P.RECOVERY_LAG_D))
        when = c["date"] + dt.timedelta(days=lag)
        if when > P.LISTING_AS_AT or when < P.RECEIPTS_FROM:
            continue
        if c["date"] < dt.date(2026, 3, 1) and rng.random() > P.P_RECOVERED:
            continue
        ins = c["tp_insurer"]
        k = ref_n.setdefault(ins, int(rng.integers(200000, 900000)))
        ref_n[ins] = k + int(rng.integers(40, 900))
        amount = float(np.round(c["od_net"] * share + 1e-9, 2))
        rec.append({"claim": c["idx"], "date": when, "payer": ins, "payer_ref": "%s%d" % (ins[:2].upper(), k),
                    "quotes_ours": bool(rng.random() < P.P_OUR_REF), "amount": amount, "share": share})
    rec.sort(key=lambda r: (r["date"], r["payer"], r["amount"]))
    W["receipts"] = rec
