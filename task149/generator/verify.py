"""Independent verifier: recomputes the call, every zone figure and every ask figure from target/ on its own code
path (pandas for the CSVs, the raw OOXML for the workbook and the note, its own PDF stream reader), reads the
golden files back, and compares with figures.json.

    python3 task149/generator/verify.py"""
import base64
import json
import os
import re
import sys
import zipfile
import zlib

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
T = os.path.join(TASK, "target")
G = os.path.join(TASK, "golden")


def pdf_strings(path):
    data = open(path, "rb").read()
    out = []
    for m in re.finditer(rb"stream\r?\n(.*?)endstream", data, re.S):
        raw = m.group(1).strip()
        if raw.startswith(b"<~"):
            raw = raw[2:]
        if raw.endswith(b"~>"):
            raw = base64.a85decode(raw[:-2])
        try:
            raw = zlib.decompress(raw)
        except zlib.error:
            continue
        out += [s.decode("latin-1") for s in re.findall(rb"\(((?:[^()\\]|\\.)*)\)\s*Tj", raw)]
    return " ".join(out)


def xlsx_rows(path, sheet_index):
    z = zipfile.ZipFile(path)
    names = z.namelist()
    shared = []
    if "xl/sharedStrings.xml" in names:
        xml = z.read("xl/sharedStrings.xml").decode()
        for si in re.findall(r"<si>(.*?)</si>", xml, re.S):
            shared.append("".join(re.findall(r"<t[^>]*>(.*?)</t>", si, re.S)))
    xml = z.read("xl/worksheets/sheet%d.xml" % sheet_index).decode()
    rows = []
    for row in re.findall(r"<row[^>]*>(.*?)</row>", xml, re.S):
        cells = []
        for c in re.finditer(r'<c r="([A-Z]+)\d+"([^>]*?)(?:/>|>(.*?)</c>)', row, re.S):
            attrs, body = c.group(2), c.group(3) or ""
            v = re.search(r"<v>(.*?)</v>", body)
            t = re.search(r"<t[^>]*>(.*?)</t>", body)
            if 't="s"' in attrs and v:
                cells.append(shared[int(v.group(1))])
            elif t:
                cells.append(t.group(1))
            elif v:
                cells.append(v.group(1))
            else:
                cells.append(None)
        rows.append(cells)
    return rows


def docx_text(path):
    xml = zipfile.ZipFile(path).read("word/document.xml").decode()
    return " ".join(re.findall(r"<w:t[^>]*>(.*?)</w:t>", xml))


