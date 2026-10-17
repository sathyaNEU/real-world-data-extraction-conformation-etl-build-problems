"""The records each system writes from task237's world: the online panel vendor's export, its incentive ledger and
paradata, the interviewer-administered vendor's item-level file and back-check log, the translation register, the
vendors' codebook and the wave 5 results by region."""
import datetime as dt

import numpy as np
import pandas as pd

import params as P

VERSION = {v[0]: v for v in P.VERSIONS}
CODES = [i[0] for i in P.ITEMS]


def utc_iso(t):
    return t.strftime("%Y-%m-%dT%H:%M:%SZ")


class Records:
    def __init__(self, W, seed=P.RECORD_SEED):
        self.W = W
        self.seed = seed

    def _stream(self, k):
        return np.random.default_rng(self.seed * 100 + k)

    @staticmethod
    def age(rng, vendor):
        a, b, span = P.AGE_BETA[vendor]
        return 18 + int(span * rng.beta(a, b))

    @staticmethod
    def raw_answers(x, miss, missing_code):
        """the answers as the respondent gave them: negatively worded items unreversed, unanswered as the vendor codes it"""
        raw = np.array(x, dtype=object)
        for i in P.NEG:
            raw[i] = 6 - int(x[i])
        out = []
        for i in range(12):
            if miss[i]:
                out.append(missing_code(i))
            else:
                out.append(int(raw[i]))
        return out

    # ------------------------------------------------------------------ the online panel (Nesscroft Panels)
    def online(self):
        rng = self._stream(1)
        R = self.W.respondents
        R = R[R.vendor == "NCP"].copy()
        start, end = P.PILOT["NCP"]
        days = (end - start).days + 1
        rows, ledger, para, merges = [], [], [], []
        used = set()

        def new_id(prefix, width):
            while True:
                x = "%s%0*d" % (prefix, width, int(rng.integers(10 ** (width - 1), 10 ** width)))
                if x not in used:
                    used.add(x)
                    return x

        def when(day, h0, h1):
            return dt.datetime.combine(start + dt.timedelta(days=day), dt.time(0)) + dt.timedelta(
                hours=float(rng.uniform(h0, h1))) - P.UTC_OFFSET

        for code in [v[0] for v in P.VERSIONS if v[2] == "NCP"]:
            v = R[R.version == code].reset_index(drop=True)
            valid_idx = v.index[v.kind == "valid"].tolist()
            sources = {int(x) for x in v.of.dropna()}
            member, finish = {}, {}
            order = sorted(range(len(v)), key=lambda j: v.kind[j] in ("retake", "merged"))
            for j in order:
                r = v.loc[j]
                rid = new_id("NC6", 7)
                dur = float(np.exp(rng.normal(6.25, 0.45)))
                while dur > 2400:                         # the panel times an entry out after 40 minutes away
                    dur = float(np.exp(rng.normal(6.25, 0.45)))
                if r.kind in ("retake", "merged"):
                    first = valid_idx[int(r.of)]
                    fday = ((finish[first] + P.UTC_OFFSET).date() - start).days
                    t0 = when(min(days - 1, fday + int(rng.integers(1, 7))), 7.0, 23.0)
                    pm = member[first] if r.kind == "retake" else new_id("PM", 8)
                elif r.kind == "soft":
                    t0, pm = when(-1, P.SOFT_OPEN, 23.0), new_id("PM", 8)
                else:
                    day = int(rng.integers(0, days - 8 if j in sources else days))
                    t0, pm = when(day, 7.0, 23.0), new_id("PM", 8)
                member[j] = pm
                if r.kind == "screenout":
                    age, status, dur = int(rng.choice([16, 17])), "screened out", float(rng.uniform(25, 70))
                else:
                    age = self.age(rng, "NCP")
                    status = "partial" if r.kind in ("partial", "past") else "complete"
                sex = "F" if rng.random() < 0.52 else ("X" if rng.random() < 0.01 else "M")
                hh = int(np.clip(rng.poisson(2.1) + 1, 1, 9))
                yrs = int(min(age - 1, np.round(rng.gamma(2.2, 7.5))))
                back = [sex, hh, yrs]
                ui = "en" if r.kind == "switch" else code
                if r.kind == "screenout":
                    answers, back = [""] * 12, ["", "", ""]
                else:
                    answers = self.raw_answers(r.X, r.miss, lambda i: 9)
                    if r.kind == "partial":
                        answers = [a if i < r.stop else "" for i, a in enumerate(answers)]
                        back = ["", "", ""]
                        dur *= (r.stop + 2) / 18
                    elif r.kind == "past":
                        back = back[:int(r.leave)] + [""] * (3 - int(r.leave))
                        dur *= (14 + int(r.leave)) / 18
                t1 = t0 + dt.timedelta(seconds=dur)
                finish[j] = t1
                rows.append(dict(respondent_id=rid, survey_code="CCS6-BCS-%s" % code.upper(), status=status,
                                 start_utc=utc_iso(t0), end_utc=utc_iso(t1) if status == "complete" else "",
                                 ui_language_at_end=ui, age=age, **{c: a for c, a in zip(CODES, answers)},
                                 sex=back[0], hh_size=back[1], yrs_in_canada=back[2]))
                pts = 150 if status == "complete" else 40 if status == "partial" else 10
                ledger.append(dict(panel_member_id=pm, respondent_id=rid, survey_code="CCS6-BCS-%s" % code.upper(),
                                   activity_utc=utc_iso(t1), outcome=status, points=pts, merged_into=""))
                if r.kind == "merged":
                    merges.append((pm, member[first], t1, pts))
                para.append(dict(respondent_id=rid, platform=str(rng.choice(["mobile", "desktop", "tablet"], p=[.58, .36, .06])),
                                 duration_seconds=int(round(dur)),
                                 module_seconds=int(round(dur * float(rng.uniform(0.32, 0.44)))) if status != "screened out" else 0,
                                 back_button_uses=int(rng.poisson(0.6))))
            # second accounts the panel found and merged whose entry here was a screen-out or a partial
            others = [j for j in range(len(v)) if v.kind[j] in ("screenout", "partial")]
            for j in rng.choice(others, size=int(round(len(valid_idx) * P.BENIGN_MERGES)), replace=False):
                k = valid_idx[int(rng.integers(len(valid_idx)))]
                merges.append((member[int(j)], member[k], finish[int(j)], 10 if v.kind[int(j)] == "screenout" else 40))
        for pm, into, t, pts in merges:
            tm = dt.datetime.combine((t + P.UTC_OFFSET).date() + dt.timedelta(days=int(rng.integers(2, 9))), dt.time(0)) \
                + dt.timedelta(hours=float(rng.uniform(1.0, 5.0)))
            tm = min(tm, P.EXPORT_UTC - dt.timedelta(hours=6))
            ledger.append(dict(panel_member_id=pm, respondent_id="", survey_code="", activity_utc=utc_iso(tm),
                               outcome="merged", points=-pts, merged_into=into))
        led = pd.DataFrame(ledger)
        led["payment_batch"] = [("2027-%02d" % (int(a[5:7]) + (1 if int(a[8:10]) > 24 else 0))) for a in led.activity_utc]
        led = led[["panel_member_id", "respondent_id", "survey_code", "activity_utc", "outcome", "points", "merged_into",
                   "payment_batch"]]
        out = pd.DataFrame(rows).sort_values(["start_utc", "respondent_id"]).reset_index(drop=True)
        led = led.sort_values(["activity_utc", "panel_member_id", "respondent_id"]).reset_index(drop=True)
        par = pd.DataFrame(para).sort_values("respondent_id").reset_index(drop=True)
        return out, led, par

    # ------------------------------------------------------------------ the interviewer-administered pilots (Fernlow Research)
    BACKGROUND = ("SEX", "HHSIZE", "YRSCAN")

    def capi(self):
        rng = self._stream(2)
        R = self.W.respondents
        R = R[R.vendor == "FLR"].copy()
        start, end = P.PILOT["FLR"]
        pdays = (end - start).days + 1
        tstart, tend = P.PRETEST
        tdays = (tend - tstart).days + 1
        rows, checks = [], []
        n_case = 0
        seen = {}

        def workday(d):
            while d.weekday() == 6:                     # no interviews on Sundays
                d += dt.timedelta(days=1)
            return d

        for code in [v[0] for v in P.VERSIONS if v[2] == "FLR"]:
            v = R[R.version == code].reset_index(drop=True)
            interviewers = ["I%03d" % int(x) for x in rng.choice(np.arange(101, 190), size=9, replace=False)]
            reissued = {int(x) for x in v.case.dropna()}
            case_of, int_of, check_of, day_of = {}, {}, {}, {}
            for j, r in v.iterrows():
                if r.kind in ("replacement", "revisit"):
                    u = int(r.case)
                    iid = case_of[u]
                    after = check_of[u] if r.kind == "replacement" else day_of[u] + dt.timedelta(days=1)
                    day = workday(after + dt.timedelta(days=int(rng.integers(2, 6))))
                    assert day <= end, (code, j)
                    who = [x for x in interviewers if x != int_of[u]][int(rng.integers(0, 8))]
                else:
                    n_case += int(rng.integers(1, 4))
                    iid = "FLR-%s-%05d" % (code.upper(), 10000 + n_case)
                    if r.kind == "pretest":
                        day = workday(tstart + dt.timedelta(days=int(rng.integers(0, tdays))))
                    elif j in reissued:
                        day = workday(start + dt.timedelta(days=int(rng.integers(0, pdays - 14))))
                    else:
                        day = start + dt.timedelta(days=int(rng.integers(0, pdays)))
                        day = workday(day) if workday(day) <= end else workday(day - dt.timedelta(days=2))
                    who = interviewers[int(rng.integers(0, 9))]
                    if r.kind == "valid":
                        seen[j] = who
                    elif r.kind == "unconfirmed":           # copied from one of the interviewer's own interviews
                        who = seen[int(r.of)]
                case_of[j], int_of[j], day_of[j] = iid, who, day
                age = self.age(rng, "FLR")
                back = [2 if rng.random() < 0.53 else 1, int(np.clip(rng.poisson(2.4) + 1, 1, 9)), 0]
                back[2] = int(min(age - 1, np.round(rng.gamma(2.4, 8.0))))
                answers = self.raw_answers(r.X, r.miss, lambda i: int(rng.choice([-8, -9], p=[.7, .3])))
                result, reached, nback = 1, 12, 3
                if r.kind == "past":
                    result, nback = 2, int(r.leave)
                elif r.kind == "inside":
                    result, reached, nback = 2, int(r.stop), 0
                base = dict(case_id=iid, version=code, interviewer_id=who, interview_date=day.isoformat())
                rows.append(dict(base, variable="RESULT", value=result))
                rows.append(dict(base, variable="AGE", value=age))
                for c, a in list(zip(CODES, answers))[:reached]:
                    rows.append(dict(base, variable=c, value=a))
                for c, a in list(zip(self.BACKGROUND, back))[:nback]:
                    rows.append(dict(base, variable=c, value=a))
                # the vendor's back-check: a quarter of the pilot interviews, by phone or a revisit
                if r.kind == "unconfirmed" or (r.kind in ("valid", "past", "inside") and rng.random() < P.BACKCHECKED):
                    out = "not confirmed" if r.kind == "unconfirmed" else (
                        "not reached" if rng.random() < P.NOT_REACHED else "confirmed")
                    bday = day + dt.timedelta(days=int(rng.integers(2, 7)))
                    check_of[j] = bday
                    checks.append(dict(case_id=iid, version=code, interviewer_id=who, backcheck_date=bday.isoformat(),
                                       method=str(rng.choice(["phone", "revisit"], p=[.8, .2])), outcome=out))
        df = pd.DataFrame(rows)
        bc = pd.DataFrame(checks).sort_values(["backcheck_date", "case_id"]).reset_index(drop=True)
        return df.sort_values(["interview_date", "case_id", "interviewer_id"], kind="stable").reset_index(drop=True), bc

    # ------------------------------------------------------------------ the translation register
    NOTES = {
        "pa": "Item 5: 'neighbourhood' rendered with the word used in the Gurmukhi press for one's local area.",
        "zh-Hans": "Item 9 back-translation queried ('welcome' read as 'greeted'); reconciled with the reviewer.",
        "yue": "Interviewer script written in standard Chinese characters, read aloud in Cantonese; item 3 idiom adapted.",
        "tl": "Taglish kept for 'community' (komunidad) after the review panel's preference.",
        "ar": "Modern Standard Arabic; item 11 'advice' (nasiha) checked with the community advisory group.",
        "es": "Neutral Latin American Spanish; item 8 'share my interests' adapted ('compartir mis intereses').",
        "ur": "Item 1 'close to' reconciled between two forward translations; Nastaliq rendering checked on paper cards.",
        "vi": "Diacritics checked on the panel's mobile layout; item 5 'neighbourhood' (khu pho) agreed.",
        "fa": "Item 12 reviewed for formal register; right-to-left layout checked on mobile.",
        "ko": "Honorific register kept throughout; item 3 back-translation reconciled.",
    }

    def register(self):
        rng = self._stream(3)
        names = ["A. Grewal", "M. Chen", "W. Lam", "R. Santos", "H. Haddad", "L. Morales", "S. Qureshi", "T. Nguyen",
                 "N. Rahimi", "J. Park", "K. Dhillon", "Y. Zhou", "C. Wong", "E. Reyes", "F. Mansour", "D. Ortega",
                 "Z. Iqbal", "P. Tran", "B. Karimi", "S. Lee"]
        rows = []
        for k, (code, lang, vendor, *_ ) in enumerate(P.VERSIONS):
            start, end = P.PILOT[vendor]
            fwd = "%s; %s" % (names[k], names[(k + 10) % 20])
            back = dt.date(2026, 11, 2) + dt.timedelta(days=int(rng.integers(0, 21)))
            rec = back + dt.timedelta(days=int(rng.integers(6, 15)))
            pre = ("%s to %s" % (P.PRETEST[0].isoformat(), P.PRETEST[1].isoformat())) if vendor == "FLR" else ""
            rows.append(dict(version=code, language=lang, mode=P.VENDORS[vendor][1], vendor=P.VENDORS[vendor][0],
                             forward_translators=fwd, back_translation_reviewed=back.isoformat(),
                             reconciled=rec.isoformat(), pretest=pre, pilot_start=start.isoformat(),
                             pilot_end=end.isoformat(), note=self.NOTES[code]))
        return pd.DataFrame(rows)

    # ------------------------------------------------------------------ a neighbouring file the analysis does not use
    REGIONS = [("Capital", 2104), ("Lakeshore", 1588), ("North Woods", 812), ("Prairie South", 1240), ("River Valley", 1376),
               ("Eastern Shield", 655), ("Western Plains", 931)]

    def wave5(self):
        rng = self._stream(4)
        rows = []
        for name, n in self.REGIONS:
            for lang, share in (("English", 0.86), ("French", 0.14)):
                m = int(round(n * share * float(rng.uniform(0.9, 1.1))))
                mean = float(rng.normal(44.2 if lang == "English" else 43.6, 0.9))
                sd = float(rng.uniform(7.4, 8.6))
                rows.append(dict(region=name, version=lang, respondents=m, mean_score=round(mean, 1),
                                 std_error=round(sd / np.sqrt(m), 2)))
        return pd.DataFrame(rows)
