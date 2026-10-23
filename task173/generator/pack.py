"""task173 pack: the exports the planner's folder holds, written from the world with the mess each system makes.

Each writer returns its row count. Text documents are in docs.py."""
from __future__ import annotations

import datetime as dt
import os

import numpy as np

import common as C
import xlsx_writer as XW
from world import D0, T_END

SUFFIX_LONG = {"ST": "STREET", "AVE": "AVENUE", "DR": "DRIVE", "LN": "LANE", "CT": "COURT", "TRL": "TRAIL",
               "RD": "ROAD", "BLVD": "BOULEVARD", "CIR": "CIRCLE", "PL": "PLACE", "WAY": "WAY", "PKWY": "PARKWAY",
               "LOOP": "LOOP", "PASS": "PASS"}
MAT_NEW = {"CU": "CU", "GALV": "GALV", "PB": "PB", "PE": "PE"}
MAT_OLD = {"CU": "C", "GALV": "G", "PB": "B", "PE": "P"}
ITEMS = {"0410": ("ASPHALT PAVEMENT PATCH, FULL DEPTH", "SY", 68.50),
         "0420": ("CONCRETE PAVEMENT REPLACEMENT, 8 IN", "SY", 112.00),
         "0430": ("CONCRETE SIDEWALK, 4 IN", "SY", 74.25),
         "0431": ("CONCRETE DRIVEWAY, 6 IN", "SY", 92.40),
         "0440": ("SOLID SOD, ST AUGUSTINE OR BERMUDA TO MATCH", "SY", 9.35),
         "0450": ("CONCRETE CURB AND GUTTER", "LF", 38.10),
         "0460": ("SAW CUT, PAVEMENT", "LF", 4.15)}
ESCALATION = 1.032       # unit prices from the October 2025 renewal


def d(k):
    return D0 + dt.timedelta(days=int(k))


