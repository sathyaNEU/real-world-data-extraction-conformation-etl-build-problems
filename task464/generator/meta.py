"""task464 architecture 10: metadata.json, written from the built pack so it never drifts from it."""
import json
import os
import world as W

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DNO = W.DNO
DATA = "%s, network data lead's 2025/26 losses and interruptions extract" % DNO

FILES = [
    ("lv_monitoring_2025-26.parquet", "spine",
     "Half-hourly readings for 2025/26 from every secondary substation monitor at Copsewell Cross and Feltmoor primaries, "
     "as the monitoring platform exports them.", DATA, "2026-06-12"),
    ("hv_settlement_2025-26.csv", "operating extract",
     "Half-hourly settlement data for 2025/26 for every HV-connected customer's import and export metering points at "
     "the two primaries.", DATA, "2026-06-12"),
    ("hv_network_model.xlsx", "operating extract",
     "The network model's export for Copsewell Cross's 11 kV feeders: every section and node in the normal running "
     "arrangement, normally-open points included.", "%s, network management system export" % DNO, "2026-06-12"),
    ("secondary_substations.csv", "reference",
     "The secondary substation register for the two primaries: site, circuit, transformer rating, monitor and network "
     "node.", "%s, asset register" % DNO, "2026-06-12"),
    ("hv_connections.csv", "reference",
     "The HV connections register for the two primaries: agreement, customer, capacities, metering points and network "
     "node.", "%s, connections register" % DNO, "2026-06-12"),
    ("hv_conductor_data_EDS-02-0310.pdf", "reference",
     "The engineering data sheet of 11 kV conductor resistances, reactances and ratings.", "%s, asset policy" % DNO,
     "2024-09-03"),
    ("losses_programme_2027-28_brief.pdf", "governing document",
     "The losses strategy lead's paper to the investment review panel on the 2027/28 reconductoring project.",
     "%s, network losses strategy" % DNO, "2026-11-18"),
    ("interruptions_2023-2026.csv", "operating extract",
     "The interruption log for Copsewell Cross's 11 kV circuits from April 2023 to March 2026: control-system HV incidents "
     "and work-management LV jobs, one row per site per restoration step.", DATA, "2026-06-12"),
    ("customers_by_substation_2023-2026.csv", "operating extract",
     "Customers connected at each site on the Copsewell Cross circuits at each month end, April 2023 to March 2026.",
     DATA, "2026-06-12"),
    ("generator_hire_2025-26.xlsx", "operating extract",
     "The generation team's hire and fuel log of mobile generators deployed in 2025/26.", "%s, generation team" % DNO,
     "2026-04-09"),
    ("iis_reporting_definitions_2025-26.pdf", "governing document",
     "The network performance team's definitions for the 2025/26 interruptions return, with the accepted exceptional "
     "event.", "%s, network performance" % DNO, "2026-05-14"),
    ("copsewell_cross_scada_2025-26.csv", "distractor",
     "Copsewell Cross primary's SCADA feeder-breaker metering for 2025/26: phase currents, MW and MVAr each half-hour.",
     "%s, control room SCADA historian" % DNO, "2026-06-12"),
    ("line_loss_factors_2025-26.pdf", "distractor",
     "The published line loss factor statement for the licence area's 2025/26 settlement year.", DNO, "2025-02-28"),
]


def main():
    from answers import FEEDER_ORDER
    f = json.load(open(os.path.join(BASE, "generator", "figures.json")))
    names = sorted(os.listdir(os.path.join(BASE, "target")))
    listed = sorted(n for n, *_ in FILES)
    assert names == listed, (names, listed)
    meta = {
        "task": "task464",
        "domain": "energy-systems-utilities",
        "subdomain": "asset-condition-maintenance",
        "objective": "opportunity-sizing-decision",
        "prompt_shape": "07",
        "as_of": "2026-12-02",
        "extract_to": "2026-03-31",
        "currency": "GBP",
        "compiled_by": "%s, network losses strategy" % DNO,
        "compiled_on": "2026-12-02",
        "licence": ("Synthetic records compiled for %s's 2027/28 losses programme paper. Every file is constructed, "
                    "describes no real network or customer, and is released for this task's use." % DNO),
        "files": [{"path": "target/" + n, "role": role, "covers": cov, "source": src, "date": d,
                   "licence": "synthetic, constructed for this task, free to use"}
                  for n, role, cov, src, d in FILES],
        "distractor_files": ["target/copsewell_cross_scada_2025-26.csv", "target/line_loss_factors_2025-26.pdf"],
        "stated_inputs": ["64.80", "64.8", "11",
                          "the brief's eight projects, their section IDs and replacement conductors, the year 1 April 2025 to "
                          "31 March 2026 (UK time), 11 kV nominal, 20 C resistances and the losses value of GBP 64.80 per MWh "
                          "(losses_programme_2027-28_brief.pdf)",
                          "the 3-minute threshold, half weight for pre-arranged interruptions, the exclusions and the accepted "
                          "storm (iis_reporting_definitions_2025-26.pdf)"],
        "field_terms": ["technical losses", "I2R losses", "reconductoring", "embedded generation", "customer interruptions",
                        "customer minutes lost"],
        "deliverables": ["losses_programme_2027.xlsx", "losses_saving_2027.png", "iis_feeders_2025-26.csv"],
        "portal": {"call": "the Copsewell Cross reconductoring project the 2027/28 losses programme funds",
                   "answer": f["call"], "saving_mwh": f["projects"][f["call"]]["year_mwh"], "runner_up": f["runner_up"]},
    }
    json.dump(meta, open(os.path.join(BASE, "metadata.json"), "w"), indent=2)
    print("  metadata.json, %d files" % len(FILES))


if __name__ == "__main__":
    main()
