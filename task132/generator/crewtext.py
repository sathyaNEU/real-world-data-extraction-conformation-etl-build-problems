"""How Tarrock's P&C crews write up their work orders: phrases composed on the job, each crew's habits (full
sentences, terse notes, capitals), the abbreviations a crew uses and the odd typo. The PM and inspection titles come
from the EAM job plans, which were reworded when the PM masters were revised in mid-2023."""
import random
import re

PM_REVISED = (2023, 7, 1)

# how each crew mostly writes; anyone on a crew can write the job up, so the habit holds about two times in three
HABIT = {"Lakeshore P&C 1": "full", "Lakeshore P&C 2": "terse", "Ridge P&C": "caps", "Valley P&C 1": "full",
         "Valley P&C 2": "terse", "Harbour P&C": "full", "Harbour Test": "terse", "North P&C 1": "terse",
         "North P&C 2": "caps", "Central P&C 1": "full", "Central P&C 2": "terse", "Central P&C 3": "full",
         "South P&C 1": "full", "South P&C 2": "terse"}
ABBR = [("power supply", "p/s"), ("replaced", "repl"), ("returned to service", "RTS"), ("back in service", "RTS"),
        (" with ", " w/ "), ("tested", "tstd"), ("feeder", "fdr"), ("breaker", "bkr"), ("battery", "batt"),
        ("charger", "chgr"), ("inspection", "insp"), ("settings", "stgs"), ("alarm", "alm"), ("station", "stn"),
        ("transformer", "xfmr"), ("secondary injection", "sec inj"), ("no fault found", "NFF"), ("checked", "chkd"),
        ("control room", "ctrl room"), ("approximately", "approx"), ("communications", "comms"), ("and", "&")]
SLIPS = {"replaced": ["replced", "repalced"], "tested": ["tesed", "testd"], "module": ["modlue", "moduel"],
         "verified": ["verfied", "verifed"], "alarm": ["alram"], "inspection": ["inspecton"], "settings": ["setings"],
         "service": ["sevice", "servcie"], "received": ["recieved"], "breaker": ["braker"], "relay": ["realy"]}


