"""Write the task249 pack into a target folder and return the world for the checks."""
import os
import docs
import records as RC

FILES = {
    "request": "june_round_pull_list_request.eml",
    "plan": "ozone_network_qa_plan_v3.pdf",
    "nodes": "nodes_o3_export_2027-09-20_2028-05-31.csv",
    "register": "nodes_register.csv",
    "log": "maintenance_log_2027-09_2028-05.pdf",
    "firmware": "ozn_firmware_4-2_release_note.pdf",
    "datasheet": "ozn_nodes_datasheet_revC.pdf",
    "visits": "visitas_ronda_marzo_2028.xlsx",
    "stations": "rrvca_ozone_station_sheet_2028-04.pdf",
    "validated": "rrvca_o3_horario_validado_2026-2027.csv",
    "provisional": "rrvca_o3_horario_provisional_2027-12_2028-05.csv",
    "weather": "meteo_alcorna_parque_2027-10_2028-05.csv",
    "dict": "DATA_DICTIONARY.md",
    "contents": "folder_contents.md",
    "deliv_xlsx": "ozone_nodes_june_2028_round.xlsx",
    "deliv_pdf": "june_2028_pull_list.pdf",
}
PACK = [k for k in FILES if not k.startswith("deliv_")]
DISTRACTORS = ["weather", "datasheet", "validated"]
CONTEXT = ["visits"]


def run(target, documents=True):
    os.makedirs(target, exist_ok=True)
    W = RC.World()
    p = lambda k: os.path.join(target, FILES[k])
    csv = lambda df, k: df.to_csv(p(k), index=False, lineterminator="\n")
    csv(W.node_rows(), "nodes")
    csv(W.register(), "register")
    csv(W.analyser_rows(True), "validated")
    csv(W.analyser_rows(False), "provisional")
    csv(W.weather(), "weather")
    if documents:
        docs.request(p("request"))
        docs.plan(p("plan"))
        docs.stations(p("stations"))
        docs.maintenance(p("log"))
        docs.firmware(p("firmware"))
        docs.datasheet(p("datasheet"))
        docs.visits(p("visits"))
        with open(p("dict"), "w", encoding="utf-8") as fh:
            fh.write(docs.dictionary(FILES))
        with open(p("contents"), "w", encoding="utf-8") as fh:
            fh.write(docs.contents(FILES))
    return dict(W=W)
