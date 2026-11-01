"""task468 architecture 6: the rest of the pack (register, documents, field jobs, email, distractors) and build()."""
import datetime as dt
import os
from email.message import EmailMessage
from email.utils import format_datetime

import numpy as np

import gen as G
import wio

C, KEYS, SWAPS, UTILITY = G.C, G.KEYS, G.SWAPS, G.UTILITY


def limits(W):
    tm = G.true_masses(W)
    out = {}
    for k in KEYS:
        t = tm[k]["cod_t"] / C[k]["target"]
        if C[k]["unit"] == "kg":
            out[k] = ("kg", int(round(t * 1000 / 500.0) * 500))
        else:
            step = 5 if t > 100 else 1
            out[k] = ("t", int(round(t / step) * step))
    return out


def limit_t(lim):
    u, v = lim
    return v / 1000.0 if u == "kg" else float(v)


def write_register(W, path):
    lim = limits(W)
    rows = [["Agreement", "Customer", "Industry", "Sampling point", "Flow meter", "COD limit", "COD limit unit",
             "SS limit (t/yr)", "Agreement year", "Review due"]]
    for i, k in enumerate(KEYS):
        c = C[k]
        u, v = lim[k]
        meter = G.METER1[k] if any(s[0] == k for s in SWAPS) else G.METER0[k]
        rows.append(["TWA-%04d" % (1180 + 37 * i), c["name"], c["industry"], c["point"], meter, v,
                     "kg/yr" if u == "kg" else "t/yr", "", "calendar", "2027-0%d-01" % (3 + i % 6)])
    notes = [["Glenbrae Water trade waste agreements in force for 2026."],
             ["Limits are the annual mass the agreement allows. Prepared by the Trade Waste unit, 9 January 2027."]]
    wio.xlsx(path, [("Agreements", rows, [1], {}), ("Notes", notes, [], {})], "Erik Marks",
             dt.datetime(2024, 7, 2, 8, 15), dt.datetime(2027, 1, 9, 6, 40),
             widths=[12, 30, 26, 14, 18, 12, 14, 14, 14, 12], company=UTILITY)
    return lim


def write_crosswalk(path):
    rows = [[C[k]["old"], C[k]["point"], C[k]["name"], "2026-02-02"] for k in sorted(KEYS, key=lambda k: C[k]["old"])]
    wio.csv_file(path, ["legacy_site_code", "point_id", "customer", "effective"], rows)


def write_jobs(W, path):
    rows = [["Job", "Customer", "Job type", "Started (local)", "Completed (local)", "Asset removed",
             "Removed final read (kL)", "Asset installed", "Installed opening read (kL)", "Technician notes"]]
    info = {s["key"]: s for s in W["swap_info"]}
    jobs = []
    for k, when, gap, opening in SWAPS:
        s = info[k]
        jobs.append((when, k, "Meter exchange", when, s["on_local"], s["old"], s["final"], s["new"], opening,
                     "logger reconnected after commissioning"))
    extra = [(dt.datetime(2026, 2, 17, 10, 30), "BELL", "Sampler service"),
             (dt.datetime(2026, 3, 9, 7, 45), "KING", "Valve repair"),
             (dt.datetime(2026, 6, 2, 11, 0), "COOL", "Sampler service"),
             (dt.datetime(2026, 7, 21, 9, 15), "TALL", "Screen clean"),
             (dt.datetime(2026, 9, 30, 14, 0), "RIVP", "Sampler service"),
             (dt.datetime(2026, 10, 14, 8, 30), "MTED", "Pit inspection")]
    for when, k, jt in extra:
        jobs.append((when, k, jt, when, when + dt.timedelta(hours=2, minutes=20), "", "", "", "", ""))
    jobs.sort(key=lambda j: j[0])
    for i, j in enumerate(jobs):
        _, k, jt, a, b, old, fin, new, op, note = j
        rows.append(["FS-26-%04d" % (311 + 29 * i), C[k]["name"], jt, a.strftime("%d/%m/%Y %H:%M"),
                     b.strftime("%d/%m/%Y %H:%M"), old, fin, new, op, note])
    wio.xlsx(path, [("Jobs", rows, [1], {})], "Brent Fisher", dt.datetime(2026, 1, 5, 7, 0),
             dt.datetime(2027, 1, 6, 4, 25), widths=[12, 30, 16, 17, 17, 18, 14, 18, 14, 34], company=UTILITY)


