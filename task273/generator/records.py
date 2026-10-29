"""task273 architecture 5: the pack's data files, each in the form the system that keeps it exports."""
from __future__ import annotations

import csv
import json
from datetime import date, datetime, timedelta

import numpy as np

import params as P
import world as Wd


def write_csv(path, head, rows, delim=","):
    with open(path, "w", newline="", encoding="utf-8") as fh:
        wr = csv.writer(fh, delimiter=delim, lineterminator="\n")
        wr.writerow(head)
        wr.writerows(rows)


def d(x):
    return "" if x is None else x.isoformat()


NAME = {s[0]: s[1] for s in P.SUBS}
LEGACY_TAG = {"TBN": "TIBB_ZS_NET_MW"}          # the historian kept Tibbarin's pre-2019 point name


class Records:
    def __init__(self, w):
        self.w = w
        self.rng = np.random.default_rng(np.random.SeedSequence(w.seed + 901))

    # -------------------------------------------------------------------------------------- SCADA historian
    def spine(self):
        """Zone substation net demand, half-hourly, as the SCADA historian exports it (UTC, interval ending)."""
        w = self.w
        r = self.rng
        head = ["point_name", "interval_end_utc", "value_mw", "quality"]
        rows = []
        # communications losses the historian filled by interpolation, on weekday nights only
        est = set()
        for c in w.codes:
            for _ in range(int(r.integers(0, 3))):
                n = int(r.integers(2, 7))
                while True:
                    k = int(r.integers(48, w.K - 48))
                    if all(w.kdow[j] < 5 and (w.khour[j] < 5 or w.khour[j] >= 21) for j in range(k, k + n)):
                        break
                for j in range(n):
                    est.add((c, k + j))
        self.est = est
        for c in w.codes:
            tag = LEGACY_TAG.get(c, P.SCADA_TAG.format(code=c))
            v = w.mw[c]
            for k in range(w.K):
                val = v[k]
                q = "GOOD"
                if (c, k) in est:
                    j0 = k
                    while (c, j0) in est:
                        j0 -= 1
                    j1 = k
                    while (c, j1) in est:
                        j1 += 1
                    val = v[j0] + (v[j1] - v[j0]) * (k - j0) / (j1 - j0)
                    q = "EST"
                rows.append([tag, w.utc_end[k].strftime("%Y-%m-%d %H:%M:%S"), "%.3f" % val, q])
        return head, rows

    # -------------------------------------------------------------------------------------- monitored sample
    def sample_json(self):
        w = self.w
        vals = []
        for k in range(w.K):
            u = w.utc_end[k]
            off = Wd.offset_hours(u - timedelta(minutes=30))
            loc = u + timedelta(hours=off)
            vals.append({"interval_end": loc.strftime("%Y-%m-%dT%H:%M:%S") + "+%02d:00" % off,
                         "output_kw_per_kw": float("%.3f" % w.sample[k])})
        doc = {"dataset": "Saltgrass Coast rooftop PV monitored sample", "provider": "Department of Energy Security "
               "and Planning, distributed energy data programme", "region": P.REGION,
               "systems_reporting": 286, "measure": "AC output per kW of inverter nameplate capacity",
               "interval_minutes": 30, "timestamp_convention": "interval ending, local time",
               "period": {"from": "2026-09-01", "to": "2026-11-30"}, "retrieved": P.SAMPLE_PULL.isoformat(),
               "values": vals}
        return json.dumps(doc, indent=1)

    # -------------------------------------------------------------------------------------- the network's outlook
    def outlook_rows(self, A):
        w = self.w
        r = np.random.default_rng(w.seed + 1201)
        head = ["Zone substation", "Code", "Forecast new systems", "Forecast new inverter capacity (kW)",
                "Forecast basis"]
        rows = []
        for c in sorted(w.codes, key=lambda c: NAME[c]):
            kw = A[c]
            n = int(round(kw / float(r.uniform(7.1, 8.4))))
            basis = ["2025-26 connection trend and approved applications",
                     "2025-26 connection trend; approved applications include a school and two sporting clubs",
                     "2025-26 connection trend, lowered for the 2026 feed-in tariff change",
                     "Approved applications and the 2024-26 average monthly connections",
                     "2025-26 connection trend and approved applications; one shopping centre system (240 kW) "
                     "deferred to 2028"][int(r.choice(5, p=[0.46, 0.14, 0.16, 0.18, 0.06]))]
            rows.append([NAME[c], c, n, kw, basis])
        return head, rows

    # -------------------------------------------------------------------------------------- metering
    def meter_register(self):
        w = self.w
        head = ["nmi", "zone_substation", "feeder", "meter_serial", "model_code", "installed", "removed"]
        rows = []
        for m in sorted(w.meters, key=lambda m: (m["nmi"], m["removed"] is not None, -m["installed"].toordinal())):
            rows.append([m["nmi"], m["sub"], m["feeder"], m["serial"], m["model"], d(m["installed"]), d(m["removed"])])
        return head, rows

    def model_rows(self):
        head = ["Model code", "Manufacturer", "Description", "Data", "Phases", "Registers",
                "Approved for new installations", "Pattern approval"]
        names = {"11": "11 general supply", "41": "41 controlled load", "01": "01 general supply",
                 "02": "02 controlled load", "E1": "E1 general import", "E2": "E2 controlled load import",
                 "E3": "E3 controlled load import", "B1": "B1 export"}
        rows = []
        r = np.random.default_rng(self.w.seed + 1303)
        for m in sorted(P.MODELS, key=lambda m: (m[1], m[0])):
            regs = "; ".join(names[x] for x in m[5] if x)
            newok = "Yes" if m[8] >= 2026 else "No (existing installations only)"
            pa = "NMI %s/%d/%03d" % (["M6", "M7", "M8"][int(r.integers(0, 3))], int(r.integers(80, 200)),
                                     int(r.integers(1, 400)))
            rows.append([m[0], m[1], m[2], m[3].capitalize(), m[4], regs, newok, pa])
        return head, rows

    def reads(self):
        w = self.w
        head = ["nmi", "meter_serial", "register_id", "read_from", "read_to", "days", "kwh"]
        rows = []
        acc = {m["serial"]: w.models[m["model"]]["data"] == "accumulation" for m in w.meters}
        for rw in sorted(w.reads, key=lambda x: (x["nmi"], x["start"], x["serial"], x["register"])):
            k = rw["kwh"]
            rows.append([rw["nmi"], rw["serial"], rw["register"], d(rw["start"]), d(rw["end"]), rw["days"],
                         ("%d" % int(k)) if acc[rw["serial"]] else "%.3f" % k])
        return head, rows

    def load_control(self):
        w = self.w
        head = ["nmi", "switching_group", "controlled_appliance", "element_kw", "tariff", "on_tariff_since"]
        rows = []
        for h in sorted(w.heaters, key=lambda h: h["nmi"]):
            rows.append([h["nmi"], h["group"] + 1, "Electric storage water heater, %d L" % h["litres"],
                         "%.1f" % h["kw"], "CL1 controlled load", d(h["since"])])
        return head, rows

    # -------------------------------------------------------------------------------------- solar connections
    def der_rows(self):
        """The connection applications register: one row per application, as at the extract date."""
        w = self.w
        r = np.random.default_rng(w.seed + 1409)
        apps = []
        for ch in w.chains:
            for ln in ch["links"]:
                apps.append((ch, ln, False))
        for g in w.ghosts:
            apps.append((g["chain"], g["link"], True))
        apps = [a for a in apps if a[1]["approved"] <= P.DER_PULL]
        apps.sort(key=lambda a: (a[1]["approved"], a[0]["nmi"]))
        ids = {}
        seq = {}
        for ch, ln, ghost in apps:
            y = ln["approved"].year
            seq[y] = seq.get(y, int(r.integers(80, 400))) + int(r.integers(1, 23))
            ids[id(ln)] = "SC%d-%06d" % (y, seq[y])
        head = ["application_id", "nmi", "zone_substation_at_approval", "application_type", "prior_application",
                "inverter_serial", "inverter_kw", "panel_kw", "status", "approved", "commissioned"]
        rows = []
        for ch, ln, ghost in apps:
            cu = ch["cust"]
            sub = cu["sub"]
            if cu.get("old_sub") and cu["old_sub"] != sub and ln["approved"] < P.RECONFIG:
                sub = cu["old_sub"]
            prior = None
            if ln["kind"] == "Alteration":
                links = ch["links"]
                if ghost:
                    if ln["status"] == "Withdrawn":
                        j = next((i for i, x in enumerate(links) if x["approved"] <= ln["approved"]
                                  and x["kind"] == ln["kind"] and x["inv"] == ln["inv"] and x["work"] == ln["work"]
                                  and x.get("serial") == ln.get("serial")), None)
                        prev = links[j - 1] if j else links[0]
                    else:
                        prev = [x for x in links if x["approved"] < ln["approved"]][-1]
                else:
                    prev = links[links.index(ln) - 1]
                prior = ids.get(id(prev))
            status, comm = ln["status"], ln["commissioned"]
            if status == "Commissioned" and comm > P.DER_PULL:
                status, comm = "Approved", None
            ser = ln.get("serial") if status != "Approved" and not ghost or status == "Withdrawn" else None
            rows.append([ids[id(ln)], cu["nmi"], NAME[sub], ln["kind"], prior or "", ser or "",
                         ln["inv"], ln["pan"], status, ln["approved"], comm])
        self.der_ids = ids
        return head, rows

    # -------------------------------------------------------------------------------------- distractor
    def enquiries(self):
        w = self.w
        r = np.random.default_rng(w.seed + 1511)
        head = ["enquiry_ref", "received", "nmi", "zone_substation", "category", "outcome", "closed"]
        cats = [("High voltage, inverter disconnecting", 0.34), ("High voltage, appliance damage claim", 0.09),
                ("Low voltage or brownout", 0.14), ("Voltage fluctuation or flicker", 0.18),
                ("Solar export limited", 0.17), ("Other power quality", 0.08)]
        outs = {"High voltage, inverter disconnecting": ([0, 2, 6, 3], [0.46, 0.08, 0.31, 0.15]),
                "High voltage, appliance damage claim": ([0, 1, 2, 4], [0.30, 0.38, 0.22, 0.10]),
                "Low voltage or brownout": ([0, 3, 5, 1, 2], [0.24, 0.31, 0.21, 0.12, 0.12]),
                "Voltage fluctuation or flicker": ([1, 2, 3, 0], [0.33, 0.41, 0.14, 0.12]),
                "Solar export limited": ([6, 2, 0, 4], [0.52, 0.27, 0.13, 0.08]),
                "Other power quality": ([2, 1, 4], [0.55, 0.30, 0.15])}
        out_names = ["Tap setting changed at distribution substation", "Customer installation fault", "No fault found",
                     "Phase rebalanced", "Referred to retailer", "Network augmentation planned",
                     "Inverter settings updated"]
        rows = []
        custs = [cu for cu in w.cust if not cu.get("abolished")]
        start = date(2026, 1, 1)
        n = 1388
        dates = sorted(start + timedelta(days=int(x)) for x in r.integers(0, 335, n))
        ref = int(r.integers(30000, 34000))
        for dd in dates:
            cu = custs[int(r.integers(0, len(custs)))]
            ref += int(r.integers(1, 9))
            cat = cats[int(r.choice(len(cats), p=[c[1] for c in cats]))][0]
            closed = dd + timedelta(days=int(r.integers(2, 60)))
            opts, pr = outs[cat]
            rows.append(["VE%06d" % ref, d(dd), cu["nmi"], cu["sub"], cat, out_names[opts[int(r.choice(len(opts), p=pr))]],
                         d(closed) if closed <= P.ENQUIRY_PULL else ""])
        return head, rows
