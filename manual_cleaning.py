from utils import read_json, write_json

to_remove = ["Fyrbodals Kommunalförbund"]

to_merge = {
    "Sveriges ambassad Tunisien": "Sveriges ambassad Tunis",
    "Sveriges representation Strasbourg, Europarådet": "Sveriges representation Europarådet Strasbourg",
    "Sveriges ambassad Bogotá Distrito Capital": "Sveriges ambassad Bogotá",
    "Sveriges ambassad Santiago de Chile": "Svergies ambassad Santigao",
    "Sveriges ambassad Bolivia": "Sveriges ambassad La Paz",
    "Sveriges delegation vid NATO i Bryssel": "Svergies delegation NATO Bryssel",
    "Sveriges ständiga representation vid Europeiska unionen i Bryssel": "Sveriges EU-representation Bryssel",
    "Sveriges ambassad Armenien": "Sveriges ambassad Jerevan",
    "Sveriges Honorärkonsulat i Angola": "Sveriges ambassad Luanda",
    "Sveriges ständiga representation vid FN i New York": "Sveriges FN-Representation New York",
    "Ekeskolans resurscenter": "Ekeskolan",
    "Ekeskolan, Örebro": "Ekeskolan",
    "Hällsboskolan, Sigtuna": "Hällsboskolan",
    "Hällsboskolans resurscenter": "Hällsboskolan",
}


def clean():
    merged = read_json("data/merged.json")
    for agency in to_remove:
        merged.pop(agency)

    for agency in to_merge:
        for source in merged[agency]:
            data = merged[agency][source]

            if isinstance(data, list):
                data = data[0]

            if agency != to_merge[agency]:
                if "other_names" not in data:
                    data["other_names"] = []

                if agency not in data["other_names"]:
                    data["other_names"].append(agency)

            merged[to_merge[agency]][source] = data
            merged.pop(agency)

    write_json(merged, "data/merged")
