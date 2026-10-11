"""How Tarrock's P&C crews write up their work orders. Each crew has a few people who do the paperwork, and each
person has habits: sentence case, all capitals or all lower case, their own separators and abbreviations, how a bay
gets written, whether a reading or a time goes in, the odd typo. A crew also has its own shorthand, picked up from
working together: the word it uses for a relay, a card, a breaker or the control room, how it says a part was changed
or reclosing was blocked, and the handful of ways it tends to word a job, so the same clause comes back on one crew's
work orders and reads differently on another's. What they write comes from the job: the alarm, what the relay and the
PSU showed, the readings taken, the spare used, the tests done; an odd symptom turns up once or twice, not as a
stock phrase. The PM and inspection titles come from the EAM job plans, which were reworded when the PM masters were
revised in mid-2023."""
import random
import re

PM_REVISED = (2023, 7, 1)

ABBR = [("power supply", "p/s"), ("replaced", "repl"), ("returned to service", "RTS"),
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

# a crew's shorthand: the word the people on one crew use for a thing, with how common each choice is across crews
TERMS = {
    "relay": (("relay", 4), ("IED", 3), ("prot relay", 2)),
    "rep": (("replaced", 3), ("changed", 3), ("changed out", 2), ("swapped", 2), ("swapped out", 1)),
    "repv": (("replaced", 3), ("changed", 3), ("changed out", 2), ("swapped out", 2)),
    "card": (("card", 3), ("board", 3), ("module", 2)),
    "cpu": (("processor", 3), ("CPU", 3), ("main processor", 1), ("proc", 1)),
    "io": (("IO", 3), ("I/O", 3), ("input/output", 1)),
    "comms": (("comms", 4), ("comm", 2), ("communications", 1), ("com", 1)),
    "net": (("network", 3), ("LAN", 2), ("station LAN", 1), ("ethernet", 2)),
    "scada": (("SCADA", 5), ("control centre", 1), ("SCADA master", 1)),
    "master": (("master", 3), ("the master", 2), ("SCADA master", 2), ("front end", 1)),
    "lost": (("lost", 3), ("no", 2), ("loss of", 2)),
    "panel": (("front panel", 3), ("HMI", 2), ("faceplate", 2), ("fascia", 1)),
    "disp": (("display", 3), ("LCD", 3), ("screen", 2)),
    "garbled": (("garbled", 3), ("scrambled", 2), ("unreadable", 2), ("corrupted", 1)),
    "ok": (("OK", 5), ("good", 2), ("normal", 1)),
    "tested": (("tested", 4), ("checked", 3), ("proven", 1)),
    "rts": (("returned to service", 3), ("back in service", 3), ("RTS", 2), ("put back in service", 1)),
    "cb": (("breaker", 4), ("CB", 4), ("bkr", 1)),
    "fixed": (("fixed", 3), ("repaired", 3), ("made good", 1), ("corrected", 2)),
    "stuck": (("stuck", 3), ("stuck on", 2), ("frozen", 2), ("latched", 1), ("hung", 1)),
    "until": (("until", 4), ("till", 3), ("pending", 1)),
    "back": (("back", 3), ("back in", 2), ("restored", 2), ("repaired", 1)),
    "reclose": (("reclosing", 3), ("reclose", 3), ("auto-reclose", 1), ("79", 1)),
    "blocked": (("blocked", 3), ("off", 2), ("disabled", 2), ("turned off", 1)),
    "selftest": (("self-test", 4), ("self test", 3), ("diagnostics", 1), ("diags", 1)),
    "cr": (("control room", 3), ("System Control", 3), ("ctrl centre", 1), ("SCC", 1)),
    "advised": (("advised", 3), ("notified", 3), ("informed", 1), ("told", 1)),
    "restarts": (("restarts", 3), ("reboots", 3), ("resets", 2)),
    "powers": (("powers up", 3), ("boots", 3), ("comes up", 2)),
    "drops": (("drops out", 3), ("dies", 2), ("shuts down", 2), ("drops off", 1)),
    "burnt": (("burnt", 4), ("burned", 2), ("scorched", 1), ("cooked", 1)),
    "smell": (("burnt smell", 3), ("burning smell", 3), ("smell of burning", 1), ("burnt odour", 1)),
    "open": (("open circuit", 3), ("o/c", 2), ("open", 2), ("burnt open", 1)),
    "lubed": (("lubed", 3), ("lubricated", 2), ("greased", 2)),
    "retimed": (("retimed", 3), ("timing rechecked", 2), ("re-timed", 1)),
    "wiring": (("wiring", 3), ("wire", 2), ("cabling", 1), ("connection", 2)),
    "term": (("panel terminal", 3), ("terminal block", 2), ("TB", 2), ("panel TB", 1)),
    "spares": (("spares", 4), ("stock", 2), ("spares stock", 1)),
    "salv": (("recovered", 4), ("salvaged", 3), ("harvested", 1)),
    "nff": (("no fault found", 4), ("nothing found", 3), ("no fault found on test", 1), ("fault not found", 1)),
    "checked": (("checked", 4), ("verified", 3), ("confirmed", 1)),
    "warranty": (("under warranty", 4), ("warranty", 2), ("covered by warranty", 1)),
    "ship": (("ship", 3), ("send", 3), ("courier", 2), ("return", 2)),
    "forrep": (("for repair", 3), ("to be repaired", 2), ("for repair and return", 1), ("on repair order", 1)),
    "rma": (("RMA return", 3), ("RMA shipment", 2), ("return under RMA", 2), ("RMA", 1)),
    "failed": (("failed", 4), ("faulty", 3), ("defective", 2), ("bad", 1)),
    "alarm": (("alarm", 5), ("alarm in", 2), ("alarm came in", 1)),
    "paged": (("paged", 3), ("called out", 3), ("called in", 1)),
    "event": (("event records", 3), ("events", 2), ("SER", 2)),
    "dl": (("downloaded", 3), ("pulled", 3), ("saved", 2)),
    "folder": (("stn folder", 3), ("station folder", 2), ("the shared drive", 1), ("the P&C share", 1)),
    "dark": (("dark", 4), ("dead", 3), ("blank", 1)),
    "spare": (("spare", 5), ("spare unit", 2), ("stock unit", 1)),
    "fitted": (("fitted", 3), ("installed", 3), ("put in", 2)),
    "returns": (("returns", 4), ("returns shelf", 3), ("RMA shelf", 1)),
    "tag": (("tagged", 4), ("labelled", 2), ("marked", 1)),
    "bagged": (("bagged and tagged", 3), ("bagged", 2), ("boxed and tagged", 1)),
    "removed": (("removed", 4), ("pulled", 3), ("out", 1)),
    "pull": (("removed", 4), ("pulled", 4), ("took out", 1)),
    "prot": (("protection", 3), ("prot", 3)),
    "busprot": (("bus diff", 3), ("bus differential", 2), ("the bus zone", 1)),
    "inserv": (("in service", 3), ("on", 2), ("active", 1), ("covering", 1)),
    "sfile": (("file", 3), ("approved file", 3), ("settings file", 1)),
    "cleared": (("cleared", 3), ("reset", 2), ("gone", 2)),
    "notop": (("not operating", 3), ("not closing", 2), ("dead", 1), ("not picking up", 1)),
    "cracked": (("cracked", 3), ("split", 2), ("broken", 1), ("leaking", 1)),
    "tcs": (("trip circuit supervision", 3), ("TCS", 3), ("trip ckt supervision", 1)),
    "lop": (("loss of potential", 3), ("LOP", 3), ("loss of PT", 1)),
    "scrapped": (("scrapped", 4), ("to e-waste", 3), ("written off", 1)),
    "input": (("input", 3), ("contact", 2), ("indication", 2), ("point", 1)),
    "resetthen": (("reset then", 3), ("reset first, then", 2), ("reset did not hold,", 1), ("tried a reset, then", 1), ("power cycled, then", 1)),
    "openv": (("open", 3), ("trip", 2), ("clear", 1)),
    "answer": (("not answering", 3), ("not responding to", 2), ("ignoring", 1), ("timing out on", 1)),
    "polls": (("polls", 3), ("SCADA polls", 2), ("the master", 1), ("poll requests", 1)),
    "coil": (("trip coil", 4), ("TC", 1), ("trip coil TC1", 1)),
    "aux": (("aux contact", 3), ("aux switch", 2), ("52a contact", 1)),
    "bench": (("bench check", 3), ("bench test", 2), ("bench", 1), ("inspection", 1)),
    "sent": (("sent", 3), ("shipped", 2), ("worth sending", 1)),
    "ber": (("BER", 3), ("beyond repair", 2), ("not repairable", 2)),
    "pickup": (("e-waste pickup", 3), ("e-waste collection", 2), ("recycler pickup", 1)),
    "cage": (("e-waste cage", 3), ("e-waste bin", 2), ("scrap cage", 1)),
    "onat": (("on", 3), ("at", 2), ("after", 2)),
    "scadashows": (("SCADA", 3), ("SCADA shows", 2), ("SCADA reports", 2), ("SCADA:", 1)),
    "noleds": (("no LEDs", 3), ("LEDs out", 2), ("no lights", 1), ("LEDs dark", 1)),
    "fault": (("fault", 3), ("problem", 1), ("issue", 1)),
    "mech": (("mechanism", 3), ("mech", 2), ("operating mechanism", 1)),
    "underrma": (("under RMA", 3), ("on RMA", 2), ("under an RMA", 1)),
    "backin": (("in service", 3), ("back in", 2), ("on line", 1)),
    "clr": (("clear", 3), ("cleared", 2), ("reset", 1)),
    "jar": (("jar", 3), ("case", 2), ("container", 1)),
    "oldrelay": (("old relay", 3), ("retired relay", 2), ("a scrapped relay", 1), ("rebuild stock", 1)),
    "tripout": (("trip output", 3), ("trip contact", 2), ("TRIP OUT", 1)),
    "exv": (("ex", 3), ("back from", 2), ("returned from", 1)),
    "compared": (("compared to", 3), ("checked against", 2), ("matched to", 1)),
    "clearout": (("clear-out", 3), ("cleanup", 2), ("emptied", 1)),
    "failtrip": (("failed to trip", 3), ("would not trip", 2), ("did not open", 2), ("no trip", 1)),
    "ontest": (("on test", 3), ("when tested", 2), ("during test", 1)),
    "analog": (("analog input", 3), ("AI", 2), ("analog point", 1)),
    "drifting": (("drifting", 3), ("wandering", 1), ("reading high", 1)),
    "putin": (("put in", 3), ("fitted", 2), ("installed", 2)),
    "followup": (("follow-up WO", 3), ("f/u WO", 2), ("next WO", 1), ("a follow-up", 1)),
    "failedv": (("failed", 3), ("failing", 2), ("fails", 1)),
    "resetv": (("reset", 3), ("restarted", 2), ("power cycled", 1)),
    "adjusted": (("adjusted", 3), ("set", 2), ("trimmed", 1)),
    "log": (("log", 3), ("event log", 2), ("record", 1)),
    "trippedv": (("tripped", 3), ("opened", 2), ("operated", 1)),
    "off": (("off", 3), ("out", 3), ("dark", 1)),
    "an_rma": (("an RMA", 3), ("sending back", 2), ("the repair cost", 1)),
    "toveldtek": (("to Veldtek", 3), ("back to Veldtek", 2), ("for repair", 2)),
    "corroded": (("corroded", 3), ("eaten away", 1), ("rotted", 1)),
    "inputst": (("input", 3), ("input stage", 2), ("front end", 1)),
    "repcentre": (("repair centre", 3), ("service centre", 2), ("repair depot", 1)),
}


class Voice:
    """one crew's shorthand: a word for each thing, and the share of the ways of wording a job the crew falls into"""

    def __init__(self, name, seed):
        r = random.Random("voice-%s-%d" % (name, seed))
        self.pick = {}
        for k in sorted(TERMS):
            opts = TERMS[k]
            rk = random.Random("voice-%s-%s-%d" % (name, k, seed))
            self.pick[k] = rk.choices([v for v, _ in opts], [w for _, w in opts])[0]
        self.share = r.choice([0.25, 0.3, 0.35])
        self.seed = r.randrange(1 << 30)

    def fill(self, text):
        return re.sub(r"\{(\w+)\}", lambda m: self.pick.get(m.group(1), m.group(0)), text)


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
        self.voice = None

    def vocab(self, slot, opts, wide=False):
        """the ways of saying a thing this person reaches for: most of their crew's own share of what the crews say, or
        for the short stock words of a trade (a part changed, a test passed) their own share of all of them"""
        if wide:
            rw = random.Random("%d-%s-w" % (self.seed, slot))
            mine = [o for o in opts if rw.random() < 0.6]
            return mine or [opts[rw.randrange(len(opts))]]
        rc = random.Random("%d-%s" % (self.voice.seed, slot))
        pool = [o for o in opts if rc.random() < self.voice.share] or [opts[rc.randrange(len(opts))]]
        rr = random.Random("%d-%s" % (self.seed, slot))
        mine = [o for o in pool if rr.random() < 0.75]
        return mine or [pool[rr.randrange(len(pool))]]


# hours a crew books for the round trip to site, and its pace on the job, are in extracts.CREW; who on a crew does the
# paperwork is drawn here, each crew three to five people with the lead doing most of it
CREWS = ["Lakeshore P&C 1", "Lakeshore P&C 2", "Ridge P&C", "Valley P&C 1", "Valley P&C 2", "Harbour P&C", "Harbour Test",
         "North P&C 1", "North P&C 2", "Central P&C 1", "Central P&C 2", "Central P&C 3", "South P&C 1", "South P&C 2"]

# odd symptoms a crew writes down when it sees them, which is once or twice across the fleet
RARE_FINDS = ["{relay} {restarts} when panel door closed", "%(psu)s fuse blown, replaced fuse, blew again",
              "{relay} only stays up with panel door open", "%(psu)s buzzing, output hunting",
              "{relay} came up on DC reset then dropped again", "%(psu)s output fine cold, collapses when warm",
              "{relay} drops out when %(b)s breaker trips", "fuse holder on %(psu)s cracked and blackened",
              "%(psu)s faceplate screws loose, board shifted", "{relay} trips its own DC breaker on power up",
              "PWR LED flickers in time with charger ripple", "%(psu)s connector pins discoloured"]

PLURAL = {"PSU": "PSUs", "p/s": "p/s", "power supply": "power supplies", "PS module": "PS modules",
          "supply module": "supply modules", "PSU card": "PSU cards", "power supply card": "power supply cards"}
# how a crew covers for a device it is waiting on a part for
HOLDS = {"relay": ["backup {prot} in service", "on backup {prot} meantime", "bus backup covering", "backup {prot} covering till part in"],
         "rtu": ["affected points on manual reporting", "points on manual {until} card in", "{cr} on manual readings meantime"],
         "recloser": ["recloser left on non-reclose", "recloser on non-reclose meantime", "{reclose} {blocked} {until} part in"]}

# what the bench check at a store finds on a failed module it does not send for repair
SCRAP_FINDS = {
    "burnt": ["{inputst} {burnt}", "board {burnt} at the {inputst}", "{burnt} input stage, not repairable",
              "input bridge and FETs {burnt}", "{burnt} through at the {inputst}"],
    "charred": ["PCB charred under the bulk caps", "board charred", "charring on PCB at DC-DC stage", "board charred through",
                "charred tracks under the caps"],
    "vented": ["bulk caps vented, board contaminated", "caps vented, electrolyte over the board", "caps blown, board contaminated",
               "bulk caps let go, board fouled"],
    "corroded": ["electrolyte leak, tracks {corroded}", "tracks {corroded} under the caps", "leaked caps, corrosion on board",
                 "corrosion from leaking caps"],
    "transformer": ["main transformer {burnt}", "transformer open, {burnt}", "transformer {burnt} out", "transformer winding open"],
    "cracked": ["board cracked, connector torn off", "PCB cracked at the mounting", "connector broken off the board",
                "board cracked in removal"],
    "water": ["water damage, board corroded", "moisture damage, corrosion on board", "water marks and corrosion",
              "kiosk leak, board corroded"],
    "surge": ["surge damage, MOV and bridge blown", "lightning damage, input blown", "surge, MOV split and input fuse blown",
              "storm surge, input stage blown"],
    "repeat": ["failed again after Veldtek repair", "second failure since repair", "failed again since the last repair",
               "already repaired once, failed again"],
}


class Writer:
    def __init__(self, seed):
        self.r = random.Random(seed)
        rp = random.Random(seed * 31 + 7)
        self.people = {}
        for c in CREWS:
            k = rp.randint(3, 5)
            w = [rp.random() + (1.5 if j == 0 else 0.2) for j in range(k)]
            v = Voice(c, seed)
            ppl = [Person(rp) for _ in range(k)]
            for p in ppl:
                p.voice = v
            self.people[c] = (ppl, w)
        self.wrong_bays = 0
        self.used = {}

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
        if self.r.random() < 0.01 and n > 1:
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

    def say(self, p, slot, opts, wide=False):
        return self.one(p.vocab(slot, opts, wide))

    def rare(self, opts, cap=2):
        """an odd symptom nobody has written down more than `cap` times yet, or None"""
        free = [o for o in opts if self.used.get(o, 0) < cap]
        if not free:
            return None
        o = self.one(free)
        self.used[o] = self.used.get(o, 0) + 1
        return o

    def clock(self):
        h = self.one(list(range(0, 24)), [2] * 6 + [1] * 2 + [3] * 10 + [2] * 6)
        return self.one(["%02d:%02d", "%02d%02d", "%02d:%02dh"]) % (h, self.r.randrange(60))

    LEDS = ["ALARM", "ENABLED", "RELAY OK", "IN SVC", "PWR", "TRIP", "TEST"]
    STATES = ["flashing", "on solid", "red", "out", "off", "flickering", "amber", "blinking"]
    DEAD = ["all LEDs off", "{noleds}", "{panel} {dark}", "{disp} blank, {noleds}", "PWR LED off", "ENABLED and PWR LEDs out",
            "{relay} {dark}", "nothing on the {panel}", "IN SVC LED {off}, {disp} blank", "no lights on {relay}", "LEDs all out",
            "{relay} completely dead", "panel {dark}", "{disp} off", "{relay} front {dark}", "no power to {relay}",
            "{panel} blank", "{disp} and LEDs dead", "dead {relay}", "PWR LED out, {disp} dead", "{relay} off, {disp} blank",
            "{disp} blank and no LEDs", "no LEDs or {disp}", "{relay} showing nothing", "{disp} dead, {noleds}", "fascia dark",
            "{panel} totally dead", "no PWR LED, no {disp}"]

    def led(self, p, dead):
        if dead:
            return self.say(p, "dead", self.DEAD)
        a, b = self.r.sample(self.LEDS, 2)
        s1, s2 = self.one(self.STATES), self.one(self.STATES)
        return self.say(p, "part", ["%s LED %s" % (a, s1), "%s LED %s, %s %s" % (a, s1, b, s2), "%s lamp %s" % (a, s1),
                                     "%s %s" % (a, s1), "{disp} frozen, %s LED %s" % (a, s1), "{disp} flickering, %s %s" % (a, s1),
                                     "{disp} {garbled}, %s %s" % (a, s1), "%s and %s LEDs %s" % (a, b, s1)])

    def dc(self, p, volts):
        nominal = {48: (51.6, 54.2), 125: (127.8, 134.6), 250: (256.0, 268.5)}[volts]
        v = round(self.r.uniform(*nominal), 1)
        tb = "TB%d-%d/%d" % (self.r.randint(1, 3), self.r.randint(1, 12), self.r.randint(13, 24))
        return self.say(p, "dc", ["%.1f VDC at %s" % (v, tb), "DC at terminals %.1f V" % v, "%.1fV DC in" % v,
                                  "station DC {ok} (%.1f V)" % v, "%.1f V at {relay} DC input" % v, "DC input %.1fV {ok}" % v,
                                  "measured %.1f VDC at {relay}" % v, "batt volts at panel %.1f" % v, "DC supply %.1fV" % v,
                                  "%.1f V on %s" % (v, tb), "input %.1f VDC" % v, "DC {ok} at %.1f V" % v])

    def rails(self, p):
        five = self.one(["0.0", "0.2", "0.4", "1.1", "2.8", "3.6", "4.1", "4.4"])
        tw = self.one(["0.0", "3.2", "6.3", "11.4", "14.8", "17.9", "19.2", "21.0"])
        return self.say(p, "rails", ["+5V rail %sV" % five, "5 V out %s" % five, "+24V rail %s V" % tw, "+5 %s / +24 %s" % (five, tw),
                                     "PSU output %s V on 5V test point" % five, "24V rail sagging to %s V" % tw,
                                     "5V TP reads %s" % five, "+24 out %sV" % tw, "outputs %s/%s V" % (five, tw),
                                     "5V rail dropping to %s" % five, "24 V rail %s, should be 24" % tw])

    def finish(self, parts, p, typo=None):
        """join the pieces the way this person writes, in their crew's words"""
        seen, uniq = set(), []
        for x in parts:
            x = p.voice.fill(x).strip() if x else ""
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
            keep = r"(PS02-\d\d-\d+|WO\d+|RMA-\d+|EW\d\d-\d{4}|SC-\d{4}-\d+|@@[A-Z]+-\d+-\d+@@)"
            out = "".join(seg if re.fullmatch(keep, seg) else seg.lower() for seg in re.split(keep, out))
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
        st = self.store(p, store)
        h0, m0 = self.r.choice([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]), self.r.randrange(60)
        fmt = self.one(["%02d:%02d", "%02d%02d", "%02d:%02dh"])
        t = lambda mins: fmt % (((h0 * 60 + m0 + mins) // 60) % 24, (h0 * 60 + m0 + mins) % 60)
        if storm:
            trig = self.say(p, "storm", ["after the %s storm, %s {relay} {dark}" % (storm, b),
                                         "post-storm patrol %s, %s {relay} fail {alarm}" % (storm, b),
                                         "%s {relay} down after %s storm" % (b, storm), "storm %s, %s {relay} found off" % (storm, b),
                                         "%s storm, found %s {relay} {dark}" % (storm, b),
                                         "storm damage check %s, %s {relay} out" % (storm, b)])
        else:
            alarm = self.say(p, "alarm", ALARMS)
            bare = alarm[6:] if alarm.startswith("relay ") else alarm
            trig = self.say(p, "trig", ["%s {alarm} on %s" % (alarm, b), "{scadashows} %s {alarm} on %s" % (alarm, b),
                                        "%s %s {alarm}" % (b, alarm),
                                        "{cr} called, %s {relay} %s" % (b, self.one(["not responding", "off line", "showing fail",
                                                                                      "no comms", "dropped off"])),
                                        "%s {relay} found {dark} on %s" % (b, self.one(["station visit", "monthly insp", "switching",
                                                                                        "stn check", "patrol"])),
                                        "{cr} call re %s %s" % (b, alarm), "%s alm rec'd %s, %s" % (alarm, t(0), b),
                                        "%s {alarm} at %s on %s" % (alarm, t(0), b), "{paged} for %s %s" % (b, alarm),
                                        "{cr} reports %s %s" % (b, alarm), "%s: %s since %s" % (b, alarm, t(0)),
                                        "%s {alarm} from {scada}, %s" % (alarm, b), "%s {relay} %s" % (b, bare)])
        lead = []
        if em and self.r.random() < 0.55:
            lead.append(self.say(p, "callout", ["call-out", "after hours call-out", "o/t call out", "emergency call", "C/O",
                                                "called in", "standby call", "night call"]))
            if self.r.random() < p.times:
                lead.append(self.say(p, "onsite", ["on site %s" % t(self.r.randint(40, 110)), "arr %s" % t(self.r.randint(40, 110)),
                                                   "at stn %s" % t(self.r.randint(40, 110))]))
        dead = self.r.random() < 0.6
        finds = [self.led(p, dead)]
        if self.r.random() < p.reads:
            finds.append(self.dc(p, volts))
        if self.r.random() < p.reads * 0.8:
            finds.append(self.rails(p))
        if p.detail >= 1 or self.r.random() < 0.5:
            odd = self.rare(RARE_FINDS) if self.r.random() < 0.06 else None
            finds.append(odd % dict(psu=psu, b=b) if odd else self.say(p, "find", [
                "{relay} {restarts} every %d min" % self.r.randint(2, 15), "{relay} cycling on and off",
                "{selftest} log: PS FAIL", "SER shows DC fail at %s" % t(-self.r.randint(1, 9)), "{smell} at %s" % psu,
                "scorch mark on %s board" % psu, "%s caps bulging" % psu, "%s input fuse blown" % psu, "%s fuse {ok}" % psu,
                "%s hot to touch" % psu, "%s dead" % psu, "%s {failed}" % psu, "%s output collapsing under load" % psu,
                "nothing out of %s" % psu, "{relay} {powers} then {drops}", "{relay} dead", "{selftest}: power supply error",
                "event log PWR FAIL at %s" % t(-2), "%s clicking, no output" % psu, "%s smells {burnt}" % psu,
                "electrolytic on %s leaking" % psu, "%s getting hot" % psu, "{relay} {powers}, dies after %d s" % self.r.randint(5, 60),
                "%s output intermittent" % psu, "PS FAIL in {selftest} {log}", "{selftest} shows PS FAIL"]))
        if p.detail == 0 and len(finds) > 2:
            finds = finds[:2]
        hold = self.maybe(0.25 if fitted == "same" else 0.9, self.say(p, "hold", [
            "feeder on backup {prot}", "bus {prot} backing up %s" % b, "%s left on backup" % b,
            "%s {reclose} {blocked} {until} {relay} {back}" % b, "load transferred off %s" % b, "upstream prot covering %s" % b,
            "%s on bus backup" % b, "TS backup {inserv} for %s" % b, "%s on non-reclose {until} repair" % b,
            "%s backed up by {busprot}" % b, "%s {reclose} {blocked} {until} {spare} fitted" % b]))
        sn = p.sn.format(serial) if serial else ""
        if fitted == "same":
            if repaired:
                act = self.say(p, "act_r", [
                    "{repv} %s with repaired unit from %s" % (psu, st), "fitted repaired %s %s" % (psu, sn),
                    "{repv} %s, used refurb {spare} from %s" % (psu, st), "installed Veldtek-repaired %s %s" % (psu, sn),
                    "{repv} %s, {spare} {exv} Veldtek repair %s" % (psu, sn), "swapped %s for repaired {spare} (%s stock)" % (psu, st),
                    "{putin} refurb %s %s" % (psu, sn), "%s {rep}, repaired unit %s" % (psu, sn),
                    "used repaired {spare} from %s, %s" % (st, sn), "refurb %s fitted from %s" % (psu, st)])
            else:
                act = self.say(p, "act_n", [
                    "{repv} %s with new module from %s" % (psu, st), "new %s {fitted} %s" % (psu, sn),
                    "{repv} %s, new unit from %s" % (psu, st), "installed new %s %s" % (psu, sn),
                    "{repv} %s, new %s" % (psu, sn), "swapped in new %s from %s stock" % (psu, st),
                    "put in new %s %s" % (psu, sn), "%s {rep}, new unit %s" % (psu, sn),
                    "new {spare} from %s, %s" % (st, sn), "new %s from %s fitted" % (psu, st)])
            tests = [self.say(p, "test", [
                "trip test {ok}", "trip {tested} {ok}, CB opened %.1f cyc" % self.r.uniform(2.6, 3.6), "secondary injection {ok}",
                "functional test {ok}", "settings {checked} against {sfile}", "settings {checked}, file rev %d" % self.r.randint(2, 9),
                "{selftest} clear", "ENABLED LED on", "trip {checked} to {cb} {ok}", "{trippedv} {cb} from {relay}, {ok}",
                "sec inj {ok}, pickup in tol", "settings {compared} {sfile}, no diffs", "{selftest} passed",
                "alarms clear at {scada}", "{relay} {backin} with alarms {clr}", "test trip {ok}", "RELAY OK LED on",
                "pickup and timing {checked}", "trip test to {cb} %.1f cyc" % self.r.uniform(2.6, 3.6),
                "sec inj all %d elements {ok}" % self.r.randint(3, 6), "{relay} {ok} on power up",
                "settings file rev %d loaded and {checked}" % self.r.randint(2, 9), "{selftest} {ok} after power up",
                "IED up, {selftest} clean", "inputs and outputs {checked}", "test trip from {scada} {ok}"])]
            if p.detail >= 1:
                tests.append(self.say(p, "close", [
                    "{event} {dl}", "{cr} {advised}", "{rts} %s" % t(self.r.randint(90, 300)) if self.r.random() < p.times
                    else "{rts}", "back in service", "SER {dl} to laptop", "{event} saved to {folder}",
                    "{cr} {advised} alarm clear", "RTS %s" % t(self.r.randint(90, 300)),
                    "{relay} back on line %s" % t(self.r.randint(90, 300)), "{scada} points back", "RTS and {cr} {advised}",
                    "closed out with {cr}", "in service %s" % t(self.r.randint(90, 300)), "{scada} confirms {relay} {back}",
                    "{cr} has {relay} back", "alarm reset at {scada}", "released to {cr} %s" % t(self.r.randint(90, 300))]))
            parts = lead + ([act, trig] + finds if p.action_first else [trig] + finds) + [hold] + ([] if p.action_first else [act]) + tests
        else:
            act = self.say(p, "act_l", [
                "no {spare} on truck, %s {removed}, follow-up WO raised to fit {spare}" % psu,
                "{pull} {failed} %s, {spare} to be {fitted} on {followup}" % psu,
                "%s {removed}, {relay} left out of service pending {spare}" % psu, "{failed} %s {removed}, fitting on next WO" % psu,
                "{pull} %s, {spare} coming from %s" % (psu, st),
                ("%s {removed}, {spare} fitted under %s" % (psu, wo_fit)) if wo_fit else ("%s {removed}, {spare} fitted on f/u WO" % psu),
                "%s out, waiting on {spare} from %s" % (psu, st), "no %s in van, pulled {failed} one, f/u to fit" % psu,
                "{pull} %s, {relay} out {until} {spare} fitted" % psu])
            parts = lead + [trig] + finds + [hold, act]
        parts.append(self.maybe(0.2, self.say(p, "extra", [
            "{failed} unit {bagged}", "{failed} %s to %s {returns}" % (psu, st), "tag %d on {failed} unit" % self.r.randint(1000, 9999),
            "{failed} unit to %s {returns}" % st, "old %s {tag} for {returns}" % psu,
            "{failed} %s {tag} %d" % (psu, self.r.randint(1000, 9999))])))
        return self.finish(parts, p)

    def psu_fitting(self, crew, bay, store, serial, repaired, wo_fail):
        p = self.who(crew)
        sn = p.sn.format(serial)
        st = self.store(p, store)
        what = (["fit %s %s (repaired unit)" % (p.words, sn), "install refurb %s %s from %s" % (p.words, sn, st),
                 "fit repaired %s %s" % (p.words, sn), "repaired %s %s fitted" % (p.words, sn), "refurb {spare} in, %s" % sn] if repaired else
                ["fit new %s %s" % (p.words, sn), "install new %s from %s" % (p.words, st),
                 "fit new %s from %s stock, %s" % (p.words, st, sn), "new %s in, %s" % (p.words, sn), "{spare} %s fitted, new" % sn])
        ref = ["follow-up to %s" % wo_fail, "ref %s" % wo_fail, "f/u %s" % wo_fail, "per %s" % wo_fail, "from %s" % wo_fail,
               "see %s" % wo_fail, "cont'd from %s" % wo_fail]
        test = ["{relay} {tested} and {rts}", "trip test {ok}, {rts}", "secondary injection {ok}, RTS",
                "settings {checked}, {relay} in service", "functional test {ok}, {cr} {advised}", "tstd OK, ENABLED on",
                "trip {checked}, {relay} in service", "{selftest} clear, RTS"]
        return self.finish(["%s {relay}" % self.bay(p, bay) if self.r.random() < 0.4 else "", self.say(p, "fit", what),
                            self.say(p, "fitref", ref), self.say(p, "fittest", test)], p)

    def psu_duplicate(self, crew, wo):
        p = self.who(crew)
        return self.finish([self.say(p, "dup", ["duplicate of %s" % wo, "dup WO, see %s" % wo,
                                                "raised twice from {scada} alarm, see %s" % wo, "duplicate, work done on %s" % wo,
                                                "{scada} alarm raised twice, closed against %s" % wo])], p, typo=0)

    def log_psu(self, crew, serials):
        p = self.who(crew)
        if len(serials) == 1:
            s = serials[0]
            opts = ["{ship} {failed} %s %s to Veldtek, RMA requested" % (p.words, p.sn.format(s)),
                    "{ship} %s %s to Veldtek {repcentre}" % (p.words, s),
                    "{ship} {failed} %s %s to Veldtek {underrma}" % (p.words, s), "{rma} {toveldtek}, %s %s" % (p.words, p.sn.format(s)),
                    "{ship} {failed} VPR-340 %s %s to Veldtek for repair" % (p.words, s)]
        else:
            a, b = serials
            many = PLURAL[p.words]
            opts = ["{ship} {failed} %s %s and %s to Veldtek, RMA requested" % (many, a, b),
                    "{ship} 2 %s (%s, %s) to Veldtek {repcentre}" % (many, a, b),
                    "{ship} 2 {failed} VPR-340 %s to Veldtek {underrma}, s/n %s %s" % (many, a, b),
                    "{rma} {toveldtek}, %s %s and %s" % (many, a, b)]
        return self.finish([self.say(p, "logpsu%d" % len(serials), opts)], p, typo=0.002)

    def ewaste(self, crew, sub, counts, contract, manifest):
        """retired equipment from a station rebuild leaving for the e-waste processor. The relays go complete: the
        rebuilds came before Veldtek's end-of-life notice, while new and repaired power supplies were still to be had
        from Veldtek, so nobody kept the modules out of them"""
        p = self.who(crew)
        items = ", ".join(("%d %s" % (n, m) if n > 1 else m) + (" relays c/w PSUs" if m == "VPR-340" else "")
                          for m, n in counts)
        return self.finish([self.one(["retired P&C equipment from %s rebuild to e-waste" % sub,
                                      "%s rebuild: old panels and relays shipped for recycling" % sub,
                                      "e-waste pickup, %s rebuild equipment" % sub]),
                            "%s, manifest %s" % (contract, manifest), items,
                            self.say(p, "ewnote", ["PSUs left in, VPR340-PSU-02 still available new from Veldtek",
                                                   "no PSUs recovered, module still orderable from Veldtek",
                                                   "PSUs not kept as spares, new and repaired units still available from Veldtek",
                                                   "{relay}s went complete with PSUs, PSU still in Veldtek's catalogue",
                                                   "PSUs not pulled for spares, Veldtek still supplying new"])], p, typo=0)

    def scrap(self, crew, store, items, contract, manifest):
        """the disposal work order for a store's e-waste collection: each failed module the store did not send for
        repair, by serial, with what the bench check found"""
        p = self.who(crew)
        st = self.store(p, store)
        n = len(items)
        lead = self.say(p, "scraplead", ["{pickup}, %s returns" % st, "%s {returns} cleared to e-waste" % st,
                                         "{returns} {clearout} %s" % st, "{pickup} at %s" % st,
                                         "%s {cage} collected" % st])
        what = self.say(p, "scrapwhat", ["%d {failed} VPR-340 PSU%s not {sent} {forrep}" % (n, "s" if n > 1 else ""),
                                         "VPR-340 PSU%s {scrapped} after {bench}" % ("s" if n > 1 else ""),
                                         "{ber} {onat} {bench}, not {sent} {toveldtek}",
                                         "%d PSU%s {ber}, not worth {an_rma}" % (n, "s" if n > 1 else ""),
                                         "{bench} done, %d {scrapped}" % n])
        lst = "; ".join("%s %s" % (p.sn.format(s), self.say(p, "scrap_" + f, SCRAP_FINDS[f])) for s, f in items)
        return self.finish([lead, what, lst, "%s, manifest %s" % (contract, manifest)], p, typo=0)

    # ------------------------------------------------------------- other corrective work

    FAULT = {
        ("relay", "CPU"): (["{relay} locked up", "{cpu} {selftest} failure", "{relay} fail alarm, {cpu} fault on {panel}",
                            "{relay} rebooting, {cpu} error logged", "{selftest} error E%d" % 0, "{cpu} watchdog trips, {relay} hangs"],
                           ["{cpu} {card} {rep}", "{cpu} {card} swapped", "{cpu} {card} {rep}, firmware reloaded",
                            "{repv} {cpu} {card}, settings reloaded"]),
        ("relay", "IO"): (["input {card} {failedv} {selftest}", "binary input chatter", "output contact welded",
                           "{cb} status {input} {stuck}", "{tripout} {notop} {ontest}"],
                          ["{io} {card} {rep}", "{repv} {io} {card}", "{io} {card} changed", "{repv} {io} {card}, inputs {checked}"]),
        ("relay", "DISP"): (["{disp} blank", "keypad unresponsive", "{panel} {disp} {garbled}"],
                            ["{panel} {rep}", "{disp} module changed", "{repv} {panel}"]),
        ("relay", "COMMS"): (["{lost} {scada} {comms} to {relay}", "DNP3 link down", "fibre transceiver {failed}",
                              "{relay} dropping off the {net}", "{relay} {answer} {polls}"],
                             ["{comms} {card} {rep}", "{comms} {card} {resetthen} {rep}", "{repv} {comms} {card} and patch lead"]),
        ("relay", "PSU"): (["{relay} power supply {failed}", "PSU fault alarm", "{relay} dead, power supply {failed}"],
                           ["power supply module {rep}", "PSU {rep}", "{repv} power supply"]),
        ("recloser", "PSU"): (["control battery failed load test", "recloser control charger {failed}", "control on battery, no AC charge"],
                              ["battery {rep}", "PSU module {rep}", "charger board {rep}"]),
        ("recloser", "CPU"): (["recloser control locked up", "control {cpu} fault"], ["{cpu} board {rep} and settings loaded"]),
        ("recloser", "IO"): (["trip/close output {failed}", "recloser status input {stuck}"], ["IO board {rep}", "{repv} IO board"]),
        ("recloser", "DISP"): (["control panel {disp} faded"], ["{panel} {rep}"]),
        ("recloser", "COMMS"): (["{lost} radio link to recloser control", "{scada} polling to recloser {failed}"],
                                ["{comms} module {rep}", "radio {rep}", "{comms} module changed"]),
        ("rtu", "CPU"): (["RTU {cpu} {failed}", "RTU locked up"], ["{cpu} {card} {rep}, config reloaded"]),
        ("rtu", "IO"): (["RTU status input {card} {failed}", "RTU {analog} {drifting}", "RTU control output {card} {failed}"],
                        ["{card} {rep}, points {checked} with {cr}", "{card} {rep} and calibrated", "{repv} {card}"]),
        ("rtu", "COMMS"): (["{lost} RTU {comms} to {scada}", "DNP3 link to {master} down"],
                           ["{comms} {card} {rep}", "port {card} {rep}", "modem {rep}"]),
        ("rtu", "PSU"): (["RTU power supply {failed}", "RTU dead, DC {ok}"], ["power supply {rep}, points {checked}"]),
    }
    TEST = {"relay": ["trip {tested}", "settings {checked}", "{tested} {ok}", "secondary injection {ok}", "{rts}"],
            "recloser": ["control {tested}", "settings loaded and {tested}", "test trip/close {ok}"],
            "rtu": ["points {checked} with {cr}", "controls {tested} with {cr}", "back on scan"]}

    def _symptom(self, p, kind, comp):
        sym, _ = self.FAULT[(kind, comp)]
        s = self.say(p, "sym-%s-%s" % (kind, comp), sym)
        if "E0" in s:
            s = s.replace("E0", "E%d" % self.r.choice([12, 14, 21, 33, 47, 52]))
        if comp == "IO" and self.r.random() < 0.3:
            s += " (%s %d)" % (self.one(["input", "IN", "output", "OUT"]), self.r.randint(1, 16))
        if comp == "COMMS" and self.r.random() < 0.25:
            s += ", port %d" % self.r.randint(1, 4)
        return s

    def fault(self, crew, kind, comp, bay, warranty=False, recovered=False):
        p = self.who(crew)
        _, act = self.FAULT[(kind, comp)]
        parts = [self.maybe(0.5, self.bay(p, bay)) if kind != "rtu" else "", self._symptom(p, kind, comp),
                 self.say(p, "act-%s-%s" % (kind, comp), act, wide=True)]
        if warranty:
            parts.append(self.say(p, "warranty", ["{warranty}", "warranty claim raised", "{card} {warranty}"]))
        elif recovered:
            parts.append(self.say(p, "recovered", ["{card} from {salv} {spares}", "used {salv} {card}",
                                                   "{card} {salv} from {oldrelay}", "{salv} {card} out of {spares}"]))
        parts.append(self.say(p, "test-" + kind, self.TEST[kind], wide=True))
        return self.finish(parts, p)

    def nff(self, crew, kind, bay):
        p = self.who(crew)
        opts = {"relay": ["{relay} fail alarm, reset and monitored, {nff}", "spurious {relay} alarm, {event} reviewed, nothing found",
                          "alarm {cleared} on arrival, {nff}", "loose {wiring} at {term}, retightened",
                          "{relay} alarm, SER shows DC dip at %s, {nff}" % self.clock()],
                "recloser": ["recloser control alarm, battery and charger {checked}, {nff}",
                             "control alarm {cleared} on arrival, {nff}"],
                "rtu": ["RTU alarm investigated, points {checked} with {cr}, {nff}", "RTU {comms} fail alarm, {cleared}, nothing found"]}[kind]
        return self.finish([self.maybe(0.4, self.bay(p, bay)) if kind != "rtu" else "", self.say(p, "nff-" + kind, opts)], p)

    def awaiting(self, crew, kind, comp, part, maker, hold, bay):
        p = self.who(crew)
        return self.finish([self.maybe(0.4, self.bay(p, bay)) if kind != "rtu" else "", self._symptom(p, kind, comp),
                            self.say(p, "await", ["awaiting replacement %s from %s" % (part, maker), "%s on order from %s" % (part, maker),
                                                  "waiting on %s %s" % (maker, part)]),
                            self.say(p, "hold-" + kind, HOLDS.get(kind, [hold]))], p)

    def log_part(self, crew, part, maker, warranty):
        p = self.who(crew)
        return self.finish([self.say(p, "logw", ["return {failed} %s to %s {warranty}" % (part, maker),
                                                 "warranty return, %s to %s" % (part, maker)]) if warranty else
                            self.say(p, "logr", ["{ship} {failed} %s to %s {forrep}" % (part, maker),
                                                 "{ship} %s to %s {forrep}" % (part, maker),
                                                 "%s repair return, %s" % (maker, part)])], p, typo=0.002)

    # ------------------------------------------------------------- station DC, breakers and instrument transformers

    def dc_fault(self, crew, kind, name):
        p = self.who(crew)
        if kind == "battery":
            sym = ["%s low cell voltage, cell %d at %.2f V" % (name, self.r.randint(1, 60), self.r.uniform(1.98, 2.09)),
                   "%s cell {jar} {cracked}, electrolyte on stand" % name, "battery ground {alarm}, traced to %s" % name,
                   "%s failed impedance limits on %d cells" % (name, self.r.randint(2, 5))]
            act = ["cells {rep}", "jar {rep} and stand cleaned", "ground {cleared}, cell connector {rep}",
                   "cells {rep}, equalize charge applied"]
        else:
            sym = ["%s fail {alarm}" % name, "%s output low, battery on discharge" % name, "%s AC fail {alarm}, {cb} tripped" % name,
                   "%s float voltage high (%.1f V)" % (name, self.r.uniform(136.5, 139.8))]
            act = ["control {card} {rep}", "charger {resetv} and float {adjusted}", "rectifier module {rep}",
                   "AC {cb} reset, charger {checked}", "{repv} charger fan and board"]
        return self.finish([self.say(p, "dcsym-" + kind, sym), self.say(p, "dcact-" + kind, act),
                            self.maybe(0.5, self.say(p, "dcend", ["DC system {checked}", "alarm {cleared}", "{cr} {advised}"]))], p)

    def cb_fault(self, crew, bay):
        p = self.who(crew)
        b = self.bay(p, bay)
        sym = ["%s {cb} {failtrip} {ontest}" % b, "%s trip coil {open}" % b, "%s {cb} fail {alarm}" % b,
               "%s {cb} slow to {openv}, %.0f ms" % (b, self.r.uniform(78, 140)), "%s {tcs} {alarm}" % b]
        act = ["{coil} {rep}", "{aux} {rep}", "{mech} {lubed} and {retimed}", "{wiring} {fault} at {cb} {fixed}",
               "{coil} and {aux} {rep}"]
        return self.finish([self.say(p, "cbsym", sym), self.say(p, "cbact", act),
                            self.say(p, "cbend", ["trip {tested} {ok}", "timing within limits", "{rts}"], wide=True)], p)

    def vt_fault(self, crew, name):
        p = self.who(crew)
        return self.finish([self.say(p, "vtsym", ["%s fuse blown, {lop} alarm" % name, "%s secondary fuse {failed}" % name,
                                                  "{lop} alarm, %s fuse" % name]),
                            self.say(p, "vtact", ["fuse {rep}", "fuses {rep}, voltages {checked}", "fuse {rep}, relays {checked} for LOP",
                                                  "fuse {rep}, Va %.1f Vb %.1f Vc %.1f" % tuple(self.r.uniform(65.8, 67.4) for _ in range(3))])], p)

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
        return self.finish([self.say(p, "stormchk", ["post-storm station check", "storm check after %s" % day, "post-storm visit",
                                                     "station check after the %s storm" % day]),
                            self.say(p, "stormend", ["alarms reviewed and reset", "targets recorded and reset", "no damage, alarms reset",
                                                     "SER {dl}, targets reset", "all clear"])], p)

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