POLICY = [
    ("s", "Glenbrae Water, Trade Waste Unit"),
    ("t", "Trade Waste Policy, version 4"),
    ("s", "Adopted 3 March 2025. Replaces version 3 (2021). Applies to every trade waste agreement in force."),
    ("h", "1. Purpose"),
    ("p", "This policy sets how Glenbrae Water measures the mass of each substance a trade waste customer discharges "
          "to sewer in an agreement year, how that mass is compared with the limit in the customer's agreement, and "
          "what follows when a limit is exceeded."),
    ("h", "2. The agreement year"),
    ("p", "An agreement year is the calendar year in Queensland time. Volumes, samples and masses are assigned to the "
          "agreement year by the local date on which the discharge or the sampling took place."),
    ("h", "3. Volume"),
    ("p", "The volume a customer discharges in a year is the volume its trade waste flow meter recorded in the year. "
          "Where a meter is exchanged, the volume recorded by the meter removed and by the meter installed both "
          "count."),
    ("h", "4. Mass of a substance"),
    ("p", "The mass of a substance a customer discharges in a year is the volume it discharged in the year multiplied "
          "by the volume-weighted mean concentration of the year's compliance samples, each sample's concentration "
          "weighted by the volume discharged on the day its composite was taken."),
    ("p", "A compliance sample is a 24-hour flow-proportional composite taken by Glenbrae Water at the customer's "
          "sampling point. A laboratory quality-control duplicate does not report the sample. A result the "
          "laboratory re-tests and re-issues replaces the earlier result for that sample. A result below the "
          "laboratory's reporting limit counts at half the reporting limit."),
    ("h", "5. Chemical oxygen demand"),
    ("p", "Limits on chemical oxygen demand (COD) are set on the dichromate method, the reference method of the "
          "agreements. Where the laboratory reports total organic carbon (TOC) for a sample in place of COD, the COD "
          "of that sample is the COD the reference method would have reported for it, estimated from the samples the "
          "laboratory tested by both methods."),
    ("h", "6. Exceedance"),
    ("p", "A customer exceeds its COD limit for a year when the mass of COD it discharged in the year is greater than "
          "the annual mass its agreement allows. Glenbrae Water lists every customer that exceeded a limit in its "
          "annual trade waste return to the state regulator, issues each such customer a notice of agreement review "
          "and recovers the excess mass charge in the following year."),
    ("h", "7. Records"),
    ("p", "The Trade Waste Unit keeps the agreements register, the flow telemetry, the field service records and the "
          "laboratory results for seven years."),
]

NOTICE = [
    ("s", "Glenbrae Water Laboratory Services"),
    ("t", "Notice to the Trade Waste Unit: total organic carbon in place of COD"),
    ("s", "Issued 19 January 2026 by Mitchell Boyd, Laboratory Manager. Reference LAB-N-2026-01."),
    ("p", "From samples collected on Monday 2 February 2026 the laboratory will report total organic carbon (TOC, by "
          "the non-purgeable organic carbon method) on trade waste compliance samples in place of chemical oxygen "
          "demand. The dichromate COD test is being withdrawn because of the mercury and hexavalent chromium wastes it "
          "produces."),
    ("p", "Between 6 October and 19 December 2025 the laboratory tested the trade waste compliance samples by both "
          "methods. Those results are in the 2025 export from the old LIMS beside the COD results, under test code "
          "TOC."),
    ("p", "Results from 2 February 2026 are issued from LabWare. Sampling points carry their LabWare point "
          "identifiers; the Trade Waste Unit holds the crosswalk from the legacy site codes. Collection and "
          "authorisation times in LabWare are in UTC."),
    ("p", "A sample identifier ending in -D is a laboratory quality-control duplicate. A result re-tested after a "
          "failed quality check is re-issued under the sample identifier with -R appended. Suspended solids below "
          "5 mg/L are reported as 5 with the flag &lt;."),
    ("p", "Chloride, suspended solids and pH continue to be reported on every compliance sample."),
]


def write_request(path):
    m = EmailMessage()
    m["From"] = "Erik Marks <erik.marks@glenbraewater.com.au>"
    m["To"] = "Trade Waste Analytics <tw.analytics@glenbraewater.com.au>"
    m["Cc"] = "Mitchell Boyd <mitchell.boyd@glenbraewater.com.au>"
    m["Date"] = format_datetime(dt.datetime(2027, 1, 12, 8, 47, tzinfo=dt.timezone(G.TZ)))
    m["Subject"] = "2026 COD review ahead of the regulator's audit"
    m["Message-ID"] = "<20270112084702.31877@glenbraewater.com.au>"
    m.set_content(
        "Hi all,\n\n"
        "The regulator's audit of the trade waste programme is booked for the week of 8 March, and our annual\n"
        "return has to list every customer over a 2026 limit. This is the first year the lab has reported TOC\n"
        "instead of COD for most of the year, so I want the COD side done properly before the notices go out.\n\n"
        "Everything is in the shared folder: both lab exports, the telemetry, the agreements register, the field\n"
        "jobs and the policy.\n\n"
        "Thanks,\nErik\n\n--\nErik Marks\nTrade Waste Manager\nGlenbrae Water\n")
    open(path, "wb").write(bytes(m))


