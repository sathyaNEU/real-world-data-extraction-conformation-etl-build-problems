"""Write the planning folder the way each system exports it: the old WMS's pick confirmations to the June cut-over and
the new WMS's after it, the pack-out stations' exception log, the item master, the client's plan, the dispatch
system's deliveries and cage contents, the store claims register, the labour system's shifts, the WMS user list,
the cycle counts and the building's temperature log. Documents are in docs.py."""
import datetime as dt
import os

import numpy as np
import openpyxl
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from openpyxl.styles import Alignment, Font, PatternFill

import params as P
import postprocess as PP
import world as W

AMS = "Europe/Amsterdam"
COMPANY = "Kroonvaart Fulfilment B.V."
NAMES = {g: n for g, n, *_r in P.GROUPS}
CS_NAMES = {"RAV": "Ravelijn Drogist", "HGH": "Hooghuys Drogisterij", "VLM": "Vlietmarkt", "ZLF": "Zelfstandig"}
OLD_FILE = "wms_pick_confirmations_2026-01-01_2026-06-12.csv"
NEW_FILE = "wms_pick_confirmations_2026-06-15_2026-12-31.parquet"
FILES = dict(
    old=OLD_FILE, new=NEW_FILE, exc="packout_exceptions_2026.csv", items="siersma_item_master_2027-01-04.xlsx",
    plan="siersma_volume_plan_q1_2027.xlsx", deliv="dispatch_deliveries_2026.csv", colli="dispatch_colli_2026-01_2026-06.csv",
    claims="siersma_store_claims_2026.csv", lms="lms_shifts_2026.csv", users="wms_users.csv",
    counts="cycle_counts_2026.csv", bms="bms_zone_temperatures_2026.csv",
    sla="schedule_3_service_levels_v2.pdf", pcn="siersma_pcn_2026-11_daily_range.pdf",
    closeout="venlo_siersma_closeout_2026-12.pdf")


def locations(a):
    """Each article's pick face: an old aisle-bay-level code and the code the new WMS gave the same face (part of the
    floor re-slotted at the cut-over), and a reserve face for the second go of a split line."""
    r = W.rng("locations")
    n = len(a)
    aisle = r.integers(1, 23, n)
    bay = r.integers(1, 40, n)
    lvl = r.integers(1, 5, n)
    old = ["%02d-%02d-%d" % (x, y, z) for x, y, z in zip(aisle, bay, lvl)]
    moved = r.random(n) < 0.35
    aisle2 = np.where(moved, r.integers(1, 23, n), aisle)
    bay2 = np.where(moved, r.integers(1, 40, n), bay)
    new = ["VL1-P%02d-%02d%s" % (x, y, "ABCD"[z - 1]) for x, y, z in zip(aisle2, bay2, lvl)]
    res_old = ["R%02d-%02d-%d" % (x, y, z) for x, y, z in zip(r.integers(30, 41, n), r.integers(1, 60, n), r.integers(2, 7, n))]
    res_new = ["VL1-R%02d-%02d%s" % (x, y, "CDEFG"[z - 2]) for x, y, z in zip(r.integers(30, 41, n), r.integers(1, 60, n), r.integers(2, 7, n))]
    return np.array(old), np.array(new), np.array(res_old), np.array(res_new)


def _utc(local):
    return pd.to_datetime(pd.Series(local)).dt.tz_localize(AMS, ambiguous="NaT", nonexistent="shift_forward").dt.tz_convert("UTC")


def _split_rows(lines):
    """One row per confirmation: a split line gives two, the second from the reserve face a few minutes later."""
    r = W.rng("splitrows")
    base = lines.copy()
    base["go"] = 1
    s = base[base["split"]].copy()
    q1 = np.maximum(1, (s["qty_conf"].values * r.uniform(0.25, 0.75, len(s))).astype(int))
    q1 = np.minimum(q1, s["qty_conf"].values - 1)
    s2 = s.copy()
    base.loc[s.index, "qty_row"] = q1
    s2["qty_row"] = s["qty_conf"].values - q1
    s2["go"] = 2
    s2["ts_local"] = s2["ts_local"] + pd.to_timedelta(r.integers(90, 900, len(s2)), unit="s")
    base["qty_row"] = base["qty_row"].fillna(base["qty_conf"]).astype(int)
    out = pd.concat([base, s2]).sort_values(["ts_local", "order_no", "line_no", "go"], kind="stable")
    return out


