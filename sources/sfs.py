import json
import requests

from utils import remove_parenthesis, get_sfs

URL = "https://beta.rkrattsbaser.gov.se/elasticsearch/SearchEsByRawJson"
PAYLOAD = json.dumps(
    {
        "searchIndexes": ["Sfs"],
        "api": "search",
        "json": {
            "sort": [],
            "query": {
                "bool": {
                    "must": [
                        {
                            "bool": {
                                "should": [
                                    {
                                        "terms": {
                                            "forfattningstypNamn.keyword": [
                                                "Förordning",
                                                "Lag",
                                            ]
                                        }
                                    }
                                ]
                            }
                        },
                        {"match_phrase": {"rubrik": "instruktion"}},
                        {"term": {"publicerad": True}},
                    ]
                }
            },
            "size": 10000,
            "from": 0,
            "_source": [
                "beteckning",
                "organisation",
                "rubrik",
                "tidsbegransadDateTime",
                "upphavdDateTime",
                "fulltext.upphavdGenom",
                "ikraftDateTime",
                "dokumenttyp",
            ],
        },
    }
)
FILEPATH = "raw_files/sfs.json"


def download():
    res = requests.post(
        URL, headers={"Content-Type": "application/json"}, data=PAYLOAD
    ).json()

    with open(FILEPATH, "w", encoding="utf-8") as file:
        json.dump(res, file, indent=2, ensure_ascii=False)


def extract():
    with open(FILEPATH, "r", encoding="utf-8") as file:
        data = json.load(file)

    agencies = {}

    for row in data["hits"]["hits"]:
        source = row["_source"]

        id = source["beteckning"]

        if id[0] == "N":
            continue

        title = source["rubrik"]
        title = title.replace("\n", " ")
        title = title.replace("\r", " ")
        title = " ".join(title.split())
        title = title.strip()

        expired = source["tidsbegransadDateTime"]
        if not expired:
            expired = source["upphavdDateTime"]

        sfs_data = {
            "id": source["beteckning"],
            "title": title,
            "enforced": source["ikraftDateTime"],
            "expired": expired,
            "expired_by": get_sfs(source["fulltext"]["upphavdGenom"]),
            "department": source["organisation"]["namnOchEnhet"],
        }

        name = title.replace(f" ({id})", "")
        name = name.replace(" provisorisk", "")
        name = name.replace(" om instruktion", " med instruktion")
        name = name.replace("Förordning med instruktion för ", "").strip()

        if "Lag" in name:
            name = title.replace(f"Lag ({id}) med instruktion för ", "").strip()
            sfs_data["parliament"] = True
        elif "Förordning" in name:
            continue

        name, other_name = remove_parenthesis(name)
        name = name[0].upper() + name[1:]
        name = name.strip()

        if other_name:
            other_name = other_name[0].upper() + other_name[1:]
            sfs_data["other_name"] = other_name.capitalize()

        if name not in agencies:
            agencies[name] = [sfs_data]
        else:
            agencies[name].append(sfs_data)

    for name in agencies:
        data = agencies[name]
        data = sorted(data, key=lambda d: d["id"])

        other_names = []
        for sfs in data:
            if "other_name" in sfs:
                other_name = sfs["other_name"]
                if other_name not in other_names:
                    other_names.append(other_name)

        agencies[name] = {
            "sfs": [sfs["id"] for sfs in data],
            "start": [sfs["enforced"] for sfs in data][0],
            "end": [sfs["expired"] for sfs in data][-1],
            "expired_by": [sfs["expired_by"] for sfs in data][-1],
            "other_names": other_names,
        }

    agencies = {key: value for key, value in sorted(agencies.items())}

    for agency in agencies:
        replaces = []
        for other_agency in agencies:
            if agencies[agency]["sfs"][0] == agencies[other_agency]["expired_by"]:
                replaces.append(other_agency)

        agencies[agency]["replaces"] = replaces

    return agencies
