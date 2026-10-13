"""Independent verifier: the call, every rung of the ladder, the settled-estimator corridor and the three asks, recomputed
from the files under target/ alone (no simulation state, its own code path).

    python3 task231/generator/verify.py [target_dir] [golden_dir]
"""
import csv
import json
import os
import sys
from collections import Counter, defaultdict
from datetime import date, datetime, timedelta, timezone

from openpyxl import load_workbook

FRAME = date(2026, 9, 1)
EXTRACT = date(2026, 9, 25)
SETTLED_LAST = date(2022, 9, 1)           # frame dates at least 48 months before the extract
RED, AMBER = 55.0, 58.0


# ------------------------------------------------------------------------------------------------ reading
def rows(path):
    with open(path, newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def ts(s):
    return datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc) if s else None


def d(s):
    return date.fromisoformat(s) if s else None


def last_sunday(y, m):
    x = (date(y, m + 1, 1) if m < 12 else date(y + 1, 1, 1)) - timedelta(days=1)
    while x.weekday() != 6:
        x -= timedelta(days=1)
    return x


def brevland_offset(utc):
    """the dictionary's Conventions sheet: UTC+1, UTC+2 from 01:00 UTC on the last Sunday in March to 01:00 UTC on the
    last Sunday in October"""
    a = datetime.combine(last_sunday(utc.year, 3), datetime.min.time(), timezone.utc) + timedelta(hours=1)
    b = datetime.combine(last_sunday(utc.year, 10), datetime.min.time(), timezone.utc) + timedelta(hours=1)
    return 2 if a <= utc < b else 1


def local_17(day):
    guess = datetime(day.year, day.month, day.day, 16, 0, tzinfo=timezone.utc)
    return datetime(day.year, day.month, day.day, 17, 0, tzinfo=timezone.utc) - timedelta(hours=brevland_offset(guess))


def local_date(utc):
    return (utc + timedelta(hours=brevland_offset(utc))).date()


def core(num):
    return num[:6] if num else ""


def band(x):
    return "red" if x < RED else ("amber" if x < AMBER else "green")