def users(people):
    """The old WMS knew pickers by a site user code; the new one logs the LMS badge. The old system's user list holds
    everyone it ever knew, so nobody who started after the cut-over."""
    r = W.rng("users")
    ppl = people[people["first"] <= P.UPGRADE_LAST_OLD]
    codes = r.choice(np.arange(100, 999), len(ppl), replace=False)
    return pd.DataFrame({"wms_user": ["KVV%03d" % c for c in codes], "badge": ppl["badge"].values,
                         "created": [max(f, dt.date(2024, 3, 1)) - dt.timedelta(days=int(r.integers(1, 9))) for f in ppl["first"]]})


def write_old(path, lines, a, loc_old, res_old, umap):
    old = lines[lines["day"] <= P.UPGRADE_LAST_OLD]
    rows = _split_rows(old)
    sku = a["sku"].values[rows["art"].values]
    loc = np.where(rows["go"].values == 2, res_old[rows["art"].values], loc_old[rows["art"].values])
    ts = pd.to_datetime(rows["ts_local"])
    df = pd.DataFrame({"ORDERNR": rows["order_no"].values, "REGELNR": rows["line_no"].values, "ARTIKELNR": sku,
                       "LOCATIE": loc, "AANTAL": rows["qty_row"].values,
                       "GEBRUIKER": rows["badge"].map(umap).values,
                       "KANAAL": np.where(rows["channel"].values == "T", "B2B", "B2C"),
                       "DATUM": ts.dt.strftime("%d-%m-%Y").values, "TIJD": ts.dt.strftime("%H:%M:%S").values})
    df.to_csv(path, sep=";", index=False, lineterminator="\r\n")
    return len(df)


def write_new(path, lines, a, loc_new, res_new, colli):
    new = lines[lines["day"] >= P.UPGRADE_FIRST_NEW]
    rows = _split_rows(new)
    r = W.rng("newwms")
    sku = a["sku"].values[rows["art"].values]
    loc = np.where(rows["go"].values == 2, res_new[rows["art"].values], loc_new[rows["art"].values])
    cmap = colli.set_index(["order_no", "line_no"])["sscc"].to_dict()
    tote = {}
    cont = []
    for o, l, ch in zip(rows["order_no"].values, rows["line_no"].values, rows["channel"].values):
        if ch == "T":
            cont.append(cmap.get((o, l), ""))
        else:
            if o not in tote:
                tote[o] = "TB%06d" % int(r.integers(100000, 999999))
            cont.append(tote[o])
    task = 9150000 + np.cumsum(r.integers(1, 5, len(rows)))
    utc = _utc(rows["ts_local"].values)
    tbl = pd.DataFrame({"task_id": task.astype("int64"), "order_id": rows["order_no"].values.astype("int64"),
                        "line_no": rows["line_no"].values.astype("int32"), "sku": sku.astype("int64"),
                        "qty_ordered": rows["qty"].values.astype("int32"), "qty_confirmed": rows["qty_row"].values.astype("int32"),
                        "location": loc, "container": np.where(rows["qty_row"].values > 0, cont, ""),
                        "user_id": ["B%d" % b for b in rows["badge"].values],
                        "channel": np.where(rows["channel"].values == "T", "RETAIL", "ECOM"),
                        "confirmed_at": utc.values})
    tbl["confirmed_at"] = tbl["confirmed_at"].dt.floor("s")
    t = pa.Table.from_pandas(tbl, preserve_index=False)
    t = t.cast(pa.schema([pa.field("task_id", pa.int64()), pa.field("order_id", pa.int64()), pa.field("line_no", pa.int16()),
                          pa.field("sku", pa.int32()), pa.field("qty_ordered", pa.int16()), pa.field("qty_confirmed", pa.int16()),
                          pa.field("location", pa.string()), pa.field("container", pa.string()), pa.field("user_id", pa.string()),
                          pa.field("channel", pa.string()), pa.field("confirmed_at", pa.timestamp("s", tz="UTC"))]))
    t = t.replace_schema_metadata(None)
    pq.write_table(t, path, compression="zstd", compression_level=9, use_dictionary=True, write_statistics=False,
                   row_group_size=1 << 20)
    return len(tbl)