def main():
    F = json.load(open(os.path.join(HERE, "figures.json")))
    bad = []

    def eq(name, got, want):
        if got != want:
            bad.append("%s: recomputed %r, figures.json %r" % (name, got, want))

    # census final release (sheet 1), shares and threshold from the refresh PDF
    rows = xlsx_rows(os.path.join(T, "census2022_pow_rathgarvan_catchment.xlsx"), 1)
    cens = {}
    for r in rows:
        if len(r) >= 4 and r[1] and str(r[1]).startswith("KW") and str(r[3]).replace('.', '').isdigit():
            cens[r[1]] = cens.get(r[1], 0) + int(float(r[3]))
    txt = pdf_strings(os.path.join(T, "rathgarvan_fbc_demand_refresh_dec2027.pdf"))
    share = {m.group(1): float(m.group(2)) for m in re.finditer(r"(KW\d\d) [^0-9]*?(\d\.\d\d)", txt)}
    thr = int(re.search(r"carries ([\d,]+) or more", txt).group(1).replace(",", ""))
    # calendar and ordinary weekdays
    cal = pd.read_csv(os.path.join(T, "kilcarrow_calendar_2018_2027.csv"))
    off = set(pd.to_datetime(cal["date"]).dt.date)
    days = [d.date() for d in pd.date_range("2027-09-06", "2027-11-26") if d.weekday() < 5 and d.date() not in off]
    eq("ordinary weekdays", len(days), F["ordinary_weekdays"])
    dayset = set(days)
    # panel
    st = pd.read_csv(os.path.join(T, "mobility_stays_2027w36_w47.csv"))
    dv = pd.read_csv(os.path.join(T, "mobility_devices_2027w36_w47.csv"))
    lk = pd.read_csv(os.path.join(T, "cell_zone_lookup_v3.csv"))
    major = lk.sort_values(["cell_id", "area_share", "zone_code"], ascending=[True, False, False]) \
              .drop_duplicates("cell_id").set_index("cell_id")["zone_code"]
    for c in ("stay_start_utc", "stay_end_utc"):
        st[c] = pd.to_datetime(st[c], utc=True).dt.tz_convert("Europe/Dublin").dt.tz_localize(None)
    st = st.merge(dv[["hashed_imsi", "home_cell"]], on="hashed_imsi")
    st["mins"] = (st["stay_end_utc"] - st["stay_start_utc"]).dt.total_seconds() / 60
    st["zone"] = st["cell_id"].map(major)
    lng = st[(st["cell_id"] != st["home_cell"]) & (st["mins"] >= 240) & st["zone"].notna()].copy()
    cnt = lng.groupby(["hashed_imsi", "zone"]).size().reset_index(name="n")
    cnt = cnt.sort_values(["hashed_imsi", "n", "zone"], ascending=[True, False, True])
    tot_long = lng.groupby("hashed_imsi").size()
    usual = cnt.drop_duplicates("hashed_imsi").set_index("hashed_imsi")
    usual = usual[tot_long.reindex(usual.index) >= 3]
    lng["day"] = lng["stay_start_utc"].dt.date
    first = pd.to_datetime(dv.set_index("hashed_imsi")["first_seen_utc"], utc=True).dt.tz_convert("Europe/Dublin").dt.date
    last = pd.to_datetime(dv.set_index("hashed_imsi")["last_seen_utc"], utc=True).dt.tz_convert("Europe/Dublin").dt.date
    num, den = {}, {}
    for did, row in usual.iterrows():
        z = row["zone"]
        sub = lng[(lng["hashed_imsi"] == did) & (lng["zone"] == z)]
        cd = {d for d in sub["day"] if d in dayset}
        obs = [d for d in days if first[did] <= d <= last[did]]
        num[z] = num.get(z, 0) + len(cd)
        den[z] = den.get(z, 0) + len(obs)
    tot = 0.0
    for z, s in share.items():
        if s <= 0:
            continue
        f = num[z] / den[z]
        b = cens[z] * s * f
        tot += b
        eq("zone %s boardings" % z, int(round(b / 10.0)) * 10, F["zone_boardings"][z])
    eq("total boardings", int(round(tot / 100.0)) * 100, F["total_boardings"])
    eq("scope", "reduced scheme" if tot < thr else "full scheme", F["scope"])
    # ask B: arrival in the workplace zone, from 07:30 up to and including 09:30 Irish time, on ordinary weekdays: the
    # day's first stay in any cell of the commuter's usual zone, on each day the commuter has a long stay there
    lng2 = lng.merge(usual[["zone"]].rename(columns={"zone": "uz"}), left_on="hashed_imsi", right_index=True)
    lng2 = lng2[(lng2["zone"] == lng2["uz"]) & lng2["day"].isin(dayset)]
    allz = st[st["cell_id"] != st["home_cell"]].copy()
    allz["day"] = allz["stay_start_utc"].dt.date
    allz = allz.merge(usual[["zone"]].rename(columns={"zone": "uz"}), left_on="hashed_imsi", right_index=True)
    allz = allz[allz["zone"] == allz["uz"]]
    firsts = allz.groupby(["hashed_imsi", "day"])["stay_start_utc"].min().rename("arr").reset_index()
    journeys = lng2.drop_duplicates(["hashed_imsi", "day"]).merge(firsts, on=["hashed_imsi", "day"])
    m = journeys["arr"].dt.hour * 60 + journeys["arr"].dt.minute
    journeys["hit"] = (m >= 450) & (m <= 570)
    for z in F["arrival_share"]:
        sub = journeys[journeys["uz"] == z]
        eq("arrival %s" % z, int(round(100 * sub["hit"].mean())), F["arrival_share"][z])
    # ask A: each location code placed at a station on the day: register codes (with the code each replaced) and gate
    # assets by the asset register's dated rows; the line is every code summed by day
    gt = pd.read_csv(os.path.join(T, "ardnagree_line_gate_entries_20180101_20271130.csv"))
    reg = pd.read_csv(os.path.join(T, "ardnagree_line_station_register.csv"), dtype=str)
    ast = pd.read_csv(os.path.join(T, "ardnagree_line_gate_asset_locations.csv"), dtype=str).fillna("")
    replaced = {}
    for _, r in reg.iterrows():
        m2 = re.search(r"(?:continues as|replaced by [A-Za-z ]+\() ?([A-Z]{3})", str(r["notes"]))
        if m2:
            replaced[r["station_code"]] = m2.group(1)
    gt["d"] = pd.to_datetime(gt["date"]).dt.date
    gt = gt[[(d.weekday() < 5 and d not in off and 9 <= d.month <= 11) for d in gt["d"]]].copy()
    gt["y"] = [d.year for d in gt["d"]]

    def place(code, d):
        if code in set(reg["station_code"]):
            return replaced.get(code, code)
        for _, r in ast[ast["asset_id"] == code].iterrows():
            a = pd.Timestamp(r["installed"]).date()
            b = pd.Timestamp(r["removed"]).date() if r["removed"] else pd.Timestamp("2099-01-01").date()
            if a <= d <= b:
                return r["station_code"]
        return None
    gt["stn"] = [place(c, d) for c, d in zip(gt["location_code"], gt["d"])]
    daily = gt.groupby(["stn", "y", "d"])["entries"].sum().reset_index()
    for s in ["ARD", "LSG", "KCN", "KDK", "KUH", "CBY"]:
        a = daily[(daily["stn"] == s) & (daily["y"] == 2027)]["entries"].mean()
        b = daily[(daily["stn"] == s) & (daily["y"] == 2019)]["entries"].mean()
        eq("station %s" % s, int(round(100 * a / b)), F["station_ratio"][s])
    line = gt.groupby(["y", "d"])["entries"].sum().reset_index()
    eq("line", int(round(100 * line[line["y"] == 2027]["entries"].mean() / line[line["y"] == 2019]["entries"].mean())),
       F["station_ratio"]["LINE"])
    # golden files read back
    book = xlsx_rows(os.path.join(G, "rathgarvan_boardings_2029.xlsx"), 1)
    flat = [str(c) for r in book for c in r if c is not None]
    if str(F["total_boardings"]) not in flat:
        bad.append("workbook does not carry the total %s" % F["total_boardings"])
    for z, v in F["zone_boardings"].items():
        if not any(r and r[0] == z and str(v) in [str(c) for c in r] for r in book):
            bad.append("workbook row %s lacks %s" % (z, v))
    b2 = xlsx_rows(os.path.join(G, "rathgarvan_boardings_2029.xlsx"), 2)
    for z, v in F["arrival_share"].items():
        if not any(r and r[0] == z and str(v) == str(r[-1]) for r in b2):
            bad.append("arrival sheet row %s lacks %s" % (z, v))
    b3 = xlsx_rows(os.path.join(G, "rathgarvan_boardings_2029.xlsx"), 3)
    names3 = {"Ardnagree", "Lisnagry", "Kilcarrow Central", "Kilcarrow Docklands", "University Hospital", "Carrigboy",
              "Ardnagree line"}
    got3 = [str(r[-1]) for r in b3 if r and r[0] in names3]
    if [str(F["station_ratio"][s]) for s in ["ARD", "LSG", "KCN", "KDK", "KUH", "CBY", "LINE"]] != got3:
        bad.append("station sheet %s" % got3)
    memo = docx_text(os.path.join(G, "rathgarvan_demand_note.docx"))
    if "{:,}".format(F["total_boardings"]) not in memo or "reduced scheme" not in memo:
        bad.append("note lacks the call")
    if "word/media/image1.png" not in zipfile.ZipFile(os.path.join(G, "rathgarvan_demand_note.docx")).namelist():
        bad.append("note lacks the chart")
    # every shipped format read back
    for fn in sorted(os.listdir(T)):
        p = os.path.join(T, fn)
        if fn.endswith(".pdf") and len(pdf_strings(p)) < 200:
            bad.append("pdf unreadable: " + fn)
        if fn.endswith(".docx") and len(docx_text(p)) < 100:
            bad.append("docx unreadable: " + fn)
        if fn.endswith(".xlsx") and len(xlsx_rows(p, 1)) < 3:
            bad.append("xlsx unreadable: " + fn)
        if fn.endswith(".csv") and len(pd.read_csv(p)) < 5:
            bad.append("csv short: " + fn)
    if bad:
        print("VERIFY FAIL")
        for b in bad:
            print("  " + b)
        sys.exit(1)
    print("VERIFY OK: total %s (%.1f), scope %s, %d zone figures, %d arrival shares, %d station ratios, golden files "
          "read back" % (F["total_boardings"], tot, F["scope"], len(F["zone_boardings"]), len(F["arrival_share"]),
                         len(F["station_ratio"])))


if __name__ == "__main__":
    main()