class Pack:
    def __init__(self, target):
        p = lambda f: os.path.join(target, f)
        wb = load_workbook(p("BCS_round_calendar.xlsx"), read_only=True)
        ws = wb["Rounds"]
        it = ws.iter_rows(values_only=True)
        hdr = next(it)
        self.rounds = {}
        for r in it:
            x = dict(zip(hdr, r))
            fr = d(x["frame_date"])
            self.rounds[x["round"]] = dict(code=x["round"], quarter=x["quarter"], frame=fr, close=d(x["main_close"]),
                                           close_utc=local_17(d(x["main_close"])), cut=d(x["data_cut_off"]))
        self.by_quarter = {v["quarter"]: v for v in self.rounds.values()}
        wb = load_workbook(p("BCS_data_dictionary.xlsx"), read_only=True)
        ws = wb["Industry groups"]
        self.group_of = {}
        for r in ws.iter_rows(min_row=2, values_only=True):
            if r[0] and r[3]:
                for sec in str(r[3]).split(","):
                    self.group_of[sec.strip()] = r[0]
        self.review = {r["old_code"]: r["new_code"] for r in rows(p("bcs_region_review_2023.csv"))}
        self.inv = {int(r["panel_id"]): r for r in rows(p("bcs_invitations_2026_09.csv"))}
        self.inv_by_core = {core(r["company_number"]): pid for pid, r in self.inv.items()}
        self.sep = defaultdict(list)
        for r in rows(p("bcs_returns_2026_09.csv")):
            self.sep[int(r["panel_id"])].append((ts(r["received_at"]), r["mode"]))
        self.clos = {}
        for r in rows(p("brevland_business_register_closures.csv")):
            self.clos[core(r["company_number"])] = (d(r["ceased_trading"]), d(r["registered"]), r["procedure"])
        self.holders = defaultdict(list)
        for r in rows(p("bcs_panel_register.csv")):
            self.holders[int(r["panel_id"])].append(dict(company=r["company_number"], recruited=d(r["recruited"]),
                                                         left=d(r["left_panel"]), wave=r["recruitment_wave"],
                                                         nace=r["nace_section"], size=r["size_band"], region=r["region"]))
        self.out = defaultdict(list)          # quarter -> rows
        for r in rows(p("bcs_round_outcomes_2017_2026.csv")):
            self.out[r["round"]].append(r)
        self.calls = rows(p("contact_centre_calls_2022_2026.csv"))
        wb = load_workbook(p("contact_centre_outcome_codes.xlsx"), read_only=True)
        self.reached = {r[0]: r[2] == "Y" for r in wb["BCB codes"].iter_rows(min_row=2, values_only=True) if r[0]}
        self.ncs_map = {str(r[0]): r[2] for r in wb["OVF codes"].iter_rows(min_row=2, values_only=True) if r[0]}

    # -------------------------------------------------------------------------------------------- linking
    def holder(self, pid, frame):
        hs = self.holders[pid]
        live = [h for h in hs if h["recruited"] <= frame and (h["left"] is None or h["left"] >= frame)]
        if len(live) == 1:
            return live[0]
        live = [h for h in hs if h["recruited"] <= frame]
        return max(live, key=lambda h: h["recruited"]) if live else hs[0]

    def bcb_code(self, row):
        return row["outcome"] if row["team"] == "BCB" else self.ncs_map.get(row["outcome"], "")

    def call_firm(self, row, rnd):
        """the panel firm a call record belongs to: BCB by panel ID, OVF by the company number's six-digit core"""
        if row["team"] == "BCB":
            return int(row["panel_id"])
        c = core(row["company_number"])
        if rnd == "2026-09":
            return self.inv_by_core.get(c)
        frame = self.rounds[rnd]["frame"]
        for pid, h in self.core_index().get(c, []):
            if h["recruited"] <= frame and (h["left"] is None or h["left"] >= frame):
                return pid
        return None

    _ci = None

    def core_index(self):
        if self._ci is None:
            self._ci = defaultdict(list)
            for pid, hs in self.holders.items():
                for h in hs:
                    self._ci[core(h["company"])].append((pid, h))
        return self._ci

    # -------------------------------------------------------------------------------------------- September
    def september(self):
        """per region: invited, returned by the close, known closed by the extract, unresolved non-returners"""
        close = self.rounds["2026-09"]["close_utc"]
        res = {}
        for pid, r in self.inv.items():
            g = res.setdefault(r["region"], dict(inv=0, R=0, known=0, nr=[]))
            g["inv"] += 1
            if any(t <= close for t, m in self.sep.get(pid, [])):
                g["R"] += 1
                continue
            c = self.clos.get(core(r["company_number"]))
            if c and c[1] <= EXTRACT and c[0] <= FRAME:
                g["known"] += 1
                continue
            g["nr"].append(pid)
        return res

    # -------------------------------------------------------------------------------------------- history
    def reach_times(self, quarter, phone_from_calls):
        """quarter -> {panel_id: reach time} for the round's returns; phone returns from 9 April 2024 can take the
        interview end from the call records (the round's COMP / 10 records) instead of the database load time"""
        rnd = self.by_quarter[quarter]
        out = {}
        comp = {}
        if phone_from_calls:
            comp = self.interview_ends(rnd["code"])
        for r in self.out[quarter]:
            if not r["received_at"]:
                continue
            pid = int(r["panel_id"])
            t = ts(r["received_at"])
            if phone_from_calls and r["mode"] == "phone" and pid in comp:
                t = comp[pid]
            out[pid] = t
        return out

    _ie = None

    def interview_ends(self, rnd):
        if self._ie is None:
            self._ie = defaultdict(dict)
            for r in self.calls:
                if self.bcb_code(r) == "COMP":
                    pid = self.call_firm(r, r["round"])
                    if pid is None:
                        continue
                    end = ts(r["started_at"]) + timedelta(seconds=int(r["duration_s"]))
                    self._ie[r["round"]][pid] = end
        return self._ie.get(rnd, {})

    def settled_share(self, first=None, last=SETTLED_LAST, key=None, pool="close", exclude="close", dead_by="frame",
                      phone_from_calls=True, known_strict=False):
        num, den = Counter(), Counter()
        for q, rnd in sorted(self.by_quarter.items(), key=lambda kv: kv[1]["frame"]):
            fr = rnd["frame"]
            if fr >= FRAME or fr > last or (first and fr < first) or q not in self.out:
                continue
            reach = self.reach_times(q, phone_from_calls)
            for r in self.out[q]:
                pid = int(r["panel_id"])
                t = reach.get(pid)
                if pool == "close":
                    if t is not None and t <= rnd["close_utc"]:
                        continue
                elif r["mode"]:
                    continue
                h = self.holder(pid, fr)
                c = self.clos.get(core(h["company"]))
                if c and exclude != "none":
                    edge = rnd["close"] if exclude == "close" else rnd["cut"]
                    if (c[1] < edge if known_strict else c[1] <= edge) and c[0] <= fr:
                        continue
                limit = fr if dead_by == "frame" else rnd["close"]
                dead = bool(c and c[0] <= limit)
                k = key(r, h, rnd) if key else "all"
                den[k] += 1
                num[k] += dead
        return {k: num[k] / den[k] for k in den}, den

    def silent_runs(self):
        """rounds without a return before each round, per panel ID, from the outcomes file (censored at March 2017)"""
        runs = {}
        last = defaultdict(int)
        seen_holder = {}
        for q, rnd in sorted(self.by_quarter.items(), key=lambda kv: kv[1]["frame"]):
            if q not in self.out:
                continue
            for r in self.out[q]:
                pid = int(r["panel_id"])
                h = id(self.holder(pid, rnd["frame"]))
                if seen_holder.get(pid) != h:
                    last[pid] = 0
                    seen_holder[pid] = h
                runs[(q, pid)] = last[pid]
                last[pid] = 0 if r["mode"] else last[pid] + 1
        return runs, last


