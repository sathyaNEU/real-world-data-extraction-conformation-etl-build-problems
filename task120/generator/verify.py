"""The independent verifier. It reads only the files under target/ and imports nothing from the generator: each
day's well production from the daily log, the tanks' levels at the Eastern midnights from the historian export
and their gallons per foot from the facilities summary, the firm capacity from the pump tests; then the meters'
water by month from the AMR reads, the vault reads on the work orders and the inventory's change-out reads, with
the meters beyond a building's service lines counted inside it, and the building groups from the space inventory.

    python3 task120/generator/verify.py [target_dir]
"""
import datetime as dt
import math
import os
import re
import sys
from zoneinfo import ZoneInfo

import pandas as pd
from openpyxl import load_workbook

ET = ZoneInfo("America/New_York")
Y0, Y1 = dt.date(2025, 10, 1), dt.date(2026, 9, 30)
REGISTER_W3 = 100_000_000


def find(target, prefix):
    return os.path.join(target, next(f for f in sorted(os.listdir(target)) if f.startswith(prefix)))


def production(target):
    """{date: gallons} from the log's midnight totalizers; a register that goes backwards has rolled over."""
    wb = load_workbook(find(target, "water_operators_daily_log"), read_only=True, data_only=True)
    reads = {}
    for ws in wb.worksheets:
        rows = list(ws.iter_rows(values_only=True))
        h = next(i for i, r in enumerate(rows) if r and r[0] == "Date")
        head = list(rows[h])
        cols = [head.index("W%d meter (gal)" % k) for k in range(1, 6)]
        for r in rows[h + 1:]:
            if r and isinstance(r[0], dt.datetime):
                reads[r[0].date()] = [int(r[c]) for c in cols]
    out = {}
    d = Y0
    while d <= Y1 + dt.timedelta(1):
        if d in reads and d + dt.timedelta(1) in reads:
            tot = 0
            for a, b in zip(reads[d], reads[d + dt.timedelta(1)]):
                tot += b - a if b >= a else b + REGISTER_W3 - a
            out[d] = tot
        d += dt.timedelta(1)
    return out


def gallons_per_foot(target):
    from docx import Document
    doc = Document(find(target, "campus_water_system_facilities_summary"))
    for tb in doc.tables:
        head = [c.text for c in tb.rows[0].cells]
        if "Gallons per foot of level" in head:
            j = head.index("Gallons per foot of level")
            return {r.cells[0].text: int(r.cells[j].text.replace(",", "")) for r in tb.rows[1:]}
    raise AssertionError("no tank table")


