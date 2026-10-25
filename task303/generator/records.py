"""The district's records from the outage process: the legacy and current outage exports, the storm crews' status
records and the system's major event days. Every clock is built here: the legacy system's Eastern local dates and
times, the current system's UTC stamps, the mobile workforce system's local times, and the storm desk's closing."""
import datetime as dt
from collections import defaultdict
from zoneinfo import ZoneInfo

import numpy as np

import params as P
import world as W

ET = ZoneInfo("America/New_York")
UTC = dt.timezone.utc


def growth(y):
    """the district's customers grew about six in a thousand a year to 2025"""
    return 1.0 - P.GROWTH * (2025 - y)


def local(day, minute):
    """an aware Eastern time for a day index and a local minute; a minute in the hour the clocks skip is moved on an
    hour, as the dispatchers' screens would show it"""
    naive = dt.datetime.combine(P.SIM0 + dt.timedelta(days=day), dt.time(0)) + dt.timedelta(minutes=minute)
    aw = naive.replace(tzinfo=ET)
    back = aw.astimezone(UTC).astimezone(ET).replace(tzinfo=None)
    if back != naive:
        aw = (naive + dt.timedelta(hours=1)).replace(tzinfo=ET)
    return aw


STATUSES = ("Assigned", "En route", "On site", "Restored", "Released")


def shown(tm, crew, status):
    """the time the mobile workforce system records with a status: the storm desk's screen for Assigned and the crew's
    own device for the rest; the contract crews' devices keep Eastern standard time all year"""
    if crew.startswith("PBL") and status != "Assigned":
        return (tm.astimezone(UTC) - dt.timedelta(hours=5)).replace(tzinfo=None)
    return tm.astimezone(ET).replace(tzinfo=None)


