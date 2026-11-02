"""The independent verifier: reads only target/ and the goldens, with its own readers (csv, pyarrow and pypdf; no
pandas, no bundle.py, no generator state), dates every 2026 refund's parcel by its own replay of the hall (each opening
takes the newest parcel waiting), recounts the return and the note, and checks the labelled openings and the 2025
deep-queue months on the same code path."""
import csv
import datetime as dt
import os
import re
import sys

import pyarrow.parquet as pq

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import world as W   # noqa: E402


def _ts(s):
    return dt.datetime.strptime(s, "%Y-%m-%d %H:%M:%S")


def read(target):
    F = W.FILES
    deliveries = []
    with open(os.path.join(target, F["goods2025"]), encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            if r["item_type"] == "RETURN":
                deliveries.append((_ts(r["scanned_at_uk"]), r["barcode"]))
    t = pq.read_table(os.path.join(target, F["goods2026"])).to_pydict()
    for ts, bc, cl in zip(t["event_ts_uk"], t["parcel_barcode"], t["parcel_class"]):
        if cl == "RET":
            deliveries.append((ts, bc))
    seen, uniq = set(), []
    for d in sorted(deliveries):
        if d[1] not in seen:
            seen.add(d[1])
            uniq.append(d)
    opens = []
    with open(os.path.join(target, F["processing"]), encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            opens.append((_ts(r["processed_at_uk"]), r["process_id"], r["order_ref"], r["return_label"], r["outcome"]))
    opens.sort()
    led = pq.read_table(os.path.join(target, F["refunds"])).to_pydict()
    made = {}
    for oref, reason, status, t_ in zip(led["order_ref"], led["reason"], led["status"], led["initiated_at_utc"]):
        if reason == "RETURN" and status == "PAID":
            uk = t_.astimezone(W.local_tz()).replace(tzinfo=None)
            assert oref not in made
            made[oref] = uk.date()
    return uniq, opens, made


def replay(uniq, opens):
    """Walk the two records in time: a delivery goes on the stack, an opening takes the stack's top."""
    out, stack, i = {}, [], 0
    for t, pid, oref, label, outcome in opens:
        while i < len(uniq) and uniq[i][0] < t:
            stack.append(uniq[i])
            i += 1
        out[pid] = stack.pop()
    return out


def main(target, gdir):
    uniq, opens, made = read(target)
    pair = replay(uniq, opens)
    lab = [(pid, label) for t, pid, oref, label, outcome in opens if label]
    exact = sum(1 for pid, label in lab if pair[pid][1] == label)
    assert exact == len(lab), "labelled openings: %d of %d" % (exact, len(lab))
    late, count, late25 = {}, {}, {}
    for t, pid, oref, label, outcome in opens:
        if outcome != "REFUND" or oref not in made:
            continue
        md = made[oref]
        days = (md - pair[pid][0].date()).days
        k = "%d-%02d" % (md.year, md.month)
        count[k] = count.get(k, 0) + 1
        if days >= W.LATE_DAY:
            late[k] = late.get(k, 0) + 1
            if md.year == 2025:
                late25[md.month] = late25.get(md.month, 0) + 1
    months = ["2026-%02d" % m for m in range(1, 7)]
    with open(os.path.join(gdir, W.GOLDEN["return"]), encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    for k, r in zip(months, rows):
        assert r["month"] == k
        assert int(r["refunds_made"]) == count[k], (k, r["refunds_made"], count[k])
        assert int(r["refunds_made_late"]) == late.get(k, 0), (k, r["refunds_made_late"], late.get(k, 0))
        share = round(100.0 * late.get(k, 0) / count[k], 1)
        assert float(r["late_share_pct"]) == share
        assert r["met_95pct_commitment"] == ("yes" if count[k] - late.get(k, 0) >= 0.95 * count[k] else "no")
    payment = 15 * sum(late.get(k, 0) for k in months)
    from pypdf import PdfReader
    note = re.sub(r"\s+", " ", "\n".join(p.extract_text() or "" for p in PdfReader(os.path.join(gdir, W.GOLDEN["note"])).pages))
    assert "We will pay" in note or "will pay" in note, "positive control: the note's payment sentence reads back"
    assert "{:,}".format(payment) in note, "payment %s not in the note" % payment
    assert sorted(late25) == [2, 12], "2025 deep-queue months %s" % late25
    print("verify: %d labelled openings exact; return rows and payment GBP {:,} recomputed from target/ alone; "
          "2025 late refunds in February %d and December %d".format(payment) % (len(lab), late25[2], late25[12]))


if __name__ == "__main__":
    T = os.path.dirname(HERE)
    main(os.path.join(T, "target"), os.path.join(T, "golden"))