# ------------------------------------------------------------------------------------------------ the call and the rungs
def rates(pk, inscope_fn):
    sep = pk.september()
    return {g: 100.0 * v["R"] / (v["R"] + inscope_fn(g, v)) for g, v in sep.items()}, sep


def call_outcomes_sep(pk, outbound_only=False):
    """September non-returners' call outcomes as BCB codes, per panel ID"""
    out = defaultdict(list)
    for r in pk.calls:
        if r["round"] != "2026-09" or (outbound_only and r["direction"] != "out"):
            continue
        pid = pk.call_firm(r, "2026-09")
        if pid is not None:
            out[pid].append(pk.bcb_code(r))
    return out


def ladder(pk):
    s_set = pk.settled_share()[0]["all"]
    s_all_nat = pk.settled_share(last=date(2026, 6, 1), phone_from_calls=False)[0]["all"]
    s_all = pk.settled_share(last=date(2026, 6, 1))[0]["all"]
    s_rec_nat = pk.settled_share(first=date(2024, 9, 1), last=date(2026, 6, 1), phone_from_calls=False)[0]["all"]
    s_rec = pk.settled_share(first=date(2024, 9, 1), last=date(2026, 6, 1))[0]["all"]
    co = call_outcomes_sep(pk)
    co_out = call_outcomes_sep(pk, outbound_only=True)
    sep = pk.september()
    out = {}
    for g, v in sep.items():
        R, nr = v["R"], v["nr"]
        n = len(nr)
        alive_strict = sum(1 for pid in nr if {"PROM", "REFU"} & set(co.get(pid, [])))
        alive_any = sum(1 for pid in nr if {"PROM", "REFU", "STAF"} & set(co.get(pid, [])))
        closed = sum(1 for pid in nr if "CEAS" in co.get(pid, []))
        unob = sum(1 for pid in nr if "UNOB" in co.get(pid, []) and "CEAS" not in co.get(pid, []))
        rate = lambda x: 100.0 * R / (R + x)
        e_s = alive_strict / (alive_strict + closed)
        e_a = alive_any / (alive_any + closed)
        alive_out = sum(1 for pid in nr if {"PROM", "REFU"} & set(co_out.get(pid, [])))
        closed_out = sum(1 for pid in nr if "CEAS" in co_out.get(pid, []))
        e_o = alive_out / (alive_out + closed_out)
        out[g] = dict(R=R, inv=v["inv"], known=v["known"], n=n,
                      R1=rate(n),
                      casro=rate(alive_strict + e_s * (n - alive_strict - closed)),
                      casro_any=rate(alive_any + e_a * (n - alive_any - closed)),
                      casro_out=rate(alive_out + e_o * (n - alive_out - closed_out)),
                      unob=rate(n - closed - unob),
                      recent=rate(n * (1 - s_rec)), recent_nat=rate(n * (1 - s_rec_nat)),
                      allr=rate(n * (1 - s_all)), allr_nat=rate(n * (1 - s_all_nat)),
                      golden=rate(n * (1 - s_set)),
                      over=rate(alive_strict))
    return out, dict(settled=s_set, all=s_all, all_nat=s_all_nat, recent=s_rec, recent_nat=s_rec_nat)


