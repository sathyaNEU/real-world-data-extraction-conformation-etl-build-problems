"""task464 architecture 9: the clean truth.

One chronological event queue for the whole network. A patient's repeat medicines are requested together and sit
on one authorisation set: every repeat in the set was authorised on the same day for the same number of issues,
so they run out together, and the request after the last authorised issue (or, at a practice that reviews in
fixed months, the first request in a review month) waits for a review that re-authorises the whole set. A patient
who does not get the review stops every repeat. Stops between reviews come one medicine at a time.

Two practices re-authorised large parts of their lists in 2026 without a review: Marrick House moved its stable
repeat patients to 56-day issues (six issues), and Fennbridge switched its simvastatin patients to atorvastatin.
A repeat that ran out during either drive was reviewed as usual and re-authorised on the new terms.

The review outcomes and the stops are drawn by systematic sampling within each practice, in time order, so every
practice's measured rates sit at the network's (closure C1 in the design note). No patient leaves a list between
a repeat set's last authorised issue and 130 days after its review, so a rate measured with or without the
patients who left is the same rate. Each patient draws from a stream keyed on the seed, the practice, the cohort
and the patient's place in it, so one parameter changed does not re-draw the rest of the world.
"""
import heapq, hashlib
import numpy as np
import world as W

SEED = 46906


class Sys:
    """Systematic Bernoulli: fires once every 1/p calls from a random phase."""
    def __init__(self, p, phase):
        self.p = p; self.acc = phase

    def __call__(self, scale=1.0):
        self.acc += self.p * scale
        if self.acc >= 1.0:
            self.acc -= 1.0
            return True
        return False


def lateness(rng, extra=(0, 0)):
    base = _lateness(rng)
    if extra[1] > 0 and base >= 0:
        base += int(rng.integers(extra[0], extra[1] + 1))
    return base


def _lateness(rng):
    u = rng.random()
    if u < 0.34: return -int(rng.integers(1, 8))
    if u < 0.82: return int(rng.integers(0, 4))
    if u < 0.985: return int(rng.integers(4, 13))
    return int(rng.integers(13, 26))


def month(t):
    return W.date_of(t).month


def pseudo(*parts):
    return hashlib.sha1(("hv9-%d-" % SEED + "-".join(str(p) for p in parts)).encode()).hexdigest()[:10].upper()


def eps_id(rng):
    hx = "".join("0123456789ABCDEF"[int(x)] for x in rng.integers(0, 16, 6))
    mid = "".join("0123456789ABCDEFGHJKLMNPQRSTUVWXYZ"[int(x)] for x in rng.integers(0, 34, 6))
    tail = "%05d" % int(rng.integers(0, 100000))
    chk = "0123456789ABCDEFGHJKLMNPQRSTUVWXYZ+"[int(rng.integers(0, 35))]
    return "%s-%s-%s%s" % (hx, mid, tail, chk)