def write_exceptions(path, lines, a):
    """The pack-out stations log every finding against the order reference and line the label carries."""
    r = W.rng("exceptions")
    pk = lines[lines["qty_conf"] > 0]
    f = pk[pk["fail"]].copy()
    q = f["qty_conf"].values
    inner = f["inner"].values
    rem = q % inner
    u = r.random(len(f))
    code = np.empty(len(f), object)
    found = q.copy()
    for i, s in enumerate(f["struct"].values):
        if s == "mixed":
            if u[i] < .58:
                code[i], found[i] = "SHORT", q[i] - rem[i]
            elif u[i] < .90:
                code[i], found[i] = "OVER", q[i] - rem[i] + inner[i]
            else:
                code[i], found[i] = "WRONG_ITEM", q[i]
        else:
            if u[i] < .45:
                code[i], found[i] = "SHORT", q[i] - (inner[i] if (s == "whole" and q[i] > inner[i] and u[i] < .2) else 1)
            elif u[i] < .70:
                code[i], found[i] = "OVER", q[i] + 1
            else:
                code[i], found[i] = "WRONG_ITEM", q[i]
    other = pk[~pk["fail"]].sample(n=int(len(pk) * 0.0007), random_state=int(r.integers(1, 10**6)))
    oc = np.where(r.random(len(other)) < 0.6, "DAMAGED", "LABEL")
    allr = pd.concat([f.assign(code=code, found=found), other.assign(code=oc, found=other["qty_conf"].values)])
    lag = r.integers(240, 6600, len(allr))
    ts = _utc((pd.to_datetime(allr["ts_local"]) + pd.to_timedelta(lag, unit="s")).values)
    st = np.where(allr["channel"].values == "T", ["PV-R%02d" % k for k in r.integers(1, 7, len(allr))],
                  ["PV-E%02d" % k for k in r.integers(1, 11, len(allr))])
    act = {"SHORT": "REPICK", "OVER": "CORRECTED", "WRONG_ITEM": "REPLACED", "DAMAGED": "REPLACED", "LABEL": "RELABELLED"}
    df = pd.DataFrame({"station": st, "event_time_utc": ts.dt.strftime("%Y-%m-%dT%H:%M:%SZ").values,
                       "order_ref": ["SIE%d" % o for o in allr["order_no"].values], "line": allr["line_no"].values,
                       "sku": a["sku"].values[allr["art"].values], "expected_qty": allr["qty_conf"].values,
                       "found_qty": allr["found"].values, "code": allr["code"].values,
                       "action": [act[c] for c in allr["code"].values]})
    df = df.sort_values(["event_time_utc", "station"], kind="stable")
    df.to_csv(path, index=False, lineterminator="\n")
    return df


def _xlsx(path, sheets, creator, last_by, created, modified, widths=None, title_rows=None):
    wb = openpyxl.Workbook()
    wb.remove(wb.active)
    for name, (header, rows) in sheets.items():
        ws = wb.create_sheet(name)
        start = 1
        for tr in (title_rows or {}).get(name, []):
            ws.cell(row=start, column=1, value=tr).font = Font(bold=start == 1)
            start += 1
        if title_rows and title_rows.get(name):
            start += 1
        for j, h in enumerate(header, 1):
            c = ws.cell(row=start, column=j, value=h)
            c.font = Font(bold=True)
            c.fill = PatternFill("solid", fgColor="DDEBF7")
        for i, row in enumerate(rows, start + 1):
            for j, v in enumerate(row, 1):
                c = ws.cell(row=i, column=j, value=v)
                if isinstance(v, dt.date):
                    c.number_format = "dd-mm-yyyy"
        for j, wdt in enumerate((widths or {}).get(name, []), 1):
            ws.column_dimensions[openpyxl.utils.get_column_letter(j)].width = wdt
        ws.freeze_panes = ws.cell(row=start + 1, column=1)
    wb.save(path)
    PP.normalize_ooxml(path, creator, last_by, created, modified, excel=True, company=COMPANY)


