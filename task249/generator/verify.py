"""Independent recomputation of task249 from the shipped bundle alone (csv module and numpy; no generator code)."""
import csv
import datetime as dt
import os
import re
import sys
from collections import defaultdict
from zoneinfo import ZoneInfo
import numpy as np

T = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "target")
TASK = os.path.dirname(os.path.abspath(T)) if os.path.basename(os.path.abspath(T)) == "target" else os.path.dirname(os.path.abspath(T))
MAD, UTC = ZoneInfo("Europe/Madrid"), dt.timezone.utc
P1 = dt.timezone(dt.timedelta(hours=1))
fails = []


def check(label, cond, extra=""):
    print(("PASS " if cond else "FAIL ") + label + ("" if cond else " " + str(extra)))
    if not cond:
        fails.append(label)


def f(name):
    hits = [x for x in os.listdir(T) if re.match(name, x)]
    return os.path.join(T, hits[0])


def utc(s):
    return dt.datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=UTC)


def loc(y, m, d):
    return dt.datetime(y, m, d, tzinfo=MAD).astimezone(UTC)


# the maintenance log: firmware 4.2 dates and the spare's id
from pypdf import PdfReader
log = " ".join(p.extract_text() for p in PdfReader(f(r"maintenance_log")).pages)
fw = {c: dt.datetime.strptime(d, "%d %b %Y").replace(hour=10, tzinfo=MAD).astimezone(UTC)
      for c, d in re.findall(r"(OZ\d\d)\s+(\d\d \w\w\w 2028)", log)}
spare = re.search(r"reported as (OZ\d\dB)", log).group(1)
check("log gives 35 firmware dates and OZ19 on 4.2 as the spare", len(fw) == 35 and "OZ19" not in fw)
EPOCH = dt.datetime(2000, 1, 1, tzinfo=UTC)

# the node export: the latest received record of each node and start
latest = {}
for r in csv.DictReader(open(f(r"nodes_o3_export"), encoding="utf-8")):
    node = r["node_id"]
    is_spare = node == spare
    if is_spare:
        node = node[:-1]
    t = utc(r["reading_start_utc"])
    if t < dt.datetime(2020, 1, 1, tzinfo=UTC):
        # stamped by a clock counting from a restart: placed by its received time
        off = t - EPOCH
        rec = utc(r["received_utc"]) - off - dt.timedelta(minutes=30)
        t = rec.replace(minute=0, second=0) + off
    key = (node, t.strftime("%Y-%m-%dT%H:%M:%SZ"))
    if key not in latest or r["received_utc"] >= latest[key][2]:
        latest[key] = (r["o3_ppb"], int(r["status"]), r["received_utc"], is_spare)
acc = defaultdict(lambda: defaultdict(list))
for (node, start), (v, st, _, sp) in latest.items():
    t = utc(start)
    ok = st == 0 or (st == 1 and (sp or t >= fw.get(node, dt.datetime(2099, 1, 1, tzinfo=UTC))))
    if ok and v != "":
        acc[node][t.replace(minute=0)].append(float(v))
w0, w1 = loc(2028, 4, 6), loc(2028, 6, 1)
nodes = sorted(acc)
check("36 nodes", len(nodes) == 36)


def aft(t):
    return 12 <= t.astimezone(MAD).hour < 18


def hourly(node):
    return np.array([np.mean(v) for h, v in sorted(acc[node].items()) if w0 <= h < w1 and aft(h)])


# the regional network, provisional release, hour ending UTC+1
ref = defaultdict(list)
for r in csv.DictReader(open(f(r"rrvca_o3_horario_provisional"), encoding="utf-8")):
    if r["validacion"] != "P" or r["o3_ugm3"] == "":
        continue
    d = dt.datetime.strptime(r["fecha"], "%d/%m/%Y").replace(tzinfo=P1) + dt.timedelta(hours=int(r["hora"]) - 1)
    if w0 <= d < w1 and aft(d):
        ref[r["estacion"]].append(float(r["o3_ugm3"]) / 1.996)
pool = np.concatenate([np.array(v) for v in ref.values()])
span = {n: hourly(n).std() / pool.std() for n in nodes}
pull = {n: ("low" if s < 0.85 else "high") for n, s in span.items() if not 0.85 <= s <= 1.15}
print("pull list", sorted(pull.items()))
sub = open(os.path.join(TASK, "submission.md"), encoding="utf-8").read()
check("submission names the same list", re.search(r"\*\*Take (\d+) nodes down.*?: ([^*]+)\.\*\*", sub).group(2).split(", ") == sorted(pull))
check("eight nodes, five low, three high", len(pull) == 8 and sum(v == "low" for v in pull.values()) == 5)
iq = {n: np.subtract(*np.percentile(hourly(n), [90, 10])) / np.subtract(*np.percentile(pool, [90, 10])) for n in nodes}
check("a quantile spread gives the same list", {n for n, s in iq.items() if not 0.85 <= s <= 1.15} == set(pull))

# ask A: local hours, 1 November 2027 to 31 January 2028, with an accepted reading
a0, a1 = loc(2027, 11, 1), loc(2028, 2, 1)
capture = {n: sum(1 for h in acc[n] if a0 <= h < a1) for n in nodes}
rows = dict(re.findall(r"\| (OZ\d\d) \| [^|]+ \| ([\d,]+) \|", sub))
check("submission's hours match for all 36 nodes", all(int(rows[n].replace(",", "")) == capture[n] for n in nodes),
      [(n, rows.get(n), capture[n]) for n in nodes if int(rows.get(n, "0").replace(",", "")) != capture[n]][:4])

print("%d failed" % len(fails))
sys.exit(1 if fails else 0)