class World:
    def __init__(self, seed=SEED):
        global SEED
        SEED = seed
        self.seed = seed
        self.patients = {}      # pid -> dict
        self.templates = []     # dicts
        self.issues = []        # dicts
        self.events = []        # dicts
        self.cancellations = []
        self.edits = []         # template change log rows
        self.heap = []
        self.seq = 0
        # one sampler per practice and cohort for reviews, per practice and medicine for stops, so the statin
        # patients' own rates are exact in time and by practice
        self.samplers = {}
        for i, p in enumerate(W.PRACTICES):
            r = np.random.default_rng([seed, i, 999])
            sm = {}
            for c in ("statin", "statin-pre", "raas", "other"):
                sm["fail", c] = Sys(W.Q_FAIL, r.random())
            for slot in ("statin", "raas", "doac", "clop"):
                sm["bge", slot] = Sys(W.BG_EARLY, r.random()); sm["bgl", slot] = Sys(W.BG_LATE, r.random())
            self.samplers[p["key"]] = sm
        self.hurdles = []       # (pid, practice, t, failed) for checks

    # ------------------------------------------------------------------ scheduling
    def push(self, t, pid, kind, arg=None):
        self.seq += 1
        heapq.heappush(self.heap, (int(t), self.seq, pid, kind, arg))

    # ------------------------------------------------------------------ patients
    def new_patient(self, key, cohort, idx, start, rng):
        pid = pseudo(key, cohort, idx)
        yob = int(rng.integers(1928, 1986)) if cohort == "statin" else int(rng.integers(1930, 1990))
        reg_from = start - int(rng.integers(30, 9000))
        reg_from = max(reg_from, W.day("%d-06-01" % (yob + 17)))
        if rng.random() < 0.08:
            reg_from = start - int(rng.integers(20, 300))
        reg_end = max(start, W.SIM_START) + int(rng.exponential(365.0 / W.DEREG_Y))
        u = rng.random(); acc = 0.0; extra = (0, 0)
        for share, lo, hi in W.LATE_TYPES:
            acc += share
            if u < acc:
                extra = (lo, hi); break
        P = dict(pid=pid, key=key, cohort=cohort, rng=rng, yob=yob, sex="F" if rng.random() < 0.47 else "M", extra=extra,
                 episodes=[[key, reg_from, None, None]], reg_end=reg_end, meds={}, set=None, last_req=None,
                 alive=True, eligible_drive=False, drive_done=False, lapsed=False, move_at=None)
        dr = W.BY_KEY[key]["drive"]
        P["eligible_drive"] = bool(dr) and rng.random() < dr[3]
        if rng.random() < 1 - np.exp(-W.MOVE_Y * 12):
            P["move_at"] = max(start, W.SIM_START) + int(rng.integers(30, 4400))
        P["own"] = None
        if cohort == "raas":
            # a patient on an ACE inhibitor or ARB alone may have their own issue length
            cfg = W.BY_KEY[key]; u = rng.random(); acc = 0.0
            for share, L in W.OWN_LENGTH[cfg["L"]]:
                acc += share
                if u < acc:
                    P["own"] = (L, max(2, int(round(cfg["M"] * cfg["L"] / L)))); break
        self.patients[pid] = P
        return P

    def statin_choice(self, P, start):
        rng = P["rng"]
        col = 3 if start >= W.day("2025-01-01") else 2
        w = np.array([s[col] for s in W.STATINS]); w = w / w.sum()
        d, s = W.STATINS[int(rng.choice(len(W.STATINS), p=w))][:2]
        return dict(slot="statin", drug=d, strength=s, form="tablets", doses=1,
                    directions=W.DIRECTIONS_NIGHT[int(rng.integers(0, len(W.DIRECTIONS_NIGHT)))]
                    if d != "Atorvastatin" or rng.random() < 0.5 else W.DIRECTIONS_ONE[int(rng.integers(0, 5))])

    def raas_choice(self, P):
        rng = P["rng"]
        w = np.array([a[3] for a in W.ACE_ARB]); w = w / w.sum()
        d, s, f, _ = W.ACE_ARB[int(rng.choice(len(W.ACE_ARB), p=w))]
        two = rng.random() < 0.12
        dirs = (W.DIRECTIONS_TWO if two else W.DIRECTIONS_ONE)
        return dict(slot="raas", drug=d, strength=s, form=f, doses=2 if two else 1,
                    directions=dirs[int(rng.integers(0, len(dirs)))])

    def doac_choice(self, P):
        rng = P["rng"]
        w = np.array([a[3] for a in W.DOACS]); w = w / w.sum()
        d, s, doses, _ = W.DOACS[int(rng.choice(len(W.DOACS), p=w))]
        dirs = W.DIRECTIONS_BD if doses == 2 else W.DIRECTIONS_ONE
        return dict(slot="doac", drug=d, strength=s, form="tablets", doses=doses,
                    directions=dirs[int(rng.integers(0, len(dirs)))])

    # ------------------------------------------------------------------ templates and issues
    def open_template(self, P, med, t, M, course=False):
        cfg = W.BY_KEY[P["key"]]
        L = P["set"]["L"] if P["set"] else cfg["L"]
        tp = dict(tid=len(self.templates), pid=P["pid"], key=P["key"], slot=med["slot"], drug=med["drug"],
                  strength=med["strength"], form=med["form"], directions=med["directions"], doses=med["doses"],
                  qty=L * med["doses"], L=L, M=M, authorised=t, ended=None, end_reason=None, made=0,
                  course=course, last=None)
        self.templates.append(tp)
        med["tid"] = tp["tid"]
        return tp

    def end_template(self, med, t, why):
        if med.get("tid") is None: return
        tp = self.templates[med["tid"]]
        if tp["ended"] is None:
            tp["ended"] = t; tp["end_reason"] = why

    def issue(self, P, med, t, token, acute=False):
        rng = P["rng"]
        if acute:
            qty = 28 * med["doses"]; tid = None
        else:
            tp = self.templates[med["tid"]]
            tp["made"] += 1; tp["last"] = t
            qty = tp["qty"]; tid = tp["tid"]
        if t < W.KEEP_FROM:
            return
        row = dict(pid=P["pid"], key=P["key"], t=t, tid=tid, slot=med["slot"], drug=med["drug"],
                   strength=med["strength"], form=med["form"], qty=qty, doses=med["doses"], eps=token,
                   acute=acute, cancelled=False, twin=False, reissue=False, directions=med["directions"])
        self.issues.append(row)
        # Ask A's hazards, on the renin-angiotensin repeats only: an out-of-stock line cancelled and re-sent to
        # another pharmacy, and the odd duplicate request that was dispensed twice.
        if med["slot"] in ("raas", "doac") and not acute:
            if med["slot"] == "raas":
                for drug, a, b in W.SHORTAGES:
                    if med["drug"] == drug and W.day(a) <= t <= W.day(b) and rng.random() < W.REISSUE_P:
                        row["cancelled"] = True
                        t2 = t + 1 + int(rng.integers(0, 4))
                        tok2 = eps_id(rng)
                        self.cancellations.append(dict(token=token, pid=P["pid"], key=P["key"], t=t, drug=med["drug"],
                                                       strength=med["strength"], form=med["form"], qty=qty,
                                                       cancelled_on=t + int(rng.integers(0, 2)),
                                                       reason="Item not available at nominated pharmacy"))
                        r2 = dict(row); r2.update(t=t2, eps=tok2, cancelled=False, reissue=True)
                        self.issues.append(r2)
                        tp = self.templates[med["tid"]]; tp["last"] = t2
                        break
            if rng.random() < W.TWIN_P:
                r3 = dict(row); r3.update(t=t + int(rng.integers(0, 6)), eps=eps_id(rng), cancelled=False, twin=True)
                self.issues.append(r3)

    def issue_all(self, P, t):
        token = eps_id(P["rng"])
        n = 0
        for slot in ("statin", "raas", "doac", "p2y12", "clop"):
            med = P["meds"].get(slot)
            if med and med["active"] and med.get("tid") is not None:
                if n and n % 4 == 0:
                    token = eps_id(P["rng"])
                self.issue(P, med, t, token)
                n += 1
                if med.get("course"):
                    med["course_used"] += 1
        P["last_req"] = t

    def new_set(self, P, t, L=None, M=None):
        cfg = W.BY_KEY[P["key"]]
        own = P.get("own") if not (P["set"] and P["set"].get("keepL")) else None
        L = L or (P["set"]["L"] if (P["set"] and P["set"].get("keepL")) else (own[0] if own else cfg["L"]))
        M = M or (P["set"]["M"] if (P["set"] and P["set"].get("keepL")) else (own[1] if own else cfg["M"]))
        keep = bool(P["set"] and P["set"].get("keepL"))
        P["set"] = dict(L=L, M=M, used=0, start=t, keepL=keep)
        for slot, med in P["meds"].items():
            if med["active"] and not med.get("course"):
                self.end_template(med, t, "reauthorised")
                self.open_template(P, med, t, M)
            elif med["active"] and med.get("course") and med.get("tid") is not None \
                    and self.templates[med["tid"]]["ended"] is not None:
                left = med["course_M"] - med["course_used"]
                if left > 0:
                    med["course_M"] = left; med["course_used"] = 0
                    self.open_template(P, med, t, left, course=True)
                else:
                    med["active"] = False

    # ------------------------------------------------------------------ the event loop
    def run(self):
        while self.heap:
            t, _, pid, kind, arg = heapq.heappop(self.heap)
            P = self.patients[pid]
            if not P["alive"]:
                continue
            if t > min(P["reg_end"], W.OUT + 40):
                self.leave(P, min(P["reg_end"], W.OUT + 40))
                continue
            getattr(self, "on_" + kind)(P, t, arg)

    def leave(self, P, t):
        P["alive"] = False
        for med in P["meds"].values():
            if med["active"]:
                med["active"] = False
                self.end_template(med, t, "left")
        if P["reg_end"] <= W.OUT + 40:
            ep = P["episodes"][-1]
            if ep[2] is None:
                ep[2] = P["reg_end"]; ep[3] = "death" if P["rng"].random() < 0.55 else "left"

    def schedule_next(self, P, t):
        rng = P["rng"]
        nxt = t + P["set"]["L"] + lateness(rng, P["extra"])
        # moves and heart attacks interrupt the request clock
        if P["move_at"] is not None and t < P["move_at"] <= nxt:
            self.push(P["move_at"], P["pid"], "move"); P["move_at"] = None; return
        if P.get("mi_at") is not None and t < P["mi_at"] <= nxt:
            self.push(P["mi_at"], P["pid"], "mi"); P["mi_at"] = None; return
        if P.get("titrate_at") is not None and t < P["titrate_at"] <= nxt:
            self.push(P["titrate_at"], P["pid"], "titrate")
            P["titrate_at"] = None
        self.push(nxt, P["pid"], "req")

    def protect(self, P, t):
        """No deregistration from a set's last authorised issue to 130 days after its review."""
        if t - 1 <= P["reg_end"] <= t + P["set"]["L"] + 130:
            P["reg_end"] = t + P["set"]["L"] + 131 + int(P["rng"].integers(0, 60))

    def near_review(self, P, t):
        cfg = W.BY_KEY[P["key"]]; s = P["set"]
        if s["used"] >= s["M"]: return True
        sea = cfg["season"]
        return bool(sea) and month(t + s["L"]) in sea and month(t) not in sea

    def on_start(self, P, t, arg):
        """A cohort member's first appearance: either a new start (acute statin first) or a prevalent patient."""
        rng = P["rng"]
        cfg = W.BY_KEY[P["key"]]
        prevalent = arg == "prevalent"
        meds = {}
        if P["cohort"] == "statin":
            meds["statin"] = self.statin_choice(P, t)
            if rng.random() < 0.50: meds["raas"] = self.raas_choice(P)
            if rng.random() < 0.09: meds["doac"] = self.doac_choice(P)
            if rng.random() < 0.04:
                meds["clop"] = dict(slot="clop", drug="Clopidogrel", strength="75mg", form="tablets", doses=1,
                                    directions=W.DIRECTIONS_ONE[int(rng.integers(0, 5))])
        else:
            meds["raas"] = self.raas_choice(P)
            if rng.random() < 0.05: meds["doac"] = self.doac_choice(P)
        for m in meds.values():
            m["active"] = True; m["since"] = t if not prevalent else t - int(rng.integers(200, 3000)); m["tid"] = None
        P["meds"] = meds
        P["set"] = dict(L=cfg["L"], M=cfg["M"], used=0, start=t, keepL=False)
        if prevalent:
            # a random point inside a running set
            for m in meds.values():
                self.open_template(P, m, t - int(rng.integers(0, cfg["L"] * cfg["M"])), cfg["M"])
            P["set"]["used"] = int(rng.integers(0, cfg["M"]))
            for m in meds.values():
                self.templates[m["tid"]]["made"] = P["set"]["used"]
            P["last_req"] = t
            self.schedule_next(P, t)
            return
        # a new start: the statin's first prescription is an acute issue, the repeat follows at the next request
        if P["cohort"] == "statin":
            st = meds["statin"]
            token = eps_id(rng)
            self.issue(P, st, t, token, acute=True)
            P["pending_statin"] = True
            P["last_req"] = t
            self.push(t + 28 + lateness(rng, P["extra"]), P["pid"], "req")
            return
        self.new_set(P, t)
        self.issue_all(P, t)
        self.schedule_next(P, t)

    def on_req(self, P, t, arg):
        rng = P["rng"]
        key = P["key"]; cfg = W.BY_KEY[key]; smp = self.samplers[key]
        s = P["set"]
        if P.pop("pending_statin", False):
            # the statin repeat is added to the set for the issues the set has left
            st = P["meds"]["statin"]
            others = [m for k, m in P["meds"].items() if k != "statin" and m["active"] and m.get("tid") is not None]
            if others and s["used"] > 0 and s["used"] < s["M"]:
                self.open_template(P, st, t, s["M"] - s["used"])
                self.templates[st["tid"]]["M_set"] = s["M"]
            else:
                self.new_set(P, t)
            self.issue_all(P, t); s = P["set"]; s["used"] += 1
            if self.near_review(P, t): self.protect(P, t)
            self.schedule_next(P, t)
            return
        sea = cfg["season"]
        at_review = s["used"] >= s["M"] or (bool(sea) and month(t) in sea and month(P["last_req"]) not in sea)
        # stops between reviews, one medicine at a time (a request that meets a review is the review's outcome)
        for slot, med in list(P["meds"].items()):
            if at_review: break
            if not med["active"] or med.get("course"): continue
            age = t - med["since"]
            hit = smp["bge", slot](s["L"] / 28) if age < 182 else smp["bgl", slot](s["L"] / 28)
            if hit:
                med["active"] = False
                self.end_template(med, t, "stopped")
                if slot == "statin" and rng.random() < W.RETURN:
                    self.push(t + int(rng.integers(W.RET_MIN, W.RET_MAX)), P["pid"], "restart", "statin")
        if not any(m["active"] for m in P["meds"].values()):
            P["alive_meds"] = False
            return
        # a 2026 drive re-authorises the whole set without a review, unless the set has run out
        dr = cfg["drive"]
        in_drive = bool(dr) and P["eligible_drive"] and not P["drive_done"] and W.day(dr[1]) <= t <= W.day(dr[2])
        if in_drive and dr[0] == "switch":
            st = P["meds"].get("statin")
            in_drive = bool(st and st["active"] and st["drug"] == "Simvastatin")
        sea = cfg["season"]
        hurdle = s["used"] >= s["M"] or (bool(sea) and month(t) in sea and month(P["last_req"]) not in sea)
        if in_drive and not hurdle:
            P["drive_done"] = True
            if dr[0] == "length":
                P["set"]["keepL"] = True
                self.drive_length(P, t)
            else:
                st = P["meds"]["statin"]
                if rng.random() < W.SWITCH_STOP:
                    st["active"] = False; self.end_template(st, t, "stopped")
                else:
                    self.end_template(st, t, "switched")
                    st.update(drug="Atorvastatin", strength="20mg", directions=W.DIRECTIONS_NIGHT[int(rng.integers(0, 5))])
                self.new_set(P, t)
            self.issue_all(P, t); P["set"]["used"] += 1
            self.schedule_next(P, t)
            return
        if hurdle:
            self.protect(P, t)
            st_on = P["meds"].get("statin") and P["meds"]["statin"]["active"]
            if P["cohort"] == "statin" and st_on:
                # a repeat authorised before the extracts start reviews on its own stream, so the rate over the
                # repeats the extracts see in full is exact in every window and at every practice
                tid = P["meds"]["statin"].get("tid")
                pre = tid is None or self.templates[tid]["authorised"] < W.EXTRACT_FROM
                stream = "statin-pre" if pre else "statin"
            else:
                stream = "raas" if P["cohort"] == "raas" else "other"
            failed = smp["fail", stream]()
            self.hurdles.append((P["pid"], key, t, failed))
            if failed:
                P["lapsed"] = True
                for med in P["meds"].values():
                    if med["active"]:
                        med["active"] = False; self.end_template(med, t, "review not done")
                if rng.random() < W.RETURN:
                    self.push(t + int(rng.integers(W.RET_MIN, W.RET_MAX)), P["pid"], "restart", "all")
                return
            if in_drive:
                P["drive_done"] = True
                if dr[0] == "length": P["set"]["keepL"] = True
                if dr[0] == "switch":
                    st = P["meds"]["statin"]
                    self.end_template(st, t, "switched")
                    st.update(drug="Atorvastatin", strength="20mg", directions=W.DIRECTIONS_NIGHT[int(rng.integers(0, 5))])
            self.push(t + 1 + int(rng.gamma(2.0, 2.5)), P["pid"], "reauth", "length" if (in_drive and dr[0] == "length") else None)
            return
        self.issue_all(P, t); s["used"] += 1
        self.after_issue(P, t)
        if self.near_review(P, t): self.protect(P, t)
        self.schedule_next(P, t)

    def after_issue(self, P, t):
        """A fixed ticagrelor course ends after its thirteenth GP issue."""
        tic = P["meds"].get("p2y12")
        if not (tic and tic["active"] and tic.get("course")): return
        if tic["course_used"] < tic["course_M"]: return
        rng = P["rng"]
        stage = tic.get("stage", "first")
        if stage == "first":
            u = rng.random()
            if u < W.TICAG_OVERRUN:
                self.end_template(tic, t, "reauthorised")
                tic["stage"] = "overrun"; tic["course_used"] = 0
                tic["course_M"] = max(1, int(rng.integers(3, 9)) * 28 // P["set"]["L"])
                self.open_template(P, tic, t + 1, tic["course_M"], course=True)
                return
            if u < W.TICAG_OVERRUN + W.TICAG_PEGASUS:
                self.end_template(tic, t, "changed")
                cm = 13 if P["set"]["L"] == 28 else 6
                tic.update(strength="60mg", stage="pegasus", course_M=cm, course_used=0)
                self.open_template(P, tic, t + 1, cm, course=True)
                return
        tic["active"] = False
        self.end_template(tic, t, "course complete")

    def drive_length(self, P, t):
        self.new_set(P, t, L=56, M=6)
        for med in P["meds"].values():
            if med["active"] and not med.get("course"):
                self.templates[med["tid"]]["qty"] = 56 * med["doses"]
        P["set"]["keepL"] = True

    def on_reauth(self, P, t, arg):
        if arg == "length":
            self.drive_length(P, t)
        else:
            self.new_set(P, t)
        self.issue_all(P, t); P["set"]["used"] += 1
        self.after_issue(P, t)
        self.schedule_next(P, t)

    def on_restart(self, P, t, arg):
        rng = P["rng"]
        P["lapsed"] = False
        if arg == "statin":
            st = P["meds"]["statin"]; st["active"] = True; st["since"] = t
            chain = any(m["active"] for k, m in P["meds"].items() if k != "statin")
            self.issue(P, st, t, eps_id(rng), acute=True)
            P["pending_statin"] = True
            if not chain:
                # nothing else on repeat, so the restart opens the patient's request clock again
                self.push(t + 28 + lateness(rng, P["extra"]), P["pid"], "req")
            return
        for slot, med in P["meds"].items():
            if not med.get("course"):
                med["active"] = True; med["since"] = t
        P["set"]["keepL"] = P["set"].get("keepL", False)
        self.new_set(P, t)
        self.issue_all(P, t); P["set"]["used"] += 1
        self.schedule_next(P, t)

    def on_move(self, P, t, arg):
        """A move to another network practice: the new practice re-authorises the patient's repeats."""
        rng = P["rng"]
        others = [p["key"] for p in W.PRACTICES if p["key"] != P["key"]]
        new = others[int(rng.integers(0, len(others)))]
        ep = P["episodes"][-1]; ep[2] = t; ep[3] = "transferred"
        t2 = t + int(rng.integers(2, 15))
        P["episodes"].append([new, t2, None, None])
        for med in P["meds"].values():
            if med["active"]: self.end_template(med, t, "transferred")
        P["key"] = new
        P["set"]["keepL"] = False
        if not any(m["active"] for m in P["meds"].values()):
            return
        self.push(t2 + int(rng.integers(3, 20)), P["pid"], "reauth", None)

    def on_titrate(self, P, t, arg):
        """Ask A: an ACE inhibitor or ARB's directions edited in place on the repeat (same product)."""
        med = P["meds"].get("raas")
        if not (med and med["active"] and med.get("tid") is not None): return
        tp = self.templates[med["tid"]]
        rng = P["rng"]
        if med["doses"] == 1:
            nd, ndir = 2, W.DIRECTIONS_TWO[int(rng.integers(0, len(W.DIRECTIONS_TWO)))]
        else:
            nd, ndir = 1, W.DIRECTIONS_ONE[int(rng.integers(0, len(W.DIRECTIONS_ONE)))]
        old_dir, old_q = tp["directions"], tp["qty"]
        med["doses"] = nd; med["directions"] = ndir
        tp["doses"] = nd; tp["directions"] = ndir; tp["qty"] = tp["L"] * nd
        who = "GP" if rng.random() < 0.7 else "Clinical pharmacist"
        stamp = t
        self.edits.append(dict(tid=tp["tid"], pid=P["pid"], key=P["key"], t=stamp, field="Dosage", old=old_dir, new=ndir, by=who))
        self.edits.append(dict(tid=tp["tid"], pid=P["pid"], key=P["key"], t=stamp, field="Quantity", old=str(old_q), new=str(tp["qty"]), by=who))

    def on_mi(self, P, t, arg):
        """Ask B: a heart attack. Ticagrelor 90mg twice a day starts in hospital; the GP repeat follows discharge."""
        rng = P["rng"]
        st = P["meds"].get("statin")
        admit = t; start = t + int(rng.integers(0, 2)); dis = t + int(rng.integers(3, 9))
        filed = dis + int(rng.integers(2, 21))
        self.events.append(dict(pid=P["pid"], key=P["key"], t=admit, code="22298006", term="Myocardial infarction",
                                value="", unit="", source="Discharge summary", filed=filed))
        self.events.append(dict(pid=P["pid"], key=P["key"], t=start, code="1290071000000109",
                                term="Ticagrelor 90mg twice daily started in secondary care", value="", unit="",
                                source="Discharge summary", filed=filed))
        self.events.append(dict(pid=P["pid"], key=P["key"], t=dis, code="58000006", term="Patient discharge",
                                value="", unit="", source="Discharge summary", filed=filed))
        L = P["set"]["L"]
        P["meds"]["p2y12"] = dict(slot="p2y12", drug="Ticagrelor", strength="90mg", form="tablets", doses=2,
                                  directions=W.DIRECTIONS_BD[int(rng.integers(0, len(W.DIRECTIONS_BD)))],
                                  active=True, since=start, tid=None, course=True,
                                  course_M=W.TICAGRELOR_ISSUES if L == 28 else 7,
                                  course_used=0, stage="first", hospital_start=start)
        if st:
            if st["active"]:
                self.end_template(st, t, "changed in hospital")
            st.update(drug="Atorvastatin", strength="80mg", active=True, since=start,
                      directions=W.DIRECTIONS_NIGHT[int(rng.integers(0, 5))])
        supply = int(rng.choice(W.DISCHARGE_SUPPLY))
        first = dis + supply - int(rng.integers(0, 5))
        self.push(first, P["pid"], "postmi")

    def on_postmi(self, P, t, arg):
        tic = P["meds"]["p2y12"]
        P["set"]["keepL"] = P["set"].get("keepL", False)
        self.new_set(P, t)
        self.open_template(P, tic, t, tic["course_M"], course=True)
        self.issue_all(P, t); P["set"]["used"] += 1
        self.schedule_next(P, t)


def simulate(seed=SEED):
    w = World(seed)
    for i, p in enumerate(W.PRACTICES):
        k = p["key"]
        # statin cohort: prevalent at the start of the simulation, then new starts through to the outcome date
        n0 = int(p["n"])
        for j in range(n0):
            rng = np.random.default_rng([seed, i, 1, j])
            st = W.SIM_START - int(rng.integers(1, 3000))
            P = w.new_patient(k, "statin", j, st, rng)
            w.push(W.SIM_START + int(rng.integers(0, 60)), P["pid"], "start", "prevalent")
            if rng.random() < 1 - np.exp(-W.MI_Y * (W.OUT - W.SIM_START) / 365):
                P["mi_at"] = W.SIM_START + int(rng.integers(30, W.OUT - W.SIM_START))
        lam = p["n"] * p["incid"] / 365.0
        r0 = np.random.default_rng([seed, i, 2])
        t = W.SIM_START; j = 0
        while True:
            t += int(r0.exponential(1.0 / lam)) + 1
            if t > W.OUT: break
            rng = np.random.default_rng([seed, i, 3, j])
            P = w.new_patient(k, "statin", 100000 + j, t, rng)
            w.push(t, P["pid"], "start", "new")
            if rng.random() < 1 - np.exp(-W.MI_Y * (W.OUT - t) / 365):
                P["mi_at"] = t + int(rng.integers(60, max(61, W.OUT - t)))
            j += 1
        # renin-angiotensin patients not on a statin
        nr = int(p["n"] * 0.32)
        for j in range(nr):
            rng = np.random.default_rng([seed, i, 4, j])
            P = w.new_patient(k, "raas", j, W.SIM_START - int(rng.integers(1, 2500)), rng)
            w.push(W.SIM_START + int(rng.integers(0, 60)), P["pid"], "start", "prevalent")
        r1 = np.random.default_rng([seed, i, 5]); t = W.SIM_START; j = 0
        lam2 = p["n"] * 0.32 * 0.12 / 365.0
        while True:
            t += int(r1.exponential(1.0 / lam2)) + 1
            if t > W.OUT: break
            rng = np.random.default_rng([seed, i, 6, j])
            P = w.new_patient(k, "raas", 100000 + j, t, rng)
            w.push(t, P["pid"], "start", "new")
            j += 1
    # Ask A's titrations: drawn per patient, placed in 2025
    for pid, P in w.patients.items():
        rng = np.random.default_rng([seed, 77, int(pid[:8], 16) % 100000007])
        if rng.random() < W.TITRATE_2025:
            P["titrate_at"] = W.day("2025-01-20") + int(rng.integers(0, 300))
    w.run()
    return w


if __name__ == "__main__":
    import time, collections
    t0 = time.time()
    w = simulate()
    print("patients", len(w.patients), "templates", len(w.templates), "issues", len(w.issues),
          "events", len(w.events), "cancellations", len(w.cancellations), "edits", len(w.edits),
          "%.1fs" % (time.time() - t0))
    ext = [r for r in w.issues if W.EXTRACT_FROM <= r["t"] <= W.ASOF]
    print("issues in extract", len(ext), collections.Counter(r["slot"] for r in ext))


def current_population(w):
    """Patients registered on ASOF with a statin issued from POP_FROM to ASOF, by practice (truth view)."""
    import collections
    reg = {}
    for pid, P in w.patients.items():
        for k, a, b, why in P["episodes"]:
            if a <= W.ASOF and (b is None or b > W.ASOF):
                reg[pid] = k
    got = set()
    for r in w.issues:
        if r["slot"] == "statin" and W.POP_FROM <= r["t"] <= W.ASOF and not r["cancelled"]:
            if reg.get(r["pid"]) == r["key"]:
                got.add(r["pid"])
    return collections.Counter(reg[p] for p in got)