def item_master(a):
    """The WMS item master as exported on 4 January 2027: one row per article and configuration, dated."""
    r = W.rng("items")
    rows = []
    for x in a.itertuples():
        frm = x.launch if x.launch is not None else dt.date(2021, 1, 4) + dt.timedelta(days=int(r.integers(0, 1100)))
        to = x.delist
        igtin = W.gs1_check("1" + x.ean[:-1])[:14]
        if x.range not in ("DLY",) and x.launch is None and r.random() < 0.035:
            # an earlier shipping case, replaced in 2025
            cut = dt.date(2025, int(r.integers(2, 12)), 1) + dt.timedelta(days=int(r.integers(0, 20)))
            old_case = x.case_qty // 2 if x.case_qty >= 2 * x.inner and (x.case_qty // 2) % x.inner == 0 else x.case_qty + x.inner * 2
            rows.append([x.sku, x.article_no, x.ean, x.description, x.range, x.inner, igtin, old_case, frm, cut - dt.timedelta(days=1)])
            frm = cut
        if x.range == "DLY" and to is not None:
            rows.append([x.sku, x.article_no, x.ean, x.description, x.range, x.inner, igtin, 24, frm, to])
        elif x.range == "DLY":
            rows.append([x.sku, x.article_no, x.ean, x.description, x.range, x.inner, igtin, 24, frm,
                         P.NEW_INNER_FROM - dt.timedelta(days=1)])
            ng = W.gs1_check("2" + x.ean[:-1])[:14]
            rows.append([x.sku, x.article_no, x.ean, x.description, x.range, P.INNER_2027["DLY"], ng, 24, P.NEW_INNER_FROM, to])
        elif x.range == "HAI" and x.case_qty == 24 and r.random() < 0.5 and (to is None or to > dt.date(2026, 9, 7)) \
                and frm < dt.date(2026, 9, 7):
            cut = dt.date(2026, 9, 7)
            rows.append([x.sku, x.article_no, x.ean, x.description, x.range, x.inner, igtin, 24, frm, cut - dt.timedelta(days=1)])
            rows.append([x.sku, x.article_no, x.ean, x.description, x.range, x.inner, igtin, 36, cut, to])
        else:
            rows.append([x.sku, x.article_no, x.ean, x.description, x.range, x.inner, igtin, x.case_qty, frm, to])
    if len(rows) % 10 == 0:
        # one more article whose shipping case changed in 2025, so the export's length is what it happens to be
        for k, z in enumerate(rows):
            if z[4] in ("SKN", "KID") and z[9] is None and z[8] < dt.date(2025, 1, 1) and z[7] >= 2 * z[5]:
                cut = dt.date(2025, 4, 7)
                rows.append(z[:7] + [z[7] + 2 * z[5], z[8], cut - dt.timedelta(days=1)])
                rows[k] = z[:8] + [cut, None]
                break
    rows.sort(key=lambda z: (z[1], z[8]))
    header = ["sku", "article_no", "ean", "description", "range", "inner_qty", "inner_gtin", "case_qty", "valid_from", "valid_to"]
    return header, rows


def write_items(path, a):
    header, rows = item_master(a)
    _xlsx(path, {"Items": (header, rows)}, "Nienke Gemen", "Nienke Gemen", "2024-02-12T08:41:00Z",
          "2027-01-04T07:52:00Z", widths={"Items": [10, 11, 15, 38, 7, 9, 16, 9, 12, 12]})
    return rows


RANGE_NAMES = {"DLY": "Daily", "HAI": "Hair", "SKN": "Skin", "KID": "Kids", "MEN": "Men", "SUN": "Sun"}


