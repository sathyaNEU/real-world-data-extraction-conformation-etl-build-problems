"""How Tarrock's P&C crews write up their work orders. Each crew has a few people who do the paperwork, and each
person has habits: sentence case, all capitals or all lower case, their own separators and abbreviations, how a bay
gets written, whether a reading or a time goes in, the odd typo. What they write comes from the job: the alarm, what
the relay and the PSU showed, the readings taken, the spare used, the tests done. The PM and inspection titles come
from the EAM job plans, which were reworded when the PM masters were revised in mid-2023."""
import random
import re

PM_REVISED = (2023, 7, 1)

ABBR = [("power supply", "p/s"), ("replaced", "repl"), ("returned to service", "RTS"), ("back in service", "RTS"),
        (" with ", " w/ "), ("tested", "tstd"), ("feeder", "fdr"), ("breaker", "bkr"), ("battery", "batt"),
        ("charger", "chgr"), ("inspection", "insp"), ("settings", "stgs"), ("alarm", "alm"), ("station", "stn"),
        ("transformer", "xfmr"), ("secondary injection", "sec inj"), ("no fault found", "NFF"), ("checked", "chkd"),
        ("control room", "ctrl rm"), ("approximately", "approx"), ("communications", "comms"), ("and", "&"),
        ("protection", "prot"), ("terminals", "terms"), ("minutes", "min"), ("verified", "vfd"), ("after hours", "a/h")]
SLIPS = {"replaced": ["replced", "repalced"], "tested": ["tesed", "testd"], "module": ["modlue", "moduel"],
         "verified": ["verfied", "verifed"], "alarm": ["alram"], "settings": ["setings"], "service": ["sevice", "servcie"],
         "received": ["recieved"], "breaker": ["braker"], "relay": ["realy"], "terminals": ["termnials"],
         "control": ["contorl"], "supply": ["suppy"]}
ALARMS = ["relay fail", "IED fail", "watchdog", "relay trouble", "relay self-test fail", "DC supply fail", "relay out of service"]
BAY_STYLES = ["F05", "F5", "F-05", "fdr 5", "feeder 5", "FDR05", "F05"]
SERIAL_STYLES = ["s/n {}", "S/N {}", "sn {}", "ser {}", "s/n: {}", "#{}"]


class Person:
    """one person's way of writing a job up"""

    def __init__(self, r):
        self.case = r.choices(["sentence", "clause", "lower", "caps"], [0.42, 0.17, 0.2, 0.21])[0]
        self.sep = r.choices([". ", ", ", " - ", "; ", " / ", ".  "], [0.34, 0.3, 0.14, 0.09, 0.07, 0.06])[0]
        self.end = r.random() < 0.45
        self.abbr = {a for a, _ in ABBR if r.random() < 0.45}
        self.detail = r.choices([0, 1, 2], [0.35, 0.4, 0.25])[0]
        self.reads = r.choice([0.08, 0.2, 0.4, 0.65])
        self.times = r.choice([0.0, 0.1, 0.35, 0.6])
        self.bay = r.choice(BAY_STYLES)
        self.sn = r.choice(SERIAL_STYLES)
        self.typo = r.choice([0.002, 0.005, 0.01, 0.02])
        self.action_first = r.random() < 0.18
        self.words = r.choice(["PSU", "PSU", "p/s", "power supply", "PS module", "supply module", "PSU card", "power supply card"])
        self.store = r.choice(["full", "short", "short", "code"])
        self.seed = r.randrange(1 << 30)

    def vocab(self, slot, opts):
        """the phrases this person reaches for in a slot: their own share of what the crews say"""
        rr = random.Random("%d-%s" % (self.seed, slot))
        mine = [o for o in opts if rr.random() < 0.45]
        return mine or [opts[rr.randrange(len(opts))]]


# hours a crew books for the round trip to site, and its pace on the job, are in extracts.CREW; who on a crew does the
# paperwork is drawn here, each crew three to five people with the lead doing most of it
CREWS = ["Lakeshore P&C 1", "Lakeshore P&C 2", "Ridge P&C", "Valley P&C 1", "Valley P&C 2", "Harbour P&C", "Harbour Test",
         "North P&C 1", "North P&C 2", "Central P&C 1", "Central P&C 2", "Central P&C 3", "South P&C 1", "South P&C 2"]