class Writer:
    def __init__(self, seed):
        self.r = random.Random(seed)

    def one(self, opts, weights=None):
        return self.r.choices(opts, weights=weights)[0] if weights else opts[self.r.randrange(len(opts))]

    def maybe(self, p, text):
        return text if self.r.random() < p else ""

    def style(self, crew):
        h = HABIT.get(crew, "full")
        return h if self.r.random() < 0.68 else self.one(["full", "terse", "caps"])

    def finish(self, parts, crew, typo=0.035):
        """join the phrases the way this crew writes them up"""
        parts = [p.strip() for p in parts if p and p.strip()]
        st = self.style(crew)
        if st == "full":
            sep = self.one([". ", ". ", "; ", ", "])
            if sep == ". ":
                out = sep.join(p[0].upper() + p[1:] for p in parts)
            else:
                out = sep.join(parts)
                out = out[0].upper() + out[1:]
            if sep == ". " and self.r.random() < 0.55:
                out += "."
        else:
            out = self.one([", ", ". ", " - ", ", "]).join(parts)
            k = 0.7 if st == "terse" else 0.45
            for a, b in ABBR:
                pat = r"(?<![\w@-])%s(?![\w@-])" % re.escape(a.strip())
                if re.search(pat, out) and self.r.random() < k:
                    out = re.sub(pat, b.strip(), out)
            if st == "caps":
                out = out.upper()
            elif out and self.r.random() < 0.7:
                out = out[0].upper() + out[1:]
        if self.r.random() < typo:
            out = self._slip(out)
        return out

    def _slip(self, s):
        words = s.split(" ")
        for i in self.r.sample(range(len(words)), len(words)):
            w = words[i]
            low = w.lower().strip(",.;")
            if low in SLIPS:
                words[i] = w.replace(w.strip(",.;"), self.one(SLIPS[low]) if w.strip(",.;").islower() else self.one(SLIPS[low]).upper())
                return " ".join(words)
        for i in self.r.sample(range(len(words)), len(words)):
            w = words[i]
            if len(w) >= 6 and w.isalpha() and w.islower():
                j = self.r.randrange(1, len(w) - 2)
                words[i] = w[:j] + w[j + 1] + w[j] + w[j + 2:]
                return " ".join(words)
        return s

    # ------------------------------------------------------------- the VPR-340 power supply

    def psu_failure(self, crew, bay, store, em, storm=None, fitted="same", repaired=False, serial=None, wo_fit=None):
        """the corrective work order on which the crew found the failed power supply. fitted: 'same' when the spare
        went in on this work order, 'later' when it was fitted on a follow-up"""
        trig = (["after the %s storm, %s relay dark" % (storm, bay), "post-storm patrol %s, %s relay fail alarm" % (storm, bay),
                 "%s relay down after %s storm" % (bay, storm)] if storm else
                ["SCADA relay fail alarm %s" % bay, "relay trouble alarm from control room, %s" % bay,
                 "IED fail alarm on %s" % bay, "control room lost comms to %s relay" % bay, "%s relay fail alarm" % bay,
                 "watchdog alarm %s" % bay, "%s relay found dark on station visit" % bay,
                 "System Control called out for %s relay trouble" % bay, "%s relay not answering SCADA poll" % bay,
                 "relay self-test fail alarm %s" % bay, "called out, %s relay trouble alarm" % bay])
        find = ["no LEDs on front panel", "front panel dark, ENABLED LED out", "relay dead, DC OK at terminals",
                "PSU output low on test", "PSU fail indication on front panel", "relay rebooting every few minutes",
                "relay dead, burnt smell at PSU", "power supply module failed", "PSU failed, fuse OK",
                "125 V DC at terminals, nothing out of PSU", "PSU failed, relay out of service",
                "relay cycling on and off, PSU output collapsing under load", "PSU dead"]
        hold = ["feeder on backup protection", "bus protection backing up %s" % bay, "%s left on backup" % bay,
                "%s blocked from reclosing until relay back" % bay]
        if fitted == "same":
            if repaired:
                act = ["replaced PSU with spare from %s (repaired unit)" % store, "fitted spare PSU s/n %s from %s" % (serial, store),
                       "swapped PSU, spare ex Veldtek repair", "installed repaired PSU from %s stock" % store,
                       "replaced power supply with spare s/n %s" % serial, "changed PSU, used refurb spare from %s" % store]
            else:
                act = ["replaced PSU with new module from %s" % store, "swapped in new PSU from %s stock" % store,
                       "new PSU fitted, s/n %s" % serial, "installed new power supply module from %s" % store,
                       "replaced power supply, new s/n %s" % serial, "changed PSU, new unit from %s" % store]
            test = ["relay tested and returned to service", "trip tested OK", "secondary injection OK, returned to service",
                    "settings verified, relay back in service", "event records downloaded, back in service",
                    "functional test OK, ENABLED LED on", "settings checked against file, returned to service",
                    "trip test OK, control room advised"]
            parts = [self.one(trig), self.one(find), self.maybe(0.15, self.one(hold)), self.one(act), self.one(test)]
        else:
            act = ["no spare on truck, PSU removed, follow-up WO raised to fit spare",
                   "pulled failed PSU, spare to be fitted on follow-up WO", "PSU removed, relay left out of service pending spare",
                   "failed PSU removed, fitting on next WO", "removed PSU, spare coming from %s" % store,
                   "PSU removed, spare fitted under %s" % wo_fit if wo_fit else "PSU removed, spare fitted on follow-up"]
            parts = [self.one(trig), self.one(find), self.one(hold), self.one(act)]
        if em and self.r.random() < 0.4:
            parts.insert(0, self.one(["call-out", "after hours call-out", "o/t call-out", "emergency call"]))
        parts.append(self.maybe(0.18, self.one(["failed unit bagged and tagged for RMA", "failed PSU to %s for return" % store,
                                                 "control room advised", "SER downloaded", "failed unit to %s quarantine shelf" % store])))
        return self.finish(parts, crew)

    def psu_fitting(self, crew, bay, store, serial, repaired, wo_fail):
        what = (["fit spare PSU s/n %s (repaired unit)" % serial, "install refurb PSU %s from %s" % (serial, store),
                 "fit repaired PSU s/n %s" % serial] if repaired else
                ["fit new PSU s/n %s" % serial, "install new power supply module from %s" % store,
                 "fit new PSU from %s stock, s/n %s" % (store, serial)])
        ref = ["follow-up to %s" % wo_fail, "ref %s" % wo_fail, "follow up %s" % wo_fail, "per %s" % wo_fail]
        test = ["relay tested and returned to service", "trip test OK, back in service", "secondary injection OK, RTS",
                "settings verified, relay in service", "functional test OK, control room advised"]
        return self.finish(["%s relay" % bay if self.r.random() < 0.4 else "", self.one(what), self.one(ref), self.one(test)], crew)

    def psu_duplicate(self, crew, wo):
        return self.finish([self.one(["duplicate of %s" % wo, "dup WO, see %s" % wo, "raised twice from SCADA alarm, see %s" % wo,
                                      "duplicate, work done on %s" % wo, "SCADA alarm raised twice, closed against %s" % wo])], crew, typo=0)

    def log_psu(self, crew, serials):
        if len(serials) == 1:
            s = serials[0]
            opts = ["ship failed PSU s/n %s to Veldtek, RMA requested" % s, "return PSU %s to Veldtek repair centre" % s,
                    "courier failed module %s to Veldtek under RMA" % s, "RMA return to Veldtek, PSU s/n %s" % s,
                    "send failed VPR-340 PSU %s to Veldtek for repair" % s]
        else:
            a, b = serials
            opts = ["ship failed PSUs s/n %s and %s to Veldtek, RMA requested" % (a, b),
                    "return 2 PSUs (%s, %s) to Veldtek repair centre" % (a, b),
                    "courier 2 failed VPR-340 PSUs to Veldtek under RMA, s/n %s %s" % (a, b),
                    "RMA return to Veldtek, PSUs %s and %s" % (a, b)]
        return self.finish([self.one(opts)], crew, typo=0.01)

    # ------------------------------------------------------------- other corrective work

    FAULT = {
        ("relay", "CPU"): (["relay locked up", "CPU self-test failure", "relay fail alarm, processor fault on front panel",
                            "relay rebooting, processor error logged"],
                           ["processor card replaced", "CPU card swapped", "processor card changed, firmware reloaded"]),
        ("relay", "IO"): (["input card failed self-test", "binary input chatter", "output contact welded",
                           "breaker status input stuck", "trip output not operating on test"],
                          ["IO card replaced", "replaced input/output card", "IO card changed"]),
        ("relay", "DISP"): (["display blank", "keypad unresponsive", "front panel display garbled"],
                            ["front panel replaced", "display module changed", "replaced front panel"]),
        ("relay", "COMMS"): (["lost SCADA comms to relay", "DNP3 link down", "fibre transceiver failed", "relay dropping off the network"],
                             ["comms card replaced", "comms card reset then replaced", "replaced comms card and patch lead"]),
        ("relay", "PSU"): (["relay power supply failed", "PSU fault alarm", "relay dead, power supply failed"],
                           ["power supply module replaced", "PSU replaced", "replaced power supply"]),
        ("recloser", "PSU"): (["control battery failed load test", "recloser control charger failed", "control on battery, no AC charge"],
                              ["battery replaced", "PSU module replaced", "charger board replaced"]),
        ("recloser", "CPU"): (["recloser control locked up", "control CPU fault"], ["processor board replaced and settings loaded"]),
        ("recloser", "IO"): (["trip/close output failed", "recloser status input stuck"], ["IO board replaced", "replaced IO board"]),
        ("recloser", "DISP"): (["control panel display faded"], ["front panel replaced"]),
        ("recloser", "COMMS"): (["radio link to recloser control lost", "SCADA polling to recloser failed"],
                                ["comms module replaced", "radio replaced", "comms module changed"]),
        ("rtu", "CPU"): (["RTU processor failed", "RTU locked up"], ["processor card replaced, config reloaded"]),
        ("rtu", "IO"): (["RTU status input card failed", "RTU analog input drifting", "RTU control output card failed"],
                        ["card replaced, points checked with control room", "card replaced and calibrated", "replaced card"]),
        ("rtu", "COMMS"): (["RTU comms to control centre lost", "DNP3 link to master down"],
                           ["comms card replaced", "port card replaced", "modem replaced"]),
        ("rtu", "PSU"): (["RTU power supply failed", "RTU dead, DC OK"], ["power supply replaced, points verified"]),
    }
    TEST = {"relay": ["trip tested", "settings verified", "tested OK", "secondary injection OK", "returned to service"],
            "recloser": ["control tested", "settings loaded and tested", "test trip/close OK"],
            "rtu": ["points verified with control room", "controls tested with control room", "back on scan"]}

    def fault(self, crew, kind, comp, bay, warranty=False, recovered=False):
        sym, act = self.FAULT[(kind, comp)]
        parts = [self.maybe(0.5, bay) if kind != "rtu" else "", self.one(sym), self.one(act)]
        if warranty:
            parts.append(self.one(["under warranty", "warranty claim raised", "card under warranty"]))
        elif recovered:
            parts.append(self.one(["card from recovered spares", "used recovered card", "spare card ex rebuild"]))
        parts.append(self.one(self.TEST[kind]))
        return self.finish(parts, crew)

    def nff(self, crew, kind, bay):
        opts = {"relay": ["relay fail alarm, reset and monitored, no fault found", "spurious relay alarm, event records reviewed, nothing found",
                          "alarm cleared on arrival, no fault found", "loose wiring at panel terminal, retightened",
                          "relay alarm, SER shows DC dip, no fault found"],
                "recloser": ["recloser control alarm, battery and charger checked, no fault found",
                             "control alarm cleared on arrival, no fault found"],
                "rtu": ["RTU alarm investigated, points checked with control room, no fault found", "RTU comms fail alarm, cleared, nothing found"]}[kind]
        return self.finish([self.maybe(0.4, bay) if kind != "rtu" else "", self.one(opts)], crew)

    def awaiting(self, crew, kind, comp, part, maker, hold, bay):
        sym, _ = self.FAULT[(kind, comp)]
        return self.finish([self.maybe(0.4, bay) if kind != "rtu" else "", self.one(sym),
                            self.one(["awaiting replacement %s from %s" % (part, maker), "%s on order from %s" % (part, maker),
                                      "waiting on %s %s" % (maker, part)]), hold], crew)

    def log_part(self, crew, part, maker, warranty):
        return self.finish([self.one(["return failed %s to %s under warranty" % (part, maker),
                                      "warranty return, %s to %s" % (part, maker)]) if warranty else
                            self.one(["ship failed %s to %s for repair" % (part, maker), "send %s to %s for repair" % (part, maker),
                                      "%s repair return, %s" % (maker, part)])], crew, typo=0.01)

    # ------------------------------------------------------------- station DC, breakers and instrument transformers

    def dc_fault(self, crew, kind, name):
        if kind == "battery":
            sym = ["%s low cell voltage, 2 cells below 2.10 V" % name, "%s cell jar cracked, electrolyte on stand" % name,
                   "battery ground alarm, traced to %s" % name, "%s failed impedance limits on 3 cells" % name]
            act = ["cells replaced", "jar replaced and stand cleaned", "ground cleared, cell connector replaced",
                   "cells replaced, equalize charge applied"]
        else:
            sym = ["%s fail alarm" % name, "%s output low, battery on discharge" % name, "%s AC fail alarm, breaker tripped" % name,
                   "%s float voltage high" % name]
            act = ["control board replaced", "charger reset and float adjusted", "rectifier module replaced",
                   "AC breaker reset, charger checked", "replaced charger fan and board"]
        return self.finish([self.one(sym), self.one(act), self.maybe(0.5, self.one(["DC system checked", "alarm cleared",
                                                                                      "control room advised"]))], crew)

    def cb_fault(self, crew, bay):
        sym = ["%s breaker failed to trip on test" % bay, "%s trip coil open circuit" % bay, "%s CB fail alarm" % bay,
               "%s breaker slow to open, timing out of limits" % bay, "%s trip circuit supervision alarm" % bay]
        act = ["trip coil replaced", "aux contact replaced", "mechanism lubed and retimed", "wiring fault at CB fixed",
               "trip coil and aux switch replaced"]
        return self.finish([self.one(sym), self.one(act), self.one(["trip tested OK", "timing within limits", "returned to service"])], crew)

    def vt_fault(self, crew, name):
        return self.finish([self.one(["%s fuse blown, loss of potential alarm" % name, "%s secondary fuse failed" % name,
                                      "LOP alarm, %s fuse" % name]),
                            self.one(["fuse replaced", "fuses replaced, voltages checked", "fuse replaced, relays checked for LOP"])], crew)

    # ------------------------------------------------------------- planned work and inspections

    def pm_title(self, cls, when, **kw):
        old = (when.year, when.month, when.day) < PM_REVISED
        bay, model, name = kw.get("bay", ""), kw.get("model", ""), kw.get("name", "")
        titles = {
            "relay": ("P&C Std 3.2 relay test - %s" % bay, "RELAY MAINT TEST %s %s" % (bay, model)),
            "relay_txbus": ("P&C Std 3.2 relay test - %s" % bay, "RELAY MAINT TEST %s %s" % (bay, model)),
            "rtu": ("RTU functional check and point-to-point test", "RTU ANNUAL MAINT - PT TO PT"),
            "recloser": ("Recloser control test and battery load test - %s" % bay, "RECLOSER CTRL ANNUAL TEST %s" % bay),
            "batt_q": ("Quarterly battery inspection %s - cell volts and SG" % name, "BATT QTRLY INSP %s" % name),
            "batt_a": ("Battery impedance test %s" % name, "BATT ANNUAL IMPEDANCE TEST %s" % name),
            "charger": ("Charger annual check %s" % name, "CHARGER ANNUAL MAINT %s" % name),
            "cb": ("CB trip test from protection - %s" % bay, "CB TRIP TEST %s" % bay),
            "ct": ("CT ratio, polarity and insulation check - %s" % bay, "CT TEST %s" % bay),
            "vt": ("VT secondary check - %s" % name, "VT SECONDARY CHECK %s" % name),
        }
        return titles[cls][0 if old else 1]

    PM_NOTE = {
        "relay": ["as found OK", "trip ckt OK, targets reset", "settings verified against approved file", "minor: lamp replaced",
                  "2 alarms in SER reviewed, OK", "as found/as left OK", "self-test log clear", "firmware version recorded",
                  "trip test OK, CB opened in 3 cyc"],
        "rtu": ["all points OK", "2 status points relabelled", "analog cal OK", "points verified with control room"],
        "recloser": ["battery load test OK", "battery replaced", "control OK", "battery 2 yrs old, OK"],
        "batt_q": ["all cells OK", "pilot cell SG 1.215", "2 cells low, equalized", "electrolyte topped up", "float 132.4 V",
                   "connectors retorqued", "ground detector OK"],
        "batt_a": ["impedance within 20% of baseline", "3 cells trending up, watch", "all cells within limits", "intercell resistance OK"],
        "charger": ["float and equalize settings OK", "alarms tested OK", "fan replaced", "output 132.6 V float"],
        "cb": ["trip from relay OK", "trip time 3.1 cyc", "trip time 2.8 cyc", "both trip coils OK", "close/trip OK"],
        "ct": ["ratio and polarity OK", "insulation OK", "burden OK"],
        "vt": ["secondary volts balanced", "fuses checked OK", "LOP alarm tested"],
    }

    def pm(self, crew, cls, when, note_p=0.35, **kw):
        t = self.pm_title(cls, when, **kw)
        key = "relay" if cls == "relay_txbus" else cls
        if self.r.random() < note_p:
            note = self.finish([self.one(self.PM_NOTE[key])], crew, typo=0.02)
            t = t + self.one([" - ", ". ", "; ", " / "]) + note
        return t

    def insp(self, crew, kind, when, note_p=0.25):
        old = (when.year, when.month, when.day) < PM_REVISED
        title = {"ts": ("Monthly station inspection - TS", "STN INSP MONTHLY TS"),
                 "ds": ("Quarterly station inspection - DS", "STN INSP QTRLY DS"),
                 "events": ("Relay event records downloaded and reviewed", "RELAY EVENT REVIEW SEMI-ANNUAL"),
                 "ir": ("Annual infrared scan, P&C panels", "IR SCAN P&C PANELS ANNUAL")}[kind][0 if old else 1]
        notes = {"ts": ["no defects", "annunciator lamp replaced", "panel heater off, breaker reset", "door seal worn, noted",
                        "yard lights out, reported to stations", "all alarms clear", "battery room fan noisy, CM raised",
                        "relay targets reset on F-bays", "minor: label missing on panel 3"],
                 "ds": ["no defects", "annunciator test OK", "fence gate latch broken, reported", "kiosk heater not working",
                        "all alarms clear", "rodent droppings in control kiosk, reported"],
                 "events": ["no misoperations found", "1 event reviewed with protection engineering", "all events correct"],
                 "ir": ["no hot spots", "hot terminal on TB4, retorqued", "all within limits"]}[kind]
        if self.r.random() < note_p:
            return title + self.one([" - ", ". ", ", "]) + self.finish([self.one(notes)], crew, typo=0.02)
        return title

    def audit(self, crew, bay, model, when):
        old = (when.year, when.month, when.day) < PM_REVISED
        title = ("Settings audit %s: as-left settings against approved file" % bay if old else
                 "SETTINGS AUDIT %s %s" % (bay, model))
        if self.r.random() < 0.3:
            note = self.one(["no differences", "settings match approved file", "1 difference, approved file updated",
                             "group 2 found active, returned to group 1", "event report settings differ, corrected",
                             "file revision on relay older than library, reloaded"])
            return title + self.one([" - ", ". ", "; "]) + self.finish([note], crew, typo=0.02)
        return title

    def storm_check(self, crew, day):
        return self.finish([self.one(["post-storm station check", "storm check after %s" % day, "post-storm visit",
                                      "station check after the %s storm" % day]),
                            self.one(["alarms reviewed and reset", "targets recorded and reset", "no damage, alarms reset",
                                      "SER downloaded, targets reset", "all clear"])], crew)

    def settings(self, crew, bay, study, when):
        return self.finish([self.one(["settings change per protection coordination study %s" % study,
                                      "revised %s settings per study %s" % (bay, study) if bay else "revised settings per study %s" % study,
                                      "new settings issued under %s, applied and tested" % study,
                                      "applied settings file from %s" % study])], crew, typo=0.01)

    def firmware(self, crew, rel):
        return self.finish([self.one(["firmware update to vendor release %s" % rel, "firmware upgraded to %s" % rel,
                                      "update firmware %s per vendor notice" % rel])], crew, typo=0.01)

    def reissue(self, crew, bay):
        return self.finish([self.one(["settings file reissued after feeder reconfiguration",
                                      "%s settings reissued after load transfer" % bay if bay else "settings reissued after load transfer",
                                      "settings group changed for feeder reconfiguration"])], crew, typo=0.01)

    def held(self, crew, study):
        return self.finish(["settings change on hold pending revised coordination study %s" % study], crew, typo=0)