def corridor(pk):
    """every settled-round estimator named in the closure table, from the files"""
    sep = pk.september()
    runs, last = pk.silent_runs()
    region_of = lambda r, h, rnd: pk.review.get(r["region"], r["region"])
    k_of = lambda r, h, rnd: min(runs[(rnd["quarter"], int(r["panel_id"]))], 6)
    size_of = lambda r, h, rnd: h["size"]
    est = {}
    for w, last_fr in ((36, date(2023, 9, 1)), (42, date(2023, 3, 1)), (48, SETTLED_LAST), (54, date(2022, 3, 1)),
                       (60, date(2021, 9, 1)), (72, date(2020, 9, 1))):
        est["w%d" % w] = ("pooled", pk.settled_share(last=last_fr)[0])
    est["region"] = ("region", pk.settled_share(key=region_of)[0])
    est["k"] = ("k", pk.settled_share(key=k_of)[0])
    est["size"] = ("size", pk.settled_share(key=size_of)[0])
    est["end"] = ("pooled", pk.settled_share(pool="end")[0])
    est["excl_end"] = ("pooled", pk.settled_share(exclude="end")[0])
    est["excl_none"] = ("pooled", pk.settled_share(exclude="none")[0])
    est["dead_close"] = ("pooled", pk.settled_share(dead_by="close")[0])
    est["known_strict"] = ("pooled", pk.settled_share(known_strict=True)[0])
    res = {}
    for g, v in sep.items():
        R, nr = v["R"], v["nr"]
        rate = lambda x: 100.0 * R / (R + x)
        row = {}
        for name, (kind, s) in est.items():
            if kind == "pooled":
                row[name] = rate(len(nr) * (1 - s["all"]))
            elif kind == "region":
                row[name] = rate(len(nr) * (1 - s[g]))
            elif kind == "k":
                row[name] = rate(sum(1 - s[min(last.get(pid, 0), 6)] for pid in nr))
            else:
                row[name] = rate(sum(1 - s[pk.holder(pid, FRAME)["size"]] for pid in nr))
        res[g] = row
    return res