class Pack:
    def __init__(self, w):
        self.w = w
        self.r = C.stream("pack")
        self._replacement_mains()
        self._addresses()

    # --------------------------------------------------------------- identities shared by several files
    def _replacement_mains(self):
        w = self.w
        r = C.stream("pack/mains")
        self.new_main = {}
        used = set(w.main_id)
        for m, day in w.cap_hist:
            while True:
                nid = "WM-%05d" % r.integers(10000, 99999)
                if nid not in used:
                    used.add(nid)
                    break
            self.new_main[m] = (nid, d(day))
        self.svc_main_id = []
        for j in range(w.n_svc):
            m = int(w.svc_main[j])
            if m in self.new_main and w.svc_renew[j] < 10 ** 6:
                self.svc_main_id.append(self.new_main[m][0])
            else:
                self.svc_main_id.append(w.main_id[m])

    def _addresses(self):
        w = self.w
        r = C.stream("pack/addr")
        self.svc_addr = [w.address(j) for j in range(w.n_svc)]
        nb = len(w.br_main)
        self.br_addr = ["%d %s" % (int(a) * 100 + int(b), w.streets[w.main_st[int(m)]])
                        for a, b, m in zip(r.integers(1, 99, nb), r.integers(0, 60, nb), w.br_main)]
        self.lk_minute = r.integers(420, 1260, len(w.lk_svc))

    def legacy_addr(self, j, rr):
        """the legacy system's free-typed address"""
        a = self.svc_addr[j]
        u = rr.random()
        no, rest = a.split(" ", 1)
        parts = rest.split(" ")
        if u < 0.05:
            parts[-1] = SUFFIX_LONG.get(parts[-1], parts[-1])
        elif u < 0.08 and parts[0] in ("N", "S", "E", "W"):
            parts = parts[1:]
        elif u < 0.10:
            no = no + " "
        return (no + " " + " ".join(parts)).replace("  ", " ")

    # --------------------------------------------------------------- GIS
    def write_gis_services(self, out):
        w = self.w
        r = C.stream("pack/gis_svc")
        rows = []
        conv16 = (dt.date(2016, 6, 1) - D0).days
        for j in range(w.n_svc):
            mat = w.svc_mat[j]
            ren = w.svc_renew[j] < 10 ** 6
            edit = w.svc_renew[j] if ren else (w.svc_start[j] if w.svc_start[j] > 0 else int(r.integers(-900, conv16)))
            if w.svc_start[j] > 0:
                code = "HDPE" if (mat == "PE" and r.random() < .18) else MAT_NEW[mat]
            elif edit < conv16 and r.random() < .55:
                code = MAT_OLD[mat]
            else:
                code = MAT_NEW[mat]
            if not ren and w.svc_start[j] < 0 and r.random() < .035:
                code = "UNK"
            yr = int(w.svc_inst[j]) if not ren else d(w.svc_renew[j]).year
            yr_s = "" if (not ren and w.svc_start[j] < 0 and r.random() < .055) else yr
            last = d(edit) if edit > -10 ** 5 else None
            if last is not None and last < dt.date(2009, 3, 2):
                last = dt.date(2009, 3, 2)          # the GIS went live on 2 March 2009
            rows.append((w.svc_id[j], self.svc_main_id[j], self.svc_addr[j], code, yr_s, w.svc_size[j],
                         w.svc_zone[j], w.svc_cen[j], "ACTIVE", C.iso(last)))
        rows.sort(key=lambda x: x[0])
        return C.write_csv(os.path.join(out, C.F_GIS_SVC),
                           ["SERVICE_ID", "MAIN_ID", "SERVICE_ADDRESS", "MATERIAL", "INSTALL_YR", "SIZE_IN",
                            "PRESSURE_ZONE", "SVC_CENTER", "STATUS", "LAST_EDIT"], rows)

    def write_gis_mains(self, out):
        w = self.w
        rows = []
        for m in range(w.n_mains):
            ret = m in self.new_main
            rows.append((w.main_id[m], w.main_mat[m], int(w.main_yr[m]), int(w.main_dia[m]), int(w.main_len[m]),
                         w.main_zone[m], w.main_cen[m], w.streets[w.main_st[m]],
                         "ABANDONED" if ret else "ACTIVE", C.iso(self.new_main[m][1]) if ret else ""))
            if ret:
                nid, dd = self.new_main[m]
                rows.append((nid, "PVC", dd.year, int(max(w.main_dia[m], 6)), int(w.main_len[m]), w.main_zone[m],
                             w.main_cen[m], w.streets[w.main_st[m]], "ACTIVE", ""))
        rows.sort(key=lambda x: x[0])
        return C.write_csv(os.path.join(out, C.F_GIS_MAIN),
                           ["MAIN_ID", "MATERIAL", "INSTALL_YR", "DIAMETER_IN", "LENGTH_FT", "PRESSURE_ZONE",
                            "SVC_CENTER", "STREET", "STATUS", "ABANDONED_DATE"], rows)

    # --------------------------------------------------------------- CIS
    def write_premises(self, out):
        w = self.w
        r = C.stream("pack/prem")
        rows = []
        self.prem_linked = np.ones(w.n_prem, dtype=bool)
        for p in range(w.n_prem):
            j = int(w.prem_svc[p])
            link = r.random() > .026
            self.prem_linked[p] = link
            unit = w.prem_unit[p]
            ptype = "RES" if unit == "" else "MF"
            if unit == "" and r.random() < .055:
                ptype = "COM"
            msize = w.svc_size[j] if ptype == "COM" else ("5/8" if r.random() < .86 else "3/4")
            conn = C.iso(d(w.svc_start[j])) if w.svc_start[j] > 0 else ""
            rows.append((w.prem_id[p], self.svc_addr[j], unit, w.route_name[w.prem_route[p]],
                         w.svc_id[j] if link else "", ptype, msize, "ACTIVE", conn))
        rows.sort(key=lambda x: x[0])
        return C.write_csv(os.path.join(out, C.F_PREM),
                           ["PREMISE_ID", "SERVICE_ADDRESS", "UNIT", "ROUTE", "SERVICE_ID", "PREMISE_TYPE",
                            "METER_SIZE", "STATUS", "CONNECT_DATE"], rows)

    def write_meter_events(self, out):
        w = self.w
        r = C.stream("pack/meter")
        rows = []
        cur_no = {p: int(w.meter_no_initial[p]) for p in range(w.n_prem)}
        # new connections: the first set
        for p in range(w.n_prem):
            j = int(w.prem_svc[p])
            if w.svc_start[j] > 0:
                rows.append((d(w.svc_start[j]), w.prem_id[p], "SET", cur_no[p], "NEW", "DEV", 0))
        reads = r.integers(200, 9000, len(w.ex_prem))
        for k in range(len(w.ex_prem)):
            p = int(w.ex_prem[k])
            t = int(w.ex_day[k])
            old = cur_no[p]
            new = int(w.meter_no_ex[k])
            by = w.ex_by[k]
            rows.append((d(t), w.prem_id[p], "REMOVE", old, w.ex_reason[k], by, int(reads[k]) * 10 + int(r.integers(0, 10))))
            rows.append((d(t + int(w.ex_gap[k])), w.prem_id[p], "SET", new, w.ex_reason[k], by, int(r.integers(0, 4))))
            cur_no[p] = new
        self.cur_meter_no = cur_no
        rows.sort(key=lambda x: (x[0], x[1], 0 if x[2] == "REMOVE" else 1))
        out_rows = []
        eid = 4410173
        for dd, pid, ev, mno, rsn, by, rd in rows:
            eid += int(r.integers(1, 4))
            out_rows.append((eid, pid, C.iso(dd), ev, "%08d" % mno, rsn, by, rd))
        return C.write_csv(os.path.join(out, C.F_METER),
                           ["EVENT_ID", "PREMISE_ID", "EVENT_DATE", "EVENT_TYPE", "METER_NO", "REASON",
                            "PERFORMED_BY", "REGISTER_READ"], out_rows)

    # --------------------------------------------------------------- work orders
    def _workorders(self):
        """every work order of both systems, before either export is cut"""
        w = self.w
        r = C.stream("pack/wo")
        wos = []      # dict rows
        # service leaks
        for i in range(len(w.lk_svc)):
            j = int(w.lk_svc[i])
            rep, fix = int(w.lk_rep[i]), int(w.lk_fix[i])
            cen = w.svc_cen[j]
            yard = C.YARD[cen] if r.random() > .05 else C.YARD[C.CENTERS[(C.CENTERS.index(cen) + 1) % 3]]
            if w.lk_inv[i]:
                wos.append(dict(kind="SVC", cls="INV", svc=j, init=rep, comp=rep + int(r.integers(0, 2)), yard=yard,
                                comp_name=w.lk_comp[i], leak=i))
            wos.append(dict(kind="SVC", cls="REP", svc=j, init=rep, comp=fix, yard=yard, comp_name=w.lk_comp[i], leak=i))
            if w.lk_rst[i]:
                wos.append(dict(kind="SVC", cls="RST", svc=j, init=fix, comp=None, yard=yard, comp_name="", leak=i))
        # customer-side investigations with no City repair
        n_cs = int(len(w.lk_svc) * 0.31)
        js = r.integers(0, w.n_svc, n_cs)
        ts = r.integers(0, T_END - 3, n_cs)
        for j, t in zip(js, ts):
            if w.svc_start[j] >= t:
                continue
            wos.append(dict(kind="SVC", cls="INV", svc=int(j), init=int(t), comp=int(t) + int(r.integers(0, 2)),
                            yard=C.YARD[w.svc_cen[j]], comp_name="CUSTOMER SIDE", leak=-1))
        # main breaks
        for b in range(len(w.br_main)):
            m = int(w.br_main[b])
            t = int(w.br_day[b])
            yard = C.YARD[w.br_yard[b]]
            mode = w.br_mode[b]
            if mode in ("CREW", "HANDOFF"):
                wos.append(dict(kind="MAIN", cls="REP", main=m, init=t, comp=int(w.br_crew_fix[b]) if mode == "CREW" else t + int(r.integers(0, 2)),
                                yard=yard, brk=b))
            if mode in ("HANDOFF", "CONTRACTOR"):
                wos.append(dict(kind="MAIN", cls="REPC", main=m, init=t + (1 if mode == "HANDOFF" else 0),
                                comp=int(w.br_perm[b]), yard=yard, brk=b))
            if w.br_rst[b]:
                wos.append(dict(kind="MAIN", cls="RST", main=m, init=int(w.br_perm[b]), comp=None, yard=yard, brk=b))
        # other work that shares the systems
        n_o = 21000
        js = r.integers(0, w.n_svc, n_o)
        ts = r.integers(0, T_END - 3, n_o)
        kinds = r.choice(["METER BOX", "HYDRANT", "VALVE", "LOCATE"], n_o, p=[.36, .26, .20, .18])
        for j, t, k in zip(js, ts, kinds):
            wos.append(dict(kind=k, cls="REP" if k != "LOCATE" else "INV", svc=int(j), init=int(t),
                            comp=int(t) + int(r.integers(0, 6)), yard=C.YARD[w.svc_cen[j]], comp_name=""))
        # call-centre duplicates, cancelled
        dup = r.random(len(wos)) < .022
        extra = []
        for k in np.nonzero(dup)[0]:
            x = dict(wos[k])
            if x["cls"] in ("REP", "REPC", "INV") and x.get("comp") is not None:
                x["cancel"] = True
                x["comp"] = None
                extra.append(x)
        wos.extend(extra)
        wos.sort(key=lambda x: (x["init"], x["kind"], x["cls"], x.get("svc", -1), x.get("main", -1)))
        self.wos = wos

    def _restoration_completion(self):
        """restoration orders complete when the contractor's restoration is done"""
        w = self.w
        done_s, done_m = {}, {}
        for typ, i, done, items in w.rst_sites:
            (done_s if typ == "S" else done_m)[i] = done
        for x in self.wos:
            if x["cls"] == "RST":
                if "leak" in x:
                    x["comp"] = done_s.get(x["leak"])
                else:
                    x["comp"] = done_m.get(x["brk"])

    def write_workorders(self, out):
        w = self.w
        self._workorders()
        self._restoration_completion()
        r = C.stream("pack/wo_write")
        cut = (C.CUTOVER - D0).days
        last_legacy = (C.LEGACY_LAST - D0).days
        leg_rows, eam_rows = [], []
        wo_no = 2203115
        eam_seq = {}
        self.rst_wo_ref = {}
        for x in self.wos:
            init, comp = x["init"], x.get("comp")
            open_at_cut = init <= last_legacy and (comp is None or comp > last_legacy) and not x.get("cancel")
            in_legacy = init <= last_legacy
            in_eam = init >= cut or open_at_cut
            if init > T_END:
                continue
            if comp is not None and comp > T_END:
                comp = None
            if x["kind"] == "SVC":
                typ_l = {"INV": "SVC INVEST", "REP": "SVC LEAK", "RST": "RESTORE"}[x["cls"]]
                typ_e = "SERVICE LEAK" if x["cls"] != "RST" else "RESTORATION"
                asset_type, asset = "SERVICE", w.svc_id[x["svc"]]
                addr = self.svc_addr[x["svc"]]
                descr = {"INV": "INVESTIGATE LEAK", "REP": "REPAIR SVC LEAK", "RST": "RESTORE SITE"}[x["cls"]]
                if x.get("comp_name") == "CUSTOMER SIDE":
                    descr = "CUST SIDE - NOTIFIED"
            elif x["kind"] == "MAIN":
                typ_l = {"REP": "MAIN BREAK", "REPC": "MAIN BREAK", "RST": "RESTORE"}[x["cls"]]
                typ_e = "MAIN BREAK" if x["cls"] != "RST" else "RESTORATION"
                asset_type, asset = "MAIN", w.main_id[x["main"]]
                addr = self.br_addr[x["brk"]]
                descr = {"REP": "MAIN BREAK REPAIR", "REPC": "MAIN BREAK - CONTRACTOR", "RST": "RESTORE SITE"}[x["cls"]]
            else:
                typ_l = typ_e = x["kind"]
                asset_type, asset = {"METER BOX": "SERVICE", "HYDRANT": "HYDRANT", "VALVE": "VALVE", "LOCATE": "SERVICE"}[x["kind"]], w.svc_id[x["svc"]]
                addr = self.svc_addr[x["svc"]]
                descr = {"METER BOX": "REPLACE METER BOX/LID", "HYDRANT": "HYDRANT REPAIR", "VALVE": "VALVE BOX ADJUST", "LOCATE": "LINE LOCATE"}[x["kind"]]
                if x["kind"] in ("HYDRANT", "VALVE"):
                    asset = "%s-%05d" % ("FH" if x["kind"] == "HYDRANT" else "WV", int(r.integers(10000, 99999)))
            legacy_no = None
            if in_legacy:
                wo_no += int(r.integers(1, 3))
                legacy_no = wo_no
                status = "CANCELLED" if x.get("cancel") else ("MIGRATED" if open_at_cut else "CLOSED")
                ladr = self.legacy_addr(x["svc"], r) if "svc" in x else addr
                lcomp = comp if (comp is not None and comp <= last_legacy) else None
                leg_rows.append((legacy_no, typ_l, status, ladr, x["yard"], d(init).strftime("%m/%d/%Y"),
                                 d(lcomp).strftime("%m/%d/%Y") if lcomp is not None else "", descr))
            if in_eam:
                yy = d(max(init, cut)).year % 100
                eam_seq[yy] = eam_seq.get(yy, 0) + int(r.integers(1, 3))
                wid = "WO%02d%06d" % (yy, eam_seq[yy] + 1500 * (yy - 20))
                status = "CANCELLED" if x.get("cancel") else ("CLOSED" if comp is not None else "OPEN")
                rep_ts = ""
                if x["kind"] == "MAIN":
                    b = x["brk"]
                    rep_ts = (dt.datetime.combine(d(w.br_day[b]), dt.time()) + dt.timedelta(minutes=int(w.br_min[b]))).strftime("%Y-%m-%d %H:%M")
                elif x["kind"] == "SVC" and x["cls"] != "RST" and x.get("leak", -1) >= 0:
                    i = x["leak"]
                    rep_ts = (dt.datetime.combine(d(w.lk_rep[i]), dt.time()) + dt.timedelta(minutes=int(self.lk_minute[i]))).strftime("%Y-%m-%d %H:%M")
                elif x["kind"] == "SVC" and x["cls"] == "INV":
                    rep_ts = (dt.datetime.combine(d(init), dt.time()) + dt.timedelta(minutes=int(r.integers(420, 1260)))).strftime("%Y-%m-%d %H:%M")
                comp_name = x.get("comp_name", "") if x["kind"] == "SVC" and x["cls"] == "REP" else ""
                eam_rows.append((wid, legacy_no if open_at_cut else "", typ_e, x["cls"], status, asset_type, asset, addr,
                                 comp_name, rep_ts, d(max(init, cut) if open_at_cut else init), d(comp) if comp is not None else None,
                                 x["yard"]))
                if x["cls"] == "RST":
                    key = ("S", x["leak"]) if "leak" in x else ("M", x["brk"])
                    self.rst_wo_ref[key] = wid
        n1 = C.write_csv(os.path.join(out, C.F_LEGACY),
                         ["WO_NO", "WO_TYPE", "STATUS", "ADDRESS", "YARD", "INIT_DATE", "COMP_DATE", "DESCR"], leg_rows)
        head = ["WORKORDER_ID", "LEGACY_WO", "WORK_TYPE", "WORK_CLASS", "STATUS", "ASSET_TYPE", "ASSET_ID",
                "ADDRESS", "COMPONENT", "REPORTED", "INITIATED", "COMPLETED", "CREW_YARD"]
        n2 = XW.write_table(os.path.join(out, C.F_EAM), "WorkOrders", head, eam_rows,
                            widths=[14, 10, 15, 11, 10, 11, 11, 30, 16, 17, 11, 11, 16])
        return n1, n2

    # --------------------------------------------------------------- AMI schedule
    def write_ami(self, out):
        w = self.w
        rows = []
        lab = {"X": "METER EXCHANGE", "R": "ENDPOINT RETROFIT", "D": "HOLD - CIP 2027"}
        for p in range(w.n_prem):
            k = w.prem_kind[p]
            if not k:
                continue
            j = int(w.prem_svc[p])
            rows.append((w.prem_id[p], w.route_name[w.prem_route[p]], w.svc_cen[j], "%08d" % self.cur_meter_no[p],
                         lab[k], C.iso(d(w.prem_week[p])) if k != "D" else ""))
        rows.sort(key=lambda x: (x[1], x[0]))
        return C.write_csv(os.path.join(out, C.F_AMI),
                           ["PREMISE_ID", "ROUTE", "SVC_CENTER", "METER_NO", "WORK_TYPE", "PLANNED_WEEK_OF"], rows)

    # --------------------------------------------------------------- restoration pay estimates and payments
    def pay_estimates(self):
        """the contractor's monthly pay estimates for fiscal 2025 and 2026, every revision submitted, and which
        revision the City paid"""
        w = self.w
        r = C.stream("pack/payest/s6")
        lines = []
        f0 = (dt.date(2024, 10, 1) - D0).days
        for typ, i, done, items in w.rst_sites:
            if not (f0 <= done <= T_END):
                continue
            ref = self.rst_wo_ref.get((typ, i))
            if ref is None:
                continue
            addr = self.svc_addr[int(w.lk_svc[i])] if typ == "S" else self.br_addr[i]
            dd = d(done)
            # billed in the month's estimate, a few lines carried to the next month (never past September 2026)
            bm = dt.date(dd.year, dd.month, 1)
            if r.random() < .07 and not (dd.year == 2026 and dd.month == 9):
                bm = dt.date(bm.year + (bm.month == 12), bm.month % 12 + 1, 1)
            for item, q in items:
                lines.append(dict(month=bm, ref=ref, addr=addr, item=item, qty=float(q), done=dd))
        months = sorted({x["month"] for x in lines})
        est = {}
        for k, mth in enumerate(months):
            est[mth] = "PE-%02d%02d" % (mth.year % 100, mth.month)
        # revision plan: in each fiscal quarter one estimate re-measured by the inspector and paid at R1, and one
        # paid at R0 that the contractor later resubmitted with added quantities, returned unpaid
        plan = {}
        self.payest_pairs = []
        by_q = {}
        for mth in months:
            by_q.setdefault(C.fy_quarter(mth), []).append(mth)
        for q, ms in sorted(by_q.items()):
            ms = sorted(ms)
            if q[0] == 2026:
                # each fiscal 2026 quarter: two consecutive months invoiced together, the first re-measured by the
                # inspector and paid at its revision, the second paid as first submitted and later resubmitted
                k = 0 if q[1] == 4 else int(r.integers(0, 2))
                plan[ms[k]], plan[ms[k + 1]] = "A", "B"
                self.payest_pairs.append((ms[k], ms[k + 1]))
            else:
                rr = list(ms)
                r.shuffle(rr)
                plan[rr[0]], plan[rr[1]] = "A", "B"
        out = []
        paid = {}
        for mth in months:
            mine = [x for x in lines if x["month"] == mth]
            sub0 = dt.date(mth.year + (mth.month == 12), mth.month % 12 + 1, 1) + dt.timedelta(days=int(r.integers(2, 7)))
            price_f = ESCALATION if mth >= dt.date(2025, 10, 1) else 1.0
            revs = [[dict(x) for x in mine]]
            kind = plan.get(mth, "")
            if kind in ("A", "B"):
                rv = [dict(x) for x in mine]
                lo, hi, share = (.72, .92, .40) if kind == "A" else (1.10, 1.35, .36)
                # the re-measure reaches every surface type the estimate carries
                pick = set(k for k in range(len(rv)) if r.random() < share)
                for g in ("0410", "0420", "0430", "0431", "0440"):
                    ks = [k for k, x in enumerate(rv) if x["item"] == g]
                    if ks:
                        for k in r.choice(ks, min(3, len(ks)), replace=False):
                            pick.add(int(k))
                for k in sorted(pick):
                    x = rv[k]
                    x["qty"] = round(x["qty"] * float(r.uniform(lo, hi)), 1 if ITEMS[x["item"]][1] == "SY" else 0)
                revs.append(rv)
            pay_rev = 1 if kind == "A" else 0
            for rv_no, rv in enumerate(revs):
                sub = sub0 + dt.timedelta(days=11 * rv_no + (int(r.integers(18, 34)) if (kind == "B" and rv_no == 1) else 0))
                if kind == "B" and rv_no == 1:
                    sub = min(sub, dt.date(2026, 10, 15))
                tot = 0.0
                for x in rv:
                    desc, unit, price = ITEMS[x["item"]]
                    pr = round(price * price_f, 2)
                    q = x["qty"] if unit == "SY" else int(round(x["qty"]))
                    amt = round(q * pr, 2)
                    tot += amt
                    out.append((est[mth], rv_no, sub, mth, x["ref"], x["addr"], x["item"], desc, unit, q, pr, amt, x["done"]))
                if rv_no == pay_rev:
                    paid[est[mth]] = (round(tot, 2), sub)
        self.payest_plan = plan
        self.payest_paid = paid
        return out

    def write_payest(self, out):
        rows = self.pay_estimates()
        rows.sort(key=lambda x: (x[0], x[1], x[4], x[6]))
        head = ["ESTIMATE_NO", "REVISION", "SUBMITTED", "PERIOD", "WO_REF", "LOCATION", "ITEM", "DESCRIPTION", "UNIT",
                "QTY", "UNIT_PRICE", "AMOUNT", "WORK_COMPLETED"]
        rows = [(a, b, c, mth.strftime("%Y-%m"), e, f, g, h, i, j, k, l, m) for (a, b, c, mth, e, f, g, h, i, j, k, l, m) in rows]
        return XW.write_table(os.path.join(out, C.F_PAYEST), "Estimate Lines", head, rows,
                              widths=[12, 9, 11, 9, 14, 30, 7, 44, 6, 9, 11, 12, 14], money_cols=(10, 11))

    def write_ap(self, out):
        r = C.stream("pack/ap")
        rows = []
        vno = 7710233
        est_of = {}
        for mth in sorted({dt.date(2000 + int(e[3:5]), int(e[5:7]), 1) for e in self.payest_paid}):
            est_of[mth] = "PE-%02d%02d" % (mth.year % 100, mth.month)
        paired = {a: b for a, b in self.payest_pairs}
        skip = set(paired.values())
        bills = []
        for mth, est in sorted(est_of.items()):
            if mth in skip:
                continue
            gross, sub = self.payest_paid[est]
            if mth in paired:
                g2, s2 = self.payest_paid[est_of[paired[mth]]]
                gross, sub = round(gross + g2, 2), max(sub, s2)
            bills.append((sub, gross))
        inv = 1
        for sub, gross in bills:
            vno += int(r.integers(11, 140))
            paid = min(sub + dt.timedelta(days=int(r.integers(12, 25))), dt.date(2026, 10, 16) - dt.timedelta(days=int(r.integers(0, 3))))
            ret = round(gross * 0.05, 2)
            rows.append(("AP%08d" % vno, "V0041877", "MABRY-TEAGUE UTILITY CONSTRUCTORS INC", "MTU-0388-%03d" % (inv + 13), C.iso(sub),
                         "%.2f" % gross, "%.2f" % ret, "%.2f" % round(gross - ret, 2), C.iso(paid), "23-0388"))
            inv += 1
        return C.write_csv(os.path.join(out, C.F_AP),
                           ["VOUCHER_NO", "VENDOR_NO", "VENDOR_NAME", "INVOICE_NO", "INVOICE_DATE", "GROSS_AMOUNT",
                            "RETAINAGE", "NET_PAID", "PAID_DATE", "CONTRACT_NO"], rows)

    # --------------------------------------------------------------- distractors
    def write_valves(self, out):
        r = C.stream("pack/valves")
        rows = []
        nv = 11800
        vid = ["WV-%05d" % x for x in r.choice(np.arange(10000, 99999), nv, replace=False)]
        cen = r.choice(C.CENTERS, nv)
        size = r.choice([6, 8, 12, 16, 24], nv, p=[.5, .26, .14, .07, .03])
        for y in range(2019, 2027):
            m = np.nonzero(r.random(nv) < .19)[0]
            for k in m:
                dd = dt.date(y, int(r.integers(1, 13)), int(r.integers(1, 29)))
                if dd > C.RECORDS_END or dd.weekday() > 4:
                    continue
                turns = int(size[k] * 3 + 2 + r.integers(-2, 3))
                res = r.choice(["EXERCISED", "EXERCISED", "EXERCISED", "EXERCISED", "PARTIAL", "INOPERABLE", "NOT FOUND - PAVED"])
                rows.append((vid[k], cen[k], int(size[k]), C.iso(dd), turns if res == "EXERCISED" else int(turns * r.uniform(.1, .7)) if res == "PARTIAL" else 0, res))
        rows.sort(key=lambda x: (x[3], x[0]))
        return C.write_csv(os.path.join(out, C.F_VALVE),
                           ["VALVE_ID", "SVC_CENTER", "SIZE_IN", "EXERCISE_DATE", "TURNS", "RESULT"], rows)

    def write_weather(self, out):
        r = C.stream("pack/wx")
        rows = []
        dd = dt.date(2012, 1, 1)
        while dd <= C.RECORDS_END:
            doy = dd.timetuple().tm_yday
            tmax = 78 + 19 * np.sin((doy - 105) / 365.25 * 2 * np.pi) + r.normal(0, 6)
            tmin = tmax - 19 + r.normal(0, 4)
            if dt.date(2021, 2, 14) <= dd <= dt.date(2021, 2, 19):
                tmax, tmin = r.uniform(18, 31), r.uniform(4, 14)
            pr = 0.0 if r.random() < .78 else round(float(r.gamma(0.7, 0.55)), 2)
            rows.append((C.iso(dd), int(round(tmax)), int(round(tmin)), "%.2f" % pr if pr > 0 else ("T" if r.random() < .05 else "0.00")))
            dd += dt.timedelta(days=1)
        return C.write_csv(os.path.join(out, C.F_WX), ["DATE", "TMAX_F", "TMIN_F", "PRCP_IN"], rows)