def write_plan(path, plan):
    rows = []
    for rg in ["DLY", "HAI", "SKN", "KID", "MEN", "SUN"]:
        for ch, lab in (("T", "Retail"), ("W", "E-commerce")):
            vals = [int(plan[(plan.range == rg) & (plan.channel == ch) & (plan.month == m)]["lines"].iloc[0]) for m in (1, 2, 3)]
            rows.append([RANGE_NAMES[rg], lab] + vals)
    titles = {"Q1 2027": ["Siersma Care, logistics volume plan Q1 2027, Venlo",
                          "Order lines per range and channel as agreed at S&OP, 24 November 2026. Article mix and order sizes in each month as in the same month of 2026."]}
    _xlsx(path, {"Q1 2027": (["Range", "Channel", "Jan 2027", "Feb 2027", "Mar 2027"], rows)}, "Lex Suijker", "Lex Suijker",
          "2026-11-24T13:05:00Z", "2026-11-26T09:18:00Z", widths={"Q1 2027": [14, 13, 11, 11, 11]}, title_rows=titles)
    return rows


def write_deliveries(path, orders):
    o = orders.sort_values("delivery_note")
    disp = [dt.datetime.combine(d, dt.time(0)) + dt.timedelta(minutes=int(m)) for d, m in zip(o["day"], o["dispatch_min"])]
    df = pd.DataFrame({"delivery_note": o["delivery_note"].values, "order_no": o["order_no"].values,
                       "customer": o["group"].values, "store": o["store_no"].values, "store_po": o["store_po"].values,
                       "dispatched_at": [x.strftime("%Y-%m-%d %H:%M") for x in disp],
                       "delivery_date": [d.isoformat() for d in o["delivery_date"]]})
    df.to_csv(path, index=False, lineterminator="\n")


def write_colli(path, colli, orders):
    """The dispatch module's cage contents; it was retired with the old WMS, whose successor records each line's
    container itself, so the export ends at the cut-over."""
    dn = orders.set_index("order_no")["delivery_note"].to_dict()
    day = orders.set_index("order_no")["day"].to_dict()
    c = colli[[day[o] <= P.UPGRADE_LAST_OLD for o in colli["order_no"]]]
    c = c.sort_values(["order_no", "sscc", "line_no"])
    df = pd.DataFrame({"sscc": c["sscc"].values, "delivery_note": c["order_no"].map(dn).values,
                       "order_no": c["order_no"].values, "line_no": c["line_no"].values, "qty": c["qty_conf"].values})
    df.to_csv(path, index=False, lineterminator="\n")


def write_claims(path, reg):
    df = pd.DataFrame({"claim_no": reg["claim_no"].values, "kanaal": reg["route"].values,
                       "klant": reg["group"].map(CS_NAMES).values, "filiaal": reg["store_no"].values,
                       "ontvangen": [d.strftime("%d-%m-%Y") for d in reg["received"]],
                       "referentie": reg["reference"].values, "sscc": reg["sscc"].fillna("").values,
                       "artikel": reg["article"].values, "aantal": reg["qty"].values, "reden": reg["reason"].values,
                       "status": reg["status"].values})
    df.to_csv(path, sep=";", index=False, lineterminator="\r\n", encoding="utf-8")


def write_lms(path, lines, people):
    """Shifts as the labour system books them: badge, agency, date, shift and hours, for every day a picker worked."""
    r = W.rng("lms")
    first_ts = lines.groupby(["badge", "day"])["ts_local"].min()
    rows = []
    ag = people.set_index("badge")["agency"].to_dict()
    area = people.set_index("badge")["area"].to_dict()
    for (b, d), t in first_ts.items():
        hour = pd.Timestamp(t).hour
        shift = "E" if hour < 14 else "L"
        hrs = round(float(r.choice([7.5, 7.75, 8.0, 8.0, 8.25, 8.5])), 2)
        rows.append([b, ag[b] or "", d.isoformat(), shift, "RETAIL PICK" if area[b] == "T" else "ECOM PICK", hrs])
    # training days before a new picker's first pick
    for p in people.itertuples():
        if p.first >= dt.date(2026, 1, 1):
            d = p.first - dt.timedelta(days=1)
            while d.weekday() >= 5:
                d -= dt.timedelta(days=1)
            rows.append([p.badge, p.agency or "", d.isoformat(), "E", "INDUCTION", 7.5])
    df = pd.DataFrame(rows, columns=["badge", "agency", "date", "shift", "activity", "hours"]).sort_values(["date", "badge"])
    df.to_csv(path, index=False, lineterminator="\n")