# ------------------------------------------------------------------------------------------------ the asks
def ask_a(pk):
    """September round, by region: firms the contact centre has reached so far (on a call either way), and outbound calls
    it has placed"""
    region = lambda pid: pk.inv[pid]["region"]
    recs = [r for r in pk.calls if r["round"] == "2026-09"]
    fields = ("team", "direction", "panel_id", "company_number", "region", "agent", "started_at", "duration_s", "outcome")
    seen, uniq = set(), []
    for r in recs:
        k = tuple(r[f] for f in fields)
        if k in seen:
            continue
        seen.add(k)
        uniq.append(r)
    calls, rows_, noid, firmday, outrows = Counter(), Counter(), Counter(), Counter(), Counter()
    reached, reached_out, reached_resp, reached_bcb = (defaultdict(set) for _ in range(4))
    fd = set()
    for r in recs:
        pid = pk.call_firm(r, "2026-09")
        g = region(pid)
        rows_[g] += 1
        if r["direction"] == "out":
            outrows[g] += 1
            key = (pid, local_date(ts(r["started_at"])))
            if key not in fd:
                fd.add(key)
                firmday[g] += 1
    for r in uniq:
        pid = pk.call_firm(r, "2026-09")
        g = region(pid)
        code = pk.bcb_code(r)
        if r["direction"] == "out":
            noid[g] += 1
            if not (r["team"] == "OVF" and r["outcome"] == "71"):
                calls[g] += 1
        if pk.reached.get(code):
            reached[g].add(pid)
            if r["direction"] == "out":
                reached_out[g].add(pid)
            if r["team"] == "BCB":
                reached_bcb[g].add(pid)
        if code in ("COMP", "PROM", "REFU"):
            reached_resp[g].add(pid)
    regs = sorted(set(r["region"] for r in pk.inv.values()))
    n = lambda c: {g: len(c[g]) for g in regs}
    return dict(reached=n(reached), calls={g: calls[g] for g in regs},
                stops=dict(calls_rows={g: rows_[g] for g in regs}, calls_outbound_rows={g: outrows[g] for g in regs},
                           calls_noid={g: noid[g] for g in regs}, calls_firmday={g: firmday[g] for g in regs},
                           reached_outbound=n(reached_out), reached_resp=n(reached_resp), reached_bcb=n(reached_bcb)))


def ask_b(pk):
    """June 2026 round, by region: returns that reached the bank after the main close, and their share of the region's
    June returns"""
    q = "2026Q2"
    rnd = pk.by_quarter[q]
    close = rnd["close_utc"]
    reach = pk.reach_times(q, True)
    late, n, late_recv, late_rec = Counter(), Counter(), Counter(), Counter()
    for r in pk.out[q]:
        if not r["mode"]:
            continue
        pid = int(r["panel_id"])
        g = pk.review.get(r["region"], r["region"])
        n[g] += 1
        late[g] += reach[pid] > close
        late_recv[g] += ts(r["received_at"]) > close
        late_rec[g] += ts(r["recorded_at"]) > close
    regs = sorted(n)
    share = lambda c: {g: round(100.0 * c[g] / n[g], 1) for g in regs}
    return dict(late={g: late[g] for g in regs}, returns={g: n[g] for g in regs}, share=share(late),
                stops=dict(late_received_at={g: late_recv[g] for g in regs}, share_received_at=share(late_recv),
                           late_recorded_at={g: late_rec[g] for g in regs}, share_recorded_at=share(late_rec)))


def ask_c(pk):
    """March 2026 refreshment, by industry group: firms recruited (distinct companies), and of them firms that have returned
    at least once (their own March and June 2026 rounds, and the September round to the close)"""
    recs = [(pid, h) for pid, hs in pk.holders.items() for h in hs if h["wave"] == "2026 refreshment"]
    grp = lambda h: pk.group_of[h["nace"]]
    firms = defaultdict(list)
    for pid, h in recs:
        firms[core(h["company"])].append((pid, h))
    returned_any = defaultdict(bool)
    for q, rows_ in pk.out.items():
        for r in rows_:
            if r["mode"]:
                returned_any[int(r["panel_id"])] = True
    first_round = {int(r["panel_id"]) for r in pk.out.get("2026Q1", [])}

    def own(pid, h):
        rounds = [q for q, v in pk.by_quarter.items() if h["recruited"] <= v["frame"] < FRAME and
                  (h["left"] is None or h["left"] >= v["frame"])]
        return any(r["mode"] for q in rounds for r in pk._by_pid(q).get(pid, [])) or bool(pk.sep.get(pid))

    rec, ret = Counter(), Counter()
    for c, lst in firms.items():
        g = grp(lst[0][1])
        rec[g] += 1
        ret[g] += any(own(pid, h) for pid, h in lst)
    rows_n, strings, kept, inv_n, letters, ret_any, ret_hist = (Counter() for _ in range(7))
    for pid, h in recs:
        g = grp(h)
        rows_n[g] += 1
        letters[h["nace"]] += 1
        if not (h["left"] is not None and h["left"] < date(2026, 3, 1)):
            kept[g] += 1
        if pid in pk.inv or pid in first_round:
            inv_n[g] += 1
        ret_any[g] += returned_any[pid] or bool(pk.sep.get(pid))
    for g_ in set(grp(h) for pid, h in recs):
        strings[g_] = len({h["company"] for pid, h in recs if grp(h) == g_})
    for c, lst in firms.items():
        g = grp(lst[0][1])
        ret_hist[g] += any(any(r["mode"] for q in [q for q, v in pk.by_quarter.items() if h["recruited"] <= v["frame"] < FRAME]
                               for r in pk._by_pid(q).get(pid, [])) for pid, h in lst)
    groups = sorted(set(pk.group_of.values()))
    z = lambda c: {g: c[g] for g in groups}
    return dict(recruited=z(rec), returned=z(ret),
                stops=dict(recruited_rows=z(rows_n), recruited_strings=z(strings), recruited_kept=z(kept),
                           recruited_invited=z(inv_n), recruited_letters={g: letters.get(g, 0) for g in groups},
                           returned_any_id=z(ret_any), returned_no_september=z(ret_hist)))


