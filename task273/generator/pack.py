"""Readers of the cut pack, shared by the analysis, the cracker and the verifier: every figure the build reports is
computed from the files in target/, never from the world."""
import csv
import datetime as dt
import json
import os
import re

import numpy as np

import common as K

EPOCH = dt.datetime(1970, 1, 1)
GAP_S = 300.0                  # requests further apart than this belong to different runs


def path(target, key):
    return os.path.join(target, K.FILES[key])


def rows(target, key):
    with open(path(target, key), encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def secs(t):
    return (t - EPOCH).total_seconds()


def utc(s):
    """An ISO stamp ending Z, to seconds since the epoch (nanoseconds kept to the microsecond's float)."""
    s = s.rstrip("Z")
    frac = 0.0
    if "." in s:
        s, f = s.split(".")
        frac = float("0." + f)
    return secs(dt.datetime.strptime(s, "%Y-%m-%dT%H:%M:%S")) + frac


# ------------------------------------------------------------------------------------------------ the register
def register(target):
    import openpyxl
    wb = openpyxl.load_workbook(path(target, "register"), read_only=True)
    ep, svc = {}, {}
    for i, r in enumerate(wb["Endpoints"].iter_rows(values_only=True)):
        if i and r[0]:
            ep[r[0]] = dict(route="%s %s" % (r[1], r[2]), service=r[3], plans=[p.strip() for p in r[4].split(",")])
    for i, r in enumerate(wb["Services"].iter_rows(values_only=True)):
        if i and r[0]:
            svc[r[0]] = dict(collector=r[1], pods=int(r[4]), image=r[5])
    return ep, svc


# ------------------------------------------------------------------------------------------------ load tests
def requests(target):
    """Every request of the campaign: code -> list of (start, end, pod, ok, client thread), seconds since the epoch."""
    out = {}
    with open(path(target, "jmeter"), encoding="utf-8", newline="") as f:
        for r in csv.DictReader(f):
            code = r["label"].split(" ", 1)[0]
            t = int(r["timeStamp"]) / 1000.0
            out.setdefault(code, []).append((t, t + int(r["elapsed"]) / 1000.0, r["servedBy"], r["success"] == "true",
                                             r["threadName"].rsplit("-", 1)[1]))
    with open(path(target, "k6"), encoding="utf-8", newline="") as f:
        for r in csv.DictReader(f):
            if r["metric_name"] != "http_req_duration":
                continue
            tags = dict(x.split("=", 1) for x in r["extra_tags"].split("&"))
            end = utc(r["timestamp"])
            d = float(r["metric_value"]) / 1000.0
            out.setdefault(tags["endpoint"], []).append((end - d, end, tags["served_by"], r["status"] == "200",
                                                         tags["vu"]))
    return out


def runs(reqs):
    """Each endpoint's runs, in order: dict(t0 (first request's start), span, start, end, pod, ok)."""
    out = {}
    for code, lst in reqs.items():
        lst = sorted(lst)
        groups, cur = [], [lst[0]]
        for x in lst[1:]:
            if x[0] - cur[-1][0] > GAP_S:
                groups.append(cur)
                cur = []
            cur.append(x)
        groups.append(cur)
        rs = []
        for g in groups:
            st = np.array([x[0] for x in g])
            rs.append(dict(t0=float(st.min()), span=float(st.max() - st.min()), start=st,
                           end=np.array([x[1] for x in g]), pod=np.array([x[2] for x in g]),
                           ok=np.array([x[3] for x in g]), thread=np.array([x[4] for x in g])))
        out[code] = rs
    return out


def run_of_record(rs):
    """The last complete run: its requests span the warm-up and the whole measurement."""
    done = [r for r in rs if r["span"] >= K.RUN_S - 5.0]
    return done[-1]


# ------------------------------------------------------------------------------------------------ GC logs
LINE = re.compile(r"^(\S+)Z (\S+) \[([^\]]+)\]\[info\]\[([^\]]+)\] GC\((\d+)\) (.*)$")
STARTUP = re.compile(r"Started \w+ in [\d.]+ seconds \(process running for ([\d.]+)\)")


def jvm_starts(target):
    """Each pod's JVM starts (seconds since the epoch): the start-up line's time less the process's running time."""
    out = {}
    for r in rows(target, "events"):
        m = STARTUP.search(r["message"])
        if m and r["reason"] == "Log":
            out.setdefault(r["pod"], []).append(utc(r["time"]) - float(m.group(1)))
    return {p: sorted(v) for p, v in out.items()}


def gc_pauses(target):
    """Every pod's stop-the-world pauses, (start, end) in seconds since the epoch, sorted; a line is written when its
    pause ends and gives the pause's length."""
    starts = jvm_starts(target)
    out = {}
    with open(path(target, "gc"), encoding="utf-8") as f:
        for line in f:
            m = LINE.match(line.rstrip("\n"))
            if not m:
                continue
            ingest, pod, deco, tags, n, body = m.groups()
            if not body.startswith("Pause "):
                continue
            dur = float(re.search(r"([\d.]+)ms$", body).group(1)) / 1000.0
            if deco.endswith("s") and "T" not in deco:
                t_ing = utc(ingest + "Z")
                js = [s for s in starts[pod] if s <= t_ing]
                end = js[-1] + float(deco[:-1])
            else:
                local = dt.datetime.strptime(deco[:23], "%Y-%m-%dT%H:%M:%S.%f")
                off = int(deco[23:26]) * 3600 + int(deco[23] + deco[26:28]) * 60
                end = secs(local) - off
            out.setdefault(pod, []).append((end - dur, end))
    return {p: sorted(v) for p, v in out.items()}


# ------------------------------------------------------------------------------------------------ the asks
def renames(target):
    """The changelog's renames: new route -> (old route, first clock hour on the new route, seconds since the epoch)."""
    page = open(path(target, "changelog"), encoding="utf-8").read()
    out = {}
    for m in re.finditer(r"GET (/[\w/\-]+) is now GET (/[\w/\-]+)[^<]*?From 10:00 ET on (\d+) (\w+) (\d{4})", page):
        day = dt.datetime.strptime("%s %s %s" % (m.group(3), m.group(4), m.group(5)), "%d %B %Y")
        out["GET " + m.group(2)] = ("GET " + m.group(1), secs(day + dt.timedelta(hours=15)))
    return out


def synthetic(target):
    import yaml
    doc = yaml.safe_load(open(path(target, "synthetic"), encoding="utf-8"))
    d = doc["defaults"]
    out = []
    for c in doc["monitors"]:
        out.append(dict(name=c["name"], created=c["created"], every=c.get("frequency_seconds", d["frequency_seconds"]),
                        locations=c.get("locations", d["locations"]), steps=[s.split("  #")[0].strip()
                                                                             for s in c["steps"]]))
    return out


def edge(target):
    """route -> {hour (seconds since the epoch): requests}."""
    out = {}
    for r in rows(target, "edge"):
        out.setdefault(r["route"], {})[utc(r["hour_start_utc"])] = int(r["requests"])
    return out


def employers(target):
    return {r["employer_id"]: r for r in rows(target, "employers")}


def subscription_events(target):
    return rows(target, "subs")


def incidents(target):
    import openpyxl
    wb = openpyxl.load_workbook(path(target, "incidents"), read_only=True)
    out = {}
    for i, r in enumerate(wb["Incidents"].iter_rows(values_only=True)):
        if i and r[0]:
            out[r[0]] = dict(start=r[1], end=r[2], sev=r[3], comp=r[4])
    return out


def legacy_credits(target):
    return rows(target, "legacy")


def new_credits(target):
    return json.load(open(path(target, "credits"), encoding="utf-8"))["credits"]
