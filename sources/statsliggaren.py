from utils import read_json, write_json
from bs4 import BeautifulSoup
import requests

URL = "https://www.esv.se/statsliggaren/?PeriodId={}"
FILEPATH = "raw_files/statsliggaren.json"


def download():
    links = []
    for year in range(2003, 2024 + 1):
        r = requests.get(URL.format(year))
        soup = BeautifulSoup(r.content, "html.parser")
        nav = soup.select("nav[id=Myndigheter] > ul > li > a")
        for a in nav:
            name = a.text.strip()
            id = a["href"]
            id = id.replace("/statsliggaren/SenasteRegleringsbrev?myndighetId=", "")
            id = id[: id.index("&")]
            links.append({"name": name, "id": int(id), "year": year})

    write_json(links, FILEPATH)


def extract():
    data = read_json(FILEPATH)

    agencies = {}
    ids = []

    for row in reversed(data):
        name = row["name"]
        id = row["id"]
        year = row["year"]

        if id not in ids:
            ids.append(id)

            agencies[name] = {"id": id, "years": [year]}
        else:
            current_name = [
                agency for agency in agencies if agencies[agency]["id"] == id
            ][0]
            sl_data = agencies[current_name]
            sl_data["years"].append(year)

            if name.lower() != current_name.lower():
                old_names = sl_data.get("old_names", [])
                if name not in old_names:
                    old_names.append(name)
                    sl_data["old_names"] = old_names

            agencies[current_name] = sl_data

    return agencies