def midnight_storage(target, gpf):
    df = pd.read_csv(find(target, "scada_historian_export"), dtype={"value": str})
    df = df[df.tag.isin(["TK%s_LIT" % t for t in gpf])]
    ts = pd.to_datetime(df.timestamp_utc, utc=True).dt.tz_convert(ET)
    df = df.assign(local=ts)
    df = df[(df.local.dt.hour == 0)]
    assert (df.quality == "G").all(), "a tank sample at a local midnight is not good"
    cents = df.value.map(lambda s: int(round(float(s) * 100)))
    df = df.assign(g=[gpf[t[2]] // 100 * c for t, c in zip(df.tag, cents)])
    s = df.groupby(df.local.dt.date).g.sum()
    n = df.groupby(df.local.dt.date).g.size()
    assert (n == len(gpf)).all()
    return s.to_dict()


def firm(target):
    wb = load_workbook(find(target, "well_pump_tests_"), read_only=True, data_only=True)
    rows = list(wb["Pump tests"].iter_rows(values_only=True))
    head = list(rows[0])
    iw, idt, ir = head.index("Well ID"), head.index("Test date"), head.index("Pumping rate (gpm)")
    last = {}
    for r in rows[1:]:
        if r and r[iw]:
            d = r[idt].date() if isinstance(r[idt], dt.datetime) else r[idt]
            if r[iw] not in last or d > last[r[iw]][0]:
                last[r[iw]] = (d, int(r[ir]))
    caps = {w: g for w, (d, g) in last.items()}
    return sum(caps.values()) - max(caps.values()), caps


def main_call(target):
    P = production(target)
    gpf = gallons_per_foot(target)
    S = midnight_storage(target, gpf)
    use = {}
    d = Y0
    while d <= Y1:
        use[d] = P[d] - (S[d + dt.timedelta(1)] - S[d])
        d += dt.timedelta(1)
    day = max(use, key=use.get)
    f, caps = firm(target)
    gap = use[day] / 1440.0 - f
    call = int(math.ceil(gap)) if gap > 0 else None
    dday = max((x for x in P if Y0 <= x <= Y1), key=P.get)
    return dict(P=P, S=S, use=use, day=day, firm=f, caps=caps, gap=gap, call=call, default_day=dday,
                default_P=P[dday])


def month_starts():
    out = [dt.date(2025, 10, 1)]
    while len(out) < 13:
        d = out[-1]
        out.append(dt.date(d.year + (d.month == 12), d.month % 12 + 1, 1))
    return out


def meter_water(target):
    """Each meter's water by month (12 months from October 2025), and each meter's building record."""
    inv = pd.read_excel(find(target, "meter_inventory"), sheet_name="Meters")
    amr = pd.read_csv(find(target, "amr_monthend_reads"), dtype={"endpoint_id": str}).drop_duplicates()
    wo = pd.read_csv(find(target, "cmms_water_work_orders"), dtype=str)
    vault = wo[wo.wo_type == "METER READ"]
    ms = month_starts()
    reads = {}
    for r in amr.itertuples():
        reads.setdefault(r.meter_no, {})[dt.date.fromisoformat(r.read_date)] = int(r.register_read)
    for r in vault.itertuples():
        t = dt.datetime.strptime(r.reading_for, "%m/%d/%Y %H:%M")
        assert t.day == 1 and t.hour == 0
        reads.setdefault(r.asset_id, {})[t.date()] = int(r.reading_1)
    water = {}
    for r in inv.itertuples():
        mult = int(r._6)
        rd = reads.get(r._1, {})
        inst = pd.Timestamp(r.Installed).date()
        rem = None if pd.isna(r.Removed) else pd.Timestamp(r.Removed).date()
        out = []
        for k in range(12):
            a, b = ms[k], ms[k + 1]
            if a in rd and b in rd:
                out.append((rd[b] - rd[a]) * mult)
            elif a in rd and rem is not None and a <= rem < b:
                out.append((int(r._12) - rd[a]) * mult)
            elif b in rd and a <= inst < b:
                out.append((rd[b] - int(r._10)) * mult)
            else:
                out.append(0)
        water[r._1] = dict(water=out, bldg=int(r._2), size=float(r._4), installed=inst, removed=rem)
    return water


def service_meters(target, water):
    """The meters on a building's service lines: where more meters run at once than the building has domestic or
    process lines in the service line inventory, the larger meters are on the lines and the rest sit inside."""
    lsl = pd.read_csv(find(target, "service_line_inventory"))
    lines = lsl[~lsl.service_use.isin(["Fire", "Irrigation"])].groupby("bldg_no").size().to_dict()
    by_b = {}
    for no, m in water.items():
        by_b.setdefault(m["bldg"], []).append(no)
    service = set()
    for b, nos in by_b.items():
        nlines = lines.get(b, 1)
        # meters running together: those whose service windows overlap
        groups = []
        for no in sorted(nos, key=lambda x: (-water[x]["size"], x)):
            m = water[no]
            placed = False
            for grp in groups:
                if all((water[o]["removed"] is not None and water[o]["removed"] <= m["installed"]) or
                       (m["removed"] is not None and m["removed"] <= water[o]["installed"]) for o in grp):
                    grp.append(no)
                    placed = True
                    break
            if not placed:
                groups.append([no])
        # groups are chains of meters that replaced each other; the largest chains are the service meters
        groups.sort(key=lambda grp: -max(water[o]["size"] for o in grp))
        for grp in groups[:nlines]:
            service.update(grp)
    return service


def groups_of(target, water):
    sp_now = pd.read_excel(find(target, "space_inventory_buildings"), sheet_name="Buildings")
    sp_old = pd.read_excel(find(target, "space_inventory_buildings"), sheet_name="Removed from inventory")
    now = dict(zip(sp_now["Bldg No."], sp_now["Primary use"]))
    name = dict(zip(sp_now["Bldg No."], sp_now["Building name"]))
    old = {int(r["Bldg No."]): (r["Primary use"], pd.Timestamp(r["Removed"]).date()) for _, r in sp_old.iterrows()}
    out = {}
    for no, m in water.items():
        b = m["bldg"]
        use = now.get(b)
        if b in old and m["removed"] is not None and m["removed"] <= old[b][1]:
            use = old[b][0]
        if use == "Residence Hall":
            out[no] = "res"
        elif use in ("Academic", "Research"):
            out[no] = "acad"
        elif use == "Athletics":
            out[no] = "ath"
        elif name.get(b) == "Central Energy Plant":
            out[no] = "cep"
        else:
            out[no] = None
    return out


def run(target):
    M = main_call(target)
    water = meter_water(target)
    service = service_meters(target, water)
    ms = month_starts()
    used = []
    for k in range(12):
        a, b = ms[k], ms[k + 1]
        p = sum(v for d, v in M["P"].items() if a <= d < b)
        used.append(p - (M["S"][b] - M["S"][a]))
    metered = [sum(water[no]["water"][k] for no in service) for k in range(12)]
    lost = [u - m for u, m in zip(used, metered)]
    share = "%.1f" % (100.0 * sum(lost) / sum(used))
    grp = groups_of(target, water)
    groups = {g: 0 for g in ("res", "acad", "ath", "cep")}
    for no in service:
        if grp[no] is not None:
            groups[grp[no]] += sum(water[no]["water"])
    return dict(day=M["day"], use=M["use"][M["day"]], firm=M["firm"], gap=M["gap"], call=M["call"],
                default_day=M["default_day"], default_P=M["default_P"], used=used, metered=metered, lost=lost,
                year=sum(lost), share=share, groups=groups, n_service=len(service), n_meters=len(water))


if __name__ == "__main__":
    tgt = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                                                            "target")
    v = run(tgt)
    print("maximum day %s: %s gal used; firm %d gpm; gap %.2f gpm; add %s gpm" % (
        v["day"], "{:,}".format(v["use"]), v["firm"], v["gap"], v["call"]))
    print("largest day of production %s: %s gal" % (v["default_day"], "{:,}".format(v["default_P"])))
    print("water lost by month:", ["{:,}".format(x) for x in v["lost"]])
    print("year %s gal, %s%% of %s used" % ("{:,}".format(v["year"]), v["share"], "{:,}".format(sum(v["used"]))))
    print("groups:", {k: "{:,}".format(x) for k, x in v["groups"].items()}, "| service meters %d of %d"
          % (v["n_service"], v["n_meters"]))
