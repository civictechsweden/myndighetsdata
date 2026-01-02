from utils import read_json, write_json
from SPARQLWrapper import SPARQLWrapper, JSON

ENDPOINT = "https://query.wikidata.org/sparql"
FILEPATH = "raw_files/wikidata_raw"


def download():
    agent = "Myndighetsbot/0.1 (https://github.com/civictechsweden/myndighetsdata)"
    sparql = SPARQLWrapper(ENDPOINT, agent=agent)
    sparql.setReturnFormat(JSON)

    with open("sources/wikidata_query.sparql", "r") as file:
        query = file.read()

    sparql.setQuery(query)

    try:
        ret = sparql.queryAndConvert()
        data = ret["results"]["bindings"]
    except Exception as e:
        print(e)

    write_json(data, FILEPATH)


def extract():
    data = read_json(FILEPATH + ".json")

    data_flat = []

    for row in data:
        for key in row.keys():
            row[key] = row[key]["value"]

        for key in ["other_names", "replaces", "replaced_by", "follows"]:
            csvalues = row[key]
            row[key] = csvalues.split(";;") if csvalues else []

        data_flat.append(row)

    new_names = {
        "org": "id",
        "part_of": "part_of",
        "mother_org": "mother_org",
        "source": "source",
        "org_nr": "org_nr",
        "start": "start",
        "end": "end",
        "replaces": "replaces",
        "replaced_by": "replaced_by",
        "name_en": "name_en",
        "wiki_url": "wiki_url",
        "other_names": "other_names",
    }

    data_clean = {}

    for row in data_flat:
        row_clean = {}
        for key in row.keys():
            if key in new_names and row[key]:
                row_clean[new_names[key]] = row[key]

        name = row["name"]

        row_clean["id"] = row_clean["id"].split("/")[-1]

        if name not in data_clean:
            data_clean[name] = row_clean

    return data_clean
