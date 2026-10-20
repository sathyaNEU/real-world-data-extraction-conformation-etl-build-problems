"""metadata.json: the files with source, date and licence, the distractors, the deliverables."""
import json

import pack as P

DATES = {"detections": "2027-04-02", "traversals": "2027-04-02", "review": "2027-04-02", "register": "2027-04-01",
         "sessions": "2027-04-02", "inventory": "2027-01-04", "crosswalk": "2027-01-04", "turnback": "2027-03-01",
         "orders": "2027-04-02", "program": "2027-04-06", "sow": "2027-01-19", "dictionary": "2027-04-03",
         "manifest": "2027-04-03", "pci": "2026-11-30", "winter": "2027-04-01", "sections": "2027-01-04"}
SOURCE = {"detections": "Kerbline Vision platform", "review": "Kerbline Vision platform, review module",
          "register": "Kerbline Vision install log", "sessions": "Kerbline Vision device API",
          "sow": "Kerbline Vision, Inc.", "traversals": "fleet telematics provider for the district",
          "turnback": "City of Tamsett, Department of Public Works"}


def write(path, n):
    files = [dict(file=fn, source="%s (fictional), synthetic records" % SOURCE.get(k, "State Department of Transportation, "
                                                                                   "Tamsett District"),
                  date=DATES[k], license="CC0-1.0 (synthetic, generated for this task)", rows=n.get(k))
             for k, fn in sorted(P.FILES.items(), key=lambda t: t[1])]
    meta = dict(task="task478", title="Tamsett District Spring Patching Program 2027 designations",
                setting="A fictional district of an unnamed U.S. state's department of transportation; every record is "
                        "synthetic.",
                as_of="2027-04-09", files=files,
                distractor_files=list(P.DISTRACTORS),
                distractors=[dict(file=P.FILES["pci"], why="the 2026 summer condition survey: roughness and cracking "
                                  "before the winter, not the March potholes the program counts"),
                             dict(file=P.FILES["winter"], why="the March storms' plow hours, salt and freeze-thaw "
                                  "cycles by section: what made potholes, not a count of them")],
                deliverables=["tamsett_spring_patching_sections_2027.csv", "tamsett_spring_patching_task_orders_2027.pdf"],
                stated_inputs=["6.0", "10.85"])
    json.dump(meta, open(path, "w", encoding="utf-8"), indent=1)