def _by_pid(self, q):
    if not hasattr(self, "_bp"):
        self._bp = {}
    if q not in self._bp:
        m = defaultdict(list)
        for r in self.out.get(q, []):
            m[int(r["panel_id"])].append(r)
        self._bp[q] = m
    return self._bp[q]


Pack._by_pid = _by_pid


# ------------------------------------------------------------------------------------------------ main
def compute(target):
    pk = Pack(target)
    lad, shares = ladder(pk)
    return dict(pack=pk, ladder=lad, shares=shares, corridor=corridor(pk), A=ask_a(pk), B=ask_b(pk), C=ask_c(pk))


def call_from(lad):
    regs = sorted(lad)
    lv = {g: band(lad[g]["golden"]) for g in regs}
    return dict(levels=lv, extension=[g for g in regs if lv[g] == "red"], email=[g for g in regs if lv[g] == "amber"],
                neither=[g for g in regs if lv[g] == "green"])


def main(target, golden_dir=None, figures_path=None):
    res = compute(target)
    lad = res["ladder"]
    call = call_from(lad)
    for g, row in res["corridor"].items():
        for name, x in row.items():
            assert band(x) == call["levels"][g], ("corridor", g, name, x)
    if figures_path and os.path.exists(figures_path):
        fig = json.load(open(figures_path))
        assert fig["levels"] == call["levels"], "figures.json levels differ from the verifier"
        assert fig["reached"] == {g: str(v) for g, v in res["A"]["reached"].items()}
        assert fig["calls"] == {g: str(v) for g, v in res["A"]["calls"].items()}
        assert fig["late"] == {g: str(v) for g, v in res["B"]["late"].items()}
        assert fig["late_share"] == {g: "%.1f" % v for g, v in res["B"]["share"].items()}
        assert fig["recruited"] == {g: str(v) for g, v in res["C"]["recruited"].items()}
        assert fig["returned_once"] == {g: str(v) for g, v in res["C"]["returned"].items()}
    if golden_dir:
        wb = load_workbook(os.path.join(golden_dir, "bcs_sep2026_extension.xlsx"), read_only=True)
        ws = wb["Alert levels"]
        got = {}
        for r in ws.iter_rows(min_row=2, values_only=True):
            if r and r[0] in call["levels"]:
                got[r[0]] = str(r[-2]).lower()
        assert got == call["levels"], ("workbook levels", got)
    print("verify: call", {k: v for k, v in call.items() if k != "levels"})
    return res, call


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    tgt = sys.argv[1] if len(sys.argv) > 1 else os.path.join(here, "..", "target")
    gd = sys.argv[2] if len(sys.argv) > 2 else None
    main(tgt, gd, os.path.join(here, "figures.json"))