class Writer:
    def __init__(self, seed):
        self.r = random.Random(seed)
        rp = random.Random(seed * 31 + 7)
        self.people = {}
        for c in CREWS:
            k = rp.randint(3, 5)
            w = [rp.random() + (1.5 if j == 0 else 0.2) for j in range(k)]
            self.people[c] = ([Person(rp) for _ in range(k)], w)
        self.wrong_bays = 0

    def one(self, opts, weights=None):
        return self.r.choices(opts, weights=weights)[0] if weights else opts[self.r.randrange(len(opts))]

    def maybe(self, p, text):
        return text if self.r.random() < p else ""

    def who(self, crew):
        ppl, w = self.people.get(crew) or self.people["Central P&C 1"]
        return self.r.choices(ppl, w)[0]

    # ------------------------------------------------------------- the pieces a person fills in

    def bay(self, p, bay):
        """the bay as this person writes it; now and then the wrong bay number goes down"""
        if not bay or not bay.startswith("F"):
            return bay
        n = int(bay[1:])
        if self.r.random() < 0.004 and n > 1:
            n += self.r.choice([-1, 1])
            self.wrong_bays += 1
        st = p.bay if self.r.random() < 0.85 else self.one(BAY_STYLES)
        return {"F05": "F%02d" % n, "F5": "F%d" % n, "F-05": "F-%02d" % n, "fdr 5": "fdr %d" % n, "feeder 5": "feeder %d" % n,
                "FDR05": "FDR%02d" % n}[st]

    STORE_SHORT = {"Central Stores (Barrie Road)": ("Central Stores", "Barrie Rd stores", "CS"),
                   "North Depot": ("North Depot", "north depot", "ND"), "South Depot": ("South Depot", "south depot", "SD")}

    def store(self, p, store):
        if p.store == "full" or store not in self.STORE_SHORT:
            return store
        s = self.STORE_SHORT[store]
        return s[2] if p.store == "code" else s[self.r.randrange(2)]

    def say(self, p, slot, opts):
        return self.one(p.vocab(slot, opts))

    def clock(self):
        h = self.one(list(range(0, 24)), [2] * 6 + [1] * 2 + [3] * 10 + [2] * 6)
        return self.one(["%02d:%02d", "%02d%02d", "%02d:%02dh"]) % (h, self.r.randrange(60))

    def dc(self, volts):
        nominal = {48: (51.6, 54.2), 125: (127.8, 134.6), 250: (256.0, 268.5)}[volts]
        v = round(self.r.uniform(*nominal), 1)
        tb = "TB%d-%d/%d" % (self.r.randint(1, 3), self.r.randint(1, 12), self.r.randint(13, 24))
        return self.one(["%.1f VDC at %s" % (v, tb), "DC at terminals %.1f V" % v, "%.1fV DC in" % v,
                         "station DC OK (%.1f V)" % v, "%.1f V at relay DC input" % v, "DC input %.1fV, OK" % v])

    def rails(self):
        five = self.one(["0.0", "0.2", "0.4", "2.8", "3.6", "4.1"])
        tw = self.one(["0.0", "6.3", "11.4", "17.9", "19.2"])
        return self.one(["+5V rail %sV" % five, "5 V out %s" % five, "+24V rail %s V" % tw, "+5 %s / +24 %s" % (five, tw),
                         "PSU output %s V on 5V test point" % five, "24V rail sagging to %s V" % tw])

    def led(self, dead):
        if dead:
            return self.one(["all LEDs off", "no LEDs", "front panel dark", "display blank, no LEDs", "PWR LED off",
                             "ENABLED and PWR LEDs out", "relay dark", "nothing on the front panel", "IN SVC LED off, display blank"])
        st = self.one(["flashing", "on solid", "red", "out", "off"])
        return self.one(["ALARM LED %s" % st, "ENABLED LED %s" % st, "RELAY OK LED %s" % st, "ALARM LED on, ENABLED off",
                         "IN SVC LED off, ALARM red", "display flickering", "display frozen, LEDs %s" % st])

    def finish(self, parts, p, typo=None):
        """join the pieces the way this person writes"""
        seen, uniq = set(), []
        for x in parts:
            x = x.strip() if x else ""
            if x and x.lower() not in seen:
                seen.add(x.lower())
                uniq.append(x)
        parts = uniq
        sep = p.sep if self.r.random() < 0.8 else self.one([". ", ", ", " - ", "; "])
        out = sep.join(parts)
        for a, b in ABBR:
            if a in p.abbr and self.r.random() < 0.85:
                pat = r"(?<![\w@/-])%s(?![\w@/-])" % re.escape(a.strip())
                out = re.sub(pat, b.strip(), out)
        if p.case == "caps":
            out = out.upper()
        elif p.case == "lower":
            keep = re.compile(r"PS02-\d\d-\d+|WO\d+|RMA-\d+")
            out = "".join(seg if keep.fullmatch(seg) else seg.lower() for seg in re.split(r"(PS02-\d\d-\d+|WO\d+|RMA-\d+)", out))
        elif p.case == "clause":
            out = re.sub(r"(^|[.;,/-] )([a-z])", lambda m: m.group(1) + m.group(2).upper(), out)
        else:
            out = re.sub(r"(^|[.!?] +)([a-z])", lambda m: m.group(1) + m.group(2).upper(), out)
        if p.end and not out.endswith("."):
            out += "."
        if self.r.random() < (p.typo if typo is None else typo):
            out = self._slip(out)
        return out

    def _slip(self, s):
        words = s.split(" ")
        for i in self.r.sample(range(len(words)), len(words)):
            w = words[i]
            low = w.lower().strip(",.;")
            if low in SLIPS:
                core = w.strip(",.;")
                rep = self.one(SLIPS[low])
                words[i] = w.replace(core, rep.upper() if core.isupper() else rep)
                return " ".join(words)
        for i in self.r.sample(range(len(words)), len(words)):
            w = words[i]
            if len(w) >= 6 and w.isalpha() and w.islower():
                j = self.r.randrange(1, len(w) - 2)
                words[i] = w[:j] + w[j + 1] + w[j] + w[j + 2:]
                return " ".join(words)
        return s

    # ------------------------------------------------------------- the VPR-340 power supply

    def psu_failure(self, crew, bay, store, em, storm=None, fitted="same", repaired=False, serial=None, wo_fit=None,
                    volts=125):
        """the corrective work order on which the crew found the failed power supply. fitted: 'same' when the spare
        went in on this work order, 'later' when it was fitted on a follow-up"""
        p = self.who(crew)
        b = self.bay(p, bay)
        psu = p.words
        if storm:
            trig = self.one(["after the %s storm, %s relay dark" % (storm, b), "post-storm patrol %s, %s relay fail alarm" % (storm, b),
                             "%s relay down after %s storm" % (b, storm), "storm %s, %s relay found off" % (storm, b)])
        else:
            alarm = self.one(ALARMS)
            trig = self.one(["%s alarm %s" % (alarm, b), "SCADA %s alarm on %s" % (alarm, b), "%s %s alarm" % (b, alarm),
                             "control room called, %s relay %s" % (b, self.one(["not responding", "off line", "showing fail", "no comms"])),
                             "%s relay found dark on %s" % (b, self.one(["station visit", "monthly insp", "switching", "stn check"])),
                             "System Control call, %s %s" % (b, alarm), "%s alm rec'd %s, %s" % (alarm, self.clock(), b)])
        lead = []
        if em and self.r.random() < 0.55:
            lead.append(self.one(["call-out", "after hours call-out", "o/t call out", "emergency call", "C/O"]))
            if self.r.random() < p.times:
                lead.append("on site %s" % self.clock())
        dead = self.r.random() < 0.6
        finds = [self.led(dead)]
        if self.r.random() < p.reads:
            finds.append(self.dc(volts))
        if self.r.random() < p.reads * 0.8:
            finds.append(self.rails())
        if p.detail >= 1 or self.r.random() < 0.5:
            finds.append(self.one(["relay rebooting every %d min" % self.r.randint(2, 15), "relay cycling on and off",
                                   "self-test log: PS FAIL", "SER shows DC fail at %s" % self.clock(), "burnt smell at %s" % psu,
                                   "scorch mark on %s board" % psu, "%s caps bulging" % psu, "%s input fuse blown" % psu,
                                   "%s fuse OK" % psu, "%s hot to touch" % psu, "%s dead" % psu, "%s failed" % psu,
                                   "%s output collapsing under load" % psu, "nothing out of %s" % psu,
                                   "relay powers up then drops out", "relay dead"]))
        if p.detail == 0 and len(finds) > 2:
            finds = finds[:2]
        hold = self.maybe(0.25 if fitted == "same" else 0.9,
                          self.one(["feeder on backup prot", "bus protection backing up %s" % b, "%s left on backup" % b,
                                    "%s reclosing blocked until relay back" % b, "load transferred off %s" % b,
                                    "upstream prot covering %s" % b]))
        sn = p.sn.format(serial) if serial else ""
        if fitted == "same":
            if repaired:
                act = self.one(["replaced %s w/ repaired unit from %s" % (psu, store), "fitted repaired %s %s" % (psu, sn),
                                "changed %s, used refurb spare from %s" % (psu, store), "installed Veldtek-repaired %s %s" % (psu, sn),
                                "replaced %s, spare ex Veldtek repair %s" % (psu, sn), "swapped %s for repaired spare (%s stock)" % (psu, store)])
            else:
                act = self.one(["replaced %s with new module from %s" % (psu, store), "new %s fitted %s" % (psu, sn),
                                "changed %s, new unit from %s" % (psu, store), "installed new %s %s" % (psu, sn),
                                "replaced %s, new %s" % (psu, sn), "swapped in new %s from %s stock" % (psu, store)])
            tests = [self.one(["trip test OK", "trip tested OK, CB opened %.1f cyc" % self.r.uniform(2.6, 3.6),
                               "secondary injection OK", "functional test OK", "settings verified against file",
                               "settings checked, file rev %d" % self.r.randint(2, 9), "self-test clear", "ENABLED LED on"])]
            if p.detail >= 1:
                tests.append(self.one(["event records downloaded", "SER downloaded", "control room advised",
                                       "returned to service %s" % self.clock() if self.r.random() < p.times else "returned to service",
                                       "back in service", "System Control notified"]))
            parts = lead + ([act, trig] + finds if p.action_first else [trig] + finds) + [hold] + ([] if p.action_first else [act]) + tests
        else:
            act = self.one(["no spare on truck, %s removed, follow-up WO raised to fit spare" % psu,
                            "pulled failed %s, spare to be fitted on follow-up WO" % psu,
                            "%s removed, relay left out of service pending spare" % psu, "failed %s removed, fitting on next WO" % psu,
                            "removed %s, spare coming from %s" % (psu, store),
                            ("%s removed, spare fitted under %s" % (psu, wo_fit)) if wo_fit else ("%s removed, spare fitted on f/u WO" % psu)])
            parts = lead + [trig] + finds + [hold, act]
        parts.append(self.maybe(0.2, self.one(["failed unit bagged and tagged for RMA", "failed %s to %s returns" % (psu, store),
                                                "tag %d on failed unit" % self.r.randint(1000, 9999), "SER downloaded",
                                                "failed unit to %s returns shelf" % store])))
        return self.finish(parts, p)

    def psu_fitting(self, crew, bay, store, serial, repaired, wo_fail):
        p = self.who(crew)
        sn = p.sn.format(serial)
        what = (["fit spare %s %s (repaired unit)" % (p.words, sn), "install refurb %s %s from %s" % (p.words, sn, store),
                 "fit repaired %s %s" % (p.words, sn)] if repaired else
                ["fit new %s %s" % (p.words, sn), "install new %s from %s" % (p.words, store),
                 "fit new %s from %s stock, %s" % (p.words, store, sn)])
        ref = ["follow-up to %s" % wo_fail, "ref %s" % wo_fail, "f/u %s" % wo_fail, "per %s" % wo_fail, "from %s" % wo_fail]
        test = ["relay tested and returned to service", "trip test OK, back in service", "secondary injection OK, RTS",
                "settings verified, relay in service", "functional test OK, control room advised", "tstd OK, ENABLED on"]
        return self.finish(["%s relay" % self.bay(p, bay) if self.r.random() < 0.4 else "", self.one(what), self.one(ref),
                            self.one(test)], p)

    def psu_duplicate(self, crew, wo):
        p = self.who(crew)
        return self.finish([self.one(["duplicate of %s" % wo, "dup WO, see %s" % wo, "raised twice from SCADA alarm, see %s" % wo,
                                      "duplicate, work done on %s" % wo, "SCADA alarm raised twice, closed against %s" % wo])], p, typo=0)

    def log_psu(self, crew, serials):
        p = self.who(crew)
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
        return self.finish([self.one(opts)], p, typo=0.002)

    def ewaste(self, crew, sub, counts, contract, manifest):
        """retired equipment from a station rebuild leaving for the e-waste processor"""
        p = self.who(crew)
        items = ", ".join(("%d %s" % (n, m) if n > 1 else m) + (" relays c/w PSUs" if m == "VPR-340" else "")
                          for m, n in counts)
        return self.finish([self.one(["retired P&C equipment from %s rebuild to e-waste" % sub,
                                      "%s rebuild: old panels and relays shipped for recycling" % sub,
                                      "e-waste pickup, %s rebuild equipment" % sub]),
                            "%s, manifest %s" % (contract, manifest), items], p, typo=0)

    # ------------------------------------------------------------- other corrective work

    FAULT = {
        ("relay", "CPU"): (["relay locked up", "CPU self-test failure", "relay fail alarm, processor fault on front panel",
                            "relay rebooting, processor error logged", "self-test error E%d" % 0],
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

    def _symptom(self, kind, comp):
        sym, _ = self.FAULT[(kind, comp)]
        s = self.one(sym)
        if "E0" in s:
            s = "self-test error E%d" % self.r.choice([12, 14, 21, 33, 47, 52])
        if comp == "IO" and self.r.random() < 0.3:
            s += " (%s %d)" % (self.one(["input", "IN", "output", "OUT"]), self.r.randint(1, 16))
        if comp == "COMMS" and self.r.random() < 0.25:
            s += ", port %d" % self.r.randint(1, 4)
        return s

    def fault(self, crew, kind, comp, bay, warranty=False, recovered=False):
        p = self.who(crew)
        _, act = self.FAULT[(kind, comp)]
        parts = [self.maybe(0.5, self.bay(p, bay)) if kind != "rtu" else "", self._symptom(kind, comp), self.one(act)]
        if warranty:
            parts.append(self.one(["under warranty", "warranty claim raised", "card under warranty"]))
        elif recovered:
            parts.append(self.one(["card from recovered spares", "used recovered card", "spare card ex rebuild"]))
        parts.append(self.one(self.TEST[kind]))
        return self.finish(parts, p)

    def nff(self, crew, kind, bay):
        p = self.who(crew)
        opts = {"relay": ["relay fail alarm, reset and monitored, no fault found", "spurious relay alarm, event records reviewed, nothing found",
                          "alarm cleared on arrival, no fault found", "loose wiring at panel terminal, retightened",
                          "relay alarm, SER shows DC dip at %s, no fault found" % self.clock()],
                "recloser": ["recloser control alarm, battery and charger checked, no fault found",
                             "control alarm cleared on arrival, no fault found"],
                "rtu": ["RTU alarm investigated, points checked with control room, no fault found", "RTU comms fail alarm, cleared, nothing found"]}[kind]
        return self.finish([self.maybe(0.4, self.bay(p, bay)) if kind != "rtu" else "", self.one(opts)], p)

    def awaiting(self, crew, kind, comp, part, maker, hold, bay):
        p = self.who(crew)
        return self.finish([self.maybe(0.4, self.bay(p, bay)) if kind != "rtu" else "", self._symptom(kind, comp),
                            self.one(["awaiting replacement %s from %s" % (part, maker), "%s on order from %s" % (part, maker),
                                      "waiting on %s %s" % (maker, part)]), hold], p)

    def log_part(self, crew, part, maker, warranty):
        p = self.who(crew)
        return self.finish([self.one(["return failed %s to %s under warranty" % (part, maker),
                                      "warranty return, %s to %s" % (part, maker)]) if warranty else
                            self.one(["ship failed %s to %s for repair" % (part, maker), "send %s to %s for repair" % (part, maker),
                                      "%s repair return, %s" % (maker, part)])], p, typo=0.002)

    # ------------------------------------------------------------- station DC, breakers and instrument transformers

    def dc_fault(self, crew, kind, name):
        p = self.who(crew)
        if kind == "battery":
            sym = ["%s low cell voltage, cell %d at %.2f V" % (name, self.r.randint(1, 60), self.r.uniform(1.98, 2.09)),
                   "%s cell jar cracked, electrolyte on stand" % name, "battery ground alarm, traced to %s" % name,
                   "%s failed impedance limits on %d cells" % (name, self.r.randint(2, 5))]
            act = ["cells replaced", "jar replaced and stand cleaned", "ground cleared, cell connector replaced",
                   "cells replaced, equalize charge applied"]
        else:
            sym = ["%s fail alarm" % name, "%s output low, battery on discharge" % name, "%s AC fail alarm, breaker tripped" % name,
                   "%s float voltage high (%.1f V)" % (name, self.r.uniform(136.5, 139.8))]
            act = ["control board replaced", "charger reset and float adjusted", "rectifier module replaced",
                   "AC breaker reset, charger checked", "replaced charger fan and board"]
        return self.finish([self.one(sym), self.one(act), self.maybe(0.5, self.one(["DC system checked", "alarm cleared",
                                                                                      "control room advised"]))], p)

    def cb_fault(self, crew, bay):
        p = self.who(crew)
        b = self.bay(p, bay)
        sym = ["%s breaker failed to trip on test" % b, "%s trip coil open circuit" % b, "%s CB fail alarm" % b,
               "%s breaker slow to open, %.0f ms" % (b, self.r.uniform(78, 140)), "%s trip circuit supervision alarm" % b]
        act = ["trip coil replaced", "aux contact replaced", "mechanism lubed and retimed", "wiring fault at CB fixed",
               "trip coil and aux switch replaced"]
        return self.finish([self.one(sym), self.one(act), self.one(["trip tested OK", "timing within limits", "returned to service"])], p)

    def vt_fault(self, crew, name):
        p = self.who(crew)
        return self.finish([self.one(["%s fuse blown, loss of potential alarm" % name, "%s secondary fuse failed" % name,
                                      "LOP alarm, %s fuse" % name]),
                            self.one(["fuse replaced", "fuses replaced, voltages checked", "fuse replaced, relays checked for LOP",
                                      "fuse replaced, Va %.1f Vb %.1f Vc %.1f" % tuple(self.r.uniform(65.8, 67.4) for _ in range(3))])], p)

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

    def pm_note(self, key):
        r = self.r
        notes = {
            "relay": ["as found OK", "trip ckt OK, targets reset", "settings verified against approved file", "minor: lamp replaced",
                      "%d alarms in SER reviewed, OK" % r.randint(1, 6), "as found/as left OK", "self-test log clear",
                      "firmware version recorded", "trip test OK, CB opened in %.1f cyc" % r.uniform(2.6, 3.8)],
            "rtu": ["all points OK", "%d status points relabelled" % r.randint(1, 4), "analog cal OK", "points verified with control room"],
            "recloser": ["battery load test OK", "battery replaced", "control OK", "battery %d yrs old, OK" % r.randint(1, 4)],
            "batt_q": ["all cells OK", "pilot cell SG %.3f" % r.uniform(1.205, 1.225), "%d cells low, equalized" % r.randint(1, 3),
                       "electrolyte topped up", "float %.1f V" % r.uniform(131.2, 134.8), "connectors retorqued", "ground detector OK"],
            "batt_a": ["impedance within 20% of baseline", "%d cells trending up, watch" % r.randint(2, 4), "all cells within limits",
                       "intercell resistance OK"],
            "charger": ["float and equalize settings OK", "alarms tested OK", "fan replaced", "output %.1f V float" % r.uniform(131.5, 134.5)],
            "cb": ["trip from relay OK", "trip time %.1f cyc" % r.uniform(2.5, 3.6), "both trip coils OK", "close/trip OK"],
            "ct": ["ratio and polarity OK", "insulation OK", "burden OK"],
            "vt": ["secondary volts balanced", "fuses checked OK", "LOP alarm tested"],
        }
        return self.one(notes[key])

    def pm(self, crew, cls, when, note_p=0.35, **kw):
        t = self.pm_title(cls, when, **kw)
        key = "relay" if cls == "relay_txbus" else cls
        if self.r.random() < note_p:
            note = self.finish([self.pm_note(key)], self.who(crew), typo=0.003)
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
                        "relay targets reset on F-bays", "minor: label missing on panel %d" % self.r.randint(1, 9),
                        "bldg temp %d C" % self.r.randint(14, 27)],
                 "ds": ["no defects", "annunciator test OK", "fence gate latch broken, reported", "kiosk heater not working",
                        "all alarms clear", "rodent droppings in control kiosk, reported", "batt float %.1f V" % self.r.uniform(131.0, 134.5)],
                 "events": ["no misoperations found", "%d events reviewed with protection engineering" % self.r.randint(1, 4),
                            "all events correct"],
                 "ir": ["no hot spots", "hot terminal on TB%d, retorqued" % self.r.randint(1, 9), "all within limits"]}[kind]
        if self.r.random() < note_p:
            return title + self.one([" - ", ". ", ", "]) + self.finish([self.one(notes)], self.who(crew), typo=0.003)
        return title

    def audit(self, crew, bay, model, when):
        old = (when.year, when.month, when.day) < PM_REVISED
        title = ("Settings audit %s: as-left settings against approved file" % bay if old else
                 "SETTINGS AUDIT %s %s" % (bay, model))
        if self.r.random() < 0.3:
            note = self.one(["no differences", "settings match approved file", "1 difference, approved file updated",
                             "group 2 found active, returned to group 1", "event report settings differ, corrected",
                             "file revision on relay older than library, reloaded"])
            return title + self.one([" - ", ". ", "; "]) + self.finish([note], self.who(crew), typo=0.003)
        return title

    def storm_check(self, crew, day):
        p = self.who(crew)
        return self.finish([self.one(["post-storm station check", "storm check after %s" % day, "post-storm visit",
                                      "station check after the %s storm" % day]),
                            self.one(["alarms reviewed and reset", "targets recorded and reset", "no damage, alarms reset",
                                      "SER downloaded, targets reset", "all clear"])], p)

    def settings(self, crew, bay, study, when):
        p = self.who(crew)
        b = self.bay(p, bay) if bay else ""
        return self.finish([self.one(["settings change per protection coordination study %s" % study,
                                      "revised %s settings per study %s" % (b, study) if b else "revised settings per study %s" % study,
                                      "new settings issued under %s, applied and tested" % study,
                                      "applied settings file from %s" % study])], p, typo=0.002)

    def firmware(self, crew, rel):
        p = self.who(crew)
        return self.finish([self.one(["firmware update to vendor release %s" % rel, "firmware upgraded to %s" % rel,
                                      "update firmware %s per vendor notice" % rel])], p, typo=0.002)

    def reissue(self, crew, bay):
        p = self.who(crew)
        b = self.bay(p, bay) if bay else ""
        return self.finish([self.one(["settings file reissued after feeder reconfiguration",
                                      "%s settings reissued after load transfer" % b if b else "settings reissued after load transfer",
                                      "settings group changed for feeder reconfiguration"])], p, typo=0.002)

    def held(self, crew, study):
        return self.finish(["settings change on hold pending revised coordination study %s" % study], self.who(crew), typo=0)
