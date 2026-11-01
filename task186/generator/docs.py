"""The governing document (the airport's screening officer competency standard) and the library's object wording."""
import io_util as IO

BASES = {
    "FA": ["semi-automatic pistol, polymer frame", "semi-automatic pistol, steel frame", "revolver", "derringer",
           "pistol slide and barrel", "pistol frame, stripped", "rifle bolt carrier", "shotgun receiver",
           "magazine, double stack", "magazine, single stack", "ammunition, loose rounds", "flare pistol",
           "replica pistol, metal", "starting pistol", "air pistol", "pistol barrel"],
    "KB": ["folding knife", "lock-blade knife", "fixed-blade knife", "kitchen knife", "ceramic knife",
           "utility knife, snap-off blade", "box cutter", "multi-tool with locking blade", "scissors, long blades",
           "machete", "cleaver", "throwing star", "push dagger", "razor blades, packet", "letter opener, metal",
           "bread knife", "filleting knife", "karambit"],
    "IE": ["electric detonator", "non-electric detonator", "battery pack with leads", "timer module",
           "simulant block, plastic explosive", "simulant sheet explosive", "initiator board", "safety fuse coil",
           "switch and wiring harness", "simulant cast charge", "pressure switch", "mobile phone wired to battery",
           "relay board", "simulant powder charge"],
    "OP": ["claw hammer", "screwdriver, 20 cm", "socket wrench", "adjustable spanner", "crowbar", "pepper spray",
           "conducted energy device", "knuckle duster", "telescopic baton", "cricket bat", "golf club head",
           "hand axe", "chisel", "lighter fluid can", "fireworks, assorted", "bear spray", "nunchaku",
           "tyre lever"],
}
SIZES = {"FA": ["9 mm", ".22", ".38", "compact", "full size", "subcompact", "", "", ""],
         "KB": ["6 cm blade", "8 cm blade", "9 cm blade", "11 cm blade", "14 cm blade", "18 cm blade", "", ""],
         "IE": ["in laptop", "in toiletry bag", "in shoe", "loose", "in torch body", "in book", "", ""],
         "OP": ["", "", "small", "large", "steel", "aluminium", "wooden handle", ""]}


def object_descriptions(world, rng):
    out = []
    used = {}
    for i in range(len(world.obj_code)):
        c = world.obj_cat[i]
        base = BASES[c][int(rng.integers(len(BASES[c])))]
        size = SIZES[c][int(rng.integers(len(SIZES[c])))]
        text = base + (", " + size if size else "")
        used[text] = used.get(text, 0) + 1
        if used[text] > 1:
            text = "%s (%s)" % (text, ["second item", "third item", "fourth item", "fifth item", "sixth item",
                                         "seventh item", "eighth item"][min(used[text] - 2, 6)])
        out.append(text[0].upper() + text[1:])
    return out


def standard(path):
    b = [
        ("t", "SCS-04 Screening officer competency standard"),
        ("s", "Silverwattle Coast Airport, Security Screening. Revision 6, approved by Teresa Malone, Head of "
              "Security Screening, on 14 July 2025, for the CT lanes. Supersedes revision 5 (March 2023), which "
              "covered the conventional X-ray lanes. Review due July 2027."),
        ("h", "1. Purpose"),
        ("p", "Passengers' cabin bags are screened at the X-ray screen of a CT lane. This standard sets what the "
              "airport expects of the screening officers who work at that screen, how their performance and "
              "currency are judged, and what happens when an officer falls short."),
        ("h", "2. Scope"),
        ("p", "Every screening officer who holds an X-ray endorsement. The domestic checkpoint has five CT lanes, "
              "D1 to D5, and the international checkpoint two, I1 and I2."),
        ("h", "3. Terms"),
        ("table", [["Term", "Meaning"],
                   ["Detection performance", "The probability that the officer detects a prohibited item carried "
                    "in a passenger's cabin bag at the X-ray screen of a CT lane."],
                   ["Screening year", "1 December to 30 November. Its quarters begin on 1 December, 1 March, "
                    "1 June and 1 September."],
                   ["X-ray time", "An officer's time at the X-ray screen of a CT lane. The officers working on a "
                    "lane take the screen in turn, so an officer's X-ray time on a lane is the time they work on "
                    "the lane divided by the number of officers working on the lane at that time."],
                   ["Passenger bags", "The bags, trays and loose items passengers put through a CT lane."],
                   ["Dates and times", "Sydney local time throughout."]]),
        ("h", "4. Annual assessment"),
        ("p", "At the close of each screening year the training and standards lead assesses the detection "
              "performance of every officer who holds an X-ray endorsement on 30 November, over the officer's "
              "screening on the CT lanes in that screening year."),
        ("p", "An officer whose detection performance is below 80 per cent does not work at the X-ray screen from "
              "1 January until they have completed remedial training and passed the image interpretation "
              "assessment. Every other endorsed officer is recertified for the calendar year."),
        ("h", "5. Currency"),
        ("p", "An officer who holds an X-ray endorsement for the whole of a calendar month needs at least 20 hours "
              "of X-ray time in that month. The training and standards lead reports each month how many endorsed "
              "officers fell short, and rosters each of them for supervised X-ray time early the next month."),
        ("h", "6. Throughput"),
        ("p", "The year-end return to the airport's security committee gives the passenger bags each CT lane "
              "screened in each quarter of the screening year."),
        ("h", "7. Records"),
        ("p", "The threat image projection system places images of prohibited items into the images of passengers' "
              "bags at random on every CT lane and records each one it shows and whether the officer at the "
              "screen marked it. The lane roster records the officers who work on each lane and when. Each CT unit "
              "keeps an hourly count of what it images."),
    ]
    IO.write_pdf(path, "SCS-04 Screening officer competency standard", "Teresa Malone",
                 "Silverwattle Coast Airport", b, "SCS-04 rev 6 | Security Screening | uncontrolled when printed",
                 "D:20250714101500+10'00'", "D:20250714104200+10'00'")
