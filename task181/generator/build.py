"""Build the task181 pack: python3 build.py  (writes ../target/; the goldens come from golden.py --write)."""
import csv
import datetime as dt
import json
import os
import re
import shutil
import subprocess
import sys
import zipfile

import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import world as W      # noqa: E402
import sim as S        # noqa: E402
import fraud as F      # noqa: E402
import messages as M   # noqa: E402
import cases as C      # noqa: E402
import docs            # noqa: E402

TARGET = os.path.join(HERE, "..", "target")
FILES = {
    "auth": "card_authorisations_2026-06-01_2026-10-04.parquet",
    "merchants": "merchant_directory_2026-10.csv",
    "cards": "card_history_2026-10-05.xlsx",
    "cases": "fraud_cases_2026-08-01_2026-10-04.xlsx",
    "chargebacks": "chargebacks_2026-08-01_2026-10-04.csv",
    "codebook": "pos_entry_mode_codebook.pdf",
    "cp14": "CP-14_card_compromise_and_reissue.pdf",
    "ms3": "MS-3_member_service_standard.docx",
    "notes": "fraud_desk_notes.md",
    "closeout": "close_out_2025_brockville_atm_skimmer.pdf",
    "logins": "online_banking_logins_2026-08-01_2026-10-04.csv",
    "atmcash": "atm_cash_replenishment_q3_2026.xlsx",
    "log": "cudw_job_fraud_weekly_20261005.txt",
}
STAMP = dt.datetime(2026, 10, 5, 6, 40, 0)


def tp(k):
    return os.path.join(TARGET, FILES[k])


# ---------------------------------------------------------------------------------------------------
def write_auth(msg):
    schema = pa.schema([
        ("message_id", pa.string()), ("card_token", pa.string()), ("message_type", pa.string()),
        ("processing_code", pa.string()), ("txn_datetime_utc", pa.timestamp("s", tz="UTC")),
        ("amount_txn", pa.float64()), ("currency_txn", pa.string()), ("amount_billing_cad", pa.float64()),
        ("merchant_id", pa.string()), ("terminal_id", pa.string()), ("mcc", pa.string()),
        ("pos_entry_mode", pa.string()), ("response_code", pa.string()), ("retrieval_ref", pa.string()),
        ("stan", pa.string())])
    cols = {}
    for f in schema:
        v = msg[f.name]
        if f.name == "txn_datetime_utc":
            cols[f.name] = pa.array(v.dt.tz_convert("UTC").dt.tz_localize(None).values.astype("datetime64[s]"),
                                    type=pa.timestamp("s")).cast(pa.timestamp("s", tz="UTC"))
        elif f.type == pa.float64():
            cols[f.name] = pa.array(v.values.astype(float))
        else:
            cols[f.name] = pa.array([None if x is None else str(x) for x in v.tolist()], type=pa.string())
    tbl = pa.Table.from_arrays([cols[f.name] for f in schema], schema=schema)
    pq.write_table(tbl, tp("auth"), compression="zstd", row_group_size=250_000, write_statistics=True)
    return tbl.num_rows


def merchant_name(m):
    nm = m["name"]
    fixed = {"Ferrier Creek Travel Plaza fuel": "Ferrier Creek Travel Plaza - Pay at Pump",
             "Ferrier Creek Travel Plaza coffee counter": "Ferrier Creek Travel Plaza - Coffee Counter",
             "Ferrier Creek Travel Plaza car wash": "Ferrier Creek Travel Plaza - Car Wash"}
    return fixed.get(nm, nm)