def write_rain(path):
    rng = np.random.RandomState(G.SEED + 7)
    rows = []
    for d in G.local_dates(2026, 2026):
        wet = rng.rand() < (0.42 if d.month in (1, 2, 3, 12) else 0.2)
        mm = round(float(rng.gamma(0.8, 11.0)), 1) if wet else 0.0
        rows.append([d.isoformat(), "%.1f" % mm, "Y" if rng.rand() < 0.995 else "N"])
    wio.csv_file(path, ["date", "rainfall_mm", "quality_ok"], rows)


def write_returns(path):
    rng = np.random.RandomState(G.SEED + 11)
    unit = {"COOL": "t fruit", "TALL": "hides", "MTED": "t cheese", "GMEA": "head", "RIVP": "birds",
            "SUND": "t powder", "HART": "hL beer", "BELL": "kL product", "KING": "t linen", "GOLD": "t flour",
            "PADD": "t produce", "WATT": "t product"}
    scale = {"COOL": 410, "TALL": 9800, "MTED": 360, "GMEA": 6100, "RIVP": 410000, "SUND": 900, "HART": 2700,
             "BELL": 5200, "KING": 610, "GOLD": 300, "PADD": 1500, "WATT": 520}
    rows = [["Customer", "Quarter", "Production", "Unit", "Submitted"]]
    for k in KEYS:
        for q in range(4):
            v = scale[k] * np.exp(rng.normal(0, 0.07))
            if q < 3:
                sub = dt.date(2026, 3 * q + 4, 1) + dt.timedelta(days=int(rng.randint(5, 26)))
            else:
                sub = dt.date(2027, 1, int(rng.randint(5, 9)))
            rows.append([C[k]["name"], "Q%d 2026" % (q + 1), int(round(v)), unit[k], sub.isoformat()])
    wio.xlsx(path, [("Returns", rows, [1], {})], "Erik Marks", dt.datetime(2026, 4, 14, 9, 2),
             dt.datetime(2027, 1, 8, 5, 31), widths=[30, 10, 12, 12, 12], company=UTILITY)


def clear_volume_edges(W):
    """Each quarter's metered volume sits near a whole kilolitre: one mid-quarter day's flow takes the remainder."""
    for k in KEYS:
        for q in range(4):
            days = [d for d in G.local_dates(2026, 2026) if (d.month - 1) // 3 == q]
            frac = sum(W["flow"][k][d] for d in days) % 1
            W["flow"][k][dt.date(2026, 3 * q + 2, 15)] += (1 - frac) if frac >= 0.5 else -frac


def build(target, nudge=True):
    os.makedirs(target, exist_ok=True)
    W = G.world()
    clear_volume_edges(W)
    for _ in range(12):
        W["swap_info"] = []
        _write(W, target)
        if not nudge:
            break
        import solve as SV
        D = SV.load(target)
        S = SV.lab(D)
        ss = SV.masses(D, S, SV.volumes(D), None, analyte="ss")
        near = [k for k in KEYS if abs(((ss[C[k]["name"]] * 10) % 1) - 0.5) < 0.12]
        if not near:
            break
        for k in near:
            top = max((s for s in W["samples"] if s["key"] == k and s["new"] and not s["rerun_ss"]),
                      key=lambda s: s["ss"])
            top["ss"] += -4.0 if ((ss[C[k]["name"]] * 10) % 1) < 0.5 else 4.0
    return W


def _write(W, target):
    tel = G.telemetry(W)
    p = lambda k: os.path.join(target, G.FILES[k])
    G.write_lims_old(W, p("lims_old"))
    G.write_lims_new(W, p("lims_new"))
    G.write_telemetry(W, tel, p("telemetry"))
    W["limits"] = write_register(W, p("register"))
    wio.pdf(p("policy"), POLICY, "Trade Waste Policy v4", "Glenbrae Water", "D:20250303091500+10'00'",
            "D:20250303091500+10'00'", "Glenbrae Water  |  Trade Waste Policy v4")
    wio.pdf(p("lab_notice"), NOTICE, "Laboratory notice LAB-N-2026-01", "Mitchell Boyd", "D:20260119143000+10'00'",
            "D:20260119143000+10'00'", "Glenbrae Water Laboratory Services  |  LAB-N-2026-01")
    write_crosswalk(p("crosswalk"))
    write_jobs(W, p("jobs"))
    write_request(p("request"))
    write_rain(p("rain"))
    write_returns(p("returns"))
    return W, tel