def write_users(path, umap_df):
    umap_df.sort_values("wms_user").assign(created=lambda d: d["created"].map(lambda x: x.isoformat())).to_csv(
        path, index=False, lineterminator="\n")


def write_counts(path, a, loc_old, loc_new):
    """Cycle counts of pick faces through 2026 (the inventory record KPI)."""
    r = W.rng("counts")
    days = [d for d in pd.date_range("2026-01-05", "2026-12-23", freq="B").date if d not in P.HOLIDAYS]
    rows = []
    for d in days:
        idx = r.choice(len(a), int(r.integers(10, 22)), replace=False)
        for i in idx:
            sysq = int(r.integers(0, 14)) * int(a["inner"].iat[i]) + int(r.integers(0, a["inner"].iat[i]))
            diff = 0 if r.random() > 0.0035 else int(r.choice([-2, -1, 1, 2, -6]))
            loc = loc_old[i] if d <= P.UPGRADE_LAST_OLD else loc_new[i]
            rows.append([d.isoformat(), loc, int(a["sku"].iat[i]), sysq, max(0, sysq + diff)])
    df = pd.DataFrame(rows, columns=["count_date", "location", "sku", "system_qty", "counted_qty"])
    # a month whose counts all agreed still turned up the odd face off by one when it was recounted
    month = pd.to_datetime(df["count_date"]).dt.month
    for m in range(1, 13):
        idx = df.index[month == m]
        if (df.loc[idx, "system_qty"] == df.loc[idx, "counted_qty"]).all():
            k = int(r.choice(idx))
            df.loc[k, "counted_qty"] = df.loc[k, "system_qty"] + (1 if df.loc[k, "system_qty"] == 0 else -1)
    df.to_csv(path, index=False, lineterminator="\n")


def write_bms(path):
    r = W.rng("bms")
    rows = []
    for d in pd.date_range("2026-01-01", "2026-12-31", freq="D").date:
        doy = d.timetuple().tm_yday
        out = 10.5 - 8.5 * np.cos(2 * np.pi * (doy - 15) / 365)
        for z, base in (("RETAIL PICK", 17.0), ("ECOM PICK", 18.0), ("MEZZANINE", 19.5)):
            mean = base + 0.35 * (out - 10) + r.normal(0, 0.6)
            rows.append([d.isoformat(), z, round(mean - abs(r.normal(1.4, 0.4)), 1), round(mean + abs(r.normal(1.8, 0.5)), 1)])
    pd.DataFrame(rows, columns=["date", "zone", "t_min_c", "t_max_c"]).to_csv(path, index=False, lineterminator="\n")


def write_all(out, w):
    os.makedirs(out, exist_ok=True)
    a = w["articles"]
    lines = w["lines"]
    loc_old, loc_new, res_old, res_new = locations(a)
    umap_df = users(w["people"])
    umap = umap_df.set_index("badge")["wms_user"].to_dict()
    j = lambda k: os.path.join(out, FILES[k])
    n_old = write_old(j("old"), lines, a, loc_old, res_old, umap)
    n_new = write_new(j("new"), lines, a, loc_new, res_new, w["colli"])
    exc = write_exceptions(j("exc"), lines, a)
    items = write_items(j("items"), a)
    plan_rows = write_plan(j("plan"), w["plan"])
    write_deliveries(j("deliv"), w["orders"])
    write_colli(j("colli"), w["colli"], w["orders"])
    write_claims(j("claims"), w["register"])
    write_lms(j("lms"), lines, w["people"])
    write_users(j("users"), umap_df)
    write_counts(j("counts"), a, loc_old, loc_new)
    write_bms(j("bms"))
    return dict(n_old=n_old, n_new=n_new, exceptions=exc, items=items, plan_rows=plan_rows)