def write_merchants(cat):
    rows = []
    for m in cat.merchants:
        rows.append([m["merchant_id"], merchant_name(m), m["mcc"], m["address"], m["town"], m["prov"], m["country"]])
    rows.sort(key=lambda r: r[0])
    with open(tp("merchants"), "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["merchant_id", "name", "mcc", "address", "town", "province_state", "country"])
        w.writerows(rows)
    return len(rows)


def write_chargebacks(cb):
    with open(tp("chargebacks"), "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(list(cb.columns))
        for r in cb.itertuples(index=False):
            amt = "" if r.amount_cad is None or (isinstance(r.amount_cad, float) and np.isnan(r.amount_cad)) \
                else "%.2f" % r.amount_cad
            w.writerow([r.chargeback_ref, r.retrieval_ref, r.card_token, r.reason, r.event_date.isoformat(), r.event, amt])
    return len(cb)


# ---------------------------------------------------------------------------------------------------
def card_history_frames(fr):
    tk = fr.tokens.copy()
    slots = fr.slots
    members = fr.members
    prod = []
    for r in tk.itertuples():
        if r.card_type == "Debit":
            prod.append("Member debit card, joint holder" if r.secondary else "Member debit card")
        else:
            prod.append("Rideau cash back credit card" if (r.slot % 5 == 0) else "Classic credit card")
    tk["product"] = prod
    status, sdate = [], []
    for r in tk.itertuples():
        if r.end_t is None or pd.isna(r.end_t):
            status.append("Open"); sdate.append(None)
        elif r.end_reason == "CL":
            status.append("Closed"); sdate.append(S.date_of(int(r.end_t) // S.DAY))
        else:
            status.append("Replaced"); sdate.append(S.date_of(int(r.end_t) // S.DAY))
    tk["status"], tk["status_date"] = status, sdate
    tk["expiry"] = ["%02d/%02d" % (m, y % 100) for y, m in tk.exp]
    cards = tk[["token", "member_id", "card_type", "product", "issued_on", "expiry", "status", "status_date"]]
    cards = cards.rename(columns={"token": "card_token"}).sort_values(["member_id", "issued_on", "card_token"])
    rep = []
    reason = {"RN": "Renewal", "LS": "Lost", "ST": "Stolen", "DM": "Damaged", "FR": "Fraud"}
    succ = {int(r.prev): r for r in tk.itertuples() if "prev" in tk.columns and not pd.isna(r.prev)}
    for r in tk.itertuples():
        if r.end_reason in reason and r.tok in succ:
            rep.append([r.token, succ[r.tok].token, S.date_of(int(r.end_t) // S.DAY), reason[r.end_reason]])
    rep = pd.DataFrame(rep, columns=["old_card_token", "new_card_token", "replaced_on", "reason"])
    rep = rep.sort_values(["replaced_on", "old_card_token"]).reset_index(drop=True)
    joint = set(slots.member[slots.secondary].tolist())
    mem = pd.DataFrame({"member_id": members.member_id, "home_branch": members.town,
                        "member_since": members.member_since,
                        "membership": ["Joint" if i in joint else "Individual" for i in range(len(members))]})
    mem = mem.sort_values("member_id").reset_index(drop=True)
    return cards.reset_index(drop=True), rep, mem


def write_card_history(fr):
    cards, rep, mem = card_history_frames(fr)
    docs.write_card_history(tp("cards"), cards, rep, mem)
    return len(cards), len(rep), len(mem)


def write_cases(wb):
    docs.write_cases_workbook(tp("cases"), wb)
    return len(wb)


# distractors -------------------------------------------------------------------------------------
def write_logins(fr):
    rng = np.random.default_rng(W.SEED + 91)
    members = fr.members
    rows = []
    seq = 5_120_000
    d0, d1 = dt.date(2026, 8, 1), dt.date(2026, 10, 4)
    active = members.member_id.values[rng.random(len(members)) < 0.62]
    rate = rng.gamma(1.4, 0.18, len(active))
    devices = {m: "%012x" % int(rng.integers(0, 2 ** 47)) for m in active}
    for m, r in zip(active, rate):
        n = rng.poisson(r * 65)
        days = sorted(rng.integers(0, (d1 - d0).days + 1, n).tolist())
        for d in days:
            day = d0 + dt.timedelta(int(d))
            h = float(np.clip(rng.normal(14.5, 4.2), 5.5, 23.9))
            t = dt.datetime.combine(day, dt.time()) + dt.timedelta(hours=h + W.UTC_OFFSET_H)
            ch = "app" if rng.random() < 0.71 else "web"
            dev = devices[m] if rng.random() < 0.93 else "%012x" % int(rng.integers(0, 2 ** 47))
            res = "success"
            u = rng.random()
            if u < 0.035:
                res = "failed password"
            elif u < 0.045:
                res = "MFA challenge failed"
            mfa = "" if (dev == devices[m] and res == "success") else ("SMS" if rng.random() < 0.6 else "app push")
            cc = "CA" if rng.random() < 0.985 else ["US", "US", "MX", "GB"][int(rng.integers(0, 4))]
            seq += int(rng.integers(1, 4))
            rows.append([seq, m, t.strftime("%Y-%m-%dT%H:%M:%SZ"), ch, dev, cc, res, mfa])
    rows.sort(key=lambda x: (x[2], x[0]))
    with open(tp("logins"), "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["session_id", "member_id", "login_utc", "channel", "client_id", "ip_country", "result",
                    "step_up_method"])
        w.writerows(rows)
    return len(rows)


def write_atm_cash(fr):
    rng = np.random.default_rng(W.SEED + 93)
    cat = fr.cat
    rows = []
    for m in cat.merchants:
        if m["role"] != "branch_atm":
            continue
        for k, term in enumerate(m["terminals"]):
            tid = cat.terminals[term]["tid_history"][0][1]
            d = dt.date(2026, 7, 2) + dt.timedelta(int(rng.integers(0, 3)))
            while d <= dt.date(2026, 9, 30):
                if d.weekday() < 5 and d not in W.HOLIDAY_SET:
                    load20 = int(rng.choice([1500, 2000, 2500])) * 20
                    load50 = int(rng.choice([200, 300, 400])) * 50
                    ret20 = int(rng.integers(150, 900)) * 20
                    ret50 = int(rng.integers(20, 160)) * 50
                    oos = int(rng.choice([0, 0, 0, 0, 15, 30, 45, 120]))
                    rows.append([d, m["town"], tid, "Branch lobby" if k == 0 else "Drive-through", load20, load50,
                                 ret20, ret50, oos, ["Route A", "Route B", "Route C"][k % 3]])
                d += dt.timedelta(int(rng.choice([3, 4, 5, 7])))
    rows.sort(key=lambda r: (r[0], r[1], r[2]))
    docs.write_atm_cash(tp("atmcash"), rows)
    return len(rows)


# ---------------------------------------------------------------------------------------------------
def rewrite_zip(path, creator):
    iso = STAMP.strftime("%Y-%m-%dT%H:%M:%SZ")
    tmp = path + ".tmp"
    with zipfile.ZipFile(path) as zin, zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            data = zin.read(item.filename)
            if item.filename == "docProps/core.xml":
                s = data.decode("utf8")
                s = re.sub(r"<dc:creator>.*?</dc:creator>", "<dc:creator>%s</dc:creator>" % creator, s)
                s = re.sub(r"<cp:lastModifiedBy>.*?</cp:lastModifiedBy>",
                           "<cp:lastModifiedBy>%s</cp:lastModifiedBy>" % creator, s)
                s = re.sub(r"(<dcterms:created[^>]*>).*?(</dcterms:created>)", r"\g<1>%s\g<2>" % iso, s)
                s = re.sub(r"(<dcterms:modified[^>]*>).*?(</dcterms:modified>)", r"\g<1>%s\g<2>" % iso, s)
                s = re.sub(r"<dc:description>[^<]*</dc:description>", "<dc:description></dc:description>", s)
                data = s.encode("utf8")
            if item.filename == "docProps/app.xml":
                s = data.decode("utf8")
                app = "Microsoft Excel" if path.endswith(".xlsx") else "Microsoft Office Word"
                s = re.sub(r"<Application>.*?</Application>", "<Application>%s</Application>" % app, s)
                data = s.encode("utf8")
            zi = zipfile.ZipInfo(item.filename, date_time=STAMP.timetuple()[:6])
            zi.compress_type = zipfile.ZIP_DEFLATED
            zout.writestr(zi, data)
    shutil.move(tmp, path)


def scrub(target):
    for fn in sorted(os.listdir(target)):
        p = os.path.join(target, fn)
        if fn.endswith((".xlsx", ".docx")):
            rewrite_zip(p, "Larchmere Credit Union")
    scr = os.path.join(HERE, "..", "..", ".claude", "skills", "reduce-house-fixes", "scripts",
                       "scrub_producer_metadata.py")
    subprocess.run([sys.executable, scr, target, "--apply", "--producer", "Larchmere Credit Union",
                    "--stamp", "2026-10-05", "--floor", "2025-01-01"], check=True, capture_output=True)
    for fn in sorted(os.listdir(target)):
        p = os.path.join(target, fn)
        if fn.endswith((".xlsx", ".docx")):
            rewrite_zip(p, "Larchmere Credit Union")
    ts = STAMP.timestamp()
    for fn in sorted(os.listdir(target)):
        os.utime(os.path.join(target, fn), (ts, ts))


def main():
    if os.path.isdir(TARGET):
        shutil.rmtree(TARGET)
    os.makedirs(TARGET)
    sim = S.simulate()
    fr = F.build(sim)
    msg = M.expand(fr)
    wb, cb = C.build(fr)
    counts = {"messages": write_auth(msg), "merchants": write_merchants(fr.cat)}
    counts["cards"], counts["replacements"], counts["members"] = write_card_history(fr)
    counts["case_rows"] = write_cases(wb)
    counts["chargebacks"] = write_chargebacks(cb)
    counts["logins"] = write_logins(fr)
    counts["atm_cash"] = write_atm_cash(fr)
    counts["cases"] = int(wb.case_number.nunique())
    docs.write_codebook(tp("codebook"))
    docs.write_cp14(tp("cp14"))
    docs.write_ms3(tp("ms3"))
    docs.write_closeout(tp("closeout"))
    docs.write_notes(tp("notes"), FILES)
    docs.write_log(tp("log"), FILES, counts, msg)
    scrub(TARGET)
    print(json.dumps(counts, sort_keys=True))


if __name__ == "__main__":
    main()
