from utils import get

import urllib.request
import pandas as pd
import ssl
import certifi

ssl._create_default_https_context = lambda: ssl.create_default_context(
    cafile=certifi.where()
)

URL = "https://www.statskontoret.se/kunskapsstod-och-regler/rapportering/myndighetsregistret/exportexcelallaarmyndigheter/"
FILEPATH = "raw_files/esv.xlsx"


def download():
    urllib.request.urlretrieve(URL, FILEPATH)


def extract():
    agencies = {}
    ids = []

    dfs = pd.read_excel(FILEPATH, sheet_name=None)
    years = [year for year in dfs if year.isdigit()]

    for year in years:
        df = dfs[year]

        for _, row in df.iterrows():
            agency_id = get(row, "LöpNr")
            name = get(row, "Myndighet").strip()
            employees = get(row, "Anställda")
            fte = get(row, "Årsarbetskrafter")

            if agency_id not in ids:
                email = get(row, "Epost").split("@")
                email = email[1] if len(email) > 1 else ""

                esv_data = {
                    "name_en": get(row, "Engelskt namn"),
                    "short_name": get(row, "MyndID"),
                    "id": agency_id,
                    "department": get(row, "Departement"),
                    "org_nr": get(row, "OrgNr"),
                    "email": get(row, "Epost"),
                    "years": [year],
                }

                if employees:
                    esv_data["employees"] = {year: employees}
                if fte:
                    esv_data["fte"] = {year: fte}

                agencies[name] = esv_data

                ids.append(agency_id)
            else:
                current_name = [
                    agency for agency in agencies if agencies[agency]["id"] == agency_id
                ][0]
                esv_data = agencies[current_name]

                esv_data["years"].append(year)

                if employees:
                    if "employees" not in esv_data:
                        esv_data["employees"] = {}
                    esv_data["employees"][year] = employees
                if fte:
                    if "fte" not in esv_data:
                        esv_data["fte"] = {}
                    esv_data["fte"][year] = fte

                if name not in agencies:
                    old_names = esv_data.get("old_names", [])
                    if name not in old_names:
                        old_names.append(name)

                    short_name = get(row, "MyndID")
                    if (
                        short_name not in old_names
                        and short_name != esv_data["short_name"]
                    ):
                        old_names.append(short_name)

                    esv_data["old_names"] = old_names

                agencies[current_name] = esv_data

    for agency in agencies:
        active_years = agencies[agency]["years"]

        if active_years[-1] != years[-1]:
            agencies[agency]["start"] = active_years[-1]

        if active_years[0] != years[0]:
            agencies[agency]["end"] = active_years[0]

        agencies[agency].pop("years")

    return agencies