def hmm(minutes):
    """hours and minutes as the trouble crews' handhelds wrote them"""
    return "%d.%02d" % (minutes // 60, minutes % 60)


class Record:
    """the record as the district's systems hold it"""

    def __init__(self):
        self.ev, self.storm, self.taps = W.simulate(P.SEED, P.SEED_STORM)
        self.med = W.med_days(P.SEED, self.storm)
        r0 = (P.REC0 - P.SIM0).days
        self.rec = [e for e in self.ev if e["day"] >= r0]
        self.rec.sort(key=lambda e: (e["day"], e["minute"], e["feeder"], e["kind"], e["mins"], e["cust"]))
        rng = np.random.default_rng(P.SEED_REC)
        for e in self.rec:
            f = e["feeder"]
            n = f[2:]
            st = local(e["day"], e["minute"])
            e["start"] = st
            e["restore"] = (st.astimezone(UTC) + dt.timedelta(minutes=e["mins"])).astimezone(ET)
            e["year"] = st.year
            e["is_med"] = e["day"] in self.med
            g = growth(st.year)
            cust_f = W.FEEDERS[f][1]
            if e["device"] == "breaker":
                e["customers"] = int(round(cust_f * g))
            elif e["device"] in ("recloser", "fuse"):
                e["customers"] = max(1, int(round(e["cust"] * g)))
            else:
                e["customers"] = e["cust"]
            if e["device"] == "breaker":
                e["dev_leg"], e["dev_new"] = "CB-%s" % n, "F%s-BKR" % n
            elif e["device"] == "recloser":
                e["dev_leg"], e["dev_new"] = "RCL-%s-%d" % (n, e["zone"]), "F%s-R%d" % (n, e["zone"])
            elif e["device"] == "fuse":
                e["dev_leg"], e["dev_new"] = "FUS-%s-%02d" % (n, e["tap"]), "F%s-FU%03d" % (n, e["tap"])
            else:
                k = int(rng.integers(1, 30))
                e["dev_leg"], e["dev_new"] = "TX-%s-%02d%02d" % (n, e["tap"], k), "F%s-T%02d%02d" % (n, e["tap"], k)
            # the legacy system: tap and transformer tickets closed from a trouble crew's handheld; on storm days the
            # control room closed nearly all of them itself
            e["handheld"] = bool(e["device"] in ("fuse", "transformer") and st.date() < P.CUTOVER
                                 and rng.random() < (P.HANDHELD_STORM if e["storm"] else P.HANDHELD))
        self._numbers(rng)
        self._crews()

    def _numbers(self, rng):
        seq = defaultdict(int)
        for e in self.rec:
            y = e["year"]
            seq[y] += int(rng.integers(1, 4))
            if e["start"].date() < P.CUTOVER:
                e["tkt"] = "%02d-%05d" % (y % 100, seq[y])
            else:
                e["tkt"] = "INT-%d-%06d" % (y, seq[y] * 3 + int(rng.integers(0, 3)))

    def _crews(self):
        """the storm days of 2023 to 2025: crews' statuses in the mobile workforce system, and the storm desk closing
        restored jobs in batches"""
        rng = np.random.default_rng(P.SEED_CREW)
        cut = (P.CUTOVER - P.SIM0).days
        storm_days = sorted(d for d in self.storm if d >= cut and d in self.med)
        self.jobs = []
        company = ["SV-L%02d" % k for k in (11, 12, 13, 14, 15, 16, 17, 18, 21, 22, 23, 24, 25, 26)]
        contract = ["PBL-%02d" % k for k in range(3, 19)]
        aid = ["MA-%03d" % k for k in range(201, 241)]
        assess = ["DA-%02d" % k for k in range(1, 13)]
        seqj = defaultdict(int)
        for d in storm_days:
            tick = [e for e in self.rec if e["day"] == d]
            for e in tick:
                y = e["start"].year
                seqj[y] += int(rng.integers(1, 3))
                job = "WJ%02d-%06d" % (y % 100, seqj[y])
                S = e["start"]
                R = e["restore"]
                span = (R - S).total_seconds() / 60.0
                pool = rng.random()
                crew = (company[int(rng.integers(0, len(company)))] if pool < 0.5 else
                        contract[int(rng.integers(0, len(contract)))] if pool < 0.82 else aid[int(rng.integers(0, len(aid)))])
                if crew.startswith("PBL") and span < P.PBL_SPAN:
                    # the contract crews take the longer repairs; a short one goes to a company crew
                    crew = company[contract.index(crew) % len(company)]
                ctype = ("Company line crew" if crew.startswith("SV") else
                         "Contract line crew" if crew.startswith("PBL") else "Mutual assistance crew")
                work = min(max(10.0, span * 0.45), float(rng.uniform(25, 140)))
                travel = min(max(4.0, span * 0.12), float(rng.uniform(10, 45)))
                onsite = R - dt.timedelta(minutes=int(round(work)))
                enroute = onsite - dt.timedelta(minutes=int(round(travel)))
                assigned = enroute - dt.timedelta(minutes=int(rng.integers(2, 21)))
                if assigned <= S:
                    assigned = S + dt.timedelta(minutes=1)
                    enroute = max(enroute, assigned + dt.timedelta(minutes=1))
                    onsite = max(onsite, enroute + dt.timedelta(minutes=1))
                rows = []
                if rng.random() < P.TWO_CREW and (assigned - S).total_seconds() > 60 * 50:
                    first = assess[int(rng.integers(0, len(assess)))] if rng.random() < 0.5 else \
                        company[int(rng.integers(0, len(company)))]
                    ftype = "Damage assessor" if first.startswith("DA") else "Company line crew"
                    a1 = S + dt.timedelta(minutes=int(rng.integers(5, 25)))
                    e1 = a1 + dt.timedelta(minutes=int(rng.integers(3, 12)))
                    o1 = e1 + dt.timedelta(minutes=int(rng.integers(8, 25)))
                    r1 = o1 + dt.timedelta(minutes=int(rng.integers(6, 20)))
                    if r1 < assigned:
                        rows += [(first, ftype, "Assigned", a1), (first, ftype, "En route", e1),
                                 (first, ftype, "On site", o1), (first, ftype, "Released", r1)]
                rel = R + dt.timedelta(minutes=int(rng.integers(8, 41)))
                rows += [(crew, ctype, "Assigned", assigned), (crew, ctype, "En route", enroute),
                         (crew, ctype, "On site", onsite), (crew, ctype, "Restored", R), (crew, ctype, "Released", rel)]
                for c, t, s_, tm in rows:
                    self.jobs.append(dict(job=job, oms=e["tkt"], kind="Outage restoration", feeder=e["feeder"],
                                          device=e["dev_new"], crew=c, ctype=t, status=s_, time=tm, day=d,
                                          shown=shown(tm, c, s_)))
                # the storm desk: closed as the crew called it in (the outage system takes the crew's Restored time as
                # it arrives from the mobile workforce system), or left for the desk's next session
                e["batch"] = bool(rng.random() < P.BATCH_SHARE)
                e["closed"] = shown(R, crew, "Restored").replace(tzinfo=ET)
            # jobs with no outage ticket: wires down and damage assessment
            for _ in range(int(round(len(tick) * P.OTHER_JOBS))):
                e = tick[int(rng.integers(0, len(tick)))]
                y = e["start"].year
                seqj[y] += int(rng.integers(1, 3))
                job = "WJ%02d-%06d" % (y % 100, seqj[y])
                kind = "Wire down" if rng.random() < 0.6 else "Damage assessment"
                c = (company[int(rng.integers(0, len(company)))] if kind == "Wire down"
                     else assess[int(rng.integers(0, len(assess)))])
                t = "Company line crew" if c.startswith("SV") else "Damage assessor"
                a = e["start"] + dt.timedelta(minutes=int(rng.integers(10, 300)))
                en = a + dt.timedelta(minutes=int(rng.integers(3, 25)))
                on = en + dt.timedelta(minutes=int(rng.integers(8, 40)))
                rl = on + dt.timedelta(minutes=int(rng.integers(20, 160)))
                for s_, tm in (("Assigned", a), ("En route", en), ("On site", on), ("Released", rl)):
                    self.jobs.append(dict(job=job, oms="", kind=kind, feeder=e["feeder"], device="", crew=c, ctype=t,
                                          status=s_, time=tm, day=d, shown=shown(tm, c, s_)))
        for e in self.rec:
            if "closed" not in e:
                e["closed"] = e["restore"]
                e["batch"] = False
        self._desk(rng)
        # the export lists the statuses oldest first by the time recorded with each
        self.jobs.sort(key=lambda j: (j["shown"], j["job"], j["crew"], STATUSES.index(j["status"])))

    def _desk(self, rng):
        """the storm desk's sessions: at the top of every third hour it works through the restored jobs whose paperwork
        has come in, one ticket after another, and each ticket's restoration is entered as the desk closes it"""
        queue = sorted((e for e in self.rec if e["batch"]), key=lambda e: e["restore"].astimezone(UTC))
        if not queue:
            return
        t = queue[0]["restore"].replace(minute=0, second=0, microsecond=0)
        last = max(e["restore"] for e in queue).astimezone(UTC) + dt.timedelta(hours=6)
        i, waiting = 0, []
        while t.astimezone(UTC) <= last:
            if t.hour in P.BATCH_HOURS:
                while i < len(queue) and queue[i]["restore"] + dt.timedelta(minutes=P.BATCH_LAG) <= t:
                    waiting.append(queue[i])
                    i += 1
                clock = t.astimezone(UTC) + dt.timedelta(minutes=float(rng.uniform(2, 9)))
                for e in waiting:
                    clock += dt.timedelta(seconds=float(rng.uniform(10, 50)))
                    c = clock.replace(second=0, microsecond=0)
                    e["closed"] = c.astimezone(ET)
                waiting = []
            t = (t.astimezone(UTC) + dt.timedelta(hours=1)).astimezone(ET)
        assert i == len(queue), "a restored job never reached the desk"

    # the exports' rows
    def legacy_rows(self):
        """the legacy report as the district's export ran it: by feeder, then by the time the interruption began"""
        rows = []
        for e in self.rec:
            if e["start"].date() >= P.CUTOVER:
                continue
            dur = hmm(e["mins"]) if e["handheld"] else str(e["mins"])
            # a handheld dates its ticket the day the crew closes it
            day = e["restore"].date() if e["handheld"] else e["start"].date()
            rows.append(((e["feeder"], day, e["start"].strftime("%H:%M"), e["tkt"]),
                         [e["tkt"], e["feeder"][2:], P.SUBS[e["sub"]][1], day.strftime("%m/%d/%Y"),
                          e["start"].strftime("%H:%M"), dur, e["customers"], P.LEG_CAUSE[e["cause"]],
                          P.LEG_DEV[e["device"]], e["dev_leg"]]))
        return [x for _, x in sorted(rows, key=lambda r: r[0])]

    def current_rows(self):
        out = []
        for e in sorted(self.rec, key=lambda e: (e["feeder"], e["start"].astimezone(UTC), e["tkt"])):
            if e["start"].date() < P.CUTOVER:
                continue
            out.append([e["tkt"], e["feeder"], P.SUBS[e["sub"]][0],
                        e["start"].astimezone(UTC).strftime("%Y-%m-%dT%H:%M:00Z"),
                        e["closed"].astimezone(UTC).strftime("%Y-%m-%dT%H:%M:00Z"), e["customers"],
                        P.NEW_CAUSE[e["cause"]], P.NEW_DEV[e["device"]], e["dev_new"]])
        return out

    def crew_rows(self):
        return [[j["job"], j["oms"], j["kind"], j["feeder"], j["device"], j["crew"], j["ctype"], j["status"],
                 j["shown"].strftime("%Y-%m-%d %H:%M")] for j in self.jobs]

    def med_rows(self):
        rng = np.random.default_rng(P.SEED_REC + 7)
        out = []
        for d in sorted(self.med):
            day = P.SIM0 + dt.timedelta(days=d)
            m = day.month
            if m in (12, 1, 2):
                what = "Ice and wind" if rng.random() < 0.5 else "Wind storm"
            elif m in (8, 9, 10):
                what = "Remnants of a tropical storm" if rng.random() < 0.45 else "Severe thunderstorms"
            else:
                what = "Severe thunderstorms" if rng.random() < 0.8 else "Wind storm"
            out.append([day.isoformat(), what, P.TMED[day.year], "Docket E-%d-0%d" % (day.year + 1, 41 + day.year % 7)])
        return out
